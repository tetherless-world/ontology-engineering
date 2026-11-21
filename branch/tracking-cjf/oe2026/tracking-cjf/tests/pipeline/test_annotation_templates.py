"""Real workbook patterns without Python state classification or invented order."""
import unittest

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from cjf_serializer import build_individuals, InputValidationError
import test_pipeline as fixtures
from test_pipeline import C, xlsx


class AnnotationTemplateTests(unittest.TestCase):
    setUp = fixtures.PipelineTests.setUp
    tearDown = fixtures.PipelineTests.tearDown
    configure = fixtures.PipelineTests.configure

    def test_id_only_placeholder_is_skipped_and_recorded(self):
        self.values['Milestones'].append(['reserved-next-id', '', '', ''])
        xlsx(self.workbook, self.values)
        built = build_individuals(self.config, output=self.root/'asserted.rdf')
        self.assertEqual(built.summary['counts']['moves'], 3)
        self.assertEqual(built.summary['skipped_rows'][0]['id'], 'reserved-next-id')
        self.assertEqual(built.summary['skipped_rows'][0]['reason'], 'unannotated placeholder')

    def test_partially_annotated_move_still_fails(self):
        self.values['Milestones'].append(['partial-id', '', 'An incomplete annotation', ''])
        xlsx(self.workbook, self.values)
        with self.assertRaises(InputValidationError):
            build_individuals(self.config, output=self.root/'asserted.rdf')
        self.assertFalse((self.root/'asserted.rdf').exists())

    def enable_turn_snapshots(self):
        self.data['state_events'] = {'same_turn_relationships': 'group_by_target_turn'}
        self.configure()

    def test_support_and_challenge_share_generic_target_turn_snapshot(self):
        self.enable_turn_snapshots()
        self.values['Relationships'].append(['C2', 'challenges', 'C1', '2', 'A separate challenge in the same turn'])
        xlsx(self.workbook, self.values)
        built = build_individuals(self.config, output=self.root/'asserted.rdf')
        events = [e for e in built.summary['events'] if e['owner'] == 'C1' and e['origin'] == 'relationship']
        self.assertEqual(len(events), 1)
        self.assertEqual(len(events[0]['triggers']), 2)
        graph = Graph().parse(built.output_path)
        self.assertEqual(set(graph.objects(URIRef(events[0]['state']), RDF.type)), {C.State})
        self.assertEqual(len(events[0]['raw']['grouped_relationship_rows']), 2)
        self.assertEqual(len(list(graph.objects(URIRef(events[0]['assignment']), C.hasPreviousAssignment))), 1)

    def test_address_and_resolve_share_generic_target_turn_snapshot(self):
        self.enable_turn_snapshots()
        self.values['Milestones'].extend([
            ['I1', 'Issue', 'Choose a platform', '1'],
            ['Outcome1', 'Outcome', 'A decision', '3'],
        ])
        self.values['Relationships'].extend([
            ['O1', 'addresses', 'I1', '1; 3', 'A response at the decision turn'],
            ['Outcome1', 'resolves', 'I1', '3', 'Explicit resolution relation'],
        ])
        xlsx(self.workbook, self.values)
        built = build_individuals(self.config, output=self.root/'asserted.rdf')
        events = [e for e in built.summary['events'] if e['owner'] == 'I1' and e['origin'] == 'relationship']
        self.assertEqual(len(events), 1)
        self.assertEqual(len(events[0]['triggers']), 2)
        self.assertEqual(events[0]['turn'], 3)
        graph = Graph().parse(built.output_path)
        self.assertEqual(set(graph.objects(URIRef(events[0]['state']), RDF.type)), {C.State})

    def test_explicit_events_are_not_merged_into_turn_snapshots(self):
        self.enable_turn_snapshots()
        self.values['Relationships'][0].append('event_id')
        self.values['Relationships'][1].append('explicit-support')
        self.values['Relationships'].append(['C2', 'challenges', 'C1', '2', 'Separate explicit event', 'explicit-challenge'])
        xlsx(self.workbook, self.values)
        with self.assertRaisesRegex(InputValidationError, 'event_order'):
            build_individuals(self.config, output=self.root/'asserted.rdf')


if __name__ == '__main__':
    unittest.main()
