"""Reified About and Selection output, evidence, triggers, and legacy schemas."""
from pathlib import Path
import unittest

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

import test_pipeline as fixtures
from test_pipeline import C, xlsx
from cjf_serializer import build_individuals, InputValidationError


class ReifiedRelationshipTests(unittest.TestCase):
    setUp = fixtures.PipelineTests.setUp
    tearDown = fixtures.PipelineTests.tearDown
    configure = fixtures.PipelineTests.configure

    def prepare(self, current_schema):
        if current_schema:
            schema = Path(__file__).resolve().parents[2] / "ontology/OE_13_TeamCJF.rdf"
            self.schema.write_bytes(schema.read_bytes())
        self.values = fixtures.sheets(False)
        self.values["Milestones"].extend([
            ["I1", "Information Request", "Why is Platform A fast?", "2"],
            ["D1", "Outcome", "Choose Platform B", "3"],
        ])
        self.values["Relationships"].extend([
            ["I1", "isAbout", "C1", "2", "Asks about the speed claim"],
            ["D1", "selects", "O1", "3", "The group chooses Platform B"],
        ])
        xlsx(self.workbook, self.values)

    def test_current_schema_reifies_evidence_and_selection_trigger(self):
        self.prepare(current_schema=True)
        graph = Graph().parse(build_individuals(self.config, output=self.root / "asserted.rdf").output_path)
        for source_id, kind, target_id, cls, makes, aim, reason in [
            ("I1", "isAbout", "C1", C.About, C.makesIsAbout, C.isAimedAtIsAbout, "Asks about the speed claim"),
            ("D1", "selects", "O1", C.Select, C.makesSelects, C.isAimedAtSelects, "The group chooses Platform B"),
        ]:
            with self.subTest(kind=kind):
                source = URIRef(C + "Demo/Move_" + source_id)
                target = URIRef(C + "Demo/Move_" + target_id)
                relationship, = graph.objects(source, makes)
                self.assertIn((relationship, RDF.type, cls), graph)
                self.assertIn((relationship, aim, target), graph)
                self.assertIn((relationship, C.hasReason, Literal(reason)), graph)
                evidence = list(graph.objects(relationship, URIRef("http://semanticscience.org/resource/SIO_000206")))
                self.assertEqual(len(evidence), 1)
                self.assertTrue(list(graph.objects(relationship, C.hasUtterance)))
                self.assertNotIn((source, C[kind], target), graph)
        selection, = graph.objects(URIRef(C + "Demo/Move_D1"), C.makesSelects)
        assignment, = graph.subjects(C.hasTriggeringRelationship, selection)
        self.assertIn((URIRef(C + "Demo/Move_O1"), C.hasStateAssignment, assignment), graph)

    def test_archived_schema_keeps_direct_relationship_output(self):
        self.prepare(current_schema=False)
        graph = Graph().parse(build_individuals(self.config, output=self.root / "asserted.rdf").output_path)
        self.assertIn((URIRef(C + "Demo/Move_I1"), C.isAbout, URIRef(C + "Demo/Move_C1")), graph)
        self.assertIn((URIRef(C + "Demo/Move_D1"), C.selects, URIRef(C + "Demo/Move_O1")), graph)
        self.assertFalse(list(graph.subjects(RDF.type, C.Select)))
        self.assertFalse(list(graph.subjects(RDF.type, C.About)))

    def test_current_schema_rejects_invalid_relationship_endpoints(self):
        for relationship_row, endpoint_index, invalid_id in [
            (-1, 0, "C1"),
            (-2, 2, "D1"),
        ]:
            with self.subTest(relationship_row=relationship_row):
                self.prepare(current_schema=True)
                self.values["Relationships"][relationship_row][endpoint_index] = invalid_id
                self.values["Relationships"][relationship_row][3] = "3"
                xlsx(self.workbook, self.values)
                with self.assertRaisesRegex(InputValidationError, "Relationship endpoint"):
                    build_individuals(self.config, output=self.root / "invalid.rdf")

