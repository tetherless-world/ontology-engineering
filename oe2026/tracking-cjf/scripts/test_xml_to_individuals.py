"""Regression checks for source quirks, data preservation, and repeat runs."""

from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from xml_to_individuals import (
    CJF, DC, DT, OWL, PROV, RDF, XSD,
    append_individuals, main, make_individuals, parse_time,
)


TEMPLATE = f'''<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="{RDF}" xmlns:owl="{OWL}"
    xmlns:tracking-cjf="{CJF}" xmlns:DatesAndTimes="{DT}"
    xmlns:prov="{PROV}" xmlns:dc="{DC}">
    <!-- Preserve this template comment and ontology IRI. -->
    <owl:Ontology rdf:about="https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/individuals">
        <owl:imports rdf:resource="{CJF}"/>
    </owl:Ontology>
</rdf:RDF>
'''.encode()

EXAMPLE = f'''
    <owl:NamedIndividual rdf:about="{CJF}DTMar11194841">
        <rdf:type rdf:resource="{DT}DateTime"/>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="{CJF}Mar11GroupBTurn1">
        <rdf:type rdf:resource="{CJF}Utterance"/>
        <prov:wasAttributedTo rdf:resource="{CJF}Mar11GroupBModerator"/>
        <DatesAndTimes:hasDateTime rdf:resource="{CJF}DTMar11194841"/>
        <tracking-cjf:hasConversationText>link</tracking-cjf:hasConversationText>
        <tracking-cjf:hasTurnNumber rdf:datatype="{XSD}integer">1</tracking-cjf:hasTurnNumber>
    </owl:NamedIndividual>
    <owl:NamedIndividual rdf:about="{CJF}Mar11GroupBModerator">
        <rdf:type rdf:resource="{CJF}Speaker"/>
    </owl:NamedIndividual>
'''.encode()


def dialogue(turns: str) -> bytes:
    return ('<Dialogue date="2010-03-11">' + turns + '</Dialogue>').encode()


def turn(number: str, timestamp: str = "20:05:36 PM", text: str = "hi", speaker: str = "meg") -> str:
    return f'<turn turn_no="{number}" speaker="{speaker}" end_time="{timestamp}">{text}</turn>'


class ConversionTests(unittest.TestCase):
    def test_preserves_manual_example_byte_for_byte(self):
        template = TEMPLATE.replace(b'</rdf:RDF>', EXAMPLE + b'</rdf:RDF>')
        generated, _ = make_individuals(dialogue(turn("1", "19:48:41 PM", "link", "moderator")), "Mar11GroupB")
        actual, added = append_individuals(template, generated)
        self.assertEqual(actual, template)
        self.assertEqual(added, 0)

    def test_turn_uris_are_distinct_when_timestamps_match(self):
        generated, report = make_individuals(dialogue(turn("35") + turn("36")), "Mar11GroupB")
        utterances = [item for item in generated if any(s.value == CJF + 'Utterance' for s in item.statements)]
        self.assertEqual([item.iri for item in utterances], [CJF + 'Mar11GroupBTurn1', CJF + 'Mar11GroupBTurn2'])
        self.assertEqual(report['date_times'], 1)
        self.assertEqual(report['utterances'], 2)
        for item in utterances:
            self.assertEqual(next(s.value for s in item.statements if s.predicate == DT + 'hasDateTime'), CJF + 'DTMar11200536')

    def test_split_source_numbers_are_preserved_without_invalid_integer_literals(self):
        generated, _ = make_individuals(dialogue(turn("117.0") + turn("117.1") + turn("118", "20:05:37 PM")), "Mar11GroupB")
        output, _ = append_individuals(TEMPLATE, generated)
        root = ET.fromstring(output)
        values = root.findall('.//{' + CJF + '}hasTurnNumber')
        self.assertEqual([value.text for value in values], ['1', '2', '3'])
        self.assertTrue(all(value.get('{' + RDF + '}datatype') == XSD + 'integer' for value in values))
        self.assertEqual([value.text for value in root.findall('.//{' + DC + '}identifier')], ['117.0', '117.1', '118'])
        utterances = [node for node in root.findall('{' + OWL + '}NamedIndividual') if node.find('{' + CJF + '}hasTurnNumber') is not None]
        self.assertEqual([node.get('{' + RDF + '}about') for node in utterances], [CJF + 'Mar11GroupBTurn1', CJF + 'Mar11GroupBTurn2', CJF + 'Mar11GroupBTurn3'])

    def test_second_run_is_byte_identical_and_preserves_header(self):
        generated, _ = make_individuals(dialogue(turn("1") + turn("2")), "Mar11GroupB")
        first, added = append_individuals(TEMPLATE, generated)
        second, repeated = append_individuals(first, generated)
        self.assertEqual(added, 4)
        self.assertEqual(repeated, 0)
        self.assertEqual(first, second)
        self.assertTrue(first.startswith(TEMPLATE.split(b'</rdf:RDF>')[0]))

    def test_text_escaping_unicode_and_whitespace_round_trip(self):
        xml = dialogue(turn('1', text='  café &amp; &lt;budget&gt; "yes"\nnext&#13;line  '))
        generated, _ = make_individuals(xml, 'Mar11GroupB')
        output, _ = append_individuals(TEMPLATE, generated)
        value = ET.fromstring(output).find('.//{' + CJF + '}hasConversationText')
        self.assertEqual(value.text, '  café & <budget> "yes"\nnext\rline  ')

    def test_conflicting_existing_text_fails_without_writing(self):
        template = TEMPLATE.replace(b'</rdf:RDF>', EXAMPLE + b'</rdf:RDF>')
        with tempfile.TemporaryDirectory() as directory:
            rdf_path = Path(directory) / 'individuals.rdf'
            xml_path = Path(directory) / 'Mar11_GroupB_annotated.xml'
            rdf_path.write_bytes(template)
            xml_path.write_bytes(dialogue(turn('1', '19:48:41 PM', 'changed', 'moderator')))
            self.assertEqual(main([str(xml_path), '--individuals', str(rdf_path)]), 1)
            self.assertEqual(rdf_path.read_bytes(), template)

    def test_cli_makes_original_backup_and_rerun_does_not_change_files(self):
        with tempfile.TemporaryDirectory() as directory:
            rdf_path = Path(directory) / 'individuals.rdf'
            xml_path = Path(directory) / 'Mar11_GroupB_annotated.xml'
            rdf_path.write_bytes(TEMPLATE)
            xml_path.write_bytes(dialogue(turn('1') + turn('2')))
            arguments = [str(xml_path), '--individuals', str(rdf_path)]
            self.assertEqual(main(arguments), 0)
            first = rdf_path.read_bytes()
            backup = rdf_path.with_name(rdf_path.name + '.bak')
            self.assertEqual(backup.read_bytes(), TEMPLATE)
            self.assertEqual(main(arguments), 0)
            self.assertEqual(rdf_path.read_bytes(), first)
            self.assertEqual(backup.read_bytes(), TEMPLATE)

    def test_bad_source_data_fails_before_generation(self):
        for source in (dialogue(turn('1') + turn('1')), dialogue(turn('1', '99:00:00 PM'))):
            with self.assertRaises(ValueError):
                make_individuals(source, 'Mar11GroupB')
        with self.assertRaises(ValueError):
            make_individuals(b'<!DOCTYPE Dialogue><Dialogue date="2010-03-11"/>', 'Mar11GroupB')

    def test_redundant_pm_and_traditional_am_pm(self):
        self.assertEqual(parse_time('19:48:41 PM').isoformat(), '19:48:41')
        self.assertEqual(parse_time('7:48:41 PM').isoformat(), '19:48:41')
        self.assertEqual(parse_time('12:00:00 AM').isoformat(), '00:00:00')
        with self.assertRaises(ValueError):
            parse_time('19:48:41 AM')

    def test_untimed_dialogue_creates_conversation_and_named_speakers(self):
        source = b'''<Dialogue id="CQ-sample conversation">
            <turn turn_no="1" speaker="Speaker A" end_time="">First</turn>
            <turn turn_no="2" speaker="Speaker B">Second</turn>
            <turn turn_no="3" speaker="Speaker C">Third</turn>
        </Dialogue>'''
        generated, report = make_individuals(source, 'CQSample')
        output, added = append_individuals(TEMPLATE, generated)
        root = ET.fromstring(output)
        self.assertEqual(added, 7)
        self.assertIsNone(report['dialogue_date'])
        self.assertEqual(report['date_times'], 0)
        self.assertEqual(report['turns_without_timestamps'], 3)
        self.assertFalse(root.findall('.//{' + DT + '}hasDateTime'))
        self.assertEqual(root.find('.//{' + CJF + '}hasConversationIdentifier').text, 'CQ-sample conversation')
        self.assertEqual([v.text for v in root.findall('.//{' + CJF + '}hasSpeakerName')], ['Speaker A', 'Speaker B', 'Speaker C'])
        links = root.findall('.//{' + PROV + '}wasGeneratedBy')
        self.assertEqual(len(links), 3)
        self.assertTrue(all(link.get('{' + RDF + '}resource') == CJF + 'CQSampleConversation' for link in links))
        self.assertEqual(len(root.findall('.//{' + PROV + '}wasAssociatedWith')), 3)
        repeated, added_again = append_individuals(output, generated)
        self.assertEqual(added_again, 0)
        self.assertEqual(repeated, output)

    def test_explicit_conversation_identifier_overrides_xml_identifier(self):
        source = b'<Dialogue id="original"><turn turn_no="1" speaker="a">Text</turn></Dialogue>'
        generated, report = make_individuals(source, 'CQSample', conversation_id='CQ-sample conversation')
        self.assertEqual(report['conversation_id'], 'CQ-sample conversation')
        output, _ = append_individuals(TEMPLATE, generated)
        conflicting, _ = make_individuals(source, 'CQSample', conversation_id='different conversation')
        with self.assertRaises(ValueError):
            append_individuals(output, conflicting)

    def test_cli_reads_conversation_id_without_fabricating_timestamps(self):
        with tempfile.TemporaryDirectory() as directory:
            rdf_path = Path(directory) / 'individuals.rdf'
            xml_path = Path(directory) / 'CQSample.xml'
            rdf_path.write_bytes(TEMPLATE)
            xml_path.write_text('<Dialogue><turn turn_no="1" speaker="Speaker A">Text</turn></Dialogue>')
            self.assertEqual(main([
                str(xml_path), '--individuals', str(rdf_path),
                '--conversation-id', 'CQ-sample conversation',
            ]), 0)
            root = ET.fromstring(rdf_path.read_bytes())
            self.assertEqual(root.find('.//{' + CJF + '}hasConversationIdentifier').text, 'CQ-sample conversation')
            self.assertFalse(root.findall('.//{' + DT + '}hasDateTime'))


if __name__ == '__main__':
    unittest.main()
