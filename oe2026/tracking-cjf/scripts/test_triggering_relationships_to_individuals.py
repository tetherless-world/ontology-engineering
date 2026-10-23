"""Check trigger timing, paired transitions, merged RDF, and safe reruns."""

from pathlib import Path
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from milestones_to_individuals import SIO_SUPPORT
from relationships_to_individuals import RELATIONSHIPS
from state_transitions_to_individuals import make_transitions, property_values
from test_state_transitions_to_individuals import fixture, rows, MOVE, PREFIX
from triggering_relationships_to_individuals import link_triggers, main
from xml_to_individuals import CJF, Statement, append_individuals, existing_subjects, individual, read_xml


SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'tracking-cjf.rdf'
SCHEMA = SCHEMA_PATH.read_bytes()


def history(changes):
    records = rows(changes)
    return records, make_transitions(records, fixture(), SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)[0]


def relationship(data, name, kind, turns, *, actual_target=MOVE):
    source = CJF + name
    cls, makes, aims, _ = RELATIONSHIPS[kind]
    iri = source + '_' + cls + '_EXAMPLE-M1'
    source_type = 'Issue' if kind == 'challenges' else 'Claim'
    generated = [individual(source, CJF + source_type, Statement(CJF + makes, iri, True)),
        individual(iri, CJF + cls, Statement(CJF + aims, actual_target, True),
            *(Statement(SIO_SUPPORT, CJF + PREFIX + 'Turn' + str(turn) + 'FullTextSpan', True) for turn in turns))]
    data = append_individuals(data, generated)[0]
    row = {'from_milestone_id': name, 'relationship': kind, 'to_milestone_id': 'EXAMPLE-M1',
           'evidence_turn_ids': '; '.join(map(str, turns)), 'reason': 'Recorded evidence', 'excel_row': 2}
    return data, row, iri


def import_triggers(records, relations, data):
    return link_triggers(records, relations, data, SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)


def workbook(path, state_rows, relationship_rows):
    namespace = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    sheets = []
    columns = [(['milestone_id', 'state', 'effective_turn_id', 'evidence_turn_ids', 'reason'], state_rows),
               (['from_milestone_id', 'relationship', 'to_milestone_id', 'evidence_turn_ids', 'reason'], relationship_rows)]
    for headers, records in columns:
        sheet = ET.Element(namespace + 'worksheet')
        data = ET.SubElement(sheet, namespace + 'sheetData')
        visible_headers = ['conversation_move_id' if key == 'milestone_id' else key for key in headers]
        for number, entries in enumerate([visible_headers, *[[row[key] for key in headers] for row in records]], 1):
            row = ET.SubElement(data, namespace + 'row', {'r': str(number)})
            for column, value in enumerate(entries):
                cell = ET.SubElement(row, namespace + 'c', {'r': chr(65 + column) + str(number), 't': 'inlineStr'})
                ET.SubElement(ET.SubElement(cell, namespace + 'is'), namespace + 't').text = value
        sheets.append(ET.tostring(sheet))
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('xl/workbook.xml', '''<workbook
          xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>
          <sheet name="States" r:id="rId1"/><sheet name="Relationships" r:id="rId2"/>
          <sheet name="Milestones" r:id="rId3"/></sheets></workbook>''')
        archive.writestr('xl/_rels/workbook.xml.rels', '''<Relationships>
          <Relationship Id="rId1" Target="worksheets/sheet1.xml"/>
          <Relationship Id="rId2" Target="worksheets/sheet2.xml"/>
          <Relationship Id="rId3" Target="worksheets/sheet3.xml"/></Relationships>''')
        for number, sheet in enumerate(sheets, 1):
            archive.writestr(f'xl/worksheets/sheet{number}.xml', sheet)
        archive.writestr('xl/worksheets/sheet3.xml', 'Unrelated worksheet must not be opened')


class TriggerImportTests(unittest.TestCase):
    def test_later_challenge_does_not_trigger_the_earlier_supported_assignment(self):
        records, original = history([('Unassessed', 1, '1'), ('Supported', 1, '1'), ('SupportedContested', 3, '1; 3')])
        original, support_row, support = relationship(original, 'SupportSource', 'supports', [1])
        original, challenge_row, challenge = relationship(original, 'ChallengeSource', 'challenges', [1, 3])
        updated, report = import_triggers(records, [support_row, challenge_row], original)
        subjects = existing_subjects(read_xml(updated))
        self.assertEqual(property_values(subjects, MOVE + '_StateAssignmentAtTurn1', 'hasTriggeringRelationship'), {support})
        self.assertEqual(property_values(subjects, MOVE + '_StateAssignmentAtTurn3', 'hasTriggeringRelationship'), {challenge})
        self.assertEqual(report['trigger_links'], 2)
        self.assertEqual(set(subjects), set(existing_subjects(read_xml(original))))
        repeated, second = import_triggers(records, [support_row, challenge_row], updated)
        self.assertEqual(repeated, updated)
        self.assertEqual(second['new_trigger_links'], 0)

    def test_multiple_joint_supports_are_linked_but_future_support_is_excluded(self):
        records, data = history([('Unassessed', 1, '1'), ('Supported', 1, '1')])
        data, first_row, first = relationship(data, 'FirstSource', 'supports', [1])
        data, second_row, second = relationship(data, 'SecondSource', 'supports', [1])
        data, future_row, _ = relationship(data, 'FutureSource', 'supports', [1, 3])
        updated, _ = import_triggers(records, [first_row, second_row, future_row], data)
        self.assertEqual(property_values(existing_subjects(read_xml(updated)), MOVE + '_StateAssignmentAtTurn1',
                                         'hasTriggeringRelationship'), {first, second})

    def test_an_earlier_context_span_cannot_establish_a_future_challenge(self):
        records, data = history([('Unassessed', 1, '1'), ('Contested', 1, '1')])
        data, row, _ = relationship(data, 'FutureSource', 'challenges', [1, 3])
        with self.assertRaisesRegex(ValueError, 'No complete relationship evidence'):
            import_triggers(records, [row], data)

    def test_supported_contested_after_contested_uses_support_as_the_trigger(self):
        records, data = history([('Unassessed', 1, '1'), ('Contested', 1, '1'), ('SupportedContested', 3, '1; 3')])
        data, challenge_row, challenge = relationship(data, 'ChallengeSource', 'challenges', [1])
        data, support_row, support = relationship(data, 'SupportSource', 'supports', [1, 3])
        updated, _ = import_triggers(records, [challenge_row, support_row], data)
        subjects = existing_subjects(read_xml(updated))
        self.assertEqual(property_values(subjects, MOVE + '_StateAssignmentAtTurn1', 'hasTriggeringRelationship'), {challenge})
        self.assertEqual(property_values(subjects, MOVE + '_StateAssignmentAtTurn3', 'hasTriggeringRelationship'), {support})

    def test_relationship_target_must_be_the_assignment_owner(self):
        records, data = history([('Unassessed', 1, '1'), ('Supported', 1, '1')])
        data, row, _ = relationship(data, 'SupportSource', 'supports', [1], actual_target=CJF + 'OtherMove')
        with self.assertRaisesRegex(ValueError, 'Import the missing relationship'):
            import_triggers(records, [row], data)

    def test_conflicting_existing_trigger_is_rejected(self):
        records, data = history([('Unassessed', 1, '1'), ('Supported', 1, '1')])
        data, row, _ = relationship(data, 'SupportSource', 'supports', [1])
        from relationships_to_individuals import append_source_links
        data, _ = append_source_links(data, {MOVE + '_StateAssignmentAtTurn1': [
            Statement(CJF + 'hasTriggeringRelationship', CJF + 'UnrelatedRelationship', True)]})
        with self.assertRaisesRegex(ValueError, 'Existing trigger conflicts'):
            import_triggers(records, [row], data)

    def test_merged_rdf_description_assignment_is_enriched_without_retyping_it(self):
        records, data = history([('Unassessed', 1, '1'), ('Supported', 1, '1')])
        data, row, support = relationship(data, 'SupportSource', 'supports', [1])
        assignment = MOVE + '_StateAssignmentAtTurn1'
        pattern = r'<owl:NamedIndividual rdf:about="' + re.escape(assignment) + r'">(.*?)</owl:NamedIndividual>'
        text, count = re.subn(pattern, lambda match: '<rdf:Description rdf:about="' + assignment + '">' +
                             match[1] + '</rdf:Description>', data.decode(), flags=re.S)
        self.assertEqual(count, 1)
        updated, _ = import_triggers(records, [row], text.encode())
        self.assertIn(('<rdf:Description rdf:about="' + assignment + '">').encode(), updated)
        self.assertEqual(property_values(existing_subjects(read_xml(updated)), assignment, 'hasTriggeringRelationship'), {support})

    def test_direct_selection_remains_unchanged_without_new_relationships(self):
        records = rows([('Under Consideration', 1, '1'), ('Selected', 3, '1; 3')])
        data = fixture().replace((CJF + 'Claim').encode(), (CJF + 'Option').encode()).replace(
            (CJF + 'Unassessed').encode(), (CJF + 'UnderConsideration').encode())
        data = make_transitions(records, data, SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)[0]
        data = append_individuals(data, [individual(CJF + 'OutcomeSource', CJF + 'Outcome',
            Statement(CJF + 'selects', MOVE, True))])[0]
        row = {'from_milestone_id': 'OutcomeSource', 'relationship': 'selects', 'to_milestone_id': 'EXAMPLE-M1',
               'evidence_turn_ids': '1; 3', 'reason': 'Group selection', 'excel_row': 2}
        updated, report = import_triggers(records, [row], data)
        self.assertEqual(updated, data)
        self.assertEqual(len(report['direct_selection_assignments_unchanged']), 1)
        self.assertEqual(report['new_relationship_individuals'], 0)

    def test_evidence_based_rejection_does_not_get_a_relationship_trigger(self):
        records, data = history([('Unassessed', 1, '1'), ('Rejected', 3, '1; 3')])
        updated, report = import_triggers(records, [], data)
        self.assertEqual(updated, data)
        self.assertEqual(len(report['skipped_non_relationship_transitions']), 1)

    def test_cli_alias_dry_run_backup_and_repeat_preserve_inputs(self):
        records, data = history([('Unassessed', 1, '1'), ('Supported', 1, '1')])
        data, row, _ = relationship(data, 'SupportSource', 'supports', [1])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target, backup = root / 'example.xlsx', root / 'example.rdf', root / 'before.rdf'
            workbook(source, records, [row])
            target.write_bytes(data)
            arguments = [str(source), '--individuals', str(target), '--ontology', str(SCHEMA_PATH),
                         '--conversation-prefix', PREFIX, '--id-column', 'conversation_move_id', '--backup', str(backup)]
            self.assertEqual(main([*arguments, '--dry-run']), 0)
            self.assertEqual(target.read_bytes(), data)
            self.assertFalse(backup.exists())
            self.assertEqual(main(arguments), 0)
            self.assertEqual(backup.read_bytes(), data)
            updated = target.read_bytes()
            self.assertEqual(main(arguments), 0)
            self.assertEqual(target.read_bytes(), updated)
            self.assertEqual(SCHEMA_PATH.read_bytes(), SCHEMA)


if __name__ == '__main__':
    unittest.main()
