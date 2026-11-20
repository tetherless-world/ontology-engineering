"""Checks for terms and license metadata declared in the OE12 schema."""

from pathlib import Path
import unittest

from rdflib import Graph, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF


class OE12SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = URIRef("https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/")
        schema_path = Path(__file__).resolve().parents[2] / "ontology" / "OE_12_TeamCJF.rdf"
        cls.schema = Graph().parse(schema_path, format="xml")

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

    def test_mit_license_is_an_ontology_annotation(self):
        self.assertIn((self.ontology, RDF.type, OWL.Ontology), self.schema)
        self.assertIn((DCTERMS.license, RDF.type, OWL.AnnotationProperty), self.schema)
        self.assertIn(
            (self.ontology, DCTERMS.license, URIRef("https://opensource.org/license/mit")),
            self.schema,
        )
