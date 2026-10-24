"""Check Markdown conversion, source fidelity, and the shared RDF importer."""

from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from markdown_to_xml import main, markdown_to_xml
from test_xml_to_individuals import TEMPLATE
from xml_to_individuals import CJF, PROV, RDF, append_individuals, make_individuals


class MarkdownConversionTests(unittest.TestCase):
    def test_bold_escaped_and_plain_speaker_labels_preserve_text(self):
        source = r'''**1. \*\*Speaker A:\*\* We need $6,000 & <tools>.**

2. **Speaker B:** I’m ready.
3. Speaker C:  Keep the extra space.'''
        root = ET.fromstring(markdown_to_xml(source, 'CQ-sample conversation'))
        self.assertEqual(root.attrib, {'id': 'CQ-sample conversation'})
        self.assertEqual([turn.get('speaker') for turn in root], ['Speaker A', 'Speaker B', 'Speaker C'])
        self.assertEqual([turn.text for turn in root], ['We need $6,000 & <tools>.', 'I’m ready.', ' Keep the extra space.'])
        self.assertTrue(all(turn.get('end_time') == '' for turn in root))
        self.assertTrue(all(turn.get('dialog_act') == '' for turn in root))

    def test_rejects_unparsed_content_and_nonsequential_turns(self):
        for source in ('', '1. Speaker A: yes\nInstructions: do something',
                       '2. Speaker A: skipped first', '1. Speaker A: yes\n1. Speaker B: duplicate',
                       '1. Speaker A: '):
            with self.subTest(source=source), self.assertRaises(ValueError):
                markdown_to_xml(source, 'CQ-sample conversation')

    def test_xml_reuses_importer_with_attribution_and_conversation_links(self):
        source = '1. Speaker A: a\n2. Speaker B: b\n3. Speaker A: a again\n4. Speaker D: d'
        xml = markdown_to_xml(source, 'CQ-sample conversation')
        generated, report = make_individuals(xml, 'CQSample')
        output, added = append_individuals(TEMPLATE, generated)
        root = ET.fromstring(output)
        self.assertEqual((report['utterances'], report['speakers'], report['conversations']), (4, 3, 1))
        self.assertEqual(added, 8)
        self.assertEqual([link.get('{' + RDF + '}resource') for link in root.findall('.//{' + PROV + '}wasAttributedTo')], [
            CJF + 'CQSampleSpeakerA', CJF + 'CQSampleSpeakerB',
            CJF + 'CQSampleSpeakerA', CJF + 'CQSampleSpeakerD',
        ])

    def test_cli_protects_source_and_repeats_identically(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'discussion.md'
            target = Path(directory) / 'discussion.xml'
            source.write_text('1. Speaker A: hello', encoding='utf-8')
            arguments = [str(source), '--output', str(target), '--conversation-id', 'CQ-sample conversation']
            self.assertEqual(main(arguments), 0)
            first = target.read_bytes()
            self.assertEqual(main(arguments), 0)
            self.assertEqual(target.read_bytes(), first)
            self.assertEqual(main([str(source), '--output', str(source), '--conversation-id', 'CQ-sample conversation']), 1)
            self.assertEqual(source.read_text(), '1. Speaker A: hello')


if __name__ == '__main__':
    unittest.main()
