# Import annotated dialogue XML into the individuals ontology

`xml_to_individuals.py` uses Python 3.10+ and the standard library only. It appends
to `../mar11_groupb-individuals.rdf`, following the existing individual structure
and using turn numbers in utterance IRIs. It retains the ontology IRI, imports,
prefixes, existing individuals, comments, and unrelated RDF statements. The main
`tracking-cjf.rdf` is never modified.

Save any pending edits in Protégé before running the converter. Afterward, reload
or reopen `mar11_groupb-individuals.rdf` to see the generated individuals; saving
an older in-memory copy from Protégé could overwrite the generated data.

From this directory:

```sh
python3 xml_to_individuals.py /Users/devindesilva/Downloads/Mar11_GroupB_annotated.xml
```

From another directory, invoke the script by its full path. The default RDF path
is resolved relative to the script, so it does not depend on the working directory.
Use `--individuals PATH` for a different existing individuals file or
`--output PATH` to generate a preview/copy. Use `--report PATH` for a JSON report
containing every source attribute and the source-turn-to-individual mapping.
Existing targets receive a `.bak` backup on the first changed run. `--backup PATH`
selects another backup location; an existing backup is never overwritten.

## Mapping used

| Source | RDF representation |
| --- | --- |
| Each `<turn>` | One `owl:NamedIndividual` of type `tracking-cjf:Utterance` |
| Utterance IRI | Conversation prefix + `Turn` + integer `hasTurnNumber`, e.g. `tracking-cjf:Mar11GroupBTurn1` |
| `speaker="moderator"` | `prov:wasAttributedTo` → `tracking-cjf:Mar11GroupBModerator`, typed `tracking-cjf:Speaker` |
| `end_time="19:48:41 PM"` | `DatesAndTimes:hasDateTime` → `tracking-cjf:DTMar11194841`, typed `DatesAndTimes:DateTime` |
| Turn text | `tracking-cjf:hasConversationText`, preserving parsed text and whitespace |
| XML document order | `tracking-cjf:hasTurnNumber`, an integer starting at 1, with the same `xsd:integer` datatype as the example |
| Original `turn_no` when it differs from the integer sequence | `dc:identifier`, preserving the exact original value |

All new individual IRIs use the same `tracking-cjf` namespace as the examples.
Speakers are reused within the conversation. DateTime individuals have only their
type assertion, exactly as in the manual example; no new date-value property or
timezone is introduced. The source date and full original timestamp are retained
in the optional JSON report.

The XML uses redundant 24-hour timestamps such as `19:48:41 PM`; these are read as
19:48:41 and used for the DateTime individuals. Utterance IRIs use the integer turn
sequence instead: `Mar11GroupBTurn1` through `Mar11GroupBTurn480` for this source.
Turns sharing a timestamp still have distinct utterance IRIs and share the same
DateTime individual. The URI suffix always matches `hasTurnNumber`.

The provided file contains 480 XML turn elements but original turn numbers up to
479, because source turn 117 is split into `117.0` and `117.1`. Generated
`hasTurnNumber` values are unique integers 1–480. The two split turns have sequence
numbers 117 and 118, and source turn 118 has sequence number 119. From this point,
`dc:identifier` retains each original source number. No subturn is dropped or
rounded into another turn.

The attributes `comm_act_type`, `dialog_act`, `link_to`, `mode`, `polarity`, `pos`,
`pos_count`, `pos_origin`, and `topic` have no mapping in the user's manual example.
They are preserved in the optional JSON report and source XML, rather than used
to infer milestone classes or relationships automatically.

Repeated runs with the same source do not duplicate individuals or change the
RDF bytes. If existing individuals disagree with the expected text, attribution,
timestamp link, or sequence, the script stops before editing the RDF. It preserves
extra annotations on otherwise matching individuals. It does not refresh or delete
data from earlier imports: use the backup or a fresh template if the source changes.

The defaults reproduce this dataset's naming convention, including the yearless
`DTMar11` prefix. For additional datasets/years, use `--conversation-prefix` and
`--datetime-prefix` to choose distinct prefixes and avoid naming collisions.

## Import the CQ sample Markdown discussion

`markdown_to_xml.py` converts numbered speaker turns, including the bold and
escaped bold formatting in `Oct21_A Discussion.md`, into the same `Dialogue` /
`turn` XML structure used by the existing importer. It rejects unrecognized
nonempty lines, duplicate numbers, and gaps so that turns cannot be silently
dropped. Dialogue text, punctuation, and speaker names are retained after removing
the Markdown wrappers and turn/speaker labels.

From this directory, import the sample with:

```sh
python3 markdown_to_xml.py '/Users/devindesilva/Downloads/Oct21_A Discussion.md' \
  --output ../files/conversations/CQ-sample-conversation.xml \
  --conversation-id 'CQ-sample conversation'
python3 xml_to_individuals.py ../files/conversations/CQ-sample-conversation.xml \
  --conversation-prefix CQSample \
  --backup /tmp/cq-sample-import/mar11_groupb-individuals.before-import.rdf \
  --report /tmp/cq-sample-import/report.json
```

The generated XML records the exact conversation ID in `Dialogue/@id`. No date
or timestamps are supplied in the Markdown, so `date` is omitted and `end_time`
is empty. Unknown dialogue annotations and modality fields are also left empty.
The importer accepts absent timing values and creates no DateTime individuals
for them. A supplied malformed date or nonempty malformed time is still rejected.

When a `Dialogue` has an `id` (or `--conversation-id` is supplied), the XML importer
also creates a `MultipartyConversation` with that exact `hasConversationIdentifier`,
links each utterance to it using `prov:wasGeneratedBy`, records `hasSpeakerName`
on speakers, and associates the conversation with its speakers using
`prov:wasAssociatedWith`. The sample creates 28 utterances, 4 speakers, and
`tracking-cjf:CQSampleConversation`; its identifier is `CQ-sample conversation`.
Utterances use `CQSampleTurn1` through `CQSampleTurn28`, and speakers use
`CQSampleSpeakerA` through `CQSampleSpeakerD`. Existing XML without conversation
metadata retains its original mapping. No CJF milestones, relationships, or states
are inferred from the sample text by these commands.

The converted XML can be reimported directly without the original Markdown.
Unchanged reruns leave the RDF bytes unchanged, and existing unrelated individuals
and the schema are preserved. The report includes every source turn's mapping;
unknown dates/times are represented by JSON `null` values.

## CQ sample conversation

The sample is stored separately in `../cq-sample-conversation.rdf`, which imports
the schema and contains 28 utterances, 4 speakers, and one `MultipartyConversation`
with the exact identifier `CQ-sample conversation`. The source XML is saved at
`../files/conversations/CQ-sample-conversation.xml`. Missing source dates and
timestamps remain unspecified.

Reimport the XML into the sample file explicitly:

```sh
python3 xml_to_individuals.py ../files/conversations/CQ-sample-conversation.xml \
  --individuals ../cq-sample-conversation.rdf --conversation-prefix CQSample
```

An unchanged rerun adds no duplicates. `mar11_groupb-individuals.rdf` retains its
contents from before the sample import.

## Verification

```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The checks cover the existing example, same-second turns, split source numbers,
text escaping, repeat runs, backups, conflicting existing data, and invalid input.
The converter checks every mapped statement after serialization. These checks
verify the conversion; they are not an OWL reasoner consistency check.

## Import the Milestones worksheet

`milestones_to_individuals.py` reads only the worksheet named `Milestones` from an
annotation workbook. It reads workbook routing metadata and only the shared-string
values referenced by that sheet; it never opens other worksheet contents.

```sh
python3 milestones_to_individuals.py '/Users/devindesilva/Downloads/Annotation workbook CJF (1).xlsx'
```

The workbook column names and existing conversation IRI prefix are configurable:

```sh
python3 milestones_to_individuals.py '/Users/devindesilva/Downloads/Annotation Workbook Synthetic Example.xlsx' \
  --individuals ../cq-sample-conversation.rdf \
  --id-column conversation_move_id --type-column conversation_move_type \
  --conversation-prefix CQSample
```

`--id-column` defaults to `milestone_id`, `--type-column` to `milestone_type`,
and `--conversation-prefix` to `Mar11GroupB` for the original dataset. Supply
different values for future workbooks/conversations. The prefix selects existing
utterances such as `CQSampleTurn1` and speakers such as `CQSampleSpeakerA`;
milestone IDs are taken verbatim from the chosen ID column. The workbook itself
is preserved. Configured aliases and the selected prefix appear in the report.
Missing configured columns and duplicate headers after alias mapping are rejected.

Each row with a `milestone_id` creates one individual with that exact identifier
in the tracking-cjf namespace, for example `tracking-cjf:MAR11_B-M0001`. Summaries,
original type names, attributes, annotation questions, and source row references
are preserved as annotations. Rows without milestone IDs are reported and skipped.
Missing milestone IDs are not invented or renumbered.

The workbook's Claim, Option, Issue, Information Request, Expressed Position, and
Outcome types map to their existing ontology classes. Conversation Management
maps to `CollectiveJudgmentFormationConversationMove`, because there is no
dedicated class for it. Expressed positions are asserted only as `ExpressedPosition`.
Explicit agreement and disagreement attributes select positive or negative
supporting evidence links; the ontology's class definitions infer `Agreement` or
`Disagreement`. Preference, uncertainty, and requested-response types remain
source annotations.

Each quoted source turn creates a TextSpan linked to its existing utterance with
`isPartOfUtterance`. Milestones link to those spans through SIO `is supported by`,
or its positive/negative subproperties for explicit agreement/disagreement.
The existing property chain can then infer `hasSpeaker`. Multi-turn ranges and
semicolon-separated source IDs are resolved to separate evidence spans.
The row's `speaker` is checked against the first source turn. Later evidence may
come from different speakers; each span retains its own utterance link, and the
report records the actual speaker for each source turn. The sample RDF declares
the `rdfs` and SIO `resource` namespaces used for annotations and evidence links.

The inferred position definitions are `Agreement EquivalentTo ExpressedPosition
and (isPositiveSupportedBy some TextSpan)` and `Disagreement EquivalentTo
ExpressedPosition and (isNegativeSupportedBy some TextSpan)`. Polarity comes from
the workbook annotation; the OWL reasoner does not interpret the quotation's
natural-language text. The report's `expected_inferred_position_subtypes` counts
these annotated polarities, rather than claiming to have run a reasoner.

Original source turn IDs are looked up through `dc:identifier`, falling back to
`hasTurnNumber` where those numbers coincide. They are not assumed to equal the
current URI suffix: source turn 361 resolves to `Mar11GroupBTurn362` in this data.
Workbook quotations are preserved even when they differ from the existing
transcript; differences are recorded in the optional JSON report.

The same `--individuals`, `--ontology`, `--output`, `--backup`, and `--report` path
options are available. Repeat runs do not duplicate existing individuals. The
importer does not modify the workbook or schema, import states from other tabs,
or infer inter-milestone relationships from annotation questions.

## Import reified relationships

`relationships_to_individuals.py` reads only the `Relationships` worksheet. Run it
after importing the milestones:

```sh
python3 relationships_to_individuals.py '/Users/devindesilva/Downloads/Annotation workbook CJF (1).xlsx'
```

Only the following relationship names are imported. Each row creates an explicit
`CollectiveJudgmentFormationConversationMoveRelationship` individual with the
specific class below, a source milestone's makes assertion, and an aims-at
assertion from the relationship individual to its target milestone.

| Workbook relationship | Explicit class | Source property | Target property | Inferred direct property |
| --- | --- | --- | --- | --- |
| positionToward | Position | makesPositionTowards | isAimedAtPositionTowards | hasPositionTowards |
| answers | Answer | makesAnswers | isAimedAtAnswers | answers |
| challenges | Challenge | makesChallenges | isAimedAtChallenges | challenges |
| addresses | Address | makesAddresses | isAimedAtAddresses | addresses |
| supports | Support | makesSupports | isAimedAtSupports | supports |
| selects / resolves | Resolve | makesResolves | isAimedAtResolves | resolves |
| response / respondsTo | Response | makesRespondsTo | isAimedAtRespondsTo | respondsTo |

Relationship IRIs use both endpoints and their specific class, for example
`MAR11_B-M0005_Position_MAR11_B-M0003`, so sorting the workbook does not rename
individuals. Workbook reasons are copied verbatim into `rdfs:comment`; the schema
has no separate reason property. Row provenance and annotation questions are
also preserved as comments. Annotation questions never supply extra assertions.

Every `evidence_turn_ids` entry links to the existing utterance through an
explicit `hasUtterance` assertion. Evidence IDs use the original source turn
numbers, resolved with the same lookup as the milestones importer. One reusable
`TextSpan` per utterance, such as `Mar11GroupBTurn366FullTextSpan`, contains that
utterance's entire `hasConversationText` value and links back with
`isPartOfUtterance`. Each relationship's SIO `is supported by` links to those
full-text spans. Ranges and semicolon-separated evidence lists include every
listed turn, including contextual turns from the target milestone.

The existing property chains infer the direct milestone-to-milestone properties;
the importer does not assert those direct edges. `selects` retains the workbook's
Option target. The corrected `resolves` schema maps Outcome to Option, and its
reified class/properties inherit from the general relationship/makes/aims-at
terms rather than from addresses, which targets Issues.

The same `--individuals`, `--ontology`, `--output`, `--backup`, and `--report`
options are available. Missing references, incompatible domains/ranges, duplicate
rows, or conflicting existing individuals stop the import before writing RDF.
Repeating an unchanged import leaves the RDF bytes unchanged. The workbook,
schema, unrequested relationship types, and existing individual data are preserved.

## Import Open state assignments

`open_states_to_individuals.py` reads only the `States` worksheet and imports rows
whose `state` is exactly `Open`:

```sh
python3 open_states_to_individuals.py '/Users/devindesilva/Downloads/Annotation workbook CJF (1).xlsx'
```

Each Open row creates its own state individual typed as the existing `Open`
class and a separate `StateAssignment`. For example,
`MAR11_B-M0002_OpenAtTurn364` links through `assignedState` to
`MAR11_B-M0002_OpenStateAtTurn364`. Its milestone links to the assignment with
`hasStateAssignment`; the assignment also records
`assignedAtUtterance` pointing to the existing utterance for `effective_turn_id`,
and `hasStateEvidence` links for every listed evidence turn. Turn IDs are resolved
through original source identifiers, so source 363 links to current turn 364.

Evidence spans contain the entire existing utterance text and link back through
`isPartOfUtterance`. Matching full-text spans from the relationship import are
reused. Reasons are copied verbatim to assignment `rdfs:comment` annotations,
alongside source row/turn provenance. Worksheet text is treated as data.

The importer compares effective turns within the States tab to distinguish
historical Open assignments from the latest state. It adds the milestone's
current `hasState` assertion pointing to that assignment's own state individual
only when its latest recorded state is Open. Later Answered or Addressed entries do not turn into Open current states;
their non-Open assignments are outside this import. Initial assignments have no
`hasPreviousAssignment` link.

For this workbook, the import creates 15 separate Open state individuals and 15
Open assignments: 10 historical and 5 current. The current Open milestones are
M0016, M0038, M0047, M0049, and M0079. Effective turns, evidence, and reasons remain
on each assignment, so every state has its own assignment context for later
classification rules.
It reuses 16 full-utterance spans and creates 2 more for source turns 375 and 409.

The same `--individuals`, `--ontology`, `--output`, `--backup`, and `--report`
options are available. Repeat runs preserve the RDF bytes. The schema, workbook,
existing individuals, and other worksheet contents are preserved. The converter
checks mapping and reference integrity; OWL consistency is a separate reasoner
check.

## Import Under Consideration and Unassessed initial states

`initial_states_to_individuals.py` reads only `States` and imports rows whose
state is exactly `Under Consideration` or `Unassessed`:

```sh
python3 initial_states_to_individuals.py '/Users/devindesilva/Downloads/Annotation workbook CJF (1).xlsx'
```

Each row creates a distinct state individual typed `UnderConsideration` for an
Option, or `Unassessed` for a Claim, and its own `StateAssignment`. For example,
`MAR11_B-M0003_UnderConsiderationAtTurn364` has `assignedState` pointing to
`MAR11_B-M0003_UnderConsiderationStateAtTurn364`. The milestone connects through
`hasStateAssignment`. Assignments have `assignedAtUtterance`, full-utterance
`hasStateEvidence` spans, verbatim reasons, and source row/turn annotations, using
the same source-turn lookup and evidence reuse as Open.

These are initial assignments: the converter requires their effective turn to be
the earliest state entry for the milestone and creates no `hasPreviousAssignment`
assertion. Each row has its own state individual. Only the latest recorded state
receives a milestone `hasState` assertion; initial states with later transitions
remain historical. The converter creates no later-state assignments.

For this workbook, there are 11 Under Consideration assignments (10 current,
1 historical) and 29 Unassessed assignments (25 current, 4 historical). M0072
later becomes Selected; M0012, M0028, M0065, and M0066 have later claim states.
M0020 has no Unassessed row, so none is invented for it. Existing Open data is
preserved; its original script uses this shared implementation in Open-only mode.

The same `--individuals`, `--ontology`, `--output`, `--backup`, and `--report`
options are available. The default backup suffix is `.initial-states.bak`.
An unchanged rerun leaves the RDF bytes unchanged. The workbook, main ontology,
and other worksheet contents are preserved.

## Import subsequent assignments as base State individuals

`state_transitions_to_individuals.py` reads only the `States` worksheet and
requires the initial assignments to exist already. It groups the rows by
conversation move and sorts them by the effective utterance's `hasTurnNumber`.
If an initial assignment and a transition share a turn, the initial comes first.
Multiple transitions at the same turn are rejected until their order is explicit.

From this directory, preview the sample import with:

```sh
python3 state_transitions_to_individuals.py '/Users/devindesilva/Downloads/Annotation Workbook Synthetic Example.xlsx' \
  --individuals ../cq-sample-conversation.rdf --conversation-prefix CQSample \
  --dry-run --report /tmp/cq-sample-transitions-preview.json
```

Remove `--dry-run` to write the RDF. `--id-column` selects the workbook's move-ID
column and defaults to `milestone_id`. `--conversation-prefix` defaults to
`Mar11GroupB`. The existing `--ontology`, `--output`, `--backup`, and `--report`
path options are also supported; the default backup suffix is
`.state-transitions.bak`.

Each new transition creates a `StateAssignment` and a distinct individual asserted
only as `State`. Their neutral IRIs use, for example,
`OCT21_A-M0023_StateAssignmentAtTurn10` and `OCT21_A-M0023_StateAtTurn10`.
The source state label is retained in an `rdfs:comment` as an annotated reference
value. No specific state subclass is asserted and no inference rules are added.

The move links to each assignment with `hasStateAssignment`. Assignments record
`assignedState`, `assignedAtUtterance`, and `hasStateEvidence`. Every new
assignment's evidence spans contain the complete source utterances. Existing
full-utterance spans are reused by IRI or matching text/utterance; a missing span
is created once. Existing assignments retain their original evidence.

The importer advances a previous-assignment pointer after each initial or
transition record. `hasPreviousAssignment` therefore identifies the immediate
preceding assignment for the same move, including consecutive changes and
initial/transition pairs at the same turn. Initial assignments keep no predecessor.
Existing transitions are matched by their move and effective utterance, preserving
merged identifiers. Conflicting predecessors, shared state individuals, duplicate
assignments, and existing history absent from the worksheet stop the import.

For the sample, the worksheet has 54 initial assignments and 26 transitions.
One transition already exists, so the first run adds 25 assignment/state pairs and
reuses all evidence spans. The report includes the latest assignment for each
move. `hasState` and `hasCurrentStateAssignment` assertions are left unchanged.
Unchanged reruns preserve the RDF bytes.

### Link state assignments to triggering relationships

`triggering_relationships_to_individuals.py` enriches existing state histories
using only the States and Relationships worksheets. Import the conversation,
milestones, relationships, and state assignments first. For example:

```sh
python3 triggering_relationships_to_individuals.py \
  "/path/to/Annotation Workbook Synthetic Example.xlsx" \
  --individuals ../cq-sample-conversation.rdf --conversation-prefix CQSample \
  --dry-run --report /tmp/cq-sample-triggers-preview.json
```

Remove `--dry-run` to write the RDF. `--id-column` selects the States sheet's
move-ID column; `--ontology`, `--output`, `--backup`, and `--report` have the same
roles as in the transition importer. A rerun is byte identical.

`hasTriggeringRelationship` has domain `StateAssignment` and range
`CollectiveJudgmentFormationConversationMoveRelationship`. The StateAssignment
class restricts its values to that range without requiring a trigger on every
assignment: initial states and evidence-based transitions may have none.

The importer links Addressed, Answered, Resolved, Supported, Contested, and
SupportedContested transitions to existing relationship individuals. It checks
the predecessor's annotated reference state, move and source types, relationship
target, and the complete evidence set. Every trigger's evidence must be included
in the assignment's evidence, with its latest evidence turn equal to the
assignment's effective turn. Matching an earlier contextual span alone cannot
make a later challenge trigger an earlier assignment. Joint triggers are all
linked. SupportedContested uses a Challenge after Supported, or a Support after
Contested, preserving the two separate transition branches.

Selected assignments remain unchanged because `selects` remains a direct
property. This importer creates no relationship individuals, classes, evidence
spans, or state subtype assertions. It reports these direct selections separately
and leaves the existing state-class expressions unchanged; those expressions
must use the trigger property before it affects state classification.

In CQ Sample, 24 assignments receive 32 links to existing relationship objects.
The two Selected assignments and 54 initial assignments receive no new trigger
links. Existing merged IDs, partial evidence, and complementary RDF descriptions
are retained. The shared assertion-appending helper supports both
`owl:NamedIndividual` and `rdf:Description` blocks.

### Derive the current assignment with SHACL

`current_state_assignments.py` executes
`../shacl/current-state-assignment-rules.ttl` with pySHACL Advanced Features,
validates the histories, and writes `hasCurrentStateAssignment` links to the
individuals RDF. It defaults to `../cq-sample-conversation.rdf`.

From this scripts directory, using your Python environment:

```sh
python -m pip install -r requirements-shacl.txt
python current_state_assignments.py --dry-run --report /tmp/current-states-preview.json
python current_state_assignments.py --report /tmp/current-states.json
```

The rule chooses the assignment with no recorded successor **for the same
move**. It follows `hasPreviousAssignment`, so an initial assignment and a
successor at the same turn are ordered correctly. Validation requires exactly
one current assignment per move and checks ownership, predecessor cardinality,
cycles, and nondecreasing effective turn numbers. Branching or disconnected
histories are rejected instead of choosing an arbitrary assignment.

SHACL CONSTRUCT rules add facts; they do not remove stale current pointers.
The runner clears this derived predicate in its working graph before running
the rule, then refreshes those pointers in the RDF/XML. All other assertions,
including historical assignments, state types, evidence, and ontology metadata,
are preserved. The SHACL output is checked against an independent traversal of
each complete assignment chain. Unchanged reruns preserve the file bytes.
Running the shapes directly against stale pointers reports a validation error;
use the runner to refresh them.

`--individuals`, `--shapes`, `--output`, `--backup`, and `--report` configure the
paths. A changed output gets a backup whose default filename includes the input
hash. A dry run makes no RDF or backup changes. Local files are parsed without
following OWL imports or running OWL inference. No current state subclass is
asserted by this operation: follow the current assignment's `assignedState` to
obtain its state individual.

For CQ Sample, all 80 assignments form 54 histories. The rule creates 54 current
assignment links and handles the nine initial/transition pairs sharing a turn.

```sparql
PREFIX cjf: <https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/>
SELECT ?move ?assignment ?state ?turn WHERE {
  ?move cjf:hasCurrentStateAssignment ?assignment .
  ?assignment cjf:assignedState ?state ;
              cjf:assignedAtUtterance/cjf:hasTurnNumber ?turn .
}
ORDER BY ?move
```

### Clear current pointers for later recomputation

`remove_current_state_assignments.py` removes only
`hasCurrentStateAssignment` assertions from an RDF/XML file. It keeps the moves,
historical assignments, states, evidence, and all other assertions. It does not
execute SHACL or assign replacement pointers. When a file changes, the CLI first
saves a backup whose filename includes its original content hash.

From this scripts directory, when removal is wanted:

```sh
python remove_current_state_assignments.py ../cq-sample-conversation.rdf
```

To clear selected moves, add `--move-iri` with the full move IRI; repeat that
option for multiple moves. Without that option, all current pointers are cleared.
No third-party dependencies are needed.

For processing streamed turns in memory, call
`clear_current_assignments(rdf_bytes, move_iris=None)` to obtain the updated XML
bytes and the number of removed links. Recompute current pointers against the
history available at that streamed turn. Passing the complete conversation to
the SHACL runner selects the final recorded assignments.
