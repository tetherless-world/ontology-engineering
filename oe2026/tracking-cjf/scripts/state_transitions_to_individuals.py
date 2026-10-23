#!/usr/bin/env python3
"""Import States-sheet transitions as base State individuals and assignment chains.

Existing initial assignments are required. Initial-before-transition ordering is
supported within a turn; multiple transitions at one turn are rejected as
ambiguous. Workbook state labels are annotations, never asserted state subtypes.
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
import zipfile

from initial_states_to_individuals import REQUIRED_COLUMNS, STATE_TYPES
from milestones_to_individuals import RDFS, parse_turn_ids, read_worksheet, utterance_index
from relationships_to_individuals import append_source_links
from xml_to_individuals import (
    CJF, OWL, RDF, DEFAULT_INDIVIDUALS, Statement, append_individuals,
    atomic_write, existing_subjects, individual, read_xml,
)


INITIAL_LABELS = {label: name for name, (label, _) in STATE_TYPES.items()}


def property_values(subjects, iri, name):
    return {child.get('{' + RDF + '}resource') or ''.join(child.itertext())
            for node in subjects.get(iri, []) for child in node
            if child.tag == '{' + CJF + '}' + name}


def class_types(subjects, iri):
    return {child.get('{' + RDF + '}resource') for node in subjects.get(iri, [])
            for child in node.findall('{' + RDF + '}type')}


def assignment_index(subjects):
    owners, state_owners = defaultdict(set), defaultdict(set)
    for move in subjects:
        for assignment in property_values(subjects, move, 'hasStateAssignment'):
            owners[assignment].add(move)
    index = defaultdict(list)
    for assignment, moves in owners.items():
        if class_types(subjects, assignment).isdisjoint({CJF + 'StateAssignment'}):
            raise ValueError(f'Linked resource is not a StateAssignment: {assignment}')
        states = property_values(subjects, assignment, 'assignedState')
        turns = property_values(subjects, assignment, 'assignedAtUtterance')
        previous = property_values(subjects, assignment, 'hasPreviousAssignment')
        if len(moves) != 1 or len(states) != 1 or len(turns) != 1 or len(previous) > 1:
            raise ValueError(f'Assignment has ambiguous ownership, state, turn, or predecessor: {assignment}')
        move, state, turn = next(iter(moves)), next(iter(states)), next(iter(turns))
        if state not in subjects:
            raise ValueError(f'Assigned state is missing: {state}')
        state_owners[state].add(assignment)
        index[(move, turn)].append({'iri': assignment, 'state': state, 'previous': previous})
    if any(len(assignments) > 1 for assignments in state_owners.values()):
        raise ValueError('Different assignments share the same state individual')
    return index, owners


def make_transitions(rows, rdf_data, schema_data, workbook_name, *, conversation_prefix='Mar11GroupB'):
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', conversation_prefix):
        raise ValueError('Conversation prefix must be an alphanumeric IRI prefix')
    schema = read_xml(schema_data)
    classes = {node.get('{' + RDF + '}about') for node in schema.findall('{' + OWL + '}Class')}
    properties = {node.get('{' + RDF + '}about') for node in schema.findall('{' + OWL + '}ObjectProperty')}
    if not {CJF + name for name in ('State', 'StateAssignment', 'TextSpan', *INITIAL_LABELS.values())} <= classes:
        raise ValueError('The schema is missing required state or evidence classes')
    if not {CJF + name for name in ('hasStateAssignment', 'assignedState', 'assignedAtUtterance',
                                   'hasPreviousAssignment', 'hasStateEvidence', 'isPartOfUtterance')} <= properties:
        raise ValueError('The schema is missing required assignment properties')
    subjects = existing_subjects(read_xml(rdf_data))
    utterances = utterance_index(rdf_data, conversation_prefix)
    existing, assignment_owners = assignment_index(subjects)
    histories = defaultdict(list)
    for row in rows:
        move_id = row.get('milestone_id', '').strip()
        if not re.fullmatch(r'[A-Za-z0-9_-]+', move_id) or CJF + move_id not in subjects:
            raise ValueError(f"States row {row['excel_row']}: invalid or missing conversation move")
        label = row.get('state', '').strip()
        if not label:
            raise ValueError(f"States row {row['excel_row']}: state label is empty")
        source_ids = parse_turn_ids(row['effective_turn_id'])
        evidence_ids = parse_turn_ids(row['evidence_turn_ids'])
        if len(source_ids) != 1 or source_ids[0] not in utterances or not evidence_ids or any(
            source not in utterances for source in evidence_ids
        ):
            raise ValueError(f"States row {row['excel_row']}: unknown or ambiguous effective/evidence turn")
        histories[CJF + move_id].append({'row': row, 'label': label,
            'effective': utterances[source_ids[0]], 'evidence_ids': evidence_ids})

    generated, links, records = {}, defaultdict(list), []
    full_spans, reused_full_spans = {}, set()
    created, reused, same_turn = 0, 0, 0
    latest = {}

    def full_span(utterance):
        iri = utterance['iri']
        if iri in full_spans:
            return full_spans[iri]
        preferred = iri + 'FullTextSpan'

        def matching(span):
            return (CJF + 'TextSpan' in class_types(subjects, span)
                    and property_values(subjects, span, 'isPartOfUtterance') == {iri}
                    and property_values(subjects, span, 'hasConversationText') == {utterance['text']})

        if preferred in subjects:
            if not matching(preferred):
                raise ValueError(f'Existing full-utterance span conflicts with its utterance: {preferred}')
            span = preferred
        else:
            candidates = sorted(span for span in subjects if matching(span))
            span = candidates[0] if candidates else preferred
            if not candidates:
                generated[span] = individual(span, CJF + 'TextSpan',
                    Statement(RDFS + 'label', 'Full utterance evidence, turn ' + str(utterance['turn_number'])),
                    Statement(CJF + 'hasConversationText', utterance['text']),
                    Statement(CJF + 'isPartOfUtterance', iri, True))
        if span in subjects:
            reused_full_spans.add(span)
        full_spans[iri] = span
        return span

    for move, history in sorted(histories.items()):
        earliest = min(entry['effective']['turn_number'] for entry in history)
        seeds = [entry for entry in history if entry['effective']['turn_number'] == earliest
                 and entry['label'] in INITIAL_LABELS]
        if len(seeds) != 1:
            raise ValueError(f'{move}: an unambiguous initial state row is required')
        seed = seeds[0]
        transitions = [entry for entry in history if entry is not seed]
        counts = Counter(entry['effective']['turn_number'] for entry in transitions)
        if any(count > 1 for count in counts.values()):
            raise ValueError(f'{move}: multiple transitions at the same turn require an explicit order')
        ordered = [seed, *sorted(transitions, key=lambda entry: entry['effective']['turn_number'])]
        previous, used = None, set()
        for position, entry in enumerate(ordered):
            effective, row = entry['effective'], entry['row']
            candidates = [item for item in existing.get((move, effective['iri']), []) if item['iri'] not in used]
            if position == 0:
                candidates = [item for item in candidates if not item['previous']
                              and CJF + INITIAL_LABELS[entry['label']] in class_types(subjects, item['state'])]
                if len(candidates) != 1:
                    raise ValueError(f'{move}: exactly one existing typed initial assignment is required')
                assignment, state = candidates[0]['iri'], candidates[0]['state']
                was_reused = True
            else:
                if effective['turn_number'] == earliest:
                    same_turn += 1
                if len(candidates) > 1:
                    raise ValueError(f'{move}: multiple existing assignments at turn {effective["turn_number"]}')
                if candidates:
                    item = candidates[0]
                    assignment, state = item['iri'], item['state']
                    if item['previous'] != {previous}:
                        raise ValueError(f'Existing predecessor conflicts with chronological order: {assignment}')
                    if class_types(subjects, state) - {CJF + 'State', OWL + 'NamedIndividual'} or CJF + 'State' not in class_types(subjects, state):
                        raise ValueError(f'Existing transition state is not asserted solely as State: {state}')
                    reused += 1
                    was_reused = True
                else:
                    suffix = 'AtTurn' + str(effective['turn_number'])
                    assignment, state = move + '_StateAssignment' + suffix, move + '_State' + suffix
                    if assignment in subjects or state in subjects:
                        raise ValueError(f'An unlinked resource conflicts with generated transition identifiers: {assignment}')
                    spans = [full_span(utterances[source]) for source in entry['evidence_ids']]
                    generated[state] = individual(state, CJF + 'State',
                        Statement(RDFS + 'label', move.removeprefix(CJF) + ' state at turn ' + str(effective['turn_number'])))
                    statements = [
                        Statement(RDFS + 'label', move.removeprefix(CJF) + ' state assignment at turn ' + str(effective['turn_number'])),
                        Statement(CJF + 'assignedState', state, True),
                        Statement(CJF + 'assignedAtUtterance', effective['iri'], True),
                        Statement(CJF + 'hasPreviousAssignment', previous, True),
                        *(Statement(CJF + 'hasStateEvidence', span, True) for span in spans),
                        Statement(RDFS + 'comment', f"Source: {workbook_name}; States!A{row['excel_row']}:E{row['excel_row']}"),
                        Statement(RDFS + 'comment', 'Annotated reference state: ' + entry['label']),
                        Statement(RDFS + 'comment', 'Source effective turn ID: ' + row['effective_turn_id']),
                        Statement(RDFS + 'comment', 'Source evidence turn ID(s): ' + row['evidence_turn_ids']),
                    ]
                    for prefix, value in [('', row.get('reason', '')), ('Annotation question: ', row.get('questions when annotating', ''))]:
                        if value:
                            statements.append(Statement(RDFS + 'comment', prefix + value))
                    generated[assignment] = individual(assignment, CJF + 'StateAssignment', *statements)
                    links[move].append(Statement(CJF + 'hasStateAssignment', assignment, True))
                    created += 1
                    was_reused = False
            used.add(assignment)
            records.append({'move_iri': move, 'assignment_iri': assignment, 'state_iri': state,
                'effective_utterance_iri': effective['iri'], 'turn_number': effective['turn_number'],
                'previous_assignment_iri': previous, 'initial': position == 0,
                'reused': was_reused, 'reference_state_label': entry['label'], 'source_row': row})
            previous = assignment
        old_assignments = {iri for iri, owners in assignment_owners.items() if move in owners}
        if not old_assignments <= used:
            raise ValueError(f'{move}: existing assignments absent from the worksheet need review')
        latest[move] = previous

    updated, added = append_individuals(rdf_data, list(generated.values()))
    updated, added_links = append_source_links(updated, dict(links))
    after = existing_subjects(read_xml(updated))
    assignment_index(after)
    paired_states = set()
    for record in records:
        assignment, state = record['assignment_iri'], record['state_iri']
        if state in paired_states:
            raise ValueError('Assignment histories share a state individual')
        paired_states.add(state)
        expected_previous = {record['previous_assignment_iri']} if record['previous_assignment_iri'] else set()
        if property_values(after, assignment, 'hasPreviousAssignment') != expected_previous:
            raise ValueError(f'Incorrect predecessor: {assignment}')
        if property_values(after, assignment, 'assignedState') != {state} or property_values(
            after, assignment, 'assignedAtUtterance'
        ) != {record['effective_utterance_iri']}:
            raise ValueError(f'Incorrect paired state or effective utterance: {assignment}')
        evidence = property_values(after, assignment, 'hasStateEvidence')
        expected_turns = {utterances[source]['iri'] for source in parse_turn_ids(record['source_row']['evidence_turn_ids'])}
        actual_turns = {turn for span in evidence for turn in property_values(after, span, 'isPartOfUtterance')}
        if not evidence or actual_turns != expected_turns:
            raise ValueError(f'Evidence does not match the worksheet: {assignment}')
        if not record['reused']:
            if class_types(after, state) != {CJF + 'State'}:
                raise ValueError(f'A specific transition state class was asserted: {state}')
            for span in evidence:
                turns = property_values(after, span, 'isPartOfUtterance')
                if len(turns) != 1 or CJF + 'TextSpan' not in class_types(after, span):
                    raise ValueError(f'Invalid full-utterance evidence span: {span}')
                text = property_values(after, next(iter(turns)), 'hasConversationText')
                if property_values(after, span, 'hasConversationText') != text:
                    raise ValueError(f'Evidence span is not a full utterance: {span}')
    for iri, nodes in subjects.items():
        for node in nodes:
            for child in node:
                if not any(ET.tostring(child).strip() == ET.tostring(other).strip()
                           for definition in after[iri] for other in definition):
                    raise ValueError(f'Original statement changed on {iri}')
    report = {'conversation_prefix': conversation_prefix, 'conversation_moves': len(histories),
        'initial_assignments_reused': len(histories), 'transition_assignments': len(records) - len(histories),
        'new_transition_assignments': created, 'reused_transition_assignments': reused,
        'new_base_state_individuals': created, 'same_turn_initial_transitions': same_turn,
        'new_text_spans': sum(CJF + 'TextSpan' == statement.value for item in generated.values()
                              for statement in item.statements if statement.predicate == RDF + 'type'),
        'full_utterance_spans_reused': len(reused_full_spans), 'added_individuals': added,
        'added_move_assignment_links': added_links, 'total_history_assignments': len(records),
        'latest_assignment_by_move': latest, 'annotated_transition_labels': dict(Counter(
            record['reference_state_label'] for record in records if not record['initial'])),
        'assignments': records}
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
        backup = (args.backup or target.with_name(target.name + '.state-transitions.bak')).resolve()
        report_path = args.report.resolve() if args.report else None
        if target in {args.workbook.resolve(), args.ontology.resolve()} or backup in inputs | {target} or (
            report_path and report_path in inputs | {target, backup}
        ):
            raise ValueError('Workbook, RDF, schema, backup, and report paths must not overlap')
        original, schema, source = args.individuals.read_bytes(), args.ontology.read_bytes(), args.workbook.read_bytes()
        rows, routing = read_worksheet(args.workbook, 'States', REQUIRED_COLUMNS,
                                      column_aliases={args.id_column: 'milestone_id'})
        updated, report = make_transitions(rows, original, schema, args.workbook.name,
                                          conversation_prefix=args.conversation_prefix)
        changed = not target.exists() or target.read_bytes() != updated
        if args.individuals.read_bytes() != original or args.ontology.read_bytes() != schema or args.workbook.read_bytes() != source:
            raise ValueError('An input changed during import; rerun against the latest files')
        if changed and not args.dry_run:
            if target.exists() and not backup.exists():
                backup.parent.mkdir(parents=True, exist_ok=True)
                with backup.open('xb') as handle:
                    handle.write(target.read_bytes())
            atomic_write(target, updated)
        report.update(routing)
        report.update({'id_column': args.id_column, 'workbook': str(args.workbook.resolve()),
            'individuals': str(target), 'workbook_sha256': hashlib.sha256(source).hexdigest(),
            'schema_sha256': hashlib.sha256(schema).hexdigest(),
            'before_sha256': hashlib.sha256(original).hexdigest(), 'after_sha256': hashlib.sha256(updated).hexdigest(),
            'dry_run': args.dry_run, 'would_change_output': changed, 'output_changed': changed and not args.dry_run,
            'backup': str(backup) if backup.exists() else None})
        if report_path:
            atomic_write(report_path, (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        print(f"States sheet: {report['transition_assignments']} transitions; {report['new_transition_assignments']} new, {report['reused_transition_assignments']} reused.")
        print(f"Added {report['added_individuals']} individuals and {report['added_move_assignment_links']} move links; {report['new_text_spans']} new evidence spans.")
        print(('Dry run. Output: ' if args.dry_run else 'Output: ') + str(target))
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
