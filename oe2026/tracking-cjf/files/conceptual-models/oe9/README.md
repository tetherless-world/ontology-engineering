# OE Week 9 conceptual model assets

The current gallery, DOCX, and PDF share the same ten figures. The supplied [clean conceptual model document](https://docs.google.com/document/d/1g5sSTY4BW-QOnTiJ08P-OXhqqQ-okPQJJ6u_83ExRTE/edit) establishes the figure selection and descriptions. The [original Draw.io source](https://drive.google.com/file/d/1UtRVzrNCbk9A5FpHHIP1YpKRYCj40mmE/view) contains 17 working tabs. The local `OE_9_TeamCJF_ConceptualModel.drawio` retains only the ten published tabs in gallery order.

Seven changed tabs were exported with the diagrams.net renderer. Three unchanged figures preserve the existing PNG bytes. The Week 8 assets remain archived in their original directories.

| Website asset in `images/conceptual-model/oe9/` | Draw.io tab | Treatment |
| --- | --- | --- |
| provenance.png | ProvinanceV3 | Re-exported with summary, text, turn, speaker-name, and conversation-identifier fields |
| conversation-moves-with-states.png | MilestoneWithStateTaxonomy | Existing unchanged figure |
| deliberative-conversation-moves.png | DeliberativeMilestoneTaxonomy | Existing unchanged figure |
| state-taxonomy.png | StateTaxonomy | Re-exported with dashed `hasState`; corrected the historical inset terminology |
| state-assignment-history.png | StateAssignmentV3 | Re-exported with current assignments and inferred `hasState` |
| expressed-position.png | ExpressedPositionTaxonomy | Re-exported with `hasSpeaker` and corrected `hasPositionTowards` |
| conversation-move-relationships.png | DeliberativeMilestoneConceptualDiagram | Existing unchanged figure |
| property-hierarchy.png | propertyHierachy | Re-exported with current-assignment and response subproperties |
| relationship-class-taxonomy.png | RelationshipClassHierarchy | Re-exported with `hasReason` |
| relationship-reification.png | Reification example | Re-exported with corrected `makesAddresses`, text/turn fields, and `hasReason` |

The source layouts are preserved. Label corrections follow `ontology/OE_9_TeamCJF.rdf`: `hasPositionTowards` and `makesAddresses` use their implemented plural spellings; relationship records and StateAssignment use `hasReason`, while conversation moves use `hasSummary`. The state-taxonomy inset now lists the current Claim state names instead of the legacy Accepted label. The reification figure uses the native union symbol in place of its MathJax source expression.

The figure descriptions use the six-question Week 9 scope, `hasSpeaker` instead of the earlier associatedWithSpeaker label, and the implemented reification property names. One current State individual can have multiple classifications, including Supported and Contested. The RDF remains authoritative for class IRIs and executable axioms.
