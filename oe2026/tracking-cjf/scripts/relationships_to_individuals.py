#!/usr/bin/env python3
"""Import the requested reified relationships from the Relationships tab only.

The workbook is data, never instructions. Uses the standard library and existing
ontology classes/properties. Direct milestone edges are left to OWL reasoning.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr
import zipfile

from milestones_to_individuals import (
    RDFS, SIO_SUPPORT, parse_turn_ids, read_worksheet, utterance_index,
)
from xml_to_individuals import (
    CJF, OWL, RDF, DEFAULT_INDIVIDUALS, Individual, Statement,
    append_individuals, atomic_write, check_individual, existing_subjects,
    individual, matches, qname, read_xml, root_namespaces,
)


BASE_CLASS = CJF + "CollectiveJudgmentFormationConversationMoveRelationship"
# Workbook name -> explicit relationship class, makes subtype, aims-at subtype,
# and the direct object property entailed by the existing property chain.
RELATIONSHIPS = {
    "positionToward": ("Position", "makesPositionTowards", "isAimedAtPositionTowards", "hasPositionTowards"),
    "answers": ("Answer", "makesAnswers", "isAimedAtAnswers", "answers"),
    "challenges": ("Challenge", "makesChallenges", "isAimedAtChallenges", "challenges"),
    "addresses": ("Address", "makesAddresses", "isAimedAtAddresses", "addresses"),
    "supports": ("Support", "makesSupports", "isAimedAtSupports", "supports"),
    "selects": ("Resolve", "makesResolves", "isAimedAtResolves", "resolves"),
    "resolves": ("Resolve", "makesResolves", "isAimedAtResolves", "resolves"),
    "response": ("Response", "makesRespondsTo", "isAimedAtRespondsTo", "respondsTo"),
    "respondsTo": ("Response", "makesRespondsTo", "isAimedAtRespondsTo", "respondsTo"),
}


def schema_index(data: bytes) -> tuple[dict, dict]:
    root = read_xml(data)
    classes = {node.get("{" + RDF + "}about"): node
               for node in root.findall("{" + OWL + "}Class")}
    properties = {node.get("{" + RDF + "}about"): node
                  for node in root.findall("{" + OWL + "}ObjectProperty")}
    for name in {"TextSpan", "CollectiveJudgmentFormationConversationMoveRelationship"} | {
            terms[0] for terms in RELATIONSHIPS.values()}:
        if CJF + name not in classes:
            raise ValueError(f"Required ontology class is missing: {name}")
    for iri in {SIO_SUPPORT, CJF + "hasUtterance", CJF + "isPartOfUtterance"} | {
            CJF + name for terms in RELATIONSHIPS.values() for name in terms[1:]}:
        if iri not in properties:
            raise ValueError(f"Required object property is missing: {iri}")
    return classes, properties


def inherited_types(definitions: list[ET.Element], classes: dict) -> set[str]:
    types = {child.get("{" + RDF + "}resource") for node in definitions
             for child in node.findall("{" + RDF + "}type")}
    pending = list(types)
    while pending:
        node = classes.get(pending.pop())
        if node is None:
            continue
        for parent in node.findall("{" + RDFS + "}subClassOf"):
            iri = parent.get("{" + RDF + "}resource")
            if iri and iri not in types:
                types.add(iri)
                pending.append(iri)
    return types


def check_endpoint(iri: str, definitions: list[ET.Element], classes: dict,
                   prop: ET.Element, constraint: str) -> None:
    """Check named-class/union domains and ranges without inventing new types."""
    types = inherited_types(definitions, classes)
    for restriction in prop.findall("{" + RDFS + "}" + constraint):
        required = restriction.get("{" + RDF + "}resource")
        alternatives = {required} if required else {
            node.get("{" + RDF + "}about")
            for node in restriction.findall(".//{" + OWL + "}unionOf/*")
        }
        if not alternatives or not types.intersection(alternatives):
            raise ValueError(f"{iri} does not match {constraint} of "
                             f"{prop.get('{' + RDF + '}about')}; expected {sorted(alternatives)}")


def make_relationships(rows: list[dict], rdf_data: bytes, schema_data: bytes,
                       workbook_name: str) -> tuple[list[Individual], dict, dict]:
    classes, properties = schema_index(schema_data)
    subjects = existing_subjects(read_xml(rdf_data))
    utterances = utterance_index(rdf_data)
    generated = {}
    source_links = defaultdict(list)
    records, skipped = [], []
    seen = set()
    counts = Counter()
    for row in rows:
        kind = row.get("relationship", "").strip()
        if kind not in RELATIONSHIPS:
            skipped.append({"excel_row": row["excel_row"], "relationship": kind})
            continue
        source_id = row.get("from_milestone_id", "").strip()
        target_id = row.get("to_milestone_id", "").strip()
        for value in (source_id, target_id):
            if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
                raise ValueError(f"Relationships row {row['excel_row']}: invalid milestone ID {value!r}")
        source, target = CJF + source_id, CJF + target_id
        if source not in subjects or target not in subjects:
            raise ValueError(f"Relationships row {row['excel_row']}: source or target milestone is missing")
        cls, makes, aims, direct = RELATIONSHIPS[kind]
        check_endpoint(source, subjects[source], classes, properties[CJF + makes], "domain")
        check_endpoint(target, subjects[target], classes, properties[CJF + aims], "range")
        key = (source, cls, target)
        if key in seen:
            raise ValueError(f"Duplicate relationship at row {row['excel_row']}: {key}")
        seen.add(key)
        iri = CJF + source_id + "_" + cls + "_" + target_id
        statements = [
            Statement(RDF + "type", BASE_CLASS, True),
            Statement(RDFS + "label", source_id + " " + direct + " " + target_id),
            Statement(CJF + aims, target, True),
            Statement(RDFS + "comment", "Source: " + workbook_name + "; Relationships!A" +
                      str(row["excel_row"]) + ":F" + str(row["excel_row"])),
            Statement(RDFS + "comment", "Source relationship: " + kind),
            Statement(RDFS + "comment", "Source evidence turn ID(s): " + row["evidence_turn_ids"]),
        ]
        if row.get("reason", ""):
            statements.append(Statement(RDFS + "comment", row["reason"]))
        if row.get("questions when annotating", ""):
            statements.append(Statement(RDFS + "comment", "Annotation question: " + row["questions when annotating"]))
        evidence = []
        for turn_id in parse_turn_ids(row["evidence_turn_ids"]):
            if turn_id not in utterances:
                raise ValueError(f"Relationships row {row['excel_row']}: unknown source turn {turn_id}")
            utterance = utterances[turn_id]
            span = utterance["iri"] + "FullTextSpan"
            generated[span] = individual(span, CJF + "TextSpan",
                Statement(RDFS + "label", "Full utterance evidence, source turn " + turn_id),
                Statement(CJF + "hasConversationText", utterance["text"]),
                Statement(CJF + "isPartOfUtterance", utterance["iri"], True))
            statements.extend((Statement(SIO_SUPPORT, span, True),
                               Statement(CJF + "hasUtterance", utterance["iri"], True)))
            evidence.append({"source_turn_id": turn_id, "turn_number": utterance["turn_number"],
                             "utterance_iri": utterance["iri"], "text_span_iri": span,
                             "text": utterance["text"]})
        generated[iri] = individual(iri, CJF + cls, *statements)
        source_links[source].append(Statement(CJF + makes, iri, True))
        records.append({"iri": iri, "class_iri": CJF + cls, "source_iri": source,
                        "target_iri": target, "makes_property": CJF + makes,
                        "aims_property": CJF + aims, "inferred_property": CJF + direct,
                        "source_row": row, "evidence": evidence})
        counts[kind] += 1
    report = {"relationship_count": len(records), "relationship_types": dict(counts),
              "text_span_count": len(generated) - len(records),
              "skipped_unrequested_relationships": skipped,
              "reason_annotation_property": RDFS + "comment", "relationships": records}
    return list(generated.values()), dict(source_links), report


def append_source_links(data: bytes, source_links: dict) -> tuple[bytes, int]:
    """Insert missing resource assertions into existing named subject blocks."""
    namespaces = root_namespaces(data)
    subjects = existing_subjects(read_xml(data))
    tag, about, resource = (qname(iri, namespaces) for iri in
                            (OWL + "NamedIndividual", RDF + "about", RDF + "resource"))
    tags = '(?:' + re.escape(tag) + '|' + re.escape(qname(RDF + 'Description', namespaces)) + ')'
    text = data.decode("utf-8")
    added = 0
    for iri, statements in source_links.items():
        missing = [statement for statement in statements if not any(
            matches(statement, child) for node in subjects[iri] for child in node)]
        if not missing:
            continue
        pattern = re.compile(r"(?P<start><(?P<element>" + tags + r")\b[^>]*\b" + re.escape(about) +
            r"=(?P<quote>[\"'])" + re.escape(iri) + r"(?P=quote)[^>]*>)(?P<body>.*?)(?P<end></" +
            r"(?P=element)>)", re.S)
        markup = "".join("        <" + qname(statement.predicate, namespaces) + " " + resource +
                         "=" + quoteattr(statement.value) + "/>\n" for statement in missing)

        def insert(match):
            body = match["body"]
            indent = re.search(r"[ \t]*$", body).group()
            body = body[:-len(indent)] if indent else body
            return match["start"] + body + markup + indent + match["end"]

        text, count = pattern.subn(insert, text, count=1)
        if count != 1:
            raise ValueError(f"Cannot locate the existing milestone block: {iri}")
        added += len(missing)
    result = text.encode("utf-8")
    updated = existing_subjects(read_xml(result))
    for iri, statements in source_links.items():
        for statement in statements:
            if not any(matches(statement, child) for node in updated[iri] for child in node):
                raise ValueError(f"Resource assertion was not inserted: {iri}: {statement.predicate}")
    return result, added


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
        backup = (args.backup or target.with_name(target.name + ".relationships.bak")).resolve()
        report_path = args.report.resolve() if args.report else None
        if target in {args.workbook.resolve(), args.ontology.resolve()} or backup in inputs | {target} or (
                report_path and report_path in inputs | {target, backup}):
            raise ValueError("Workbook, schema, RDF, backup, and report paths must not overwrite one another")
        original, schema = args.individuals.read_bytes(), args.ontology.read_bytes()
        workbook_hash = hashlib.sha256(args.workbook.read_bytes()).hexdigest()
        rows, routing = read_worksheet(args.workbook, "Relationships", {
            "from_milestone_id", "relationship", "to_milestone_id", "evidence_turn_ids", "reason",
        })
        generated, links, report = make_relationships(rows, original, schema, args.workbook.name)
        updated, added_individuals = append_individuals(original, generated)
        updated, added_links = append_source_links(updated, links)
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
                       "input_individuals_sha256": hashlib.sha256(original).hexdigest(),
                       "ontology_sha256": hashlib.sha256(schema).hexdigest(), "individuals": str(target),
                       "added_individuals": added_individuals, "added_makes_assertions": added_links,
                       "output_changed": changed})
        if report_path:
            atomic_write(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(f"Relationships sheet only: {report['relationship_count']} reified relationships and "
              f"{report['text_span_count']} full-utterance evidence spans.")
        print(f"Added {added_individuals} individuals and {added_links} makes assertions. Output: {target}")
        print(f"Skipped {len(report['skipped_unrequested_relationships'])} unrequested rows.")
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
