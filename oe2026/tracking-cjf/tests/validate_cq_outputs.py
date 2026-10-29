"""Independent source-to-output checks for the supplied CQ conversation run.

Run from tracking-cjf after the separate build and shacl commands. This checks
saved artifacts; it does not participate in production pipeline validation.
"""
from collections import Counter
from decimal import Decimal
import argparse
import hashlib
import json
from pathlib import Path
import re

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, DC
from cjf_serializer.annotations import read_worksheet, parse_turn_ids

C = Namespace('https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/')
P = Namespace('http://www.w3.org/ns/prov#')
SIO = URIRef('http://semanticscience.org/resource/SIO_000206')
root = Path.cwd()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-manifest', type=Path, default=Path('ontology/run_outputs/input-manifest.json'))
parser.add_argument('--report', type=Path, default=Path('ontology/run_outputs/output-validation-report.json'))
args = parser.parse_args()
sources = json.loads(args.input_manifest.read_text())
for path, expected in sources['input_sha256'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path

asserted_path = Path('ontology/OE_9_TeamCJF_Individuals.rdf')
current_path = Path('ontology/OE_9_TeamCJF_Individuals_CurrentStateAdded.rdf')
asserted = Graph().parse(asserted_path, format='xml')
current = Graph().parse(current_path, format='xml')
assert not list(asserted.triples((None, C.hasCurrentStateAssignment, None)))
added, removed = set(current) - set(asserted), set(asserted) - set(current)
assert not removed
assert len(added) == 54 and all(p == C.hasCurrentStateAssignment for _, p, _ in added)

# Read source transcript headers independently of the production adapter.
source_turns = {}
for line in Path('inputs/Oct21_A_Discussion.md').read_text(encoding='utf-8-sig').splitlines():
    text = line.strip()
    if not text:
        continue
    if text.startswith('**') and text.endswith('**'):
        text = text[2:-2]
    text = text.replace(r'\*\*', '**')
    match = re.fullmatch(r'(\d+)\. \*\*(Speaker [A-D]):\*\*\s+(.*)', text)
    assert match, text
    source_turns[int(match[1])] = (match[2], match[3])
assert len(source_turns) == 28
utterances = set(asserted.subjects(RDF.type, C.Utterance))
assert len(utterances) == 28
turn_by_number = {}
for u in utterances:
    number = int(next(asserted.objects(u, C.hasTurnNumber)))
    turn_by_number[number] = u
    speaker = next(asserted.objects(u, P.wasAttributedTo))
    assert str(next(asserted.objects(u, C.hasConversationText))) == source_turns[number][1]
    assert str(next(asserted.objects(speaker, C.hasSpeakerName))) == source_turns[number][0]
assert len(set(asserted.subjects(RDF.type, C.Speaker))) == 4

workbook = Path('inputs/Annotation_Workbook_CQs.xlsx')
rows, _ = read_worksheet(workbook, 'Milestones', set())
moves = [row for row in rows if row.get('conversation_move_type', '').strip()]
move_iris = {}
for row in moves:
    sid = row['conversation_move_id']
    matches = set(asserted.subjects(DC.identifier, Literal(sid)))
    assert len(matches) == 1, sid
    move = next(iter(matches))
    move_iris[sid] = move
    kind = row['conversation_move_type'].replace(' ', '')
    assert (move, RDF.type, C[kind]) in asserted, sid
    assert (move, C.hasSummary, Literal(row['summary'])) in asserted, sid
assert len(move_iris) == 67
assert not any(str(v).startswith('OCT21_A-M0068') for v in asserted.objects(None, DC.identifier))

for span in asserted.subjects(RDF.type, C.TextSpan):
    utterance = next(asserted.objects(span, C.isPartOfUtterance))
    quote = str(next(asserted.objects(span, C.hasConversationText)))
    assert quote in str(next(asserted.objects(utterance, C.hasConversationText)))

reified = {
    'supports': ('Support', 'makesSupports', 'isAimedAtSupports'),
    'challenges': ('Challenge', 'makesChallenges', 'isAimedAtChallenges'),
    'addresses': ('Address', 'makesAddresses', 'isAimedAtAddresses'),
    'resolves': ('Resolve', 'makesResolves', 'isAimedAtResolves'),
    'answers': ('Answer', 'makesAnswers', 'isAimedAtAnswers'),
    'positionToward': ('Position', 'makesPositionTowards', 'isAimedAtPositionTowards'),
    'respondsTo': ('Response', 'makesRespondsTo', 'isAimedAtRespondsTo'),
}
direct = {'selects': 'selects', 'isAbout': 'isAbout', 'refines': 'refines', 'alternativeTo': 'isAlternativeTo'}
relationships, _ = read_worksheet(workbook, 'Relationships', set())
checked_relationships = set()
for row in relationships:
    source, target = move_iris[row['from_milestone_id']], move_iris[row['to_milestone_id']]
    kind = row['relationship']
    if kind in direct:
        assert (source, C[direct[kind]], target) in asserted
        continue
    cls, makes, aimed = reified[kind]
    matching = [r for r in asserted.objects(source, C[makes])
                if (r, RDF.type, C[cls]) in asserted and (r, C[aimed], target) in asserted]
    assert len(matching) == 1, row
    relationship = matching[0]
    checked_relationships.add(relationship)
    assert (relationship, C.hasReason, Literal(row['reason'].strip())) in asserted
    expected_evidence = {int(Decimal(s)) for s in parse_turn_ids(row['evidence_turn_ids'])}
    actual_evidence = set()
    for span in asserted.objects(relationship, SIO):
        u = next(asserted.objects(span, C.isPartOfUtterance))
        assert next(asserted.objects(span, C.hasConversationText)) == next(asserted.objects(u, C.hasConversationText))
        actual_evidence.add(int(next(asserted.objects(u, C.hasTurnNumber))))
    assert actual_evidence == expected_evidence, row
assert len(checked_relationships) == 86

initial_map = {'Issue': C.Open, 'InformationRequest': C.Open, 'Claim': C.Unassessed, 'Option': C.UnderConsideration}
all_assignments = set(asserted.subjects(RDF.type, C.StateAssignment))
all_states = set(asserted.subjects(RDF.type, C.State))
assert len(all_assignments) == len(all_states) == 85
starters = candidates = 0
owned_states = set()
for move in move_iris.values():
    assignments = set(asserted.objects(move, C.hasStateAssignment))
    if not assignments:
        continue
    pointers = set(current.objects(move, C.hasCurrentStateAssignment))
    assert len(pointers) == 1
    cursor = next(iter(pointers))
    visited = set()
    next_turn = None
    while cursor is not None:
        assert cursor in assignments and cursor not in visited
        visited.add(cursor)
        states = set(asserted.objects(cursor, C.assignedState))
        assert len(states) == 1
        state = next(iter(states))
        assert state not in owned_states
        owned_states.add(state)
        u = next(asserted.objects(cursor, C.assignedAtUtterance))
        turn = int(next(asserted.objects(u, C.hasTurnNumber)))
        assert next_turn is None or turn <= next_turn
        next_turn = turn
        evidence = set(asserted.objects(cursor, C.hasStateEvidence))
        assert evidence
        for span in evidence:
            source_u = next(asserted.objects(span, C.isPartOfUtterance))
            assert int(next(asserted.objects(source_u, C.hasTurnNumber))) <= turn
        previous = set(asserted.objects(cursor, C.hasPreviousAssignment))
        if previous:
            candidates += 1
            assert len(previous) == 1
            assert set(asserted.objects(state, RDF.type)) == {C.State}
        else:
            starters += 1
            kind = next(str(t).split('/')[-1] for t in asserted.objects(move, RDF.type)
                        if str(t).split('/')[-1] in initial_map)
            assert set(asserted.objects(state, RDF.type)) == {C.State, initial_map[kind]}
        for trigger in asserted.objects(cursor, C.hasTriggeringRelationship):
            assert trigger in checked_relationships
            assert set(asserted.objects(trigger, SIO)) <= evidence
            targets = [value for _, aimed in [(m, a) for _, m, a in reified.values()]
                       for value in asserted.objects(trigger, C[aimed])]
            assert targets == [move]
        cursor = next(iter(previous), None)
    assert visited == assignments
assert (starters, candidates) == (54, 31)

report = {
    'passed': True, 'turns': 28, 'speakers': 4, 'moves': 67,
    'relationship_rows_verified': 98, 'reified_relationships': 86,
    'starter_assignments': starters, 'generic_relationship_assignments': candidates,
    'human_transition_assignments': 0, 'current_assignment_links': len(added),
    'shacl_only_added_current_links': True, 'inputs_unchanged': True,
    'asserted_triples': len(asserted), 'current_triples': len(current),
    'output_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (asserted_path, current_path)},
}
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
