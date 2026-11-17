---
layout: default
title: Use Case
---

## Use Case Document

**Current version: OE Week 11.**

<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=https%3A%2F%2Ftetherless-world.github.io%2Fontology-engineering%2Fbranch%2Ftracking-cjf%2Foe2026%2Ftracking-cjf%2Ffiles%2Fuse-cases%2FOE_11_TeamCJF_UseCase_Clean.docx" title="OE Week 11 use case preview" style="width:100%;height:700px;border:0;" allowfullscreen></iframe>

### Download

[Download the OE Week 11 use case (.docx)](files/use-cases/OE_11_TeamCJF_UseCase_Clean.docx)

The **CJF-TRACKING** use case represents the evolving state of collective judgment formation in multiparty dialogue. A human user or researcher can query the group's developing reasoning, the relationships among its contributions, and the matters that remain unresolved as the conversation unfolds.

The model preserves utterances, speakers, turn order, and evidence text spans. A single utterance can express several distinct conversation moves. State assignments retain the evidence and conversation point for each recorded change, allowing current state information to be retrieved alongside its history.

## Scope

The class implementation uses annotated segments from multiparty conversations. Candidate annotations may be prepared with LLM assistance, but a human reviewer verifies them before they are represented in the ontology. Transcription, speaker identification, automatic ontology modification, generating interventions, and judging whether a group decision is correct are outside the use case.

State changes require positive conversational evidence. The absence of further objections alone does not establish that an issue has been resolved.

## Competency Questions

The OE Week 11 use case develops six questions around a group choosing a software platform.

1. Which CJF conversation moves have occurred in the conversation, and what are their identifiers, types, summaries, and recorded states, where applicable?
2. Which Issues raised during the conversation have been assigned an Addressed or Resolved state, and what conversational evidence is associated with each Issue and its recorded states?
3. Which Claims support or challenge Platform A, what are their summaries and recorded states, and which of these Claims have been assigned a Supported state?
4. Which Issues associated with Platform A have been assigned an Open, Addressed, or Resolved state, and what conversational evidence is associated with each Issue and its recorded states?
5. Which speakers explicitly agreed with the Option selected by the group, and what are the identifiers, supporting utterances, and turn numbers of their Expressed Positions?
6. What positions did Speaker C express toward Platform A and Platform B throughout the conversation, and what are the identifiers, target Options, summaries, supporting utterances, and turn numbers of these Expressed Positions?

The document includes the full scenarios for all six questions. The [OE Week 11 demonstration](demo.html) provides runnable queries and recorded answers for CQ1, CQ2, CQ3, CQ5, and CQ6. See the [conceptual model](ontology.html#conceptual-model) and [terminology list](termlist.html) for the vocabulary used in the questions.

## Previous Versions

- [OE Week 10 use case (.docx)](files/use-cases/OE_10_TeamCJF_UseCase.docx)
- [OE Week 9 use case (.docx)](files/use-cases/OE_9_TeamCJF_UseCase_Clean.docx)
- [OE Week 8 use case (.docx)](files/use-cases/OE_8_TeamCJF_UseCase_Clean.docx)
- [OE Week 6 use case (.docx)](files/use-cases/OE_6_TeamCJF_UseCase_Clean.docx)
- [OE Week 5 use case (.docx)](files/use-cases/OE_5_TeamCJF_UseCase_Clean.docx)
- [OE Week 4 use case (.docx)](files/use-cases/OE_4_TeamCJF_UseCase_Clean.docx)
- [Previously published Google Docs copy](https://docs.google.com/document/d/e/2PACX-1vSjFTlpi4ZBLQ6mj3VrDoGTW96Ub5LIWQ2qtSNZrMmotNfi34l-CE4Pk-8AbZPWJA/pub)
