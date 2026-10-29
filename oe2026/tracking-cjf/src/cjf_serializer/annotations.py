"""Refactored standard-library XLSX reader and evidence-reference helpers.

Originally milestones_to_individuals.py; shared by the installed library and
legacy importers. No ontology filename, graph state, or CLI defaults live here.
"""
from __future__ import annotations
from pathlib import Path
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile
SHEET_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
def read_worksheet(workbook: Path, sheet_name: str,
                   required: set[str], *,
                   column_aliases: dict[str, str] | None = None) -> tuple[list[dict], dict]:
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
                aliases = column_aliases or {}
                if not set(aliases).issubset({text.strip() for text in values.values()}):
                    raise ValueError(f"The {sheet_name} header is missing a configured column alias")
                headers = {column: aliases.get(text.strip(), text.strip())
                           for column, text in values.items()}
                if True:
                    names = [name for name in headers.values() if name]
                    if len(names) != len(set(names)):
                        raise ValueError(f"The {sheet_name} header has duplicate columns after applying aliases")
                if not required.issubset(set(headers.values())):
                    raise ValueError(f"The {sheet_name} header does not have the required columns")
                continue
            record = {headers[column]: text for column, text in values.items() if column in headers}
            record["excel_row"] = int(row.attrib["r"])
            if any(str(v).strip() for k,v in record.items() if k != "excel_row"):
                rows.append(record)
        return rows, {"sheet": sheet.attrib["name"], "worksheet_member": member,
                      "worksheet_members_read": [member]}

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
