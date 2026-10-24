#!/usr/bin/env python3
"""Link recorded relationship-based state changes to their triggering objects.

Reads only States and Relationships. Requires the state histories and milestone
relationships to have been imported first. Reference state labels select the
annotated transition; this importer does not assert inferred state subclasses.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

from initial_states_to_individuals import REQUIRED_COLUMNS
from milestones_to_individuals import RDFS, parse_turn_ids, read_worksheet, utterance_index
from relationships_to_individuals import (
    BASE_CLASS, RELATIONSHIPS, append_source_links, inherited_types, schema_index,
)
from state_transitions_to_individuals import make_transitions, property_values
from xml_to_individuals import (
    CJF, RDF, DEFAULT_INDIVIDUALS, Statement, atomic_write, existing_subjects, read_xml,
)


# Current reference label -> target type, predecessor label -> triggering kind,
# and permitted source types. These are the relationship-based transitions only.
RULES = {
    'Addressed': ('Issue', {'Open': 'addresses'}, {'Claim', 'Option', 'Outcome'}),
    'Answered': ('InformationRequest', {'Open': 'answers'}, {'Claim', 'Option', 'Issue', 'ExpressedPosition'}),
    'Resolved': ('Issue', {'Open': 'resolves', 'Addressed': 'resolves'}, {'Outcome'}),
    'Contested': ('Claim', {'Unassessed': 'challenges'}, {'Issue', 'Claim'}),
    'Supported': ('Claim', {'Unassessed': 'supports'}, {'Claim'}),
    'SupportedContested': ('Claim', {'Supported': 'challenges', 'Contested': 'supports'}, {'Issue', 'Claim'}),
}
RELATIONSHIP_COLUMNS = {'from_milestone_id', 'relationship', 'to_milestone_id', 'evidence_turn_ids', 'reason'}


def reference_label(label):
    return 'SupportedContested' if label == 'Supported and Contested' else label


def parent_properties(properties, iri):
    parents, pending = {iri}, [iri]
    while pending:
        node = properties.get(pending.pop())
        if node is None:
            continue
        for parent in node.findall('{' + RDFS + '}subPropertyOf'):
            value = parent.get('{' + RDF + '}resource')
            if value and value not in parents:
                parents.add(value)
                pending.append(value)
    return parents


def link_triggers(state_rows, relationship_rows, rdf_data, schema_data, workbook_name, *,
                  conversation_prefix='Mar11GroupB'):
    classes, properties = schema_index(schema_data)
    trigger = CJF + 'hasTriggeringRelationship'
    if trigger not in properties:
        raise ValueError('The schema is missing hasTriggeringRelationship')
    prop = properties[trigger]
    domain, range_ = prop.find('{' + RDFS + '}domain'), prop.find('{' + RDFS + '}range')
    if (domain is None or range_ is None
            or domain.get('{' + RDF + '}resource') != CJF + 'StateAssignment'
            or range_.get('{' + RDF + '}resource') != BASE_CLASS):
        raise ValueError('hasTriggeringRelationship has the wrong domain or range')
    checked, history = make_transitions(state_rows, rdf_data, schema_data, workbook_name,
                                        conversation_prefix=conversation_prefix)
    if checked != rdf_data:
        raise ValueError('Import all state assignments before linking their triggers')
    subjects = existing_subjects(read_xml(rdf_data))
    utterances = utterance_index(rdf_data, conversation_prefix)
    by_iri = {turn['iri']: turn for turn in utterances.values()}
    assignments = {record['assignment_iri']: record for record in history['assignments']}
    parents = {iri: parent_properties(properties, iri) for iri in properties}
    targets = defaultdict(set)
    for source, definitions in subjects.items():
        for node in definitions:
            for child in node:
                target = child.get('{' + RDF + '}resource')
                if not target:
                    continue
                predicate = child.tag[1:].replace('}', '', 1)
                for parent in parents.get(predicate, {predicate}):
                    targets[(parent, source)].add(target)

    def row_turns(row):
        ids = parse_turn_ids(row['evidence_turn_ids'])
        if not ids or any(source not in utterances for source in ids):
            raise ValueError(f"Relationships row {row['excel_row']}: unknown evidence turn")
        return {utterances[source]['iri'] for source in ids}

    def evidence_turns(iri):
        spans = property_values(subjects, iri, 'hasStateEvidence')
        spans |= {child.get('{' + RDF + '}resource') for node in subjects.get(iri, [])
                  for child in node if child.tag == '{http://semanticscience.org/resource/}SIO_000206'}
        turns = property_values(subjects, iri, 'hasUtterance')
        for span in spans:
            span_turns = property_values(subjects, span, 'isPartOfUtterance')
            if len(span_turns) != 1:
                raise ValueError(f'Evidence span has ambiguous or missing utterance: {span}')
            turns |= span_turns
        if not turns or not turns <= by_iri.keys():
            raise ValueError(f'Missing or cross-conversation evidence: {iri}')
        return turns

    source_links, expected, records = defaultdict(list), {}, []
    skipped, direct_selections = [], []
    for record in history['assignments']:
        assignment, move = record['assignment_iri'], record['move_iri']
        if record['initial']:
            if property_values(subjects, assignment, 'hasTriggeringRelationship'):
                raise ValueError(f'Initial assignment unexpectedly has a trigger: {assignment}')
            continue
        label = reference_label(record['reference_state_label'])
        if label == 'Selected':
            direct_selections.append({'assignment_iri': assignment,
                'reason': 'Selection remains a direct selects assertion; no relationship individual is introduced.'})
            continue
        if label not in RULES:
            skipped.append({'assignment_iri': assignment, 'reference_state_label': label})
            continue
        move_type, predecessors, source_types = RULES[label]
        previous = assignments[record['previous_assignment_iri']]
        previous_label = reference_label(previous['reference_state_label'])
        if previous_label not in predecessors:
            raise ValueError(f'No relationship-based transition from {previous_label} to {label}: {assignment}')
        kind = predecessors[previous_label]
        if kind == 'supports':
            source_types = {'Claim'}
        if CJF + move_type not in inherited_types(subjects[move], classes):
            raise ValueError(f'Wrong conversation move type for {label}: {move}')
        cls, makes, aims, _ = RELATIONSHIPS[kind]
        assignment_evidence = evidence_turns(assignment)
        matches = {}
        for row in relationship_rows:
            if row['relationship'].strip() != kind or CJF + row['to_milestone_id'].strip() != move:
                continue
            evidence = row_turns(row)
            # Require the complete evidence, not one shared context span. A
            # trigger must also include the utterance where the change applies.
            if (not evidence <= assignment_evidence
                    or max(by_iri[turn]['turn_number'] for turn in evidence) != record['turn_number']):
                continue
            source = CJF + row['from_milestone_id'].strip()
            if source == move or source not in subjects or not inherited_types(subjects[source], classes).intersection(
                {CJF + name for name in source_types}
            ):
                raise ValueError(f'Invalid triggering relationship source: {source}')
            candidates = {iri for iri in targets.get((CJF + makes, source), ())
                          if move in targets.get((CJF + aims, iri), ())
                          and CJF + cls in inherited_types(subjects.get(iri, []), classes)}
            if len(candidates) > 1:
                raise ValueError(f'Duplicate relationship individuals for {source} {kind} {move}')
            if candidates:
                iri = next(iter(candidates))
                if evidence_turns(iri) != evidence:
                    raise ValueError(f'Relationship evidence differs from the worksheet: {iri}')
            else:
                raise ValueError(f'Import the missing relationship before linking its trigger: {source} {kind} {move}')
            matches[iri] = {'relationship_iri': iri, 'source_iri': source,
                            'evidence_turns': sorted(by_iri[turn]['turn_number'] for turn in evidence)}
        if not matches:
            raise ValueError(f'No complete relationship evidence establishes this transition: {assignment}')
        expected[assignment] = set(matches)
        unexpected = property_values(subjects, assignment, 'hasTriggeringRelationship') - matches.keys()
        if unexpected:
            raise ValueError(f'Existing trigger conflicts with the annotated transition: {assignment}: {sorted(unexpected)}')
        source_links[assignment].extend(Statement(trigger, iri, True) for iri in sorted(matches))
        records.append({'assignment_iri': assignment, 'move_iri': move, 'turn_number': record['turn_number'],
                        'reference_state_label': label, 'trigger_kind': kind, 'triggers': list(matches.values())})

    source_links = {iri: list(dict.fromkeys(links)) for iri, links in source_links.items()}
    updated, new_links = append_source_links(rdf_data, source_links)
    after = existing_subjects(read_xml(updated))
    for assignment, triggers in expected.items():
        if property_values(after, assignment, 'hasTriggeringRelationship') != triggers:
            raise ValueError(f'Trigger links failed verification: {assignment}')
        for iri in triggers:
            if BASE_CLASS not in inherited_types(after[iri], classes):
                raise ValueError(f'Trigger is not a CJF conversation move relationship: {iri}')
    for iri, nodes in subjects.items():
        old = {ET.tostring(child).strip() for node in nodes for child in node}
        current = {ET.tostring(child).strip() for node in after[iri] for child in node}
        if not old <= current:
            raise ValueError(f'An original assertion changed: {iri}')
    report = {'conversation_prefix': conversation_prefix,
        'rule_based_assignments': len(records), 'initial_assignments_without_triggers': history['initial_assignments_reused'],
        'trigger_links': sum(map(len, expected.values())),
        'new_trigger_links': sum(len(values - property_values(subjects, iri, 'hasTriggeringRelationship'))
                                 for iri, values in expected.items()),
        'trigger_links_by_kind': dict(Counter(record['trigger_kind'] for record in records
                                            for _ in record['triggers'])),
        'new_relationship_individuals': 0,
        'new_assertions': new_links, 'direct_selection_assignments_unchanged': direct_selections,
        'skipped_non_relationship_transitions': skipped,
        'original_assertions_preserved': True, 'assignments': records}
    return updated, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--individuals', type=Path, default=DEFAULT_INDIVIDUALS)
    parser.add_argument('--ontology', type=Path, default=DEFAULT_INDIVIDUALS.with_name('tracking-cjf.rdf'))
    parser.add_argument('--conversation-prefix', default='Mar11GroupB')
    parser.add_argument('--id-column', default='milestone_id')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--backup', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        target = (args.output or args.individuals).resolve()
        inputs = {args.workbook.resolve(), args.individuals.resolve(), args.ontology.resolve()}
        backup = (args.backup or target.with_name(target.name + '.triggers.bak')).resolve()
        report_path = args.report.resolve() if args.report else None
        if target in {args.workbook.resolve(), args.ontology.resolve()} or backup in inputs | {target} or (
            report_path and report_path in inputs | {target, backup}
        ):
            raise ValueError('Workbook, RDF, schema, backup, and report paths must not overlap')
        original, schema, source = args.individuals.read_bytes(), args.ontology.read_bytes(), args.workbook.read_bytes()
        state_rows, state_routing = read_worksheet(args.workbook, 'States', REQUIRED_COLUMNS,
                                                   column_aliases={args.id_column: 'milestone_id'})
        relationship_rows, relationship_routing = read_worksheet(args.workbook, 'Relationships', RELATIONSHIP_COLUMNS)
        updated, report = link_triggers(state_rows, relationship_rows, original, schema, args.workbook.name,
                                        conversation_prefix=args.conversation_prefix)
        repeated, second = link_triggers(state_rows, relationship_rows, updated, schema, args.workbook.name,
                                         conversation_prefix=args.conversation_prefix)
        if repeated != updated or second['new_trigger_links'] or second['new_relationship_individuals']:
            raise ValueError('An unchanged rerun would modify the RDF')
        if args.individuals.read_bytes() != original or args.ontology.read_bytes() != schema or args.workbook.read_bytes() != source:
            raise ValueError('An input changed during import; rerun against the latest files')
        changed = not target.exists() or target.read_bytes() != updated
        if changed and not args.dry_run:
            if target.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                if backup.exists() and backup.read_bytes() != target.read_bytes():
                    raise ValueError('Existing backup differs from the current target; choose a new backup path')
                if not backup.exists():
                    with backup.open('xb') as handle:
                        handle.write(target.read_bytes())
            atomic_write(target, updated)
        report.update({'workbook': str(args.workbook.resolve()), 'individuals': str(target),
            'id_column': args.id_column, 'worksheets': [state_routing, relationship_routing],
            'workbook_sha256': hashlib.sha256(source).hexdigest(), 'schema_sha256': hashlib.sha256(schema).hexdigest(),
            'before_sha256': hashlib.sha256(original).hexdigest(), 'after_sha256': hashlib.sha256(updated).hexdigest(),
            'dry_run': args.dry_run, 'output_changed': changed and not args.dry_run,
            'repeat_import_byte_identical': True, 'backup': str(backup) if backup.exists() else None})
        if report_path:
            atomic_write(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode())
        print(f"Linked {report['rule_based_assignments']} rule-based assignments to {report['trigger_links']} triggering relationships.")
        print(f"Added {report['new_trigger_links']} trigger links and {report['new_relationship_individuals']} relationship individuals.")
        print(('Dry run. Output: ' if args.dry_run else 'Output: ') + str(target))
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
