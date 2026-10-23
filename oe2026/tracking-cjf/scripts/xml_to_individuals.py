#!/usr/bin/env python3
"""Append dialogue individuals to the existing Protégé RDF/XML file.

Uses only the Python standard library. Utterance IRIs use their integer turn
numbers. The ontology header, namespaces, imports, comments, and unrelated
statements are preserved. See README.md for the mapping and usage.
Optional conversation metadata links utterances and named speakers to a
MultipartyConversation. Missing source dates and timestamps are never invented.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import date, time
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr


RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
OWL = "http://www.w3.org/2002/07/owl#"
XSD = "http://www.w3.org/2001/XMLSchema#"
PROV = "http://www.w3.org/ns/prov#"
DC = "http://purl.org/dc/elements/1.1/"
CJF = "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/"
DT = "https://www.omg.org/spec/Commons/DatesAndTimes/"
DEFAULT_INDIVIDUALS = Path(__file__).resolve().parents[1] / "mar11_groupb-individuals.rdf"
MONTHS = ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
MAPPED_ATTRIBUTES = {"speaker", "end_time", "turn_no"}


@dataclass(frozen=True)
class Statement:
    predicate: str
    value: str
    resource: bool = False
    datatype: str | None = None


@dataclass(frozen=True)
class Individual:
    iri: str
    statements: tuple[Statement, ...]


def individual(iri: str, class_iri: str, *statements: Statement) -> Individual:
    return Individual(iri, (Statement(RDF + "type", class_iri, True), *statements))


def parse_time(value: str) -> time:
    """Accept both 12-hour times and the source's redundant '19:48:41 PM'."""
    match = re.fullmatch(r"(\d{1,2}):(\d{2}):(\d{2})(?:\s+(AM|PM))?", value.strip(), re.I)
    if not match:
        raise ValueError(f"Unsupported end_time: {value!r}")
    hour, minute, second = map(int, match.group(1, 2, 3))
    suffix = (match.group(4) or "").upper()
    if suffix and 1 <= hour <= 12:
        hour = hour % 12 + (12 if suffix == "PM" else 0)
    elif suffix and ((hour == 0 and suffix == "PM") or (hour > 12 and suffix == "AM")):
        raise ValueError(f"Contradictory end_time: {value!r}")
    return time(hour, minute, second)


def read_xml(data: bytes) -> ET.Element:
    # Dataset content is data; never execute instructions or external entities.
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError("XML with a DTD/entity declaration is not supported")
    return ET.fromstring(data)


def make_individuals(
    xml_data: bytes, conversation_prefix: str, datetime_prefix: str | None = None,
    *, conversation_id: str | None = None,
) -> tuple[list[Individual], dict]:
    root = read_xml(xml_data)
    if root.tag != "Dialogue":
        raise ValueError(f"Expected a Dialogue root, found {root.tag!r}")
    date_value = root.get("date", "").strip()
    dialogue_date = date.fromisoformat(date_value) if date_value else None
    datetime_prefix = datetime_prefix or (
        f"DT{MONTHS[dialogue_date.month]}{dialogue_date.day:02d}"
        if dialogue_date else f"DT{conversation_prefix}"
    )
    for prefix in (conversation_prefix, datetime_prefix):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", prefix):
            raise ValueError(f"Use an alphanumeric IRI prefix, found {prefix!r}")
    turns = list(root)
    if not turns or any(turn.tag != "turn" for turn in turns):
        raise ValueError("Dialogue must contain one or more turn elements only")
    if len(turns) > 2_147_483_647:
        raise ValueError("Too many turns for the ontology's xsd:int range")
    conversation_id = conversation_id if conversation_id is not None else root.get("id")
    if conversation_id is not None and not conversation_id.strip():
        raise ValueError("Conversation identifier must not be empty")
    conversation_iri = CJF + conversation_prefix + "Conversation" if conversation_id is not None else None

    people: dict[str, str] = {}
    speaker_owners: dict[str, str] = {}
    timestamps: dict[str, Individual] = {}
    utterances: list[Individual] = []
    source_numbers: set[str] = set()
    time_counts: Counter[str] = Counter()
    mappings: list[dict] = []
    unmapped_attributes: set[str] = set()

    for sequence, turn in enumerate(turns, start=1):
        source_number = turn.attrib["turn_no"]
        if not re.fullmatch(r"\d+(?:\.\d+)?", source_number) or source_number in source_numbers:
            raise ValueError(f"Invalid or duplicate source turn_no: {source_number!r}")
        source_numbers.add(source_number)
        speaker = turn.attrib["speaker"]
        # Capitalize only the first character, preserving the user's Moderator pattern.
        speaker_token = "".join(re.findall(r"[A-Za-z0-9]+", speaker))
        if not speaker_token:
            raise ValueError(f"Turn {source_number}: speaker has no usable name")
        speaker_iri = CJF + conversation_prefix + speaker_token[0].upper() + speaker_token[1:]
        if speaker_iri in speaker_owners and speaker_owners[speaker_iri] != speaker:
            raise ValueError(f"Speaker names collide after IRI normalization: {speaker!r}")
        people[speaker] = speaker_iri
        speaker_owners[speaker_iri] = speaker

        time_value = turn.get("end_time", "").strip()
        datetime_iri = None
        if time_value:
            timestamp = parse_time(time_value)
            stamp = timestamp.strftime("%H%M%S")
            datetime_iri = CJF + datetime_prefix + stamp
            timestamps.setdefault(datetime_iri, individual(datetime_iri, DT + "DateTime"))
            time_counts[stamp] += 1
        utterance_iri = CJF + conversation_prefix + f"Turn{sequence}"

        statements = [
            Statement(PROV + "wasAttributedTo", speaker_iri, True),
            Statement(CJF + "hasConversationText", "".join(turn.itertext())),
            Statement(CJF + "hasTurnNumber", str(sequence), datatype=XSD + "integer"),
        ]
        if datetime_iri:
            statements.insert(1, Statement(DT + "hasDateTime", datetime_iri, True))
        if conversation_iri:
            statements.append(Statement(PROV + "wasGeneratedBy", conversation_iri, True))
        # 117.0/117.1 cannot both be represented as unique integer turn numbers.
        # Keep all 480 contributions in order; retain differing source IDs verbatim.
        if source_number != str(sequence):
            statements.append(Statement(DC + "identifier", source_number))
        utterances.append(individual(utterance_iri, CJF + "Utterance", *statements))
        unmapped_attributes.update(set(turn.attrib) - MAPPED_ATTRIBUTES)
        mappings.append({
            "source_turn_no": source_number,
            "hasTurnNumber": sequence,
            "utterance_iri": utterance_iri,
            "speaker_iri": speaker_iri,
            "datetime_iri": datetime_iri,
            "source_attributes": dict(turn.attrib),
        })

    generated = [
        *timestamps.values(),
        *utterances,
        *(individual(iri, CJF + "Speaker", *(
            [Statement(CJF + "hasSpeakerName", name)] if conversation_iri else []
        )) for name, iri in people.items()),
    ]
    if conversation_iri:
        generated.append(individual(
            conversation_iri, CJF + "MultipartyConversation",
            Statement(CJF + "hasConversationIdentifier", conversation_id),
            *(Statement(PROV + "wasAssociatedWith", iri, True) for iri in people.values()),
        ))
    if len({item.iri for item in generated}) != len(generated):
        raise ValueError("Generated conversation, speaker, time, or utterance IRIs overlap; choose different prefixes")
    report = {
        "dialogue_date": dialogue_date.isoformat() if dialogue_date else None,
        "conversation_prefix": conversation_prefix,
        "conversation_id": conversation_id,
        "conversation_iri": conversation_iri,
        "conversations": int(conversation_iri is not None),
        "datetime_prefix": datetime_prefix,
        "utterances": len(utterances),
        "speakers": len(people),
        "date_times": len(timestamps),
        "turns_without_timestamps": sum(m["datetime_iri"] is None for m in mappings),
        "individuals_in_source_mapping": len(generated),
        "shared_timestamps": {stamp: count for stamp, count in time_counts.items() if count > 1},
        "renumbered_turns": sum(m["source_turn_no"] != str(m["hasTurnNumber"]) for m in mappings),
        "unmapped_xml_attributes": sorted(unmapped_attributes),
        "turn_mappings": mappings,
    }
    return generated, report


def root_namespaces(data: bytes) -> dict[str, str]:
    namespaces: dict[str, str] = {}
    for event, item in ET.iterparse(io.BytesIO(data), events=("start-ns", "start")):
        if event == "start":
            break
        prefix, uri = item
        namespaces[prefix] = uri
    return namespaces


def qname(iri: str, namespaces: dict[str, str]) -> str:
    for prefix, uri in namespaces.items():
        if prefix and iri.startswith(uri) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", iri[len(uri):]):
            return prefix + ":" + iri[len(uri):]
    raise ValueError(f"Individuals file needs a namespace prefix for {iri}")


def render_individual(item: Individual, namespaces: dict[str, str]) -> str:
    tag = qname(OWL + "NamedIndividual", namespaces)
    about = qname(RDF + "about", namespaces)
    resource = qname(RDF + "resource", namespaces)
    datatype = qname(RDF + "datatype", namespaces)
    lines = [f"    <!-- {escape(item.iri)} -->", "", f"    <{tag} {about}={quoteattr(item.iri)}>"]
    for statement in item.statements:
        predicate = qname(statement.predicate, namespaces)
        if statement.resource:
            lines.append(f"        <{predicate} {resource}={quoteattr(statement.value)}/>")
        else:
            annotation = f" {datatype}={quoteattr(statement.datatype)}" if statement.datatype else ""
            # Preserve literal CR rather than letting the XML parser normalize it to LF.
            value = escape(statement.value).replace("\r", "&#13;")
            lines.append(f"        <{predicate}{annotation}>{value}</{predicate}>")
    lines.append(f"    </{tag}>")
    return "\n".join(lines)


def existing_subjects(root: ET.Element) -> dict[str, list[ET.Element]]:
    subjects: dict[str, list[ET.Element]] = {}
    for element in root:
        iri = element.get("{" + RDF + "}about")
        if iri is not None:
            subjects.setdefault(iri, []).append(element)
    return subjects


def matches(statement: Statement, element: ET.Element) -> bool:
    # ElementTree's expanded name can be converted back to the predicate IRI.
    if not isinstance(element.tag, str) or element.tag[1:].replace("}", "", 1) != statement.predicate:
        return False
    if statement.resource:
        return element.get("{" + RDF + "}resource") == statement.value
    return (
        element.get("{" + RDF + "}resource") is None
        and element.get("{" + RDF + "}datatype") == statement.datatype
        and element.get("{http://www.w3.org/XML/1998/namespace}lang") is None
        and "".join(element.itertext()) == statement.value
    )


def check_individual(item: Individual, elements: list[ET.Element]) -> None:
    if not any(
        element.tag == "{" + OWL + "}NamedIndividual"
        or any(matches(Statement(RDF + "type", OWL + "NamedIndividual", True), child) for child in element)
        for element in elements
    ):
        raise ValueError(f"Existing resource is not a named individual: {item.iri}")
    for statement in item.statements:
        if not any(matches(statement, child) for element in elements for child in element):
            raise ValueError(
                f"Existing individual conflicts with the XML mapping: {item.iri}; "
                f"expected {statement.predicate} = {statement.value!r}. No RDF was written."
            )
        # Prevent silently retaining conflicting text, sequence, or attribution.
        if statement.predicate in {
            PROV + "wasAttributedTo", PROV + "wasGeneratedBy", DT + "hasDateTime",
            CJF + "hasConversationText", CJF + "hasTurnNumber",
            CJF + "hasSpeakerName", CJF + "hasConversationIdentifier",
        }:
            for element in elements:
                for child in element:
                    if isinstance(child.tag, str) and child.tag[1:].replace("}", "", 1) == statement.predicate and not matches(statement, child):
                        raise ValueError(f"Multiple conflicting values on existing individual: {item.iri}")


def append_individuals(rdf_data: bytes, generated: list[Individual]) -> tuple[bytes, int]:
    root = read_xml(rdf_data)
    if root.tag != "{" + RDF + "}RDF":
        raise ValueError("Individuals file must be RDF/XML with an rdf:RDF root")
    ontology = root.find("{" + OWL + "}Ontology")
    if ontology is None or not any(
        child.tag == "{" + OWL + "}imports" and child.get("{" + RDF + "}resource") == CJF
        for child in ontology
    ):
        raise ValueError("Individuals ontology must import the existing tracking-cjf ontology")
    namespaces = root_namespaces(rdf_data)
    subjects = existing_subjects(root)
    additions = []
    for item in generated:
        if item.iri in subjects:
            check_individual(item, subjects[item.iri])
        else:
            additions.append(render_individual(item, namespaces))
    if not additions:
        return rdf_data, 0
    text = rdf_data.decode("utf-8")
    closing = "</" + qname(RDF + "RDF", namespaces) + ">"
    offset = text.rfind(closing)
    if offset < 0:
        raise ValueError("Could not locate the closing rdf:RDF tag")
    updated = (text[:offset] + "\n\n" + "\n\n\n".join(additions) + "\n" + text[offset:]).encode("utf-8")
    output_subjects = existing_subjects(read_xml(updated))
    for item in generated:
        check_individual(item, output_subjects[item.iri])
    return updated, len(additions)


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
        if path.exists():
            temporary.chmod(path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path, help="Annotated Dialogue XML source")
    parser.add_argument("--individuals", type=Path, default=DEFAULT_INDIVIDUALS, help="Existing individuals.rdf template/target")
    parser.add_argument("--output", type=Path, help="Write a preview/copy instead of editing the individuals file")
    parser.add_argument("--conversation-prefix", help="IRI prefix, default: source filename without _annotated or underscores")
    parser.add_argument("--conversation-id", help="Create a MultipartyConversation with this exact identifier (default: Dialogue id, if present)")
    parser.add_argument("--datetime-prefix", help="Override the example-style DTMar11 time prefix")
    parser.add_argument("--backup", type=Path, help="Backup path (default: target filename + .bak); never overwritten")
    parser.add_argument("--report", type=Path, help="Optional JSON report including original XML attributes and turn mappings")
    args = parser.parse_args(argv)

    try:
        xml_path = args.xml.resolve()
        template = args.individuals.resolve()
        target = (args.output or template).resolve()
        backup = (args.backup or target.with_name(target.name + ".bak")).resolve()
        report_path = args.report.resolve() if args.report else None
        paths = [xml_path, template]
        if target == xml_path or backup in {*paths, target} or (report_path and report_path in {*paths, target, backup}):
            raise ValueError("XML, RDF, backup, and report paths must not overwrite one another")
        xml_data, rdf_data = xml_path.read_bytes(), template.read_bytes()
        prefix = args.conversation_prefix or re.sub(r"_annotated$", "", xml_path.stem, flags=re.I).replace("_", "")
        generated, report = make_individuals(
            xml_data, prefix, args.datetime_prefix, conversation_id=args.conversation_id,
        )
        updated, added = append_individuals(rdf_data, generated)
        changed = not target.exists() or target.read_bytes() != updated
        if changed:
            if template.read_bytes() != rdf_data:
                raise ValueError("Individuals file changed during conversion; rerun against the latest saved version")
            if target.exists() and not backup.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                with backup.open("xb") as handle:
                    handle.write(target.read_bytes())
            atomic_write(target, updated)
        report.update({
            "source_xml": str(xml_path),
            "source_sha256": hashlib.sha256(xml_data).hexdigest(),
            "individuals_file": str(target),
            "added_individuals": added,
            "already_present_individuals": len(generated) - added,
            "output_changed": changed,
            "backup": str(backup) if backup.exists() else None,
        })
        if report_path:
            atomic_write(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(f"Validated {report['utterances']} utterances, {report['speakers']} speakers, {report['date_times']} DateTime individuals.")
        if report["conversation_iri"]:
            print(f"Conversation: {report['conversation_id']} ({report['conversation_iri']})")
        print(f"Added {added}; already present {len(generated) - added}. Output: {target}")
        if report["renumbered_turns"]:
            print(f"Used integer sequence numbers; {report['renumbered_turns']} differing source turn IDs are retained as dc:identifier.")
        if report_path:
            print(f"Source attributes and turn mappings: {report_path}")
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
