---
layout: default
title: Use Case
---

## Use Case Document

**Latest available use case document: OE Week 10.**

<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=https%3A%2F%2Ftetherless-world.github.io%2Fontology-engineering%2Fbranch%2Ftracking-cjf%2Foe2026%2Ftracking-cjf%2Ffiles%2Fuse-cases%2FOE_10_TeamCJF_UseCase.docx" title="OE Week 10 use case preview" style="width:100%;height:700px;border:0;" allowfullscreen></iframe>

### Download

[Download the OE Week 10 use case (.docx)](files/use-cases/OE_10_TeamCJF_UseCase.docx)

The **CJF-TRACKING** use case represents the evolving state of collective judgment formation in multiparty dialogue. A human user or researcher can query the group's developing reasoning, the relationships among its contributions, and the matters that remain unresolved as the conversation unfolds.

The model preserves utterances, speakers, turn order, and evidence text spans. A single utterance can express several distinct conversation moves. State assignments retain the evidence and conversation point for each recorded change, allowing current state information to be retrieved alongside its history.

## Scope

The class implementation uses annotated segments from multiparty conversations. Candidate annotations may be prepared with LLM assistance, but a human reviewer verifies them before they are represented in the ontology. Transcription, speaker identification, automatic ontology modification, generating interventions, and judging whether a group decision is correct are outside the use case.

State changes require positive conversational evidence. The absence of further objections alone does not establish that an issue has been resolved.

## Competency Questions

The OE Week 10 document develops six questions around a group choosing a software platform:

1. Which CJF conversation moves have occurred, and what is the latest known state of each move where a state applies?
2. Which Issues raised during the conversation are currently Addressed or Resolved, and what conversational evidence supports each Issue's current state?
3. What Claims support or challenge Platform A? Are any of the Claims Supported?
4. Which Issues associated with Platform A are currently Open, Addressed, or Resolved, and what conversational evidence supports their latest known states?
5. Which speakers explicitly agreed with the Option selected by the group?
6. What positions did Speaker C express toward Platforms A and B throughout the conversation?

The downloadable document contains the full scenarios, flows, examples, and requirements. In the Week 10 revision, the sample answers for CQ2 and CQ6 are the recorded SPARQL results. See also the [conceptual model](ontology.html#conceptual-model), [latest term list](termlist.html), and [OE Week 11 query demonstrations](demo.html) and the [OE Week 10 recorded answers](demo-oe10.html).

## Previous Versions

- [OE Week 9 use case (.docx)](files/use-cases/OE_9_TeamCJF_UseCase_Clean.docx)
- [OE Week 8 use case (.docx)](files/use-cases/OE_8_TeamCJF_UseCase_Clean.docx)
- [OE Week 6 use case (.docx)](files/use-cases/OE_6_TeamCJF_UseCase_Clean.docx)
- [OE Week 5 use case (.docx)](files/use-cases/OE_5_TeamCJF_UseCase_Clean.docx)
- [OE Week 4 use case (.docx)](files/use-cases/OE_4_TeamCJF_UseCase_Clean.docx)
- [Previously published Google Docs copy](https://docs.google.com/document/d/e/2PACX-1vSjFTlpi4ZBLQ6mj3VrDoGTW96Ub5LIWQ2qtSNZrMmotNfi34l-CE4Pk-8AbZPWJA/pub) — retained for reference; the OE Week 10 download is linked above.
