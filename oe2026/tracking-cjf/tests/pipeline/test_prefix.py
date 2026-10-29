"""Prefix snapshots exclude future evidence without doing state inference."""
import json
import unittest
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from cjf_serializer import run_pipeline
import test_pipeline as fixtures
from test_pipeline import C, xlsx


class PrefixTests(unittest.TestCase):
    setUp = fixtures.PipelineTests.setUp
    tearDown = fixtures.PipelineTests.tearDown
    configure = fixtures.PipelineTests.configure

    def test_conflicting_human_event_ids_are_rejected(self):
        self.values['States'][0].append('event_id')
        self.values['States'][1].append('human-choice')
        self.values['States'].append(['O1', 'Selected', '3', '3', 'Conflicting judgment', 'human-choice'])
        xlsx(self.workbook, self.values)
        from cjf_serializer import InputValidationError
        with self.assertRaisesRegex(InputValidationError, 'Conflicting human state event'):
            run_pipeline(self.config, output=self.root/'conflict.rdf')
        self.assertFalse((self.root/'conflict.rdf').exists())

    def test_snapshot_keeps_only_available_turns_and_assignment_events(self):
        self.data['state_events'] = {'as_of_turn': 1}
        self.configure()
        result = run_pipeline(self.config, output=self.root/'prefix.rdf')
        graph = Graph().parse(result.output_path)
        self.assertEqual({int(v) for v in graph.objects(None, C.hasTurnNumber)}, {1})
        self.assertEqual(len(set(graph.subjects(RDF.type, C.StateAssignment))), 2)
        self.assertEqual(result.summary['current_assignment_links'], 2)
        self.assertFalse(list(graph.subjects(RDF.type, C.Rejected)))
        self.assertFalse(list(graph.subjects(RDF.type, C.Support)))

    def test_second_snapshot_keeps_generic_relationship_and_excludes_later_human(self):
        self.data['state_events'] = {'as_of_turn': 2}
        self.configure()
        result = run_pipeline(self.config, output=self.root/'prefix.rdf')
        graph = Graph().parse(result.output_path)
        self.assertEqual({int(v) for v in graph.objects(None, C.hasTurnNumber)}, {1, 2})
        self.assertEqual(len(set(graph.subjects(RDF.type, C.StateAssignment))), 4)
        self.assertFalse(list(graph.subjects(RDF.type, C.Rejected)))
        built = json.loads((self.root/'asserted-individuals.rdf.manifest.json').read_text())
        relationship = next(e for e in built['events'] if e['origin'] == 'relationship')
        self.assertEqual(set(graph.objects(URIRef(relationship['state']), RDF.type)), {C.State})

    def test_initial_assignment_has_only_introduction_evidence(self):
        self.values['Milestones'][1][3] = '1; 3'
        xlsx(self.workbook, self.values)
        self.data['state_events'] = {'as_of_turn': 1}
        self.configure()
        result = run_pipeline(self.config, output=self.root/'prefix.rdf')
        graph = Graph().parse(result.output_path)
        for assignment in graph.subjects(RDF.type, C.StateAssignment):
            for span in graph.objects(assignment, C.hasStateEvidence):
                utterance = next(graph.objects(span, C.isPartOfUtterance))
                self.assertEqual(int(next(graph.objects(utterance, C.hasTurnNumber))), 1)


if __name__ == '__main__':
    unittest.main()

