"""Checks for OE13 term names and license metadata."""

from pathlib import Path
import unittest

from rdflib import Graph, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF


class OE13SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = URIRef("https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/")
        cls.ontology_dir = Path(__file__).resolve().parents[2] / "ontology"
        cls.schema = Graph().parse(cls.ontology_dir / "OE_13_TeamCJF.rdf", format="xml")

    def test_cjf_term_names_follow_class_and_property_conventions(self):
        categories = {
            OWL.Class: r"^[A-Z][A-Za-z0-9]*$",
            OWL.ObjectProperty: r"^[a-z][A-Za-z0-9]*$",
            OWL.DatatypeProperty: r"^[a-z][A-Za-z0-9]*$",
            OWL.AnnotationProperty: r"^[a-z][A-Za-z0-9]*$",
        }
        namespace = str(self.ontology)
        for kind, pattern in categories.items():
            for term in self.schema.subjects(RDF.type, kind):
                if isinstance(term, URIRef) and str(term).startswith(namespace):
                    with self.subTest(term=term, kind=kind):
                        self.assertRegex(str(term).removeprefix(namespace), pattern)

    def test_cjf_class_and_property_names_used_in_examples_follow_conventions(self):
        namespace = str(self.ontology)
        for filename in ("OE_13_TeamCJF_Individuals.rdf", "OE_13_TeamCJF_Individuals_withoutCurrentState.rdf"):
            graph = Graph().parse(self.ontology_dir / filename, format="xml")
            for terms, pattern in (
                (graph.objects(None, RDF.type, unique=True), r"^[A-Z][A-Za-z0-9]*$"),
                (graph.predicates(unique=True), r"^[a-z][A-Za-z0-9]*$"),
            ):
                for term in terms:
                    if isinstance(term, URIRef) and str(term).startswith(namespace):
                        with self.subTest(file=filename, term=term):
                            self.assertRegex(str(term).removeprefix(namespace), pattern)

    def test_mit_license_is_an_ontology_annotation(self):
        self.assertIn((self.ontology, RDF.type, OWL.Ontology), self.schema)
        self.assertIn((DCTERMS.license, RDF.type, OWL.AnnotationProperty), self.schema)
        self.assertIn(
            (self.ontology, DCTERMS.license, URIRef("https://spdx.org/licenses/MIT.html")),
            self.schema,
        )
