#!/usr/bin/env python3
"""Import identified milestones from the Milestones worksheet only.

Uses the standard library to read the selected worksheet's XML directly. Other
worksheet contents are never opened. Workbook text is data, not instructions.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

from xml_to_individuals import (
    CJF, DC, OWL, PROV, RDF, DEFAULT_INDIVIDUALS,
    Individual, Statement, append_individuals, atomic_write, individual,
)


RDFS = "http://www.w3.org/2000/01/rdf-schema#"
SIO_SUPPORT = "http://semanticscience.org/resource/SIO_000206"
SHEET_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
TYPE_MAP = {
    "Claim": "Claim",
    "Option": "Option",
    "Issue": "Issue",
    "Information Request": "InformationRequest",
    "Expressed Position": "ExpressedPosition",
    "Outcome": "Outcome",
    "Conversation Management": "CollectiveJudgmentFormationConversationMove",
}


def read_worksheet(workbook: Path, sheet_name: str,
                   required: set[str]) -> tuple[list[dict], dict]:
    """Read only the selected worksheet and the shared strings it references."""
    with zipfile.ZipFile(workbook) as archive:
        book = ET.fromstring(archive.read("xl/workbook.xml"))
        relations = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {item.attrib["Id"]: item.attrib["Target"] for item in relations}
        matches = [sheet for sheet in book.find(SHEET_NS + "sheets")
                   if sheet.attrib["name"].casefold() == sheet_name.casefold()]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one worksheet named {sheet_name}")
        sheet = matches[0]
        target = targets[sheet.attrib[REL_NS + "id"]]
        member = posixpath.normpath(target.lstrip("/") if target.startswith("/")
                                   else posixpath.join("xl", target))
        root = ET.fromstring(archive.read(member))
        cells = root.findall(".//" + SHEET_NS + "sheetData/" + SHEET_NS + "row/" + SHEET_NS + "c")
        if any(cell.find(SHEET_NS + "f") is not None for cell in cells):
            raise ValueError(f"{sheet_name} contains formulas; this importer requires recorded cell values")
        needed = {int(cell.find(SHEET_NS + "v").text) for cell in cells
                  if cell.get("t") == "s" and cell.find(SHEET_NS + "v") is not None}
        strings = {}
        if needed:
            index = 0
            with archive.open("xl/sharedStrings.xml") as stream:
                for _, item in ET.iterparse(stream, events=("end",)):
                    if item.tag == SHEET_NS + "si":
                        if index in needed:
                            strings[index] = "".join(text.text or "" for text in item.iter(SHEET_NS + "t"))
                        index += 1
                        item.clear()

        def value(cell):
            stored = cell.find(SHEET_NS + "v")
            if cell.get("t") == "s":
                return strings[int(stored.text)] if stored is not None else ""
            if cell.get("t") == "inlineStr":
                return "".join(text.text or "" for text in cell.iter(SHEET_NS + "t"))
            return stored.text or "" if stored is not None else ""

        headers = None
        rows = []
        for row in root.findall(SHEET_NS + "sheetData/" + SHEET_NS + "row"):
            values = {re.sub(r"\d+$", "", cell.attrib["r"]): value(cell)
                      for cell in row if cell.tag == SHEET_NS + "c"}
            if not any(values.values()):
                continue
            if headers is None:
                headers = {column: text.strip() for column, text in values.items()}
                if not required.issubset(set(headers.values())):
                    raise ValueError(f"The {sheet_name} header does not have the required columns")
                continue
            record = {headers[column]: text for column, text in values.items() if column in headers}
            record["excel_row"] = int(row.attrib["r"])
            rows.append(record)
        return rows, {"sheet": sheet.attrib["name"], "worksheet_member": member,
                      "worksheet_members_read": [member]}


def read_milestones(workbook: Path) -> tuple[list[dict], dict]:
    return read_worksheet(workbook, "Milestones", {
        "milestone_id", "milestone_type", "summary", "source_turn_id",
        "text_span", "utterance", "speaker",
    })


def parse_turn_ids(value: str) -> list[str]:
    result = []
    for part in value.split(";"):
        part = part.strip()
        if re.fullmatch(r"\d+(?:\.\d+)?", part):
            result.append(part)
        elif re.fullmatch(r"\d+\s*-\s*\d+", part):
            first, last = map(int, re.split(r"\s*-\s*", part))
            if last < first or last - first > 1000:
                raise ValueError(f"Unsupported source turn range: {part}")
            result.extend(str(number) for number in range(first, last + 1))
        else:
            raise ValueError(f"Unsupported source_turn_id: {value!r}")
    if len(result) != len(set(result)):
        raise ValueError(f"Repeated source turns: {value!r}")
    return result


def split_quotes(value: str, sources: list[str]) -> dict[str, str]:
    if len(sources) == 1:
        return {sources[0]: value}
    labeled = re.findall(r"(?:^|\s*\|\s*)(\d+(?:\.\d+)?):\s*(.*?)(?=\s*\|\s*\d+(?:\.\d+)?:|$)", value, re.S)
    if len(labeled) == len(sources) and [source for source, _ in labeled] == sources:
        return dict(labeled)
    quoted = re.findall(r'"([^"]*)"', value)
    if len(quoted) == len(sources) and not re.sub(r'"[^"]*"', "", value).strip():
        return dict(zip(sources, quoted))
    raise ValueError(f"Cannot split the evidence among source turns {sources}: {value!r}")


def utterance_index(rdf_data: bytes) -> dict[str, dict]:
    """Resolve original source IDs through dc:identifier, not the URI suffix."""
    root = ET.fromstring(rdf_data)
    nodes = defaultdict(list)
    for node in root:
        iri = node.get("{" + RDF + "}about")
        if iri:
            nodes[iri].append(node)
    index = {}
    for iri, definitions in nodes.items():
        values = defaultdict(set)
        for node in definitions:
            for child in node:
                values[child.tag].add(child.get("{" + RDF + "}resource") or child.text or "")
        if CJF + "Utterance" not in values["{" + RDF + "}type"]:
            continue
        turns = values["{" + CJF + "}hasTurnNumber"]
        texts = values["{" + CJF + "}hasConversationText"]
        speakers = values["{" + PROV + "}wasAttributedTo"]
        if len(turns) != 1 or len(texts) != 1 or len(speakers) != 1:
            raise ValueError(f"Utterance has conflicting or missing fields: {iri}")
        original_ids = values["{" + DC + "}identifier"] or turns
        if len(original_ids) != 1:
            raise ValueError(f"Utterance has ambiguous source identifiers: {iri}")
        source_id = next(iter(original_ids))
        record = {"iri": iri, "turn_number": int(next(iter(turns))),
                  "text": next(iter(texts)), "speaker_iri": next(iter(speakers))}
        if source_id in index and index[source_id] != record:
            raise ValueError(f"Source turn ID is ambiguous: {source_id}")
        index[source_id] = record
    return index


def make_milestones(rows: list[dict], rdf_data: bytes, schema_data: bytes,
                    workbook_name: str) -> tuple[list[Individual], dict]:
    index = utterance_index(rdf_data)
    schema = ET.fromstring(schema_data)
    classes = {node.get("{" + RDF + "}about") for node in schema.findall("{" + OWL + "}Class")}
    generated = []
    milestones = []
    skipped = []
    warnings = []
    seen = set()
    counts = Counter()
    expected_subtype_counts = Counter()
    norm = lambda text: " ".join(text.split())
    for row in rows:
        milestone_id = row.get("milestone_id", "").strip()
        if not milestone_id:
            skipped.append(row)
            continue
        if milestone_id in seen or not re.fullmatch(r"[A-Za-z0-9_-]+", milestone_id):
            raise ValueError(f"Invalid or repeated milestone_id: {milestone_id!r}")
        seen.add(milestone_id)
        kind = row.get("milestone_type", "").strip()
        if kind not in TYPE_MAP or CJF + TYPE_MAP[kind] not in classes:
            raise ValueError(f"No existing ontology class for milestone type {kind!r}")
        sources = parse_turn_ids(row["source_turn_id"])
        quotes = split_quotes(row["text_span"], sources)
        full_texts = split_quotes(row["utterance"], sources)
        iri = CJF + milestone_id
        statements = [
            Statement(DC + "identifier", milestone_id),
            Statement(RDFS + "label", milestone_id),
            Statement(RDFS + "comment", row.get("summary", "")),
            Statement(RDFS + "comment", "Source: " + workbook_name + "; Milestones!A" + str(row["excel_row"]) + ":I" + str(row["excel_row"])),
            Statement(RDFS + "comment", "Source milestone type: " + row["milestone_type"]),
            Statement(RDFS + "comment", "Source turn ID(s): " + row["source_turn_id"]),
        ]
        attributes = next((text for header, text in row.items() if header.startswith("attributes")), "")
        questions = row.get("questions when annotating", "")
        for prefix, text in (("Attributes: ", attributes), ("Annotation question: ", questions)):
            if text:
                statements.append(Statement(RDFS + "comment", prefix + text))
        support_property = SIO_SUPPORT
        if kind == "Expressed Position":
            position = re.fullmatch(r"positionType\s*=\s*(\w+)\s*", attributes)
            if position and position.group(1) in {"agreement", "disagreement"}:
                subtype = "Agreement" if position.group(1) == "agreement" else "Disagreement"
                if CJF + subtype not in classes:
                    raise ValueError(f"Missing ontology class: {subtype}")
                # Assert the annotated evidence polarity; OWL class definitions
                # infer Agreement/Disagreement from these object property links.
                support_property = CJF + ("isPositiveSupportedBy" if subtype == "Agreement" else "isNegativeSupportedBy")
                expected_subtype_counts[subtype] += 1
        evidence_records = []
        for source in sources:
            if source not in index:
                raise ValueError(f"{milestone_id}: source turn {source} has no existing utterance")
            utterance = index[source]
            expected_speaker = CJF + "Mar11GroupB" + row["speaker"].strip().capitalize()
            if utterance["speaker_iri"] != expected_speaker:
                raise ValueError(f"{milestone_id}: source turn {source} has a different speaker")
            for field, text in (("utterance", full_texts[source]), ("text_span", quotes[source])):
                if norm(text) not in norm(utterance["text"]):
                    warnings.append({"milestone_id": milestone_id, "source_turn_id": source,
                                     "column": field, "workbook_text": text,
                                     "existing_utterance_text": utterance["text"]})
            span_iri = iri + "TextSpanTurn" + str(utterance["turn_number"])
            statements.append(Statement(support_property, span_iri, True))
            generated.append(individual(span_iri, CJF + "TextSpan",
                Statement(RDFS + "label", milestone_id + " evidence, source turn " + source),
                Statement(CJF + "hasConversationText", quotes[source]),
                Statement(CJF + "isPartOfUtterance", utterance["iri"], True)))
            evidence_records.append({"source_turn_id": source, "utterance_iri": utterance["iri"],
                                     "hasTurnNumber": utterance["turn_number"], "text_span_iri": span_iri,
                                     "text": quotes[source], "support_property": support_property})
        generated.append(individual(iri, CJF + TYPE_MAP[kind], *statements))
        milestones.append({"milestone_id": milestone_id, "iri": iri, "class_iri": CJF + TYPE_MAP[kind],
                           "source_row": row, "evidence": evidence_records})
        counts[kind] += 1
    return generated, {"milestone_count": len(milestones),
                       "text_span_count": len(generated) - len(milestones),
                       "milestone_types": dict(counts),
                       "expected_inferred_position_subtypes": dict(expected_subtype_counts),
                       "skipped_rows_without_milestone_id": skipped,
                       "text_alignment_warnings": warnings, "milestones": milestones}


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
        paths = [args.workbook.resolve(), args.individuals.resolve(), args.ontology.resolve()]
        backup = (args.backup or target.with_name(target.name + ".milestones.bak")).resolve()
        report_path = args.report.resolve() if args.report else None
        if target in {paths[0], paths[2]} or backup in {*paths, target} or (report_path and report_path in {*paths, target, backup}):
            raise ValueError("Workbook, schema, RDF, backup, and report paths must not overwrite one another")
        original = args.individuals.read_bytes()
        rows, routing = read_milestones(args.workbook)
        generated, report = make_milestones(rows, original, args.ontology.read_bytes(), args.workbook.name)
        updated, added = append_individuals(original, generated)
        changed = not target.exists() or target.read_bytes() != updated
        if args.individuals.read_bytes() != original:
            raise ValueError("Individuals file changed during import; rerun against the latest saved version")
        if changed:
            if target.exists() and not backup.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                with backup.open("xb") as handle:
                    handle.write(target.read_bytes())
            atomic_write(target, updated)
        report.update(routing)
        report.update({"workbook": str(args.workbook.resolve()),
                       "workbook_sha256": hashlib.sha256(args.workbook.read_bytes()).hexdigest(),
                       "individuals": str(target), "added_individuals": added,
                       "already_present_individuals": len(generated) - added, "output_changed": changed})
        if report_path:
            atomic_write(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(f"Milestones sheet only: {report['milestone_count']} milestones and {report['text_span_count']} evidence TextSpans.")
        print(f"Added {added} individuals; already present {len(generated) - added}. Output: {target}")
        print(f"Skipped {len(report['skipped_rows_without_milestone_id'])} rows without milestone IDs; text alignment warnings: {len(report['text_alignment_warnings'])}.")
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
