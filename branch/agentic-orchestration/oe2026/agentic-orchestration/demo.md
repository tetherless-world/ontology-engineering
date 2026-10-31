---
layout: default
title: queries
---

## Queries

SPARQL queries for the three competency questions that scope the ontology (CQ 1, CQ 3 and CQ 5 of the
[use case](usecase.html)). They run on [OE_9_TeamAgenticCapabilities_Individuals.rdf](OE_9_TeamAgenticCapabilities_Individuals.rdf),
which imports [OE_9_TeamAgenticCapabilities.rdf](OE_9_TeamAgenticCapabilities.rdf). CQ 1 follows the semantic processes
of the use case in order: step 1 finds the skills, tools and servers that Ken's request needs, step 2 finds the candidate
plans that meet all of his requirements and constraints, and the CQ 1 query returns the plan the reasoner selects.
The [query file](OE_9_TeamAgenticCapabilities_SPARQLQueries.txt) gives every query with its prefixes, the reasoning it
needs, the individuals it uses and its expected answer; it also has versions of CQ 1 and CQ 5 for Protégé's SPARQL
Query tab.

Queries marked **OWL 2 DL** need a reasoner: run them in the Snap SPARQL Query plugin with Pellet or HermiT started.
Queries marked **none** also run in Protégé's SPARQL Query tab. Each query below returned the answer shown when run
through the Snap SPARQL Query plugin 6.0.0 with Pellet and with HermiT.

### CQ 1, step 1 (semantic lookup): which skills, tools and MCP servers does Ken's request need?

**Reasoning: none.** The query starts from Ken's request. It takes the information requirements the request expresses and the hard constraints derived from a preference setting of the person the request is attributed to (or from the request itself), finds the capabilities that satisfy them, and lists the skills with those capabilities, the tools each skill uses for that capability and the MCP servers that expose the tools. Ken's soft constraints are not satisfied by a capability; they are measured by decision criteria when the candidate plans are ranked.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?requirementLabel ?hardConstraintLabel ?capabilityLabel ?skillLabel ?tool ?toolServer
WHERE {
  {
    oe-agtorch-ind:kenRequest oe-agtorch:expresses ?requirement .
    ?requirement a oe-agtorch:InformationRequirement .
    ?requirement rdfs:label ?requirementLabel .
    ?capability oe-agtorch:satisfiesRequirement ?requirement .
  }
  UNION
  {
    {
      oe-agtorch-ind:kenRequest prov:wasAttributedTo ?person .
      ?settings a oe-agtorch:PreferenceSetting .
      ?settings prov:wasAttributedTo ?person .
      ?constraint prov:wasDerivedFrom ?settings .
    }
    UNION
    {
      ?constraint prov:wasDerivedFrom oe-agtorch-ind:kenRequest .
    }
    ?constraint a oe-agtorch:HardConstraint .
    ?constraint rdfs:label ?hardConstraintLabel .
    ?capability oe-agtorch:satisfiesConstraint ?constraint .
  }
  ?capability rdfs:label ?capabilityLabel .
  ?skill a oe-agtorch:Skill .
  ?skill oe-agtorch:hasCapability ?capability .
  ?skill rdfs:label ?skillLabel .
  OPTIONAL {
    ?skill oe-agtorch:usesTool ?toolInd .
    ?toolInd oe-agtorch:hasCapability ?capability .
    ?toolInd skos:altLabel ?tool .
    OPTIONAL {
      ?server oe-agtorch:exposes ?toolInd .
      ?server rdfs:label ?toolServer .
    }
  }
}
ORDER BY ?hardConstraintLabel ?requirementLabel ?tool
```

**Answer** (6 rows):

| requirementLabel | hardConstraintLabel | capabilityLabel | skillLabel | tool | toolServer |
|---|---|---|---|---|---|
| affordable products with good reviews (Ken) |  | product search capability | product selection skill | search |  |
| supplement recommendations for building muscle mass (Ken) |  | supplement recommendation capability | personalized supplement recommendation skill | recommend_supplement | Supplement Advisor MCP server |
| supporting scientific evidence (Ken) |  | evidence verification capability | evidence verification skill | download_articles_batch | PubMed MCP server |
| supporting scientific evidence (Ken) |  | evidence verification capability | evidence verification skill | search_articles | PubMed MCP server |
|  | evidence verification (Ken) | evidence verification capability | evidence verification skill | download_articles_batch | PubMed MCP server |
|  | evidence verification (Ken) | evidence verification capability | evidence verification skill | search_articles | PubMed MCP server |

### CQ 1, step 2 (dependency and constraint-based reasoning): which candidate orchestration plans can answer Ken's request, and how does each one meet his information requirements and constraints?

**Reasoning: none.** The query starts from Ken's request, as in step 1, and keeps a plan for the request only if (a) every information requirement the request expresses is satisfied by the capability a task of one of the plan's steps requires, (b) every hard constraint of the request (from the requester's preference settings or from the request itself) is satisfied in the same way, and the plan violates no hard constraint, (c) every information artifact a task of the plan consumes is produced by a task of one of the plan's steps, so no step waits for an input the plan never creates. (Without property paths the query cannot follow agento:nextStep to check that the producing step comes earlier; CQ 2 derives the step order from these inputs and outputs.) For each plan that is kept, it lists the step and skill that meet each requirement and hard constraint, found through the capability that satisfies it, and the decision criterion of the plan's evaluation that measures each soft constraint. Which candidate is then selected is the CQ 1 query below. The plans still have to address Ken's request: Jessica's plan also passes (a) to (c) for Ken's requirements, but its tasks work on Jessica's candidate supplements and products.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?planLabel ?requirementLabel ?constraintLabel ?stepLabel ?skillLabel ?criterionLabel
WHERE {
  ?plan a oe-agtorch:CandidateOrchestrationPlan .
  ?plan oe-agtorch:addresses oe-agtorch-ind:kenRequest .
  ?plan rdfs:label ?planLabel .
  # (a) drop the plan if an information requirement of the request is not satisfied by a capability that a task of
  #     one of the plan's steps requires
  MINUS {
    ?plan oe-agtorch:addresses oe-agtorch-ind:kenRequest .
    oe-agtorch-ind:kenRequest oe-agtorch:expresses ?r1 .
    ?r1 a oe-agtorch:InformationRequirement .
    MINUS {
      ?plan oe-agtorch:hasStep ?s1 .
      ?s1 agento:hasAssociatedTask ?t1 .
      ?t1 agento:requiresCapability ?c1 .
      ?c1 oe-agtorch:satisfiesRequirement ?r1 .
    }
  }
  # (b) drop the plan if a hard constraint of the request is not satisfied in the same way, or if it violates one
  MINUS {
    ?plan oe-agtorch:addresses oe-agtorch-ind:kenRequest .
    {
      oe-agtorch-ind:kenRequest prov:wasAttributedTo ?p2 .
      ?settings2 a oe-agtorch:PreferenceSetting .
      ?settings2 prov:wasAttributedTo ?p2 .
      ?h2 prov:wasDerivedFrom ?settings2 .
    }
    UNION
    {
      ?h2 prov:wasDerivedFrom oe-agtorch-ind:kenRequest .
    }
    ?h2 a oe-agtorch:HardConstraint .
    MINUS {
      ?plan oe-agtorch:hasStep ?s2 .
      ?s2 agento:hasAssociatedTask ?t2 .
      ?t2 agento:requiresCapability ?c2 .
      ?c2 oe-agtorch:satisfiesConstraint ?h2 .
    }
  }
  MINUS {
    ?plan oe-agtorch:violatesConstraint ?h3 .
  }
  # (c) drop the plan if a task of one of its steps consumes an information artifact that no task of the plan produces
  MINUS {
    ?plan oe-agtorch:hasStep ?s4 .
    ?s4 agento:hasAssociatedTask ?t4 .
    ?t4 oe-agtorch:consumes ?artifact .
    MINUS {
      ?plan oe-agtorch:hasStep ?s5 .
      ?s5 agento:hasAssociatedTask ?t5 .
      ?t5 oe-agtorch:produces ?artifact .
    }
  }
  {
    {
      oe-agtorch-ind:kenRequest oe-agtorch:expresses ?requirement .
      ?requirement a oe-agtorch:InformationRequirement .
      ?requirement rdfs:label ?requirementLabel .
      ?capability oe-agtorch:satisfiesRequirement ?requirement .
    }
    UNION
    {
      {
        oe-agtorch-ind:kenRequest prov:wasAttributedTo ?person .
        ?settings a oe-agtorch:PreferenceSetting .
        ?settings prov:wasAttributedTo ?person .
        ?constraint prov:wasDerivedFrom ?settings .
      }
      UNION
      {
        ?constraint prov:wasDerivedFrom oe-agtorch-ind:kenRequest .
      }
      ?constraint a oe-agtorch:HardConstraint .
      ?constraint rdfs:label ?constraintLabel .
      ?capability oe-agtorch:satisfiesConstraint ?constraint .
    }
    ?plan oe-agtorch:hasStep ?step .
    ?step agento:hasAssociatedTask ?task .
    ?task agento:requiresCapability ?capability .
    ?step rdfs:label ?stepLabel .
    ?skill a oe-agtorch:Skill .
    ?skill oe-agtorch:hasCapability ?capability .
    ?skill rdfs:label ?skillLabel .
  }
  UNION
  {
    {
      oe-agtorch-ind:kenRequest prov:wasAttributedTo ?person .
      ?settings a oe-agtorch:PreferenceSetting .
      ?settings prov:wasAttributedTo ?person .
      ?softConstraint prov:wasDerivedFrom ?settings .
    }
    UNION
    {
      ?softConstraint prov:wasDerivedFrom oe-agtorch-ind:kenRequest .
    }
    ?softConstraint a oe-agtorch:SoftConstraint .
    ?softConstraint rdfs:label ?constraintLabel .
    ?softConstraint oe-agtorch:isMeasuredBy ?criterion .
    ?eval oe-agtorch:evaluates ?plan .
    ?eval oe-agtorch:usesCriterion ?criterion .
    ?criterion rdfs:label ?criterionLabel .
  }
}
ORDER BY ?planLabel ?criterionLabel ?constraintLabel ?requirementLabel ?stepLabel
```

**Answer** (14 rows):

| planLabel | requirementLabel | constraintLabel | stepLabel | skillLabel | criterionLabel |
|---|---|---|---|---|---|
| Ken plan 1 | affordable products with good reviews (Ken) |  | Ken plan 1, step 4 | product selection skill |  |
| Ken plan 1 | supplement recommendations for building muscle mass (Ken) |  | Ken plan 1, step 2 | personalized supplement recommendation skill |  |
| Ken plan 1 | supporting scientific evidence (Ken) |  | Ken plan 1, step 6 | evidence verification skill |  |
| Ken plan 1 |  | evidence verification (Ken) | Ken plan 1, step 6 | evidence verification skill |  |
| Ken plan 1 |  | minimize external tool calls (Ken) |  |  | fewest external tool calls (Ken) |
| Ken plan 1 |  | minimize token usage (Ken) |  |  | lowest token cost (Ken) |
| Ken plan 2 | affordable products with good reviews (Ken) |  | Ken plan 2, step 2 | product selection skill |  |
| Ken plan 2 | supplement recommendations for building muscle mass (Ken) |  | Ken plan 2, step 1 | personalized supplement recommendation skill |  |
| Ken plan 2 | supporting scientific evidence (Ken) |  | Ken plan 2, step 3 | evidence verification skill |  |
| Ken plan 2 | supporting scientific evidence (Ken) |  | Ken plan 2, step 5 | evidence verification skill |  |
| Ken plan 2 |  | evidence verification (Ken) | Ken plan 2, step 3 | evidence verification skill |  |
| Ken plan 2 |  | evidence verification (Ken) | Ken plan 2, step 5 | evidence verification skill |  |
| Ken plan 2 |  | minimize external tool calls (Ken) |  |  | fewest external tool calls (Ken) |
| Ken plan 2 |  | minimize token usage (Ken) |  |  | lowest token cost (Ken) |

### CQ 1. What orchestration plan should the agent follow to answer Ken's request for supplement recommendations, given his preference for few tool calls and low token use?

**Reasoning: OWL 2 DL.** No plan is asserted to be selected. SelectedOrchestrationPlan is a defined class: a candidate orchestration plan whose plan evaluation has rank 1. The reasoner classifies Ken plan 1 into it from its evaluation, so without a reasoner this query returns no rows. Tools are listed for a step only when they provide the capability its task requires.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?planLabel ?stepLabel ?taskLabel ?skillLabel ?tool ?toolServer
WHERE {
  ?plan a oe-agtorch:SelectedOrchestrationPlan .
  ?plan oe-agtorch:addresses oe-agtorch-ind:kenRequest .
  ?plan rdfs:label ?planLabel .
  ?plan oe-agtorch:hasStep ?step .
  ?step rdfs:label ?stepLabel .
  ?step agento:hasAssociatedTask ?task .
  ?task rdfs:label ?taskLabel .
  OPTIONAL {
    ?task oe-agtorch:performedBySkill ?skill .
    ?skill rdfs:label ?skillLabel .
    OPTIONAL {
      ?task agento:requiresCapability ?capability .
      ?skill oe-agtorch:usesTool ?toolInd .
      ?toolInd oe-agtorch:hasCapability ?capability .
      ?toolInd skos:altLabel ?tool .
      OPTIONAL {
        ?server oe-agtorch:exposes ?toolInd .
        ?server rdfs:label ?toolServer .
      }
    }
  }
}
ORDER BY ?stepLabel ?tool
```

**Answer** (10 rows):

| planLabel | stepLabel | taskLabel | skillLabel | tool | toolServer |
|---|---|---|---|---|---|
| Ken plan 1 | Ken plan 1, step 1 | get user profile (Ken) |  |  |  |
| Ken plan 1 | Ken plan 1, step 2 | get candidate supplements (Ken) | personalized supplement recommendation skill | recommend_supplement | Supplement Advisor MCP server |
| Ken plan 1 | Ken plan 1, step 3 | remove redundant supplements (Ken) |  |  |  |
| Ken plan 1 | Ken plan 1, step 4 | get supplement products sorted by price (Ken) | product selection skill | search |  |
| Ken plan 1 | Ken plan 1, step 5 | rank supplement products by cost (Ken) |  |  |  |
| Ken plan 1 | Ken plan 1, step 6 | verify evidence (Ken) | evidence verification skill | download_articles_batch | PubMed MCP server |
| Ken plan 1 | Ken plan 1, step 6 | verify evidence (Ken) | evidence verification skill | search_articles | PubMed MCP server |
| Ken plan 1 | Ken plan 1, step 7 | rank supplement products by evidence (Ken) |  |  |  |
| Ken plan 1 | Ken plan 1, step 8 | select supplement product (Ken) | product selection skill |  |  |
| Ken plan 1 | Ken plan 1, step 9 | produce recommendation (Ken) |  |  |  |

#### CQ 1, supporting query: how Ken's two candidate plans were evaluated

**Reasoning: none.** Ken's soft constraints (few external tool calls, low token use) are the criteria of both plan evaluations; the evaluation with the higher score has rank 1.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?planLabel ?toolCalls ?tokenCost ?score ?rank
WHERE {
  ?plan oe-agtorch:addresses oe-agtorch-ind:kenRequest .
  ?plan rdfs:label ?planLabel .
  ?eval oe-agtorch:evaluates ?plan .
  ?eval oe-agtorch:hasScore ?score .
  ?eval oe-agtorch:hasRank ?rank .
  ?eval oe-agtorch:hasMeasurement ?calls .
  ?calls a oe-agtorch:ToolCallCount .
  ?calls oe-agtorch:hasValue ?toolCalls .
  ?eval oe-agtorch:hasMeasurement ?cost .
  ?cost a oe-agtorch:TokenCost .
  ?cost oe-agtorch:hasValue ?tokenCost .
}
ORDER BY ?rank
```

**Answer** (2 rows):

| planLabel | toolCalls | tokenCost | score | rank |
|---|---|---|---|---|
| Ken plan 1 | 4 | 0.02 | 2.00 | 1 |
| Ken plan 2 | 9 | 0.05 | 0.00 | 2 |

#### CQ 1, supporting query: which of Ken's candidate plans is rejected

**Reasoning: OWL 2 DL.** A request has at most one selected plan, and every candidate plan is selected or rejected. Once Ken plan 1 is selected, the reasoner concludes that plan 2 is rejected. This needs the owl:AllDifferent axiom in the individuals file: without it, kenPlan1 and kenPlan2 could name the same plan.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?planLabel
WHERE {
  ?plan a oe-agtorch:RejectedOrchestrationPlan .
  ?plan oe-agtorch:addresses oe-agtorch-ind:kenRequest .
  ?plan rdfs:label ?planLabel .
}
```

**Answer** (1 row):

| planLabel |
|---|
| Ken plan 2 |

### CQ 3. What skills are required to satisfy Jessica's request for supplement recommendations, given she explicitly mentions her diagnosis and prescribed medication?

**Reasoning: none.** A skill is kept when one of its capabilities satisfies an information requirement that Jessica's request expresses, or a hard constraint derived from a preference setting of the person the request is attributed to.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?skillLabel ?capabilityLabel ?requirementLabel ?hardConstraintLabel
WHERE {
  ?skill a oe-agtorch:Skill .
  ?skill rdfs:label ?skillLabel .
  ?skill oe-agtorch:hasCapability ?capability .
  ?capability rdfs:label ?capabilityLabel .
  OPTIONAL {
    oe-agtorch-ind:jessicaRequest oe-agtorch:expresses ?requirement .
    ?capability oe-agtorch:satisfiesRequirement ?requirement .
    ?requirement rdfs:label ?requirementLabel .
  }
  OPTIONAL {
    oe-agtorch-ind:jessicaRequest prov:wasAttributedTo ?person .
    ?settings a oe-agtorch:PreferenceSetting .
    ?settings prov:wasAttributedTo ?person .
    ?constraint a oe-agtorch:HardConstraint .
    ?constraint prov:wasDerivedFrom ?settings .
    ?constraint rdfs:label ?hardConstraintLabel .
    ?capability oe-agtorch:satisfiesConstraint ?constraint .
  }
  FILTER (BOUND(?requirementLabel) || BOUND(?hardConstraintLabel))
}
ORDER BY ?skillLabel
```

**Answer** (4 rows):

| skillLabel | capabilityLabel | requirementLabel | hardConstraintLabel |
|---|---|---|---|
| evidence verification skill | evidence verification capability | supporting scientific evidence (Jessica) | evidence verification (Jessica) |
| personalized supplement recommendation skill | supplement recommendation capability | supplement recommendations (Jessica) |  |
| product selection skill | product search capability | purchasable supplement products (Jessica) |  |
| supplement safety screening skill | interaction screening capability |  | safety screening against celecoxib (Jessica) |

#### CQ 3, supporting query: which of those skills are constraint-satisfying skills

**Reasoning: OWL 2 DL.** ConstraintSatisfyingSkill is a defined class: a skill with a capability that satisfies at least one hard constraint (ConstraintSatisfyingCapability). Neither class is asserted for any individual; the reasoner classifies the skills a plan for Jessica must include because of her hard constraints.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT ?skillLabel ?capabilityLabel ?hardConstraintLabel
WHERE {
  ?skill a oe-agtorch:ConstraintSatisfyingSkill .
  ?skill rdfs:label ?skillLabel .
  ?skill oe-agtorch:hasCapability ?capability .
  ?capability rdfs:label ?capabilityLabel .
  ?capability oe-agtorch:satisfiesConstraint ?constraint .
  ?constraint a oe-agtorch:HardConstraint .
  ?constraint rdfs:label ?hardConstraintLabel .
  ?constraint prov:wasDerivedFrom ?settings .
  ?settings prov:wasAttributedTo ?person .
  oe-agtorch-ind:jessicaRequest prov:wasAttributedTo ?person .
}
ORDER BY ?skillLabel
```

**Answer** (2 rows):

| skillLabel | capabilityLabel | hardConstraintLabel |
|---|---|---|
| evidence verification skill | evidence verification capability | evidence verification (Jessica) |
| supplement safety screening skill | interaction screening capability | safety screening against celecoxib (Jessica) |

### CQ 5. Why was each agent capability chosen to execute in a given orchestration plan? (Dante's plan from the CQ 4 example)

**Reasoning: OWL 2 DL.** Dante's plan is selected by inference, as in CQ 1. For each step, the capability its task requires is listed with the information requirement of Dante's request or the constraint from his preference settings that it satisfies, and with the skill and MCP server that provide it.

```sparql
PREFIX rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:           <http://www.w3.org/2004/02/skos/core#>
PREFIX prov:           <http://www.w3.org/ns/prov#>
PREFIX agento:         <http://www.w3id.org/agentic-ai/onto#>
PREFIX oe-agtorch:     <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/>
PREFIX oe-agtorch-ind: <https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/>

SELECT DISTINCT ?stepLabel ?taskLabel ?skillLabel ?toolServer ?capabilityLabel ?requirementLabel ?constraintLabel
WHERE {
  ?plan a oe-agtorch:SelectedOrchestrationPlan .
  ?plan oe-agtorch:addresses oe-agtorch-ind:danteRequest .
  ?plan oe-agtorch:hasStep ?step .
  ?step rdfs:label ?stepLabel .
  ?step agento:hasAssociatedTask ?task .
  ?task rdfs:label ?taskLabel .
  ?task agento:requiresCapability ?capability .
  ?capability rdfs:label ?capabilityLabel .
  OPTIONAL {
    ?task oe-agtorch:performedBySkill ?skill .
    ?skill rdfs:label ?skillLabel .
  }
  OPTIONAL {
    ?task oe-agtorch:performedBySkill ?skill .
    ?skill oe-agtorch:usesTool ?toolInd .
    ?toolInd oe-agtorch:hasCapability ?capability .
    ?server oe-agtorch:exposes ?toolInd .
    ?server rdfs:label ?toolServer .
  }
  OPTIONAL {
    oe-agtorch-ind:danteRequest oe-agtorch:expresses ?requirement .
    ?capability oe-agtorch:satisfiesRequirement ?requirement .
    ?requirement rdfs:label ?requirementLabel .
  }
  OPTIONAL {
    oe-agtorch-ind:danteRequest prov:wasAttributedTo ?person .
    ?settings a oe-agtorch:PreferenceSetting .
    ?settings prov:wasAttributedTo ?person .
    ?constraint prov:wasDerivedFrom ?settings .
    ?capability oe-agtorch:satisfiesConstraint ?constraint .
    ?constraint rdfs:label ?constraintLabel .
  }
  FILTER (BOUND(?requirementLabel) || BOUND(?constraintLabel))
}
ORDER BY ?stepLabel
```

**Answer** (5 rows):

| stepLabel | taskLabel | skillLabel | toolServer | capabilityLabel | requirementLabel | constraintLabel |
|---|---|---|---|---|---|---|
| Dante's orchestration plan, step 1a | verify evidence (magnesium glycinate) | evidence verification skill | PubMed MCP server | evidence verification capability | evidence summary (Dante) |  |
| Dante's orchestration plan, step 1b | screen interactions (magnesium glycinate) | supplement safety screening skill | OpenFDA MCP server | interaction screening capability |  | safety screening (Dante) |
| Dante's orchestration plan, step 2a | verify evidence (magnesium citrate) | evidence verification skill | PubMed MCP server | evidence verification capability | evidence summary (Dante) |  |
| Dante's orchestration plan, step 2b | screen interactions (magnesium citrate) | supplement safety screening skill | OpenFDA MCP server | interaction screening capability |  | safety screening (Dante) |
| Dante's orchestration plan, step 3 | synthesize evidence (Dante) | evidence synthesis skill |  | evidence synthesis capability | comparison of magnesium glycinate and magnesium citrate (Dante) |  |
