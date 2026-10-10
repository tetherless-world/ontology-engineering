# Editable team ontology and Figure 4/7 imports

Open [`../agentic-orchestration.rdf`](../agentic-orchestration.rdf) in Protégé. It is an editable RDF/XML OWL ontology containing the team's core, skills, plans, and evidence model together with Figure 4 tool interfaces and Figure 7 execution/provenance. Keep `../catalog-v001.xml`, this folder, and the repository's `../Commons/` folder with it. Existing FIBO dependencies may still require network access.

The additions were integrated with branch commit `7d4eca8`; the team's existing definitions, classes, individuals, and plan/evidence restrictions were retained. The ontology and version IRIs are unchanged.

## Active vocabulary imports

The main file imports the full AgentO and OWL-S **1.2** vocabularies already used by the team, plus the existing Commons/FIBO dependencies. Figure 4 references were aligned from the earlier standalone implementation's OWL-S 1.1 to the team's 1.2 IRIs. AgentO and the four OWL-S 1.2 files below are unmodified source copies resolved through the local catalog.

| Local source | Published source |
| --- | --- |
| `AgentO.owl` | https://sepses.ifs.tuwien.ac.at/onto/ontology.owl (published target of https://w3id.org/agentic-ai/onto) |
| `Process-1.2.owl` | https://www.daml.org/services/owl-s/1.2/Process.owl |
| `Expression-1.2.owl` | https://www.daml.org/services/owl-s/1.2/generic/Expression.owl |
| `Service-1.2.owl` | https://www.daml.org/services/owl-s/1.2/Service.owl |
| `ObjectList-1.2.owl` | https://www.daml.org/services/owl-s/1.2/generic/ObjectList.owl |
| `prov-o.owl` | https://www.w3.org/ns/prov-o.owl |
| `p-plan.owl` | https://dgarijo.github.io/Vocabularies/P-PLAN/Releases/Release12032014/p-plan.owl |

The active PROV-O and P-Plan imports are local compatibility copies, `prov-o-dl.rdf` and `p-plan-dl.rdf`, under the explicit local ontology IRIs `imports/PROVOCompatible/` and `imports/PPlanCompatible/`. Their class and object-property axioms, property chains, and functional `pplan:correspondsToStep` are retained. Published entity IRIs are unchanged. The unmodified downloads remain alongside them.

Compatibility changes:

- Remove the PROV annotation-property declarations for `prov:wasRevisionOf` and `prov:specializationOf`, retaining their object-property declarations. Remove those two statements from the ontology header; the original header remains in `prov-o.owl`. This removes annotation/object-property punning that violates OWL 2 DL.
- Use local ontology IRIs, remove the upstream PROV version IRI and redundant second ontology declaration, and add explicit source/compatibility annotations.
- Declare `dct:source` in both copies and `dct:creator`/`dct:license` in P-Plan. The main ontology declares the `xsd:date` datatype used by the team's publication-date property.

The old `Figure4Vocabulary.rdf` subset and the unversioned `Process.owl`, `Expression.owl`, `Service.owl`, and `ObjectList.owl` (OWL-S 1.1) are retained as provenance for the earlier Figure 4 work. They are **not active imports** of the current merged ontology. That subset was an explicit MIREOT-style selection, not a complete upstream ontology or locality module.

Upstream metadata and notices are retained in source files. AgentO and P-Plan identify CC BY 4.0 licenses in their published documentation; OWL-S is described in the [W3C member submission](https://www.w3.org/submissions/OWL-S/).

## Integration decisions

- Shared entity definitions from the team branch take precedence where the local Figure 4/7 draft used slightly different wording. Skill remains separate from Capability, following the conceptual model Figure 3 decision.
- Local Tool is a subclass of AgentO Tool. Local Capability is equivalent to AgentO Capability, aligning the Figure 4 view with the team's `hasCapability` range.
- `usesTool` retains the team's AgentO Tool range and has no global domain, since skills can also use tools. The Figure 4 agent-to-tool constraint is scoped to LLMAgent, avoiding classification of skills as agents.
- One existing disjointness pair, `prov:Agent` versus `agento:Tool`, was removed. AgentO declares LLMAgent a subclass of both; that pair made LLMAgent and the new invocation classes unsatisfiable. Every other pair from the team's large disjointness group is retained using a smaller group plus explicit Agent disjointness assertions.
- Invocation is a `pplan:Activity`; InformationArtifact is a `prov:Entity`. Answer and ExecutionTrace are information artifacts. Every Invocation corresponds to some AgentO WorkflowStep; P-Plan functionality makes that step unique.
- Agent association, used artifacts, and generated artifacts are existential restrictions. Generation is expressed as `Invocation subClassOf inverse(prov:wasGeneratedBy) some InformationArtifact`, so supplied input artifacts are not required to have been generated inside this workflow.
- ToolInvocation invokes some Tool and is part of some SkillInvocation; SkillInvocation invokes some Skill. `invokes` has one union range, Tool or Skill, instead of two intersecting range declarations.
- Imported PROV domains/ranges are preserved. No runtime individuals or timestamps were invented. OWL open-world restrictions are not explicit-record completeness checks such as SHACL.

## Diagrams and review

In Protégé's OntoGraf tab, use the folder icon to open a layout from `../files/conceptual_models/`:

- `Figures4-and-7-Combined.graph`: the 20 focal classes together.
- `Figure7-Execution-Provenance.graph`: the 10 Figure 7 classes including shared references.
- `Figure4-Tools-Servers.graph`: the earlier Figure 4 view.

These are editable layouts over the RDF ontology. The corresponding PNGs are review exports of the Protégé canvas; editing a PNG does not edit the ontology. Property labels appear on hover in OntoGraf. Solid “has subclass” arcs point from parent to child; dashed arcs show properties/restrictions. Layout files preserve positions, while view filters and pinning are session settings. The combined and Figure 7 PNGs were rendered before team integration; their focal classes and relationship endpoints remain the same, while the current RDF includes the additional team model and import/range reconciliation above.

## Validation and remaining team issues

Checked with OWLAPI and HermiT from Protégé 5.6.9 on 2026-10-09, using the updated Commons library and the full import closure:

- RDF/XML parses; all cataloged local imports load.
- OWL 2 DL profile passes for the merged ontology and imports.
- HermiT reports a consistent ontology; no local project class or AgentO LLMAgent is unsatisfiable.
- The incoming team ontology had **24 unsatisfiable imported classes**, including LLMAgent. The merged file has **23**, all inherited from that baseline; no new unsatisfiable classes were introduced. Those remaining issues concern P-Plan MultiStep and Commons classes constrained by the team's broad disjointness group. They are outside the Figure 4/7 integration and remain for team review. For example, declaring P-Plan Plan and Step disjoint conflicts with MultiStep being a subclass of both; Document versus Reference similarly conflicts with Commons ReferenceDocument.

The earlier standalone Figure 4/7 model passed with no unsatisfiable classes. That result should not be confused with the larger team model's coherence results above. Logical consistency alone does not imply that every class can have instances or that every competency question is implemented.
