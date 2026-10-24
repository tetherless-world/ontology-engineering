---
layout: default
title: Demonstration and Queries
---

## Sample Conversation

The demonstration uses the [CQ sample conversation individuals](OE_8_TeamCJF_Individuals.rdf) with the [current CJF schema](OE_8_TeamCJF.rdf). The [source conversation XML](files/conversations/CQ-sample-conversation.xml) preserves the utterance sequence and speaker labels.

## CQ1 Conversation Moves and Current States

**Question:** Which CJF conversation moves have occurred in the conversation, and what is the latest known state of each conversation move, where a state applies?

- [SPARQL query (.rq)](CQAnswers/CQ1/cq1-conversation-moves-current-states.rq)
- [Recorded sample answers (.md)](CQAnswers/CQ1/answers.md)

The query returns the move, its known move type, and its known state type. Its optional state pattern retains conversation moves without an applicable or known specific state. When querying `hasState`, the ontology's property chain derives the state through `hasCurrentStateAssignment` followed by `assignedState`; the corresponding inferred triples must be available to the query engine. Inferred superclass types can produce several rows for one move.

The [SHACL rules](shacl/current-state-assignment-rules.ttl) identify terminal assignments in each move's recorded history. The [Python runner](scripts/current_state_assignments.py) refreshes the current assignment links and validates the histories. “Current” refers to the latest assignment in the loaded conversation data. The [script documentation (.md)](scripts/README.md) describes the import and validation workflow.

The remaining competency questions and their scenarios are described in the [current use case](usecase.html#competency-questions).
