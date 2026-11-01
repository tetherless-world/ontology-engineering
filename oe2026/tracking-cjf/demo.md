---
layout: default
title: Demonstration and Queries
---

## Sample Conversation

The demonstration uses the [CQ sample conversation individuals](ontology/OE_9_TeamCJF_Individuals_CurrentStateAdded.rdf) with the [current CJF schema](ontology/OE_9_TeamCJF.rdf). The [source conversation transcript](inputs/Oct21_A_Discussion.md) preserves the 28 turns and speaker labels used by the [current generation configuration](configs/cq-sample.yaml). The [earlier conversation XML](files/conversations/CQ-sample-conversation.xml) is retained for reference.

## Running the Queries

These queries use OWL DL reasoning. Open the current-state-added individuals file linked above in Protégé, with the schema and its imports available. Run HermiT, then execute the queries in SNAP SPARQL.

- [Download the combined CQ1, CQ3, and CQ5 queries (.txt)](CQAnswers/OE_9_TeamCJF_SPARQLQueries.txt)

## CQ1 Conversation Moves and Current States

**Question:** Which CJF conversation moves have occurred in the conversation, and what is the latest known state of each conversation move, where a state applies?

- [SPARQL query (.rq)](CQAnswers/CQ1/CQ1.conversation-moves.current-states.snap.rq)
- [Recorded sample answers (.csv)](CQAnswers/CQ1/CQ1.claims-that-supports-platform-a.answers.csv)

The query returns each move, its move type, state result, and summary. Its optional state pattern retains conversation moves without an applicable or known specific state. When querying `hasState`, the ontology's property chain derives the state through `hasCurrentStateAssignment` followed by `assignedState`; the corresponding inferred triples must be available to the query engine. Multiple state classifications can produce more than one row for a move.

The [SHACL rules](shacl/current-state-assignment-rules.ttl) identify terminal assignments in each move's recorded history. The [Python pipeline](src/cjf_serializer/pipeline.py) refreshes the current assignment links and validates the histories. “Current” refers to the latest assignment in the loaded conversation data. The [pipeline documentation](PIPELINE.html) describes the import and validation workflow.

## CQ3 Claims Supporting or Challenging Platform A

**Question:** What Claims support or challenge Platform A? Are any of the Claims Supported?

- [Claims and their states: query (.rq)](CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq)
- [Claims and their states: recorded answers (.csv)](CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv)
- [Supported Claims: query (.rq)](CQAnswers/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.snap.rq)
- [Supported Claims: recorded answers (.csv)](CQAnswers/CQ3/CQ3.supported-claims-that-support-challenges-platform-a.answers.csv)

The first query finds Claims that support or challenge Platform A and shows their current states and summaries. Property chains infer the `supports`, `challenges`, and `hasState` links used by the query. The second query keeps Claims whose current state is `Supported`. A Claim can challenge Platform A and still have a Supported state. The recorded answers contain six supporting and three challenging Claims; five supporting Claims and one challenging Claim have a Supported current state.

## CQ5 Speakers Agreeing with the Selected Option

**Question:** For the final platform-selection Outcome, which speakers explicitly agreed with its selected Option, and which ExpressedPosition moves and source turns provide the evidence?

- [SPARQL query (.rq)](CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.span.rq)
- [Recorded sample answers (.csv)](CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.answer.csv)

The query follows `selects` from the final Outcome to the chosen Option, then finds Agreement moves targeting that Option. It returns each position, speaker, supporting text, and turn number. The reasoner infers `Agreement` from the positions’ `isPositiveSupportedBy` links to TextSpans. Property chains infer `hasPositionTowards`, `hasSpeaker`, and `hasUtterance`. The recorded answer identifies Speaker D at turn 25, Speaker B at turn 26, Speaker C at turn 27, and Speaker A at turn 28.

The remaining competency questions and their scenarios are described in the [current use case](usecase.html#competency-questions).
