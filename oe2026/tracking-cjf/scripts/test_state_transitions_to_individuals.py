"""Check transition chronology, merged data reuse, full evidence, and CLI writes."""

import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from state_transitions_to_individuals import make_transitions, main, property_values
from xml_to_individuals import CJF, OWL, RDF, Statement, append_individuals, existing_subjects, individual, make_individuals, read_xml
from test_milestones_to_individuals import TEMPLATE


PREFIX = 'FutureGroupA'
MOVE = CJF + 'EXAMPLE-M1'
SEED = MOVE + '_InitialAssignment'
SEED_STATE = MOVE + '_InitialState'
CLASS_NAMES = ['State', 'StateAssignment', 'TextSpan', 'Open', 'Unassessed', 'UnderConsideration']
PROPERTY_NAMES = ['hasStateAssignment', 'assignedState', 'assignedAtUtterance', 'hasPreviousAssignment', 'hasStateEvidence', 'isPartOfUtterance']
SCHEMA = (f'<rdf:RDF xmlns:rdf="{RDF}" xmlns:owl="{OWL}">' +
          ''.join(f'<owl:Class rdf:about="{CJF}{name}"/>' for name in CLASS_NAMES) +
          ''.join(f'<owl:ObjectProperty rdf:about="{CJF}{name}"/>' for name in PROPERTY_NAMES) + '</rdf:RDF>').encode()


def rows(changes):
    return [{'milestone_id': 'EXAMPLE-M1', 'state': state, 'effective_turn_id': str(turn),
             'evidence_turn_ids': evidence, 'reason': 'Recorded conversational evidence', 'excel_row': number}
            for number, (state, turn, evidence) in enumerate(changes, start=2)]


def fixture(*, existing_transition=False, wrong_previous=False, span_suffix='FullTextSpan', wrong_span=False):
    xml = ET.Element('Dialogue', {'id': 'Future conversation'})
    for number, text in enumerate(['First contribution', 'Second contribution', 'Third contribution'], start=1):
        ET.SubElement(xml, 'turn', {'turn_no': str(number), 'speaker': 'Speaker A'}).text = text
    generated, report = make_individuals(ET.tostring(xml), PREFIX)
    for number, mapping in enumerate(report['turn_mappings'], start=1):
        utterance = mapping['utterance_iri']
        text = ['First contribution', 'Second contribution', 'Third contribution'][number - 1]
        generated.append(individual(utterance + span_suffix, CJF + 'TextSpan',
            Statement(CJF + 'isPartOfUtterance', utterance, True),
            Statement(CJF + 'hasConversationText', 'Wrong text' if wrong_span and number == 2 else text)))
    links = [Statement(CJF + 'hasStateAssignment', SEED, True)]
    generated.extend([
        individual(SEED_STATE, CJF + 'Unassessed'),
        individual(SEED, CJF + 'StateAssignment',
            Statement(CJF + 'assignedState', SEED_STATE, True),
            Statement(CJF + 'assignedAtUtterance', CJF + PREFIX + 'Turn1', True),
            Statement(CJF + 'hasStateEvidence', CJF + PREFIX + 'Turn1' + span_suffix, True)),
    ])
    if existing_transition:
        assignment, state = MOVE + '_MergedAssignment', MOVE + '_MergedState'
        links.append(Statement(CJF + 'hasStateAssignment', assignment, True))
        generated.extend([
            individual(state, CJF + 'State'),
            individual(assignment, CJF + 'StateAssignment',
                Statement(CJF + 'assignedState', state, True),
                Statement(CJF + 'assignedAtUtterance', CJF + PREFIX + 'Turn2', True),
                Statement(CJF + 'hasPreviousAssignment', CJF + 'AnotherMoveAssignment' if wrong_previous else SEED, True),
                Statement(CJF + 'hasStateEvidence', CJF + PREFIX + 'Turn2' + span_suffix, True)),
        ])
    generated.append(individual(MOVE, CJF + 'Claim', *links))
    return append_individuals(TEMPLATE, generated)[0]


def workbook(path, records):
    ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    sheet = ET.Element(ns + 'worksheet')
    data = ET.SubElement(sheet, ns + 'sheetData')
    headers = ['conversation_move_id', 'state', 'effective_turn_id', 'evidence_turn_ids', 'reason']
    source_headers = ['milestone_id', *headers[1:]]
    for number, entries in enumerate([headers, *[[row[key] for key in source_headers] for row in records]], start=1):
        target = ET.SubElement(data, ns + 'row', {'r': str(number)})
        for column, entry in enumerate(entries):
            cell = ET.SubElement(target, ns + 'c', {'r': chr(65 + column) + str(number), 't': 'inlineStr'})
            ET.SubElement(ET.SubElement(cell, ns + 'is'), ns + 't').text = entry
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('xl/workbook.xml', '''<workbook
            xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
            <sheets><sheet name="States" r:id="rId1"/><sheet name="Milestones" r:id="rId2"/></sheets></workbook>''')
        archive.writestr('xl/_rels/workbook.xml.rels', '''<Relationships>
            <Relationship Id="rId1" Target="worksheets/sheet1.xml"/>
            <Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>''')
        archive.writestr('xl/worksheets/sheet1.xml', ET.tostring(sheet))
        archive.writestr('xl/worksheets/sheet2.xml', 'Unrelated worksheet must not be parsed')


class TransitionImportTests(unittest.TestCase):
    def test_same_turn_and_later_changes_form_generic_state_chain(self):
        records = rows([('Unassessed', 1, '1'), ('Supported', 1, '1'), ('SupportedContested', 3, '1; 3')])
        original = fixture()
        updated, report = make_transitions(records, original, SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)
        nodes = existing_subjects(read_xml(updated))
        first, second = MOVE + '_StateAssignmentAtTurn1', MOVE + '_StateAssignmentAtTurn3'
        self.assertEqual(property_values(nodes, first, 'hasPreviousAssignment'), {SEED})
        self.assertEqual(property_values(nodes, second, 'hasPreviousAssignment'), {first})
        self.assertEqual(property_values(nodes, second, 'hasStateEvidence'), {CJF + PREFIX + 'Turn1FullTextSpan', CJF + PREFIX + 'Turn3FullTextSpan'})
        for state in [MOVE + '_StateAtTurn1', MOVE + '_StateAtTurn3']:
            self.assertEqual({child.get('{' + RDF + '}resource') for node in nodes[state] for child in node.findall('{' + RDF + '}type')}, {CJF + 'State'})
        self.assertEqual(report['same_turn_initial_transitions'], 1)
        self.assertEqual(report['latest_assignment_by_move'][MOVE], second)
        self.assertEqual((report['added_individuals'], report['new_text_spans']), (4, 0))
        repeated, rerun = make_transitions(records, updated, SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)
        self.assertEqual(repeated, updated)
        self.assertEqual(rerun['added_individuals'], 0)

    def test_existing_transition_is_reused_despite_different_identifier(self):
        original = fixture(existing_transition=True)
        records = rows([('Unassessed', 1, '1'), ('Supported', 2, '2')])
        updated, report = make_transitions(records, original, SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)
        self.assertEqual(updated, original)
        self.assertEqual(report['reused_transition_assignments'], 1)
        self.assertEqual(report['latest_assignment_by_move'][MOVE], MOVE + '_MergedAssignment')

    def test_conflicting_cross_move_predecessor_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'predecessor conflicts'):
            make_transitions(rows([('Unassessed', 1, '1'), ('Supported', 2, '2')]),
                fixture(existing_transition=True, wrong_previous=True), SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)

    def test_multiple_transitions_in_one_turn_need_explicit_order(self):
        with self.assertRaisesRegex(ValueError, 'explicit order'):
            make_transitions(rows([('Unassessed', 1, '1'), ('Supported', 2, '2'), ('SupportedContested', 2, '2')]),
                fixture(), SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)

    def test_unlisted_existing_history_is_not_silently_skipped(self):
        with self.assertRaisesRegex(ValueError, 'absent from the worksheet'):
            make_transitions(rows([('Unassessed', 1, '1')]), fixture(existing_transition=True),
                SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)

    def test_full_evidence_can_reuse_an_existing_span_with_another_identifier(self):
        updated, report = make_transitions(rows([('Unassessed', 1, '1'), ('Supported', 2, '2')]),
            fixture(span_suffix='CompleteEvidence'), SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)
        nodes = existing_subjects(read_xml(updated))
        self.assertEqual(report['new_text_spans'], 0)
        self.assertEqual(property_values(nodes, MOVE + '_StateAssignmentAtTurn2', 'hasStateEvidence'),
                         {CJF + PREFIX + 'Turn2CompleteEvidence'})

    def test_conflicting_full_utterance_span_fails(self):
        with self.assertRaisesRegex(ValueError, 'span conflicts'):
            make_transitions(rows([('Unassessed', 1, '1'), ('Supported', 2, '2')]),
                fixture(wrong_span=True), SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)

    def test_cli_alias_prefix_dry_run_backup_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, rdf, schema, report = [base / name for name in ['source.xlsx', 'sample.rdf', 'schema.rdf', 'report.json']]
            workbook(source, rows([('Unassessed', 1, '1'), ('Supported', 2, '1-2')]))
            original = fixture()
            rdf.write_bytes(original)
            schema.write_bytes(SCHEMA)
            arguments = [str(source), '--individuals', str(rdf), '--ontology', str(schema),
                         '--conversation-prefix', PREFIX, '--id-column', 'conversation_move_id', '--report', str(report)]
            self.assertEqual(main([*arguments, '--dry-run']), 0)
            self.assertEqual(rdf.read_bytes(), original)
            self.assertFalse(rdf.with_name(rdf.name + '.state-transitions.bak').exists())
            self.assertEqual(main(arguments), 0)
            first = rdf.read_bytes()
            self.assertEqual(rdf.with_name(rdf.name + '.state-transitions.bak').read_bytes(), original)
            result = json.loads(report.read_text())
            self.assertEqual(result['worksheet_members_read'], ['xl/worksheets/sheet1.xml'])
            self.assertEqual(result['new_transition_assignments'], 1)
            self.assertEqual(main(arguments), 0)
            self.assertEqual(rdf.read_bytes(), first)
            self.assertFalse(json.loads(report.read_text())['output_changed'])


if __name__ == '__main__':
    unittest.main()
