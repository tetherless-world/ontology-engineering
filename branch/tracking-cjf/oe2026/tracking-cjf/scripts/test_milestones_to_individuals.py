"""Regression checks for configurable columns, conversation IDs, and evidence."""

import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from milestones_to_individuals import (
    RDFS, SHEET_NS, main, make_milestones, read_milestones,
)
from xml_to_individuals import (
    CJF, DC, DT, OWL, PROV, RDF, append_individuals, make_individuals,
)


TEMPLATE = f'''<rdf:RDF xmlns:rdf="{RDF}" xmlns:owl="{OWL}"
    xmlns:cjf="{CJF}" xmlns:prov="{PROV}" xmlns:dc="{DC}"
    xmlns:rdfs="{RDFS}" xmlns:sio="http://semanticscience.org/resource/"
    xmlns:dt="{DT}">
    <owl:Ontology rdf:about="https://example.test/individuals">
        <owl:imports rdf:resource="{CJF}"/>
    </owl:Ontology>
</rdf:RDF>'''.encode()
SCHEMA = f'''<rdf:RDF xmlns:rdf="{RDF}" xmlns:owl="{OWL}">
    <owl:Class rdf:about="{CJF}Claim"/>
</rdf:RDF>'''.encode()
HEADERS = ['milestone_id', 'milestone_type', 'summary', 'source_turn_id',
           'text_span', 'utterance', 'speaker']


def row(speaker='Speaker A'):
    return dict(zip(HEADERS, ['EXAMPLE-M1', 'Claim', 'A claim', '1',
                             'alpha', 'alpha', speaker]), excel_row=2)


def dialogue(prefix, turns):
    root = ET.Element('Dialogue', {'id': 'example conversation'})
    for number, (speaker, text) in enumerate(turns, start=1):
        ET.SubElement(root, 'turn', {'turn_no': str(number), 'speaker': speaker}).text = text
    generated, _ = make_individuals(ET.tostring(root), prefix)
    return generated


def write_workbook(path, headers):
    sheet = ET.Element(SHEET_NS + 'worksheet')
    data = ET.SubElement(sheet, SHEET_NS + 'sheetData')
    for number, values in enumerate([headers, [row()[key] for key in HEADERS]], start=1):
        target = ET.SubElement(data, SHEET_NS + 'row', {'r': str(number)})
        for index, value in enumerate(values):
            cell = ET.SubElement(target, SHEET_NS + 'c', {'r': chr(65 + index) + str(number), 't': 'inlineStr'})
            ET.SubElement(ET.SubElement(cell, SHEET_NS + 'is'), SHEET_NS + 't').text = value
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('xl/workbook.xml', '''<workbook
            xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
            <sheets><sheet name="Milestones" r:id="rId1"/>
            <sheet name="Relationships" r:id="rId2"/></sheets></workbook>''')
        archive.writestr('xl/_rels/workbook.xml.rels', '''<Relationships>
            <Relationship Id="rId1" Target="worksheets/sheet1.xml"/>
            <Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>''')
        archive.writestr('xl/worksheets/sheet1.xml', ET.tostring(sheet))
        # The selected-sheet reader must not parse this unrelated worksheet.
        archive.writestr('xl/worksheets/sheet2.xml', 'invalid unrelated worksheet XML')


class MilestoneImportTests(unittest.TestCase):
    def test_configurable_columns_read_only_milestones(self):
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / 'annotations.xlsx'
            write_workbook(workbook, ['conversation_move_id', 'conversation_move_type', *HEADERS[2:]])
            rows, routing = read_milestones(workbook, id_column='conversation_move_id', type_column='conversation_move_type')
            self.assertEqual(rows[0]['milestone_id'], 'EXAMPLE-M1')
            self.assertEqual(rows[0]['milestone_type'], 'Claim')
            self.assertEqual(routing['worksheet_members_read'], ['xl/worksheets/sheet1.xml'])
            self.assertEqual(routing['column_aliases']['milestone_id'], 'conversation_move_id')

    def test_bad_aliases_fail_instead_of_choosing_another_column(self):
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / 'annotations.xlsx'
            write_workbook(workbook, HEADERS)
            with self.assertRaises(ValueError):
                read_milestones(workbook, id_column='nonexistent')
            write_workbook(workbook, [*HEADERS, 'conversation_move_id'])
            with self.assertRaises(ValueError):
                read_milestones(workbook, id_column='conversation_move_id')

    def test_original_columns_and_prefix_remain_defaults(self):
        rdf, _ = append_individuals(TEMPLATE, dialogue('Mar11GroupB', [('meg', 'alpha')]))
        generated, report = make_milestones([row('meg')], rdf, SCHEMA, 'example.xlsx')
        self.assertEqual(len(generated), 2)
        self.assertEqual(report['milestones'][0]['evidence'][0]['speaker_iri'], CJF + 'Mar11GroupBMeg')
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / 'annotations.xlsx'
            write_workbook(workbook, HEADERS)
            rows, _ = read_milestones(workbook)
            self.assertEqual(rows[0]['milestone_id'], 'EXAMPLE-M1')

    def test_prefix_selects_correct_conversation_when_turn_numbers_overlap(self):
        generated = dialogue('Other', [('Speaker B', 'wrong conversation')])
        generated += dialogue('FutureGroupA', [('Speaker A', 'alpha')])
        rdf, _ = append_individuals(TEMPLATE, generated)
        _, report = make_milestones([row()], rdf, SCHEMA, 'example.xlsx', conversation_prefix='FutureGroupA')
        evidence = report['milestones'][0]['evidence'][0]
        self.assertEqual(evidence['utterance_iri'], CJF + 'FutureGroupATurn1')
        self.assertEqual(evidence['speaker_iri'], CJF + 'FutureGroupASpeakerA')

    def test_cross_speaker_evidence_keeps_each_utterance_attribution(self):
        rdf, _ = append_individuals(TEMPLATE, dialogue('CQSample', [('Speaker A', 'alpha'), ('Speaker D', 'beta')]))
        record = {**row(), 'source_turn_id': '1; 2', 'text_span': '1: alpha | 2: beta', 'utterance': '1: alpha | 2: beta'}
        generated, report = make_milestones([record], rdf, SCHEMA, 'example.xlsx', conversation_prefix='CQSample')
        output, _ = append_individuals(rdf, generated)
        root = ET.fromstring(output)
        self.assertEqual([item['speaker_iri'] for item in report['milestones'][0]['evidence']], [
            CJF + 'CQSampleSpeakerA', CJF + 'CQSampleSpeakerD',
        ])
        self.assertEqual([node.get('{' + RDF + '}resource') for node in root.findall('.//{' + CJF + '}isPartOfUtterance')], [
            CJF + 'CQSampleTurn1', CJF + 'CQSampleTurn2',
        ])
        self.assertEqual(len(root.findall('.//{http://semanticscience.org/resource/}SIO_000206')), 2)
        with self.assertRaises(ValueError):
            make_milestones([{**record, 'speaker': 'Speaker B'}], rdf, SCHEMA, 'example.xlsx', conversation_prefix='CQSample')

    def test_cli_options_backup_and_repeat_import(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workbook, rdf, schema, report = [base / name for name in ('annotations.xlsx', 'sample.rdf', 'schema.rdf', 'report.json')]
            write_workbook(workbook, ['conversation_move_id', 'conversation_move_type', *HEADERS[2:]])
            original, _ = append_individuals(TEMPLATE, dialogue('FutureGroupA', [('Speaker A', 'alpha')]))
            rdf.write_bytes(original)
            schema.write_bytes(SCHEMA)
            arguments = [str(workbook), '--individuals', str(rdf), '--ontology', str(schema),
                         '--id-column', 'conversation_move_id', '--type-column', 'conversation_move_type',
                         '--conversation-prefix', 'FutureGroupA', '--report', str(report)]
            self.assertEqual(main(arguments), 0)
            first = rdf.read_bytes()
            self.assertEqual(rdf.with_name(rdf.name + '.milestones.bak').read_bytes(), original)
            result = json.loads(report.read_text())
            self.assertEqual((result['milestone_count'], result['text_span_count']), (1, 1))
            self.assertEqual(result['conversation_prefix'], 'FutureGroupA')
            self.assertEqual(result['column_aliases']['milestone_id'], 'conversation_move_id')
            self.assertEqual(main(arguments), 0)
            self.assertEqual(rdf.read_bytes(), first)
            self.assertEqual(json.loads(report.read_text())['added_individuals'], 0)


if __name__ == '__main__':
    unittest.main()
