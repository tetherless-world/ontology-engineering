#!/usr/bin/env python3
"""Import Under Consideration and Unassessed initial states from States only.

Uses the existing ontology and utterances. Other worksheet contents are never
opened. Historical assignments are distinct from the current hasState value.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

from milestones_to_individuals import RDFS, parse_turn_ids, read_worksheet, utterance_index
from relationships_to_individuals import append_source_links as append_milestone_assertions
from xml_to_individuals import (
    CJF, OWL, RDF, DEFAULT_INDIVIDUALS, Individual, Statement,
    append_individuals, atomic_write, existing_subjects, individual, read_xml,
)


REQUIRED_COLUMNS = {"milestone_id", "state", "effective_turn_id", "evidence_turn_ids", "reason"}
STATE_TYPES = {
    "Open": ("Open", {"Issue", "InformationRequest"}),
    "UnderConsideration": ("Under Consideration", {"Option"}),
    "Unassessed": ("Unassessed", {"Claim"}),
}
DEFAULT_STATES = ("UnderConsideration", "Unassessed")


def make_initial_states(rows: list[dict], rdf_data: bytes, schema_data: bytes,
                        workbook_name: str, state_types: tuple[str, ...] = DEFAULT_STATES
                        ) -> tuple[list[Individual], dict, dict]:
    if not state_types or len(set(state_types)) != len(state_types) or set(state_types) - STATE_TYPES.keys():
        raise ValueError(f"Unsupported or repeated initial state types: {state_types}")
    selected_types = {STATE_TYPES[name][0]: name for name in state_types}
    schema = read_xml(schema_data)
    classes = {node.get("{" + RDF + "}about") for node in schema.findall("{" + OWL + "}Class")}
    properties = {node.get("{" + RDF + "}about")
                  for node in schema.findall("{" + OWL + "}ObjectProperty")}
    required_classes = {"StateAssignment", "TextSpan", *state_types}
    required_classes.update(name for state in state_types for name in STATE_TYPES[state][1])
    for name in required_classes:
        if CJF + name not in classes:
            raise ValueError(f"Missing ontology class: {name}")
    for name in {"hasState", "hasStateAssignment", "assignedState", "assignedAtUtterance",
                 "hasStateEvidence", "isPartOfUtterance"}:
        if CJF + name not in properties:
            raise ValueError(f"Missing object property: {name}")
    subjects = existing_subjects(read_xml(rdf_data))
    utterances = utterance_index(rdf_data)
    selected = [row for row in rows if row.get("state", "").strip() in selected_types]
    milestone_ids = {row["milestone_id"].strip() for row in selected}
    histories = defaultdict(list)

    def effective_utterance(row):
        sources = parse_turn_ids(row["effective_turn_id"])
        if len(sources) != 1 or sources[0] not in utterances:
            raise ValueError(f"States row {row['excel_row']}: effective turn must identify one existing utterance")
        return utterances[sources[0]]

    # The complete States history determines whether an initial state is current.
    # Rows outside the selected initial state types never generate individuals.
    for row in rows:
        milestone_id = row.get("milestone_id", "").strip()
        if milestone_id in milestone_ids:
            histories[milestone_id].append((effective_utterance(row)["turn_number"], row))
    latest = {}
    for milestone_id, history in histories.items():
        last = max(turn for turn, _ in history)
        candidates = [row for turn, row in history if turn == last]
        if len({row["state"].strip() for row in candidates}) != 1:
            raise ValueError(f"Conflicting states at the same effective turn for {milestone_id}")
        latest[milestone_id] = candidates[0]

    generated = {}
    milestone_links = defaultdict(list)
    records, seen = [], set()
    for row in selected:
        state_label = row["state"].strip()
        state_class = selected_types[state_label]
        milestone_id = row["milestone_id"].strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", milestone_id):
            raise ValueError(f"Invalid milestone ID: {milestone_id!r}")
        milestone = CJF + milestone_id
        if milestone not in subjects:
            raise ValueError(f"Milestone is missing: {milestone_id}")
        types = {child.get("{" + RDF + "}resource") for node in subjects[milestone]
                 for child in node.findall("{" + RDF + "}type")}
        expected_types = {CJF + name for name in STATE_TYPES[state_class][1]}
        if not types.intersection(expected_types):
            raise ValueError(f"{state_label} requires {sorted(expected_types)}: {milestone_id}")
        effective = effective_utterance(row)
        if effective["turn_number"] != min(turn for turn, _ in histories[milestone_id]):
            raise ValueError(f"States row {row['excel_row']}: {state_label} must be the initial assignment")
        key = (milestone, effective["iri"])
        if key in seen:
            raise ValueError(f"Repeated initial assignment: {milestone_id}, turn {row['effective_turn_id']}")
        seen.add(key)
        assignment = CJF + milestone_id + "_" + state_class + "AtTurn" + str(effective["turn_number"])
        state = CJF + milestone_id + "_" + state_class + "StateAtTurn" + str(effective["turn_number"])
        if any(node.find("{" + CJF + "}hasPreviousAssignment") is not None
               for node in subjects.get(assignment, [])):
            raise ValueError(f"Initial assignment already has a previous assignment: {assignment}")
        generated[state] = individual(state, CJF + state_class,
            Statement(RDFS + "label", milestone_id + " " + state_label + " state at turn " + str(effective["turn_number"])))
        statements = [
            Statement(RDFS + "label", milestone_id + " " + state_label + " assignment at turn " + str(effective["turn_number"])),
            Statement(CJF + "assignedState", state, True),
            Statement(CJF + "assignedAtUtterance", effective["iri"], True),
            Statement(RDFS + "comment", "Source: " + workbook_name + "; States!A" +
                      str(row["excel_row"]) + ":E" + str(row["excel_row"])),
            Statement(RDFS + "comment", "Source effective turn ID: " + row["effective_turn_id"]),
            Statement(RDFS + "comment", "Source evidence turn ID(s): " + row["evidence_turn_ids"]),
        ]
        if row.get("reason", ""):
            statements.append(Statement(RDFS + "comment", row["reason"]))
        if row.get("questions when annotating", ""):
            statements.append(Statement(RDFS + "comment", "Annotation question: " + row["questions when annotating"]))
        evidence = []
        evidence_sources = parse_turn_ids(row["evidence_turn_ids"])
        if not evidence_sources:
            raise ValueError(f"States row {row['excel_row']}: initial assignment needs evidence")
        for source in evidence_sources:
            if source not in utterances:
                raise ValueError(f"Unknown evidence source turn: {source}")
            utterance = utterances[source]
            span = utterance["iri"] + "FullTextSpan"
            generated[span] = individual(span, CJF + "TextSpan",
                Statement(RDFS + "label", "Full utterance evidence, source turn " + source),
                Statement(CJF + "hasConversationText", utterance["text"]),
                Statement(CJF + "isPartOfUtterance", utterance["iri"], True))
            statements.append(Statement(CJF + "hasStateEvidence", span, True))
            evidence.append({"source_turn_id": source, "turn_number": utterance["turn_number"],
                             "utterance_iri": utterance["iri"], "text_span_iri": span,
                             "text": utterance["text"]})
        generated[assignment] = individual(assignment, CJF + "StateAssignment", *statements)
        milestone_links[milestone].append(Statement(CJF + "hasStateAssignment", assignment, True))
        is_current = latest[milestone_id]["state"].strip() == state_label and (
            effective["turn_number"] == effective_utterance(latest[milestone_id])["turn_number"])
        if is_current:
            existing = {child.get("{" + RDF + "}resource") for node in subjects[milestone]
                        for child in node.findall("{" + CJF + "}hasState")}
            if existing - {state}:
                raise ValueError(f"Existing current state conflicts with {state_label} for {milestone_id}: {sorted(existing)}")
            milestone_links[milestone].append(Statement(CJF + "hasState", state, True))
        records.append({"milestone_iri": milestone, "milestone_class_iris": sorted(types),
                        "assignment_iri": assignment, "state_iri": state,
                        "effective_utterance_iri": effective["iri"], "effective_turn_number": effective["turn_number"],
                        "state_class_iri": CJF + state_class, "state_label": state_label,
                        "current_state": is_current, "latest_recorded_state": latest[milestone_id]["state"],
                        "initial_assignment": True,
                        "source_row": row, "evidence": evidence})
    counts = {}
    for state in state_types:
        matching = [row for row in records if row["state_class_iri"] == CJF + state]
        counts[state] = {"assignments": len(matching), "state_individuals": len(matching),
                         "current": sum(row["current_state"] for row in matching),
                         "historical": sum(not row["current_state"] for row in matching)}
    report = {"state_individuals": [row["state_iri"] for row in records],
              "state_count": len(records), "assignment_count": len(records), "counts_by_state": counts,
              "current_count": sum(row["current_state"] for row in records),
              "historical_count": sum(not row["current_state"] for row in records),
              "evidence_span_count": len({entry["text_span_iri"] for row in records for entry in row["evidence"]}),
              "other_state_rows_not_imported": len(rows) - len(selected), "assignments": records}
    # Retain the existing Open import report fields for its wrapper and callers.
    if state_types == ("Open",):
        report.update({"open_state_individuals": report["state_individuals"],
                       "open_state_count": report["state_count"], "open_assignment_count": report["assignment_count"],
                       "current_open_count": report["current_count"], "historical_open_count": report["historical_count"],
                       "non_open_rows_not_imported": report["other_state_rows_not_imported"]})
        for row in records:
            row["current_open"] = row["current_state"]
    return list(generated.values()), dict(milestone_links), report


def main(state_types: tuple[str, ...] = DEFAULT_STATES) -> int:
    labels = ", ".join(STATE_TYPES[name][0] for name in state_types)
    parser = argparse.ArgumentParser(description=f"Import {labels} initial state rows from States only.")
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--individuals", type=Path, default=DEFAULT_INDIVIDUALS)
    parser.add_argument("--ontology", type=Path, default=DEFAULT_INDIVIDUALS.with_name("tracking-cjf.rdf"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--backup", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        target = (args.output or args.individuals).resolve()
        inputs = {args.workbook.resolve(), args.individuals.resolve(), args.ontology.resolve()}
        suffix = ".open-states.bak" if state_types == ("Open",) else ".initial-states.bak"
        backup = (args.backup or target.with_name(target.name + suffix)).resolve()
        report_path = args.report.resolve() if args.report else None
        if target in {args.workbook.resolve(), args.ontology.resolve()} or backup in inputs | {target} or (
                report_path and report_path in inputs | {target, backup}):
            raise ValueError("Workbook, schema, RDF, backup, and report paths must not overwrite one another")
        original, schema = args.individuals.read_bytes(), args.ontology.read_bytes()
        workbook_hash = hashlib.sha256(args.workbook.read_bytes()).hexdigest()
        rows, routing = read_worksheet(args.workbook, "States", REQUIRED_COLUMNS)
        generated, links, report = make_initial_states(rows, original, schema, args.workbook.name, state_types)
        updated, added = append_individuals(original, generated)
        updated, added_links = append_milestone_assertions(updated, links)
        changed = not target.exists() or target.read_bytes() != updated
        if args.individuals.read_bytes() != original or args.ontology.read_bytes() != schema or (
                hashlib.sha256(args.workbook.read_bytes()).hexdigest() != workbook_hash):
            raise ValueError("An input changed during import; rerun against the latest saved files")
        if changed:
            if target.exists() and not backup.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                with backup.open("xb") as handle:
                    handle.write(target.read_bytes())
            atomic_write(target, updated)
        report.update(routing)
        report.update({"workbook": str(args.workbook.resolve()), "workbook_sha256": workbook_hash,
                       "schema_sha256": hashlib.sha256(schema).hexdigest(),
                       "input_individuals_sha256": hashlib.sha256(original).hexdigest(),
                       "individuals": str(target), "added_individuals": added,
                       "added_milestone_assertions": added_links, "output_changed": changed})
        if report_path:
            atomic_write(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(f"States sheet only: {report['assignment_count']} initial assignments ({labels}); "
              f"{report['current_count']} current, {report['historical_count']} historical.")
        print(f"Added {added} individuals and {added_links} milestone assertions. Output: {target}")
        print(f"Other state rows not imported: {report['other_state_rows_not_imported']}.")
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
