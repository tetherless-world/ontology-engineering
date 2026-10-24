#!/usr/bin/env python3
"""Clear hasCurrentStateAssignment pointers without removing state histories.

Usage: python remove_current_state_assignments.py conversation.rdf
Add --move-iri IRI to clear only one move; repeat it to select several moves.
The CLI creates a backup before modifying the file. The bytes-based function
can also be called between streamed turns without writing files.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from current_state_assignments import remove_current_pointers
from xml_to_individuals import CJF, atomic_write, existing_subjects, read_xml


CURRENT = '{' + CJF + '}hasCurrentStateAssignment'


def clear_current_assignments(data: bytes, move_iris: set[str] | None = None) -> tuple[bytes, int]:
    """Return RDF/XML with the selected current pointers removed, plus a count."""
    before = existing_subjects(read_xml(data))
    selected = set(before) if move_iris is None else set(move_iris)
    count = sum(child.tag == CURRENT for iri in selected for node in before.get(iri, []) for child in node)
    if not count:
        return data, 0
    updated = remove_current_pointers(data, selected)
    after = existing_subjects(read_xml(updated))
    if before.keys() != after.keys():
        raise ValueError('Removing current pointers unexpectedly changed the named resources')
    for iri, nodes in before.items():
        expected = {ET.tostring(child).strip() for node in nodes for child in node
                    if not (iri in selected and child.tag == CURRENT)}
        actual = {ET.tostring(child).strip() for node in after[iri] for child in node}
        if actual != expected:
            raise ValueError(f'Current pointers could not be cleared without changing other assertions: {iri}')
    return updated, count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rdf', type=Path, help='RDF/XML individuals file to update in place')
    parser.add_argument('--move-iri', action='append', help='Clear only this move; repeat to select several')
    args = parser.parse_args(argv)
    try:
        target = args.rdf.resolve()
        original = target.read_bytes()
        selected = set(args.move_iri) if args.move_iri else None
        updated, count = clear_current_assignments(original, selected)
        if count:
            backup = target.with_name(target.name + '.before-clear-current.' +
                                      hashlib.sha256(original).hexdigest()[:12] + '.bak')
            if target.read_bytes() != original:
                raise ValueError('The RDF changed while being read; rerun against the latest file')
            if backup.exists():
                if backup.read_bytes() != original:
                    raise ValueError('The backup path contains different data')
            else:
                with backup.open('xb') as handle:
                    handle.write(original)
            atomic_write(target, updated)
            print('Backup:', backup)
        print(f'Removed {count} hasCurrentStateAssignment links. File: {target}')
        return 0
    except (OSError, ValueError, ET.ParseError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
