"""File pipeline integration tests, including real SHACL execution."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
import yaml
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import RDF, RDFS, OWL, XSD
from cjf_serializer import load_config, build_individuals, run_shacl, run_pipeline, validate_inputs, materialize
from cjf_serializer.models import InputValidationError, OutputWriteError, ShaclValidationError
from cjf_serializer.cli import main

C = Namespace("https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/")
ROOT = Path(__file__).resolve().parents[2]
REAL_SCHEMA = ROOT / "ontology/OE_9_TeamCJF.rdf"


def xlsx(path, sheets):
    ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    relationships = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    book = ET.Element("workbook", xmlns=ns)
    listing = ET.SubElement(book, "sheets")
    rels = ET.Element("Relationships", xmlns="http://schemas.openxmlformats.org/package/2006/relationships")
    with zipfile.ZipFile(path, "w") as archive:
        for i, (name, rows) in enumerate(sheets.items(), 1):
            ET.SubElement(listing, "sheet", {"name": name, "sheetId": str(i), "{"+relationships+"}id": "r"+str(i)})
            ET.SubElement(rels, "Relationship", {"Id": "r"+str(i), "Target": f"worksheets/sheet{i}.xml"})
            sheet = ET.Element("worksheet", xmlns=ns)
            data = ET.SubElement(sheet, "sheetData")
            for row_no, values in enumerate(rows, 1):
                row = ET.SubElement(data, "row", r=str(row_no))
                for col, value in enumerate(values):
                    cell = ET.SubElement(row, "c", r=f"{chr(65+col)}{row_no}", t="inlineStr")
                    ET.SubElement(ET.SubElement(cell, "is"), "t").text = str(value)
            archive.writestr(f"xl/worksheets/sheet{i}.xml", ET.tostring(sheet))
        archive.writestr("xl/workbook.xml", ET.tostring(book))
        archive.writestr("xl/_rels/workbook.xml.rels", ET.tostring(rels))


def sheets(states=True):
    values = {
        "Transcript": [["source_turn_id", "sequence", "speaker", "utterance"],
            ["1", 1, "Speaker A", "Platform A is fast."],
            ["2", 2, "Speaker B", "It saves time."],
            ["3", 3, "Speaker A", "We reject Platform B."]],
        "Milestones": [["milestone_id", "milestone_type ", "summary", "source_turn_id"],
            ["C1", "Claim", "A is fast", "1"], ["C2", "Claim", "A saves time", "2"], ["O1", "Option", "Platform B", "1"]],
        "Relationships": [["from_milestone_id", "relationship", "to_milestone_id", "evidence_turn_ids", "reason"],
            ["C2", "supports", "C1", "2", "Supports the speed claim"]],
    }
    if states:
        values["States"] = [["milestone_id", "state", "effective_turn_id", "evidence_turn_ids", "reason"],
            ["O1", "Rejected", "3", "3", "Human-observed rejection"]]
    return values


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.schema = self.root / "arbitrary-renamed-ontology.rdf"
        self.schema.write_bytes(REAL_SCHEMA.read_bytes())
        self.workbook = self.root / "annotations.xlsx"
        self.values = sheets()
        xlsx(self.workbook, self.values)
        self.config_path = self.root / "settings.yaml"
        self.data = {"config_version": 1, "conversation": {"id": "Demo", "key": "Demo"},
            "inputs": {"annotations": "annotations.xlsx", "transcript_sheet": "Transcript"},
            "ontology": {"file": self.schema.name}, "reasoner": {"enabled": False, "runtime": "missing-worker.yaml"}}
        self.configure()

    def configure(self):
        self.config_path.write_text(yaml.safe_dump(self.data))
        self.config = load_config(self.config_path)

    def tearDown(self):
        self.temp.cleanup()

    def test_three_state_sources_and_file_outputs(self):
        built = build_individuals(self.config, output=self.root/"asserted.rdf")
        self.assertTrue(built.output_path.is_file())
        graph = Graph().parse(built.output_path)
        self.assertFalse(list(graph.triples((None, C.hasCurrentStateAssignment, None))))
        self.assertEqual(built.summary["counts"]["assignments"], 5)
        origins = {e["origin"] for e in built.summary["events"]}
        self.assertEqual(origins, {"initial", "relationship", "explicit-human"})
        relationship = next(e for e in built.summary["events"] if e["origin"] == "relationship")
        self.assertEqual(set(graph.objects(URIRef(relationship["state"]), RDF.type)), {C.State})
        human = next(e for e in built.summary["events"] if e["origin"] == "explicit-human")
        self.assertIn(C.Rejected, graph.objects(URIRef(human["state"]), RDF.type))
        self.assertEqual({v.datatype for v in graph.objects(None, C.hasTurnNumber)}, {XSD.int})
        current = run_shacl(built.output_path, config=self.config, output=self.root/"current.rdf", report=self.root/"validation.json")
        self.assertEqual(current.summary["current_assignment_links"], 3)
        self.assertTrue(current.report_paths["validation_rdf"].is_file())

    def test_combined_equals_individual_steps_and_retains_intermediate(self):
        a = build_individuals(self.config, output=self.root/"separate.rdf")
        b = run_shacl(a.output_path, config=self.config, output=self.root/"separate-current.rdf")
        result = run_pipeline(self.config, output=self.root/"combined.rdf")
        self.assertTrue((self.root/"asserted-individuals.rdf").exists())
        self.assertTrue(isomorphic(Graph().parse(b.output_path), Graph().parse(result.output_path)))
        self.assertEqual(result.summary["inference_status"], "skipped")
        self.assertFalse((self.root/"inference").exists())

    def test_optional_states_absent(self):
        xlsx(self.workbook, sheets(False))
        result = run_pipeline(self.config, output=self.root/"current.rdf")
        self.assertEqual(result.summary["current_assignment_links"], 3)

    def test_shacl_failure_retains_intermediate_and_old_final(self):
        shapes = self.root/"reject.ttl"
        shapes.write_text('@prefix sh: <http://www.w3.org/ns/shacl#> . <urn:shape> a sh:NodeShape; sh:targetNode <urn:bad>; sh:nodeKind sh:Literal .')
        self.data["validation"] = {"shapes": "reject.ttl"}; self.configure()
        final = self.root/"current.rdf"; final.write_text("old verified output")
        with self.assertRaises(ShaclValidationError):
            run_pipeline(self.config, output=final, overwrite=True, report=self.root/"failed.json")
        self.assertTrue((self.root/"asserted-individuals.rdf").exists())
        self.assertEqual(final.read_text(), "old verified output")
        self.assertFalse(json.loads((self.root/"failed.json").read_text())["shacl_conforms"])

    def test_report_cannot_overwrite_workbook_or_final(self):
        before = self.workbook.read_bytes()
        for report in [self.workbook, self.root/"final.rdf"]:
            with self.assertRaises((OutputWriteError, InputValidationError)):
                run_pipeline(self.config, output=self.root/"final.rdf", report=report, overwrite=True)
        self.assertEqual(before, self.workbook.read_bytes())
        self.assertFalse((self.root/"asserted-individuals.rdf").exists())

    def test_config_report_combined_does_not_collide(self):
        self.data["outputs"] = {"report": "summary.json"}; self.configure()
        result = run_pipeline(self.config, output=self.root/"current.rdf")
        self.assertTrue(result.output_path.is_file())
        self.assertEqual(json.loads((self.root/"summary.json").read_text())["inference_status"], "skipped")

    def test_same_turn_starter_and_relationship_do_not_need_order(self):
        self.values["Relationships"][1][3] = "1"
        self.values["Milestones"][2][3] = "1"
        xlsx(self.workbook, self.values)
        result = run_pipeline(self.config, output=self.root/"current.rdf")
        self.assertEqual(result.summary["current_assignment_links"], 3)

    def test_separate_same_turn_events_require_order(self):
        self.values["States"].append(["C1", "Contested", "2", "2", "Human observation"])
        xlsx(self.workbook, self.values)
        with self.assertRaisesRegex(InputValidationError, "event_order"):
            build_individuals(self.config, output=self.root/"asserted.rdf")

    def test_duplicate_move_deduplicates_and_conflict_rejects(self):
        self.values["Milestones"].append(self.values["Milestones"][1].copy())
        xlsx(self.workbook, self.values)
        self.assertEqual(validate_inputs(self.config).summary["moves"], 3)
        self.values["Milestones"][-1][2] = "changed"
        xlsx(self.workbook, self.values)
        with self.assertRaisesRegex(InputValidationError, "Conflicting move"):
            validate_inputs(self.config)

    def test_fractional_source_ids_and_integer_alias(self):
        self.values["Transcript"][1][0] = "1.0"
        self.values["Transcript"][2][0] = "117.1"
        self.values["Milestones"][2][3] = "117.1"
        self.values["Relationships"][1][3] = "117.1"
        xlsx(self.workbook, self.values)
        result = build_individuals(self.config, output=self.root/"asserted.rdf")
        self.assertIn("117.1", result.summary["source_id_to_iri"])
        self.assertIn("1.0", result.summary["source_id_to_iri"])

    def test_stale_pointer_refresh_and_cycle_rejection(self):
        built = build_individuals(self.config, output=self.root/"asserted.rdf")
        graph = Graph().parse(built.output_path)
        events = [e for e in built.summary["events"] if e["owner"] == "C1"]
        initial, later = events
        move = next(graph.subjects(C.hasStateAssignment, URIRef(initial["assignment"])))
        graph.add((move, C.hasCurrentStateAssignment, URIRef(initial["assignment"])))
        graph.serialize(built.output_path, format="xml")
        result = run_shacl(built.output_path, config=self.config, output=self.root/"current.rdf")
        self.assertEqual(result.summary["stale_current_links_removed"], 1)
        graph.add((URIRef(initial["assignment"]), C.hasPreviousAssignment, URIRef(later["assignment"])))
        graph.serialize(built.output_path, format="xml")
        with self.assertRaises(ShaclValidationError):
            run_shacl(built.output_path, config=self.config, output=self.root/"cycle.rdf")
        self.assertFalse((self.root/"cycle.rdf").exists())

    def test_input_immutable_and_overwrite_explicit(self):
        workbook, schema = self.workbook.read_bytes(), self.schema.read_bytes()
        build_individuals(self.config, output=self.root/"asserted.rdf")
        with self.assertRaises(OutputWriteError):
            build_individuals(self.config, output=self.root/"asserted.rdf")
        self.assertEqual(workbook, self.workbook.read_bytes()); self.assertEqual(schema, self.schema.read_bytes())

    def test_dry_run_writes_only_requested_report(self):
        result = run_pipeline(self.config, output=self.root/"current.rdf", report=self.root/"preview.json", dry_run=True)
        self.assertIsNone(result.output_path)
        self.assertTrue((self.root/"preview.json").exists())
        self.assertFalse((self.root/"current.rdf").exists())
        self.assertFalse((self.root/"asserted-individuals.rdf").exists())

    def test_missing_transcript_not_invented(self):
        self.data["inputs"].pop("transcript_sheet"); self.configure()
        with self.assertRaisesRegex(InputValidationError, "exactly one"):
            validate_inputs(self.config)

    def test_cli_real_module_from_other_directory(self):
        completed = subprocess.run([sys.executable, "-m", "cjf_serializer", "run", "--config", str(self.config_path), "--output", str(self.root/"cli.rdf")], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue((self.root/"cli.rdf").exists())

    def test_configuration_error_exit_two(self):
        self.data["unknown"] = {}; self.config_path.write_text(yaml.safe_dump(self.data))
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["validate-input", "--config", str(self.config_path)]), 2)

    def test_prefix_configuration_accepts_positive_turn(self):
        self.data["state_events"] = {"as_of_turn": 2}
        self.configure()
        self.assertEqual(self.config.data["state_events"]["as_of_turn"], 2)

    def test_optional_worker_missing_is_not_hidden_core_dependency(self):
        result = run_pipeline(self.config, output=self.root/"current.rdf")
        with self.assertRaises(InputValidationError):
            materialize(result.output_path, config=self.config, output_directory=self.root/"inference")
        self.assertTrue(result.output_path.exists())

    def test_declared_relationship_event_merges_evidence(self):
        header = self.values["Relationships"][0]
        header.extend(["event_id", "effective_turn_id"])
        self.values["Relationships"][1].extend(["joint-1", "3"])
        self.values["Relationships"].append(["C2", "supports", "C1", "3", "Additional observed evidence", "joint-1", "3"])
        xlsx(self.workbook, self.values)
        result = build_individuals(self.config, output=self.root/"asserted.rdf")
        event = next(e for e in result.summary["events"] if e["origin"] == "relationship")
        self.assertEqual(set(event["evidence"]), {"2", "3"})
        self.assertEqual(len([e for e in result.summary["events"] if e["origin"] == "relationship"]), 1)

    def test_changed_namespace_requires_explicit_shapes(self):
        profile = self.root/"profile.yaml"
        profile.write_text('namespace: "https://example.org/alternate/"\n')
        self.data["ontology"]["profile"] = "profile.yaml"; self.configure()
        # A simple supplied graph suffices to check that custom vocabulary is not
        # incorrectly remapped while embedded SPARQL still uses the CJF prefix.
        graph = Graph(); graph.serialize(self.root/"empty.rdf", format="xml")
        with self.assertRaisesRegex(InputValidationError, "explicit compatible SHACL"):
            run_shacl(self.root/"empty.rdf", config=self.config, output=self.root/"current.rdf")

    def test_numbered_and_corpus_adapters_preserve_missing_times(self):
        for adapter, text in [
            ("numbered_speakers", "1. **Speaker A:** Platform A is fast.\n2. Speaker B: It saves time.\n3. Speaker A: We reject Platform B.\n"),
            ("corpus_chat", "Speaker A (19:48:41 PM): Platform A is fast.\nSpeaker B (19:48:42 PM): It saves time.\nSpeaker A (19:48:43 PM): We reject Platform B.\n")]:
            transcript = self.root/(adapter+".txt"); transcript.write_text(text)
            self.data["inputs"].pop("transcript_sheet", None)
            self.data["inputs"].update({"transcript": transcript.name, "adapter": adapter}); self.configure()
            result = build_individuals(self.config, output=self.root/(adapter+".rdf"))
            graph = Graph().parse(result.output_path)
            dt = Namespace("https://www.omg.org/spec/Commons/DatesAndTimes/")
            self.assertEqual(len(list(graph.triples((None, dt.hasDateTime, None)))), 0 if adapter == "numbered_speakers" else 3)

    def test_base_graph_with_histories_is_rejected(self):
        built = build_individuals(self.config, output=self.root/"populated.rdf")
        self.data["inputs"].pop("transcript_sheet")
        self.data["inputs"]["base_individuals"] = "populated.rdf"; self.configure()
        with self.assertRaisesRegex(InputValidationError, "transcript-only"):
            validate_inputs(self.config)

    def test_external_worker_protocol_fixture(self):
        # This tests transport/publication, not actual HermiT inference.
        worker = self.root/"protocol_fixture.py"
        worker.write_text('''import json, pathlib, sys
request = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert request['protocol_version'] == 1
pathlib.Path(request['inferred_output']).write_text('<urn:fixture> <urn:observed> "worker-contract" .')
pathlib.Path(request['result_output']).write_text(json.dumps({'engine':'HermiT','consistent':True,'materialized':True,'fixture':True}))
''')
        runtime = self.root/"worker.yaml"
        runtime.write_text(yaml.safe_dump({"command": [sys.executable, str(worker), "{request}"]}))
        self.data["reasoner"]["runtime"] = runtime.name; self.configure()
        result = run_pipeline(self.config, output=self.root/"current.rdf", report=self.root/"summary.json")
        inferred = materialize(result.output_path, config=self.config, output_directory=self.root/"inference")
        self.assertTrue(inferred.output_path.is_file())
        self.assertEqual(inferred.summary["new_triples"], 1)
        self.assertTrue(result.output_path.is_file())


if __name__ == "__main__":
    unittest.main()
