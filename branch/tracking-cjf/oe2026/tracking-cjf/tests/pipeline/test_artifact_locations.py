"""A separate artifact directory must work for both public build workflows."""
import unittest
import test_pipeline as fixtures
from cjf_serializer import build_individuals, run_pipeline, OutputWriteError


class ArtifactLocationTests(unittest.TestCase):
    setUp = fixtures.PipelineTests.setUp
    tearDown = fixtures.PipelineTests.tearDown
    configure = fixtures.PipelineTests.configure

    def test_standalone_build_uses_config_relative_artifact_directory(self):
        self.data['outputs'] = {'artifacts_directory': 'reports'}
        self.configure()
        output = self.root/'ontology/asserted.rdf'
        result = build_individuals(self.config, output=output)
        self.assertEqual(result.report_paths['manifest'], self.root/'reports/asserted.rdf.manifest.json')
        self.assertTrue(result.report_paths['manifest'].is_file())
        self.assertFalse(output.with_name(output.name+'.manifest.json').exists())

    def test_combined_command_uses_the_same_manifest_destination(self):
        self.data['outputs'] = {'artifacts_directory': 'reports'}
        self.configure()
        result = run_pipeline(self.config, output=self.root/'ontology/current.rdf')
        self.assertTrue(result.output_path.is_file())
        self.assertTrue((self.root/'reports/asserted-individuals.rdf.manifest.json').is_file())
        self.assertFalse((self.root/'ontology/asserted-individuals.rdf.manifest.json').exists())

    def test_existing_manifest_fails_before_any_rdf_is_published(self):
        self.data['outputs'] = {'artifacts_directory': 'reports'}
        self.configure()
        (self.root/'reports').mkdir()
        manifest = self.root/'reports/asserted-individuals.rdf.manifest.json'
        manifest.write_text('existing artifact')
        with self.assertRaises(OutputWriteError):
            run_pipeline(self.config, output=self.root/'ontology/current.rdf')
        self.assertFalse((self.root/'ontology/asserted-individuals.rdf').exists())
        self.assertEqual(manifest.read_text(), 'existing artifact')


if __name__ == '__main__':
    unittest.main()
