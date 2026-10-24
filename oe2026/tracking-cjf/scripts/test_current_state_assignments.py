"""Execute real SHACL rules against valid and malformed assignment histories."""

from pathlib import Path
import tempfile
import unittest

try:
    from pyshacl import validate
    from rdflib import Graph, Literal, Namespace, URIRef
    from rdflib.namespace import RDF as RDF_NS
except ImportError:
    raise unittest.SkipTest('Install requirements-shacl.txt to run the SHACL integration tests')

from current_state_assignments import DEFAULT_SHAPES, main, refresh_current_assignments
from relationships_to_individuals import append_source_links
from state_transitions_to_individuals import make_transitions
from test_state_transitions_to_individuals import fixture, rows, MOVE, PREFIX, SEED
from xml_to_individuals import CJF, Statement


C = Namespace(CJF)
SH = Namespace('http://www.w3.org/ns/shacl#')
SHAPES = DEFAULT_SHAPES.read_bytes()
SCHEMA = DEFAULT_SHAPES.parents[1].joinpath('tracking-cjf.rdf').read_bytes()


def data(changes=None):
    changes = changes or [('Unassessed', 1, '1'), ('Supported', 2, '2'), ('SupportedContested', 3, '2; 3')]
    return make_transitions(rows(changes), fixture(), SCHEMA, 'example.xlsx', conversation_prefix=PREFIX)[0]


def graph(source):
    return Graph().parse(data=source, format='xml')


def shacl(source):
    return validate(source, shacl_graph=Graph().parse(data=SHAPES, format='turtle'),
                    advanced=True, inplace=True, inference='none', do_owl_imports=False, iterate_rules=True)


class CurrentAssignmentTests(unittest.TestCase):
    def assert_current(self, source, assignment):
        self.assertEqual(set(graph(source).objects(URIRef(MOVE), C.hasCurrentStateAssignment)), {URIRef(assignment)})

    def test_initial_only_history_uses_its_initial_assignment(self):
        updated, report = refresh_current_assignments(data([('Unassessed', 1, '1')]), SHAPES)
        self.assert_current(updated, SEED)
        self.assertEqual(report['moves_with_state'], 1)

    def test_same_turn_transition_is_selected_over_the_initial_assignment(self):
        updated, report = refresh_current_assignments(data([('Unassessed', 1, '1'), ('Supported', 1, '1')]), SHAPES)
        self.assert_current(updated, MOVE + '_StateAssignmentAtTurn1')
        self.assertEqual(report['same_turn_predecessor_pairs'], 1)

    def test_latest_is_the_end_of_the_complete_chain(self):
        original = data()
        updated, report = refresh_current_assignments(original, SHAPES)
        self.assert_current(updated, MOVE + '_StateAssignmentAtTurn3')
        self.assertEqual(len(graph(updated)) - len(graph(original)), 1)
        self.assertTrue(report['non_current_assertions_preserved'])

    def test_rerun_is_byte_identical(self):
        updated, _ = refresh_current_assignments(data(), SHAPES)
        repeated, report = refresh_current_assignments(updated, SHAPES)
        self.assertEqual(repeated, updated)
        self.assertEqual(report['new_current_links'], 0)
        self.assertEqual(report['stale_current_links_removed'], 0)

    def test_refresh_replaces_a_stale_pointer_instead_of_accumulating_currents(self):
        original, _ = append_source_links(data(), {MOVE: [Statement(CJF + 'hasCurrentStateAssignment', SEED, True)]})
        conforms, _, text = shacl(graph(original))
        self.assertFalse(conforms)
        self.assertIn('exactly one current state assignment', text)
        updated, report = refresh_current_assignments(original, SHAPES)
        self.assert_current(updated, MOVE + '_StateAssignmentAtTurn3')
        self.assertEqual(report['stale_current_links_removed'], 1)
        self.assertEqual(report['new_current_links'], 1)

    def test_branching_history_is_rejected(self):
        g = graph(data())
        last = URIRef(MOVE + '_StateAssignmentAtTurn3')
        g.set((last, C.hasPreviousAssignment, URIRef(SEED)))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('exactly one current state assignment', text)

    def test_disconnected_history_is_rejected(self):
        g = graph(data())
        g.remove((URIRef(MOVE + '_StateAssignmentAtTurn2'), C.hasPreviousAssignment, None))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('exactly one current state assignment', text)

    def test_cycles_are_rejected(self):
        g = graph(data())
        g.add((URIRef(SEED), C.hasPreviousAssignment, URIRef(MOVE + '_StateAssignmentAtTurn3')))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('must not contain cycles', text)

    def test_foreign_successor_cannot_suppress_this_moves_terminal_assignment(self):
        g = graph(data([('Unassessed', 1, '1')]))
        other, assignment = URIRef(CJF + 'OtherMove'), URIRef(CJF + 'OtherAssignment')
        g.add((other, C.hasStateAssignment, assignment))
        g.add((assignment, RDF_NS.type, C.StateAssignment))
        g.add((assignment, C.assignedState, URIRef(CJF + 'OtherState')))
        g.add((assignment, C.assignedAtUtterance, URIRef(CJF + PREFIX + 'Turn2')))
        g.add((assignment, C.hasPreviousAssignment, URIRef(SEED)))
        shapes = Graph().parse(data=SHAPES, format='turtle')
        query = next(shapes.objects(None, SH.construct))
        result = g.query(str(query), initBindings={'this': URIRef(MOVE)})
        self.assertIn((URIRef(MOVE), C.hasCurrentStateAssignment, URIRef(SEED)), set(result))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('previous assignment must belong to the same', text)

    def test_effective_turn_cannot_go_backwards(self):
        g = graph(data())
        g.set((URIRef(MOVE + '_StateAssignmentAtTurn3'), C.assignedAtUtterance, URIRef(CJF + PREFIX + 'Turn1')))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('must not become effective before', text)

    def test_one_assignment_cannot_belong_to_two_moves(self):
        g = graph(data())
        g.add((URIRef(CJF + 'OtherMove'), C.hasStateAssignment, URIRef(SEED)))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('must belong to exactly one conversation move', text)

    def test_turn_number_must_be_an_integer(self):
        g = graph(data())
        g.set((URIRef(CJF + PREFIX + 'Turn3'), C.hasTurnNumber, Literal('three')))
        conforms, _, _ = shacl(g)
        self.assertFalse(conforms)

    def test_orphan_current_pointer_is_rejected(self):
        g = graph(data())
        g.add((URIRef(CJF + 'OtherMove'), C.hasCurrentStateAssignment, URIRef(SEED)))
        conforms, _, text = shacl(g)
        self.assertFalse(conforms)
        self.assertIn('current assignment must belong', text)

    def test_cli_dry_run_backup_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target, backup = root / 'example.rdf', root / 'before.rdf'
            original = data()
            target.write_bytes(original)
            args = ['--individuals', str(target), '--backup', str(backup)]
            self.assertEqual(main([*args, '--dry-run']), 0)
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse(backup.exists())
            self.assertEqual(main(args), 0)
            self.assertEqual(backup.read_bytes(), original)
            updated = target.read_bytes()
            self.assertEqual(main(args), 0)
            self.assertEqual(target.read_bytes(), updated)


if __name__ == '__main__':
    unittest.main()
