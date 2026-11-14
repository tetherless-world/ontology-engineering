"""Transcript adapters yielding the same ordered Turn contract."""
from __future__ import annotations
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from .annotations import read_worksheet
from .models import Turn, InputValidationError
from .time_utils import parse_time
from .config import read_yaml


def transcript_turns(config, workbook):
    inputs = config.data["inputs"]
    source, sheet = inputs.get("transcript"), inputs.get("transcript_sheet")
    if sheet:
        aliases_path = config.data["annotations"].get("column_map")
        aliases = read_yaml(aliases_path).get("transcript", {}) if aliases_path else {}
        rows, _ = read_worksheet(workbook, sheet, {"source_turn_id", "speaker", "utterance", "sequence"}, column_aliases=aliases)
        turns = [Turn(str(r["source_turn_id"]), int(r["sequence"]), r["speaker"], r["utterance"], r.get("end_time", ""), {"sheet": sheet, "row": r["excel_row"]}) for r in rows]
        turns.sort(key=lambda t: t.sequence)
    else:
        if not source:
            raise InputValidationError("Supply a transcript file, transcript_sheet, or base_individuals; move summaries are not a transcript")
        text = Path(source).read_text(encoding="utf-8-sig")
        adapter = inputs.get("adapter")
        turns = []
        if adapter == "dialogue_xml":
            if "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
                raise InputValidationError("Transcript XML must not contain a DTD")
            root = ET.fromstring(text)
            if root.tag != "Dialogue" or not root.get("id"):
                raise InputValidationError("Transcript XML requires Dialogue id")
            for i, node in enumerate(root.findall("turn"), 1):
                turns.append(Turn(node.get("turn_no", ""), int(node.get("sequence", i)), node.get("speaker", ""), "".join(node.itertext()), node.get("end_time", ""), {"xml_attributes": dict(node.attrib)}))
        elif adapter in {"numbered_speakers", "corpus_chat"}:
            for line_no, raw in enumerate(text.splitlines(), 1):
                if not raw.strip():
                    continue
                line = raw.strip()
                if adapter == "numbered_speakers":
                    # Refactored from markdown_to_xml: remove structural bold
                    # only around the numbered header/speaker, not utterance text.
                    if line.startswith("**") and line.endswith("**"):
                        line = line[2:-2]
                    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\.[ \t]+(?:\\?\*\\?\*)?(Speaker [A-Za-z0-9_-]+):(?:\\?\*\\?\*)?[ \t]+(.*)", line)
                    if match:
                        sid, speaker, utterance = match.groups()
                        timestamp = ""
                else:
                    match = re.fullmatch(r"(.+?) \((\d{1,2}:\d{2}:\d{2}(?:\s+[AP]M)?)\):[ \t]*(.*)", line)
                    if match:
                        speaker, timestamp, utterance = match.groups()
                        parse_time(timestamp)
                        sid = str(len(turns) + 1)
                if not match:
                    if inputs.get("continuation_lines", "reject") == "append" and turns and not re.match(r"^\d+\.", line):
                        turns[-1].text += "\n" + raw
                        turns[-1].provenance.setdefault("continuation_lines", []).append(line_no)
                        continue
                    raise InputValidationError(f"Transcript line {line_no}: malformed {adapter} header")
                turns.append(Turn(sid, len(turns) + 1, speaker, utterance, timestamp, {"line": line_no}))
        else:
            raise InputValidationError("Select adapter numbered_speakers, corpus_chat, or dialogue_xml")
    if not turns:
        raise InputValidationError("Transcript contains no turns")
    if [t.sequence for t in turns] != list(range(1, len(turns) + 1)):
        raise InputValidationError("Transcript sequence must be unique, consecutive positive integers")
    if len({t.source_id for t in turns}) != len(turns):
        raise InputValidationError("Transcript source IDs must be unique strings")
    if any(not t.source_id or not t.speaker.strip() or not t.text.strip() for t in turns):
        raise InputValidationError("Each transcript turn requires source ID, speaker and text")
    return turns


def dialogue_xml(turns, conversation_id):
    root = ET.Element("Dialogue", {"id": conversation_id})
    for turn in turns:
        attrs = {"turn_no": turn.source_id, "sequence": str(turn.sequence), "speaker": turn.speaker}
        if turn.timestamp:
            attrs["end_time"] = turn.timestamp
        ET.SubElement(root, "turn", attrs).text = turn.text
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)
