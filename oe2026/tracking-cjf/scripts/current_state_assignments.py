#!/usr/bin/env python3
"""Run SHACL rules and refresh each move's current state assignment.

Requires requirements-shacl.txt. Executes local SHACL Advanced Features without
following ontology imports or materializing OWL state classifications. Existing
current pointers are refreshed; all other RDF/XML content is preserved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from relationships_to_individuals import append_source_links
from xml_to_individuals import CJF, OWL, RDF, Statement, atomic_write, qname, root_namespaces


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_SHAPES = PROJECT / 'shacl' / 'current-state-assignment-rules.ttl'


def history_ends(graph, namespace):
    """Independently check the rule result against complete predecessor chains."""
    moves = set(graph.subjects(namespace.hasStateAssignment, None))
    result, same_turn = {}, 0
    for move in moves:
        assignments = set(graph.objects(move, namespace.hasStateAssignment))
        previous = {assignment: set(graph.objects(assignment, namespace.hasPreviousAssignment))
                    for assignment in assignments}
        leaves = assignments - {value for values in previous.values() for value in values}
        if len(leaves) != 1:
            raise ValueError(f'Expected one terminal assignment for {move}')
        latest = next(iter(leaves))
        visited, cursor = set(), latest
        latest_turn = None
        while cursor is not None:
            if cursor in visited or cursor not in assignments:
                raise ValueError(f'History is cyclic or crosses conversation moves: {move}')
            visited.add(cursor)
            utterances = set(graph.objects(cursor, namespace.assignedAtUtterance))
            if len(utterances) != 1:
                raise ValueError(f'Missing or ambiguous effective utterance: {cursor}')
            numbers = set(graph.objects(next(iter(utterances)), namespace.hasTurnNumber))
            if len(numbers) != 1:
                raise ValueError(f'Missing or ambiguous turn number: {cursor}')
            turn = int(next(iter(numbers)))
            if latest_turn is not None:
                if turn > latest_turn:
                    raise ValueError(f'A predecessor occurs after its successor: {move}')
                same_turn += turn == latest_turn
            latest_turn = turn
            if len(previous[cursor]) > 1:
                raise ValueError(f'A state assignment has several predecessors: {cursor}')
            cursor = next(iter(previous[cursor]), None)
        if visited != assignments:
            raise ValueError(f'Assignment history is disconnected or branches: {move}')
        result[str(move)] = str(latest)
    return result, same_turn


def remove_current_pointers(data, moves):
    """Remove derived pointers from named XML blocks, preserving other content."""
    namespaces = root_namespaces(data)
    tags = '(?:' + '|'.join(re.escape(qname(iri, namespaces)) for iri in
                           (OWL + 'NamedIndividual', RDF + 'Description')) + ')'
    about = re.escape(qname(RDF + 'about', namespaces))
    predicate = re.escape(qname(CJF + 'hasCurrentStateAssignment', namespaces))
    pointer = re.compile(r'[ \t]*<' + predicate + r'\b[^>]*(?:/\s*>|>.*?</' + predicate +
                         r'>)[ \t]*(?:\r?\n)?', re.S)
    text = data.decode('utf-8')
    for iri in moves:
        block = re.compile(r'(?P<start><(?P<tag>' + tags + r')\b[^>]*\b' + about +
                           r'=(?P<quote>[\"\'])' + re.escape(iri) +
                           r'(?P=quote)[^>]*>)(?P<body>.*?)(?P<end></(?P=tag)>)', re.S)
        text = block.sub(lambda match: match['start'] + pointer.sub('', match['body']) + match['end'], text)
    return text.encode('utf-8')


def refresh_current_assignments(rdf_data, shapes_data):
    import pyshacl
    import rdflib
    from pyshacl import validate
    from rdflib.compare import isomorphic

    namespace = rdflib.Namespace(CJF)
    graph = rdflib.Graph().parse(data=rdf_data, format='xml')
    shapes = rdflib.Graph().parse(data=shapes_data, format='turtle')
    original = set(graph)
    moves = set(graph.subjects(namespace.hasStateAssignment, None))
    existing = set(graph.triples((None, namespace.hasCurrentStateAssignment, None)))
    # SHACL CONSTRUCT rules add triples. Recompute this derived predicate rather
    # than retaining a historical "current" pointer after a successor is added.
    for move in moves:
        graph.remove((move, namespace.hasCurrentStateAssignment, None))
    before_rules = set(graph)
    conforms, _, validation_text = validate(
        graph, shacl_graph=shapes, advanced=True, inference='none', inplace=True,
        iterate_rules=True, do_owl_imports=False, meta_shacl=True,
    )
    if not conforms:
        raise ValueError('SHACL validation failed; the RDF has not been changed.\n' + validation_text)
    latest, same_turn = history_ends(graph, namespace)
    expected = {(rdflib.URIRef(move), namespace.hasCurrentStateAssignment, rdflib.URIRef(assignment))
                for move, assignment in latest.items()}
    actual = set(graph.triples((None, namespace.hasCurrentStateAssignment, None)))
    if actual != expected:
        raise ValueError('The SHACL result differs from the independently checked assignment histories')
    if set(graph) - before_rules != expected - before_rules or not before_rules <= set(graph):
        raise ValueError('The SHACL shapes changed assertions outside the current-assignment predicate')
    if existing == expected:
        updated = rdf_data
    else:
        updated = remove_current_pointers(rdf_data, {str(move) for move in moves}) if existing else rdf_data
        links = {move: [Statement(CJF + 'hasCurrentStateAssignment', assignment, True)]
                 for move, assignment in sorted(latest.items())}
        updated, _ = append_source_links(updated, links)
    saved = rdflib.Graph().parse(data=updated, format='xml')
    if set(saved.triples((None, namespace.hasCurrentStateAssignment, None))) != expected:
        raise ValueError('The saved current pointers differ from the SHACL result')
    before_other, after_other = rdflib.Graph(), rdflib.Graph()
    for triple in original:
        if triple[1] != namespace.hasCurrentStateAssignment:
            before_other.add(triple)
    for triple in saved:
        if triple[1] != namespace.hasCurrentStateAssignment:
            after_other.add(triple)
    if not isomorphic(before_other, after_other):
        raise ValueError('An unrelated RDF assertion changed while refreshing current pointers')
    report = {'engine': 'pySHACL', 'pyshacl_version': pyshacl.__version__,
        'rdflib_version': rdflib.__version__, 'shacl_conforms': True,
        'validation_report': validation_text, 'moves_with_state': len(latest),
        'current_assignment_links': len(expected), 'new_current_links': len(expected - existing),
        'stale_current_links_removed': len(existing - expected),
        'same_turn_predecessor_pairs': same_turn,
        'non_current_assertions_preserved': True, 'current_assignment_by_move': dict(sorted(latest.items()))}
    return updated, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--individuals', type=Path, default=PROJECT / 'cq-sample-conversation.rdf')
    parser.add_argument('--shapes', type=Path, default=DEFAULT_SHAPES)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--backup', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        original, shapes = args.individuals.read_bytes(), args.shapes.read_bytes()
        target = (args.output or args.individuals).resolve()
        backup = (args.backup or target.with_name(target.name + '.before-current.' +
                    hashlib.sha256(original).hexdigest()[:12] + '.bak')).resolve()
        report_path = args.report.resolve() if args.report else None
        inputs = {args.individuals.resolve(), args.shapes.resolve()}
        if target == args.shapes.resolve() or backup in inputs | {target} or (
            report_path and report_path in inputs | {target, backup}
        ):
            raise ValueError('RDF, shapes, output, backup, and report paths must not overlap')
        updated, report = refresh_current_assignments(original, shapes)
        repeated, second = refresh_current_assignments(updated, shapes)
        if repeated != updated or second['new_current_links'] or second['stale_current_links_removed']:
            raise ValueError('An unchanged rerun would modify the RDF')
        if args.individuals.read_bytes() != original or args.shapes.read_bytes() != shapes:
            raise ValueError('An input changed during SHACL execution; rerun against the latest files')
        changed = not target.exists() or target.read_bytes() != updated
        if changed and not args.dry_run:
            if target.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                if backup.exists() and backup.read_bytes() != target.read_bytes():
                    raise ValueError('Existing backup differs from the current target')
                if not backup.exists():
                    with backup.open('xb') as handle:
                        handle.write(target.read_bytes())
            atomic_write(target, updated)
        report.update({'individuals': str(target), 'shapes': str(args.shapes.resolve()),
            'before_sha256': hashlib.sha256(original).hexdigest(),
            'after_sha256': hashlib.sha256(updated).hexdigest(),
            'shapes_sha256': hashlib.sha256(shapes).hexdigest(), 'dry_run': args.dry_run,
            'output_changed': changed and not args.dry_run, 'repeat_run_byte_identical': True,
            'backup': str(backup) if backup.exists() else None})
        if report_path:
            atomic_write(report_path, (json.dumps(report, indent=2) + '\n').encode())
        print(f"SHACL conforms: {report['current_assignment_links']} current assignments for {report['moves_with_state']} moves.")
        print(f"Added {report['new_current_links']} pointers; removed {report['stale_current_links_removed']} stale pointers.")
        print(('Dry run. Output: ' if args.dry_run else 'Output: ') + str(target))
        return 0
    except ImportError:
        print('Install SHACL dependencies: python -m pip install -r requirements-shacl.txt', file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, ET.ParseError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
