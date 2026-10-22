#!/usr/bin/env python3
"""Convert numbered Speaker A/B/etc. Markdown turns to the dialogue XML format.

Accepts plain or bold turns, including escaped bold around speaker labels.
Unknown dates, timestamps, and dialogue annotations are left absent or empty.
Use xml_to_individuals.py to import the resulting XML into the ontology.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from xml_to_individuals import atomic_write


def markdown_to_xml(markdown: str, conversation_id: str) -> bytes:
    if not conversation_id.strip():
        raise ValueError("Conversation identifier must not be empty")
    root = ET.Element("Dialogue", {"id": conversation_id})
    for line_number, raw_line in enumerate(markdown.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("**") and line.endswith("**"):
            line = line[2:-2]
        numbered = re.fullmatch(r"([1-9]\d*)\.[ \t]+(.*)", line)
        if not numbered:
            raise ValueError(f"Line {line_number}: expected a numbered speaker turn")
        source_number, content = numbered.groups()
        if int(source_number) != len(root) + 1:
            raise ValueError(f"Line {line_number}: expected turn {len(root) + 1}, found {source_number}")
        for marker in (r"\*\*", "**", ""):
            label = re.fullmatch(
                re.escape(marker) + r"(Speaker [A-Za-z0-9_-]+):" + re.escape(marker) + r"[ \t](.*)",
                content,
            )
            if label:
                break
        if label is None or not label.group(2).strip():
            raise ValueError(f"Line {line_number}: expected a Speaker label and nonempty utterance")
        speaker, text = label.groups()
        turn = ET.SubElement(root, "turn", {
            "comm_act_type": "", "dialog_act": "", "end_time": "", "link_to": "",
            "mode": "", "polarity": "", "pos": "", "pos_count": "", "pos_origin": "",
            "speaker": speaker, "topic": "", "turn_no": source_number,
        })
        turn.text = text
    if not len(root):
        raise ValueError("Markdown contains no conversation turns")
    ET.indent(root)
    declaration = b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    return declaration + ET.tostring(root, encoding="utf-8") + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="Destination dialogue XML")
    parser.add_argument("--conversation-id", required=True, help="Exact conversation identifier")
    args = parser.parse_args(argv)
    try:
        source, target = args.markdown.resolve(), args.output.resolve()
        if source == target:
            raise ValueError("XML output must not overwrite the Markdown source")
        xml_data = markdown_to_xml(source.read_text(encoding="utf-8-sig"), args.conversation_id)
        if not target.exists() or target.read_bytes() != xml_data:
            atomic_write(target, xml_data)
        print(f"Validated {len(ET.fromstring(xml_data))} turns. XML: {target}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
