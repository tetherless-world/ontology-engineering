[Concept Map](#conceptual-model) | [Ontology File](#ontology) | [Ontologies Reused](#ontologies-reused) | [Ontology Prefixes](#ontology-prefixes)

## Conceptual Model

**Current version: 3.0 (Assignment 8, October 22, 2026), unchanged in Assignment 9.** The model is aligned with the
ontology below: every class, is-a line, arrow and attribute in the diagrams is a term of the ontology with the same name,
and every class and property of the ontology appears in a diagram.

![Figure 1a. Requests, requirements, constraints and capabilities](files/conceptual_models/v3.0/fig1a_overview_requests.png)

![Figure 1b. Plans, steps, tasks, evaluation and invocations](files/conceptual_models/v3.0/fig1b_overview_plans.png)

<iframe src="files/conceptual_models/OE_8_TeamAgenticCapabilities_ConceptualModel.pdf" style="width: 100%;height: 700px;border: none;"></iframe>

Figures as images (PNG and SVG; the PlantUML sources, which load into PlantUML, are in
[files/conceptual_models/v3.0/src](files/conceptual_models/v3.0/src/)):
[1a](files/conceptual_models/v3.0/fig1a_overview_requests.png) ·
[1b](files/conceptual_models/v3.0/fig1b_overview_plans.png) ·
[2](files/conceptual_models/v3.0/fig2_requests_constraints.png) ·
[3a](files/conceptual_models/v3.0/fig3a_skills_resources.png) ·
[3b](files/conceptual_models/v3.0/fig3b_capabilities.png) ·
[3c](files/conceptual_models/v3.0/fig3c_justified_capabilities.png) ·
[4](files/conceptual_models/v3.0/fig4_tools_servers.png) ·
[5a](files/conceptual_models/v3.0/fig5a_plan_structure.png) ·
[5b](files/conceptual_models/v3.0/fig5b_task_dependencies.png) ·
[5c](files/conceptual_models/v3.0/fig5c_inferred_dependencies.png) ·
[6a](files/conceptual_models/v3.0/fig6a_plan_selection.png) ·
[6b](files/conceptual_models/v3.0/fig6b_plan_metrics.png) ·
[7a](files/conceptual_models/v3.0/fig7a_invocations.png) ·
[7b](files/conceptual_models/v3.0/fig7b_artifact_provenance.png) ·
[8a](files/conceptual_models/v3.0/fig8a_artifact_kinds.png) ·
[8b](files/conceptual_models/v3.0/fig8b_artifact_roles.png)

### Previous Versions

- [Version 2.0 (Assignment 6)](files/conceptual_models/OE_6_TeamAgenticCapabilities_ConceptualModel.pdf)
  ([redlined](files/conceptual_models/OE_6_TeamAgenticCapabilities_RedlinedConceptualModel.pdf)), figures and PlantUML
  sources in [files/conceptual_models/v2.0](files/conceptual_models/v2.0/src/)
- [Version 1.1 (Assignment 5)](files/conceptual_models/OE_5_TeamAgenticCapabilities_ConceptualModel.pdf)
- Protégé OntoGraf views of the Figure 4 and Figure 7 classes:
  [Figure 4](files/conceptual_models/Figure4-Tools-Servers.png),
  [Figure 7](files/conceptual_models/Figure7-Execution-Provenance.png),
  [combined](files/conceptual_models/Figures4-and-7-Combined.png)

## Ontology

- **Files (Assignment 9):** [OE_9_TeamAgenticCapabilities.rdf](OE_9_TeamAgenticCapabilities.rdf) (classes and properties)
  and [OE_9_TeamAgenticCapabilities_Individuals.rdf](OE_9_TeamAgenticCapabilities_Individuals.rdf) (individuals; imports
  the main ontology), OWL 2 in RDF/XML written with the course serializer
- **SPARQL queries:** [OE_9_TeamAgenticCapabilities_SPARQLQueries.txt](OE_9_TeamAgenticCapabilities_SPARQLQueries.txt);
  the queries for CQ 1, CQ 3 and CQ 5 and their answers are on the [Demonstration & Queries](demo.html) page
- **Namespace:** `https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/`
- **Size:** 64 classes, 27 object properties and 8 datatype properties of the team's own, and 146 individuals; consistent,
  with no unsatisfiable classes (Pellet 2.2.0 and HermiT 1.4.3.456); [test log](files/ontology/OE_9_TeamAgenticCapabilities_TestLog.txt)
- **Scope:** competency questions 1, 3 and 5 of the [use case](usecase.html) (Section VII)
- **Opening it in Protégé:** open OE_9_TeamAgenticCapabilities_Individuals.rdf from this folder. `catalog-v001.xml` maps
  the main ontology IRI to OE_9_TeamAgenticCapabilities.rdf and the AgentO and P-Plan imports to the copies in `imports/`:
  the AgentO IRI redirects to a web page, and the P-Plan purl did not resolve on October 29, 2026.
- **Previous versions:** Assignment 8, [main](archived/OE_8_TeamAgenticCapabilities.txt) and
  [individuals](archived/OE_8_TeamAgenticCapabilities_Individuals.txt); Assignment 6,
  [main](archived/agentic-orchestration.txt), [example individuals](archived/cq_examples.txt) and
  [reasoner answers](archived/cq_results.txt). Archived ontology files are stored as .txt so that the hygiene check
  skips them.

### Main Classes and Definitions

| Class | Superclass | Definition |
|---|---|---|
| Request | — | user input that expresses a task, action, or information need for an agent to address |
| InformationRequirement | — | formalized description of information that a user needs to obtain |
| UserConstraint | agento:Constraint | constraint derived from a user's request, profile, or execution preferences that governs the selection or execution of an orchestration plan |
| Capability | equivalent to agento:Capability | ability of an agent to perform a type of action or task |
| Skill | — | specification of a focused agent behavior that can be applied to perform a class of tasks |
| Tool | agento:Tool, process:Process | callable computational resource that performs a defined operation when invoked |
| Server | — | software component that exposes computational resources and operations to clients through a communication protocol |
| OrchestrationPlan | pplan:Plan | plan that prescribes which capabilities to invoke, and in what order, to satisfy the information requirements of one request |
| OrchestrationWorkflowStep | agento:WorkflowStep | workflow step of an orchestration plan that is associated with the task carried out at that point in the plan |
| InformationArtifact | prov:Entity | information content entity represented as an identifiable item that can be consumed, produced, or retained during an agent workflow |
| PlanEvaluation | — | evaluation record that associates an orchestration plan with the criteria used and the plan metrics obtained |
| DecisionCriterion | — | criterion used to compare and select candidate orchestration plans based on measurable attributes and preferences |
| PlanMetric | cmns-qtu:Measure | measure used in an evaluation to characterize an orchestration plan on a specified dimension |
| Invocation | pplan:Activity | execution activity in which a particular tool or skill is called or applied |
| EvidenceAssessment | Assessment | assessment that summarizes and weighs the research findings about one candidate supplement |

The full list of classes, properties and individuals, with sources, is the [terminology list](termlist.html).

## Ontologies Reused

- [AgentO v0.2](https://w3id.org/agentic-ai/onto) (`agento:`): agents, tasks, tools, capabilities, workflow steps
- [P-Plan](http://purl.org/net/p-plan) (`pplan:`): plans, steps and the activities that carry them out (version 1.3, copy in `imports/`)
- [OWL-S 1.2 Process](https://www.w3.org/submissions/OWL-S/) (`process:`): tool parameters and preconditions
- [BEAM](http://w3id.org/beam/core) (`beam:`): the resource class above SkillResource
- [PROV-O](https://www.w3.org/TR/prov-o/) (`prov:`): provenance of invocations and information artifacts
- [OMG Commons Ontology Library](https://www.omg.org/spec/Commons/): annotation vocabulary, classifiers, collections,
  documents, organizations, quantities and units
- [FIBO FND Goals and Objectives](https://spec.edmcouncil.org/fibo/ontology/FND/GoalsAndObjectives/Objectives/), imported
  by the course seed ontology

## Ontology Prefixes

| Prefix | Namespace |
|---|---|
| oe-agtorch | `https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/` |
| agento | `http://www.w3id.org/agentic-ai/onto#` |
| pplan | `http://purl.org/net/p-plan#` |
| process | `http://www.daml.org/services/owl-s/1.2/Process.owl#` |
| prov | `http://www.w3.org/ns/prov#` |
| cmns-av | `https://www.omg.org/spec/Commons/AnnotationVocabulary/` |
| cmns-cls | `https://www.omg.org/spec/Commons/Classifiers/` |
| cmns-col | `https://www.omg.org/spec/Commons/Collections/` |
| cmns-doc | `https://www.omg.org/spec/Commons/Documents/` |
| cmns-org | `https://www.omg.org/spec/Commons/Organizations/` |
| cmns-qtu | `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` |
| beam | `http://w3id.org/beam/core#` |
| fibo-fnd-gao-obj | `https://spec.edmcouncil.org/fibo/ontology/FND/GoalsAndObjectives/Objectives/` |
| dct | `http://purl.org/dc/terms/` |
| skos | `http://www.w3.org/2004/02/skos/core#` |
| owl | `http://www.w3.org/2002/07/owl#` |
| rdfs | `http://www.w3.org/2000/01/rdf-schema#` |
| xsd | `http://www.w3.org/2001/XMLSchema#` |
