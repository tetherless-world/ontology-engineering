# OE Week 10 conceptual model assets

`OE_10_TeamCJF_ConceptualModel.docx` is the supplied Week 10 conceptual model document. `OE_10_TeamCJF_ConceptualModel.pdf` was exported from it with Microsoft Word. No Draw.io source was supplied for this week; the Week 9 source remains in `../oe9/`.

The ten website figures in `images/conceptual-model/oe10/` were extracted from the DOCX unchanged, in document order:

| Website asset | Document figure | Compared with Week 9 |
| --- | --- | --- |
| provenance.png | Provenance Diagram | New export: adds a Conversation Move Components group and the date-time link on Utterance |
| conversation-moves-with-states.png | CJF Conversation Moves that have states | Reverts to the Week 8 image that includes the detached Claim/Issue/Option fragment |
| deliberative-conversation-moves.png | A Deliberative CJF Conversation Move | Unchanged |
| state-taxonomy.png | CJF Conversation Moves state taxonomy | New export, including the inset table of applicable states, the description, and the legend |
| state-assignment-history.png | Previous State Assignment Diagram | New export |
| expressed-position.png | Expressed Position Subdiagram | New export with a Provenance Component group |
| conversation-move-relationships.png | Relationships between CJF Conversation Moves | Unchanged |
| property-hierarchy.png | Diagram of Property Hierarchy | New export |
| relationship-class-taxonomy.png | Reification CJF Relationship Class Taxonomy | New export |
| relationship-reification.png | Reification Diagram | New export |

The figures still differ from `ontology/OE_10_TeamCJF.rdf` in a few labels, and the RDF is authoritative:

- The figures label `hasPositionToward` and `makesAddress`. The schema uses `hasPositionTowards` and `makesAddresses`.
- The state taxonomy shows SupportedContested, and its inset lists Accepted for Claims. The Week 10 schema defines neither, and SupportedContested was removed from the Week 10 term list.
- The relationship class taxonomy shows `hasSummary` on CJFConversationMoveRelationship. The reification figure and the schema use `hasReason`, and the schema reserves `hasSummary` for conversation moves.
- The schema also defines a Refinement relationship class, which the relationship class taxonomy does not show.
- The document's provenance and expressed-position descriptions mention a CQ7. The Week 10 use case defines six competency questions.
