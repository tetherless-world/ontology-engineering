---
---

## Queries

The following SPARQL queries address the team's four competency questions. Results below are **expected results specified in `OE_10_TeamAffordance_Queries.txt`**, not outputs independently executed for this Markdown document.

**Execution:** Load `OE_10_TeamAffordance_Individuals.rdf` and its import of `OE_10_TeamAffordance.rdf` in Protégé. **Asserted RDF** queries run in the standard SPARQL Query tab without a reasoner. Queries requiring **OWL/SWRL inference** use HermiT with a reasoner-aware interface (such as Snap SPARQL Query) or an exported ontology containing asserted and inferred class/object-property assertions.

**Source status:** The supplied TXT is marked as a draft merge: CQ1 and CQ3 were inherited from OE9, CQ2 and CQ4 were updated for OE10, and final execution against the complete OE10 RDF combination remained to be checked. The tables therefore document expected behavior rather than confirmed final submission results.

### CQ1: Can a rigid plastic card be used to cut a carrot, and why?

For the represented carrot (`af:hardness = af:high`), CUT requires low edge thickness and high rigidity. The card is represented with both required feature levels.

#### Query 1.1: Retrieve the inferred feasibility judgment for the card–carrot CUT assessment

*Reasoning: OWL/SWRL inference (rules S1, S3, and S4); run with HermiT and a reasoner-aware query interface.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?judgment
WHERE {
    af:cardCarrotCutAssessment af:hasJudgment ?judgment .
}
```

#### Result 1.1: Expected card feasibility judgment

| Judgment |
|---|
| `af:feasibleJudgment` |

One row is expected with reasoning. Without inferred `af:hasJudgment` assertions, the standard asserted-only query may return no rows.

#### Query 1.2: Compare the applicable CUT requirements with the card’s represented features

*Reasoning: Asserted RDF; no reasoner needed.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate ?target ?action
       ?targetFeature ?targetLevel
       ?requirement ?requiredFeature ?requiredLevel
       ?candidateLevel ?requirementStatus
WHERE {
  VALUES ?assessment { af:cardCarrotCutAssessment }

  ?assessment af:hasCandidate ?candidate ;
              af:hasTarget ?target ;
              af:hasAction ?action .

  ?action af:hasRequirement ?requirement .

  ?target af:hasFeatureValue ?targetFeatureValue .
  ?targetFeatureValue af:hasFeatureType ?targetFeature ;
                      af:hasLevel ?targetLevel .

  ?mapping a af:RequirementMapping ;
           af:usesTargetFeatureType ?targetFeature ;
           af:usesTargetLevel ?targetLevel ;
           af:affectsRequirement ?requirement ;
           af:specifiesRequiredLevel ?requiredLevel .

  ?requirement af:concernsFeature ?requiredFeature .

  OPTIONAL {
    ?candidate af:hasFeatureValue ?candidateFeatureValue .
    ?candidateFeatureValue af:hasFeatureType ?requiredFeature ;
                           af:hasLevel ?candidateLevel .
  }

  BIND(
    IF(!BOUND(?candidateLevel),
       "Insufficient information",
       IF(?candidateLevel = ?requiredLevel,
          "Satisfied",
          "NotSatisfied"))
    AS ?requirementStatus
  )
}
ORDER BY ?requirement
```

#### Result 1.2: Expected requirement matches

| Requirement | Required feature | Required level | Candidate level | Status |
|---|---|---|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | Satisfied |
| `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | Satisfied |

Both rows refer to `af:cardCandidate`, `af:carrotTarget`, and `af:cut`, with target feature `af:hardness = af:high`. This query returns per-requirement statuses; it does not select `af:hasJudgment`.

### CQ2: Given the same carrot, which of a rigid plastic card, a rolling pin, a kitchen sponge, and a metal spatula satisfy the CUT requirements?

For the high-hardness carrot, the represented CUT requirements remain `af:edgeThickness = af:low` and `af:rigidity = af:high`. The spatula has high rigidity but its edge thickness is explicitly unspecified in the supplied scenario.

#### Query 2.1: Retrieve inferred feasibility judgments for all four candidates

*Reasoning: OWL/SWRL inference (rules S1, S5, S6, S10, S4, S7, and S8).*

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate ?judgment
WHERE {
  ?assessment rdf:type af:Assessment .
  ?assessment af:hasTarget af:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
  FILTER (?candidate = af:cardCandidate || ?candidate = af:rollingPinCandidate ||
          ?candidate = af:spongeCandidate || ?candidate = af:spatulaCandidate)
}
ORDER BY ?candidate
```

#### Result 2.1: Expected judgments

| Candidate | Judgment |
|---|---|
| `af:cardCandidate` | `af:feasibleJudgment` |
| `af:rollingPinCandidate` | `af:infeasibleJudgment` |
| `af:spatulaCandidate` | `af:insufficientInformationJudgment` |
| `af:spongeCandidate` | `af:infeasibleJudgment` |

Four rows are expected with HermiT-driven inference; the source expects no rows from an asserted-only query.

#### Query 2.2: Identify satisfied, conflicting, and unspecified requirements or features

*Reasoning: OWL/SWRL inference for satisfaction and conflict (S1, S5, S6); asserted RDF for the unspecified feature.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate ?satisfied ?conflicting ?missingFeature
WHERE {
  ?assessment af:hasTarget af:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  { ?assessment af:satisfiesRequirement ?satisfied . }
  UNION
  { ?assessment af:conflictsWithRequirement ?conflicting . }
  UNION
  { ?candidate af:hasUnspecifiedFeatureType ?missingFeature . }
  FILTER (?candidate = af:cardCandidate || ?candidate = af:rollingPinCandidate ||
          ?candidate = af:spongeCandidate || ?candidate = af:spatulaCandidate)
}
ORDER BY ?candidate ?satisfied ?conflicting
```

#### Result 2.2: Expected requirement explanations

| Candidate | Satisfied requirement | Conflicting requirement | Missing feature |
|---|---|---|---|
| `af:cardCandidate` | `af:cutEdgeThicknessRequirement` | — | — |
| `af:cardCandidate` | `af:cutRigidityRequirement` | — | — |
| `af:rollingPinCandidate` | — | `af:cutEdgeThicknessRequirement` | — |
| `af:rollingPinCandidate` | `af:cutRigidityRequirement` | — | — |
| `af:spatulaCandidate` | — | — | `af:edgeThickness` |
| `af:spatulaCandidate` | `af:cutRigidityRequirement` | — | — |
| `af:spongeCandidate` | — | `af:cutEdgeThicknessRequirement` | — |
| `af:spongeCandidate` | — | `af:cutRigidityRequirement` | — |

Eight rows are expected with inference. A dash denotes an unbound variable. In the asserted-only graph, the source expects only the spatula’s explicitly unspecified-feature row.

#### Query 2.3: Cross-check verdicts using asserted feature levels without a reasoner

*Reasoning: Asserted RDF with SPARQL `OPTIONAL`, `BIND`, aggregation, and conditional expressions.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate
       (GROUP_CONCAT(?detail; separator=" | ") AS ?explanation)
       (IF(SUM(?isConflict) > 0, "INFEASIBLE",
           IF(SUM(?isUnresolved) > 0, "INSUFFICIENT INFORMATION", "FEASIBLE")) AS ?verdict)
WHERE {
  VALUES ?candidate { af:cardCandidate af:rollingPinCandidate af:spongeCandidate af:spatulaCandidate }
  ?assessment af:hasCandidate ?candidate ;
              af:hasTarget af:carrotTarget ;
              af:hasAction ?action .
  af:carrotTarget af:hasFeatureValue ?targetValue .
  ?targetValue af:hasFeatureType ?targetFeature ;
               af:hasLevel ?targetLevel .
  ?action af:hasRequirement ?requirement .
  ?requirement af:concernsFeature ?feature .
  ?mapping af:affectsRequirement ?requirement ;
           af:usesTargetFeatureType ?targetFeature ;
           af:usesTargetLevel ?targetLevel ;
           af:specifiesRequiredLevel ?requiredLevel .
  OPTIONAL {
    ?candidate af:hasFeatureValue ?candidateValue .
    ?candidateValue af:hasFeatureType ?feature ;
                    af:hasLevel ?candidateLevel .
  }
  BIND(IF(!BOUND(?candidateLevel), 1, 0) AS ?isUnresolved)
  BIND(IF(BOUND(?candidateLevel) && ?candidateLevel != ?requiredLevel, 1, 0) AS ?isConflict)
  BIND(CONCAT(STRAFTER(STR(?feature), "physical-properties/"), ": required ",
              STRAFTER(STR(?requiredLevel), "physical-properties/"), ", has ",
              IF(BOUND(?candidateLevel), STRAFTER(STR(?candidateLevel), "physical-properties/"), "NO VALUE"),
              IF(?isUnresolved = 1, " (unresolved)", IF(?isConflict = 1, " (conflict)", " (satisfied)"))) AS ?detail)
}
GROUP BY ?candidate
ORDER BY ?candidate
```

#### Result 2.3: Expected computed verdicts

| Candidate | Explanation | Verdict |
|---|---|---|
| `af:cardCandidate` | Edge thickness: required low, has low (satisfied); rigidity: required high, has high (satisfied) | FEASIBLE |
| `af:rollingPinCandidate` | Edge thickness: required low, has high (conflict); rigidity: required high, has high (satisfied) | INFEASIBLE |
| `af:spatulaCandidate` | Edge thickness: required low, has NO VALUE (unresolved); rigidity: required high, has high (satisfied) | INSUFFICIENT INFORMATION |
| `af:spongeCandidate` | Edge thickness: required low, has high (conflict); rigidity: required high, has low (conflict) | INFEASIBLE |

The actual `?explanation` output concatenates the two feature descriptions using ` | `; their order may vary. The query computes a verdict using its SPARQL conditions, rather than retrieving an ontology-inferred `af:hasJudgment`.

#### Query 2.4: Validate inferred judgments across all carrot-cutting assessment individuals

*Reasoning: OWL/SWRL inference (rules S1 and S4–S10).*

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?judgment ?candidate
WHERE {
  ?assessment rdf:type af:Assessment .
  ?assessment af:hasTarget af:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
}
ORDER BY ?judgment ?candidate
```

#### Result 2.4: Expected judgments for all test individuals

| Judgment | Candidate |
|---|---|
| `af:feasibleJudgment` | `af:cardCandidate` |
| `af:feasibleJudgment` | `af:knifeCandidate` |
| `af:feasibleJudgment` | `af:scissorsCandidate` |
| `af:feasibleJudgment` | `af:testCandidateA` |
| `af:infeasibleJudgment` | `af:rollingPinCandidate` |
| `af:infeasibleJudgment` | `af:spongeCandidate` |
| `af:infeasibleJudgment` | `af:testCandidateB` |
| `af:insufficientInformationJudgment` | `af:spatulaCandidate` |
| `af:insufficientInformationJudgment` | `testCandidateC` (individuals namespace) |

Nine rows are expected with inference and none without it, according to the source. The source notes that `testCandidateC` has an IRI ending in `/individuals/testCandidateC`, rather than the displayed `af:` namespace.

### CQ3: Can a knife and scissors both meet the CUT requirements for the same carrot, and how does the ontology represent their different part structures?

These queries distinguish represented part relationships and OWL-derived structural classifications from the SWRL-based feasibility assessment.

#### Query 3.1: Retrieve represented parts and their asserted types

*Reasoning: Asserted RDF; no reasoner needed.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part
WHERE {
 ?candidate a af:WholeObject .
 ?candidate af:hasPart ?part .
 ?part a af:ObjectPart .
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate || ?candidate = af:testCandidate3 || ?candidate = af:testCandidate4)
}
ORDER BY ?candidate ?part
```

#### Result 3.1: Expected represented part counts

| Candidate | Represented parts |
|---|---:|
| `af:knifeCandidate` | 1 |
| `af:scissorsCandidate` | 2 |
| `af:testCandidate3` | 2 |
| `af:testCandidate4` | 2 |

Seven part rows are expected. The counts describe represented `af:hasPart` links, not exact OWL cardinality constraints.

#### Query 3.2: Retrieve explicitly distinct pairs of parts

*Reasoning: Asserted RDF; no reasoner needed.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?candidate ?part1 ?part2
WHERE {
 ?candidate af:hasPart ?part1 .
 ?candidate af:hasPart ?part2 .
 { ?part1 owl:differentFrom ?part2 . } UNION { ?part2 owl:differentFrom ?part1 . }
 FILTER (STR(?part1) < STR(?part2))
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate || ?candidate = af:testCandidate3 || ?candidate = af:testCandidate4)
}
ORDER BY ?candidate
```

#### Result 3.2: Expected distinct part pairs

| Candidate | Explicitly distinct pair |
|---|---|
| `af:scissorsCandidate` | `af:scissorsBlade1`, `af:scissorsBlade2` |
| `af:testCandidate3` | `af:testCandidate3Part1`, `af:testCandidate3Part2` |
| `af:testCandidate4` | `af:testCandidate4Part1`, `af:testCandidate4Part2` |

Three unordered pairs are expected. Distinct IRIs alone do not establish `owl:differentFrom`.

#### Query 3.3: Retrieve interactions between represented parts of each candidate

*Reasoning: Asserted RDF, with an additional reverse interaction under OWL inference.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?candidate ?part1 ?part2
WHERE {
 ?candidate af:hasPart ?part1 .
 ?candidate af:hasPart ?part2 .
 ?part1 af:interactsWith ?part2 .
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate || ?candidate = af:testCandidate3 || ?candidate = af:testCandidate4)
}
ORDER BY ?candidate ?part1 ?part2
```

#### Result 3.3: Expected part interactions

| Candidate | Part 1 | Part 2 | Availability |
|---|---|---|---|
| `af:scissorsCandidate` | `af:scissorsBlade1` | `af:scissorsBlade2` | Asserted |
| `af:scissorsCandidate` | `af:scissorsBlade2` | `af:scissorsBlade1` | Asserted |
| `af:testCandidate4` | `af:testCandidate4Part1` | `af:testCandidate4Part2` | Asserted |
| `af:testCandidate4` | `af:testCandidate4Part2` | `af:testCandidate4Part1` | Inferred |

The source expects three rows from asserted data and four with inference. No interaction row for `af:testCandidate3` does not establish that its parts cannot interact.

#### Query 3.4: Retrieve inferred structural classifications

*Reasoning: OWL DL inference; HermiT and a reasoner-aware query interface or exported inferred graph.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?candidate ?structureClass
WHERE {
 ?candidate a ?structureClass .
 FILTER (?structureClass = af:MultiPartObject || ?structureClass = af:InteractingPartObject)
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate || ?candidate = af:testCandidate3 || ?candidate = af:testCandidate4)
}
ORDER BY ?candidate ?structureClass
```

#### Result 3.4: Expected structural classes

| Candidate | Inferred structural class |
|---|---|
| `af:scissorsCandidate` | `af:MultiPartObject` |
| `af:scissorsCandidate` | `af:InteractingPartObject` |
| `af:testCandidate3` | `af:MultiPartObject` |
| `af:testCandidate4` | `af:MultiPartObject` |
| `af:testCandidate4` | `af:InteractingPartObject` |

Five rows are expected with inference, zero from the asserted-only graph. The missing knife row does not entail non-membership in either structural class.

#### Query 3.5: Retrieve inferred inverse part relationships

*Reasoning: OWL DL inference.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part
WHERE {
 ?candidate af:hasPart ?part .
 ?part af:isPartOf ?candidate .
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate || ?candidate = af:testCandidate3 || ?candidate = af:testCandidate4)
}
ORDER BY ?candidate ?part
```

#### Result 3.5: Expected inverse relationships

| Candidate | Expected `af:isPartOf` rows |
|---|---:|
| `af:knifeCandidate` | 1 |
| `af:scissorsCandidate` | 2 |
| `af:testCandidate3` | 2 |
| `af:testCandidate4` | 2 |

Seven inferred `af:isPartOf` rows correspond to seven represented `af:hasPart` links. The source expects zero rows without inference.

#### Query 3.6: Retrieve knife and scissors requirement satisfaction and feasibility

*Reasoning: OWL DL and SWRL inference.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?assessment ?requirement ?judgment
WHERE {
 ?assessment a af:Assessment .
 ?assessment af:hasCandidate ?candidate .
 ?assessment af:hasTarget af:carrotTarget .
 ?assessment af:hasAction af:cut .
 ?assessment af:satisfiesRequirement ?requirement .
 ?assessment af:hasJudgment ?judgment .
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate)
}
ORDER BY ?candidate ?requirement
```

#### Result 3.6: Expected feasible judgments

| Candidate | Satisfied requirement | Judgment |
|---|---|---|
| `af:knifeCandidate` | `af:cutEdgeThicknessRequirement` | `af:feasibleJudgment` |
| `af:knifeCandidate` | `af:cutRigidityRequirement` | `af:feasibleJudgment` |
| `af:scissorsCandidate` | `af:cutEdgeThicknessRequirement` | `af:feasibleJudgment` |
| `af:scissorsCandidate` | `af:cutRigidityRequirement` | `af:feasibleJudgment` |

Four rows are expected with inference; none without it. `testCandidate3` and `testCandidate4` are structural controls without assessment or feature-value data in the supplied source.

#### Query 3.7: Retrieve part-level feature matches against target-dependent CUT requirements

*Reasoning: Asserted RDF; no reasoner needed.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part ?requirement ?feature ?requiredLevel ?partLevel
WHERE {
 ?assessment af:hasCandidate ?candidate .
 ?assessment af:hasTarget af:carrotTarget .
 ?assessment af:hasAction af:cut .
 af:cut af:hasRequirement ?requirement .
 af:carrotTarget af:hasFeatureValue ?targetValue .
 ?targetValue af:hasFeatureType ?targetFeature .
 ?targetValue af:hasLevel ?targetLevel .
 ?mapping a af:RequirementMapping .
 ?mapping af:affectsRequirement ?requirement .
 ?mapping af:usesTargetFeatureType ?targetFeature .
 ?mapping af:usesTargetLevel ?targetLevel .
 ?mapping af:specifiesRequiredLevel ?requiredLevel .
 ?requirement af:concernsFeature ?feature .
 ?candidate af:hasPart ?part .
 ?part af:hasFeatureValue ?partValue .
 ?partValue af:hasFeatureType ?feature .
 ?partValue af:hasLevel ?partLevel .
 FILTER (?partLevel = ?requiredLevel)
 FILTER (?candidate = af:knifeCandidate || ?candidate = af:scissorsCandidate)
}
ORDER BY ?candidate ?part ?requirement
```

#### Result 3.7: Expected part-level matches

| Candidate | Represented part(s) | Matched requirements per part | Expected rows |
|---|---|---|---:|
| `af:knifeCandidate` | Knife blade | Edge thickness and rigidity | 2 |
| `af:scissorsCandidate` | Both scissors blades | Edge thickness and rigidity for each blade | 4 |

Six rows are expected in total. The feature-level matches do not by themselves assert an overall ontology feasibility judgment or require every part to match every requirement.

### CQ4: Why is the rigid plastic card returned as a qualifying candidate for cutting the carrot while the kitchen sponge is excluded?

The card is represented with low edge thickness and high rigidity; the sponge has high edge thickness and low rigidity. Both features are specified for both objects, so the difference concerns conflicts rather than missing information.

#### Query 4.1: Compare inferred requirement statuses and actual feature levels for card and sponge

*Reasoning: OWL DL and SWRL inference (S1, S5, S6, S4, S7), joined to asserted requirement mappings and feature levels.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate ?judgment ?satisfied ?conflicting ?feature ?requiredLevel ?candidateLevel
WHERE {
  ?assessment af:hasTarget af:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
  { ?assessment af:satisfiesRequirement ?satisfied .
    ?satisfied af:concernsFeature ?feature .
    ?mapping af:affectsRequirement ?satisfied . }
  UNION
  { ?assessment af:conflictsWithRequirement ?conflicting .
    ?conflicting af:concernsFeature ?feature .
    ?mapping af:affectsRequirement ?conflicting . }
  af:carrotTarget af:hasFeatureValue ?targetValue .
  ?targetValue af:hasFeatureType ?targetFeature .
  ?targetValue af:hasLevel ?targetLevel .
  ?mapping af:usesTargetFeatureType ?targetFeature .
  ?mapping af:usesTargetLevel ?targetLevel .
  ?mapping af:specifiesRequiredLevel ?requiredLevel .
  ?candidate af:hasFeatureValue ?candidateValue .
  ?candidateValue af:hasFeatureType ?feature .
  ?candidateValue af:hasLevel ?candidateLevel .
  FILTER (?candidate = af:cardCandidate || ?candidate = af:spongeCandidate)
}
ORDER BY ?candidate ?feature
```

#### Result 4.1: Expected requirement-by-requirement comparison

| Candidate | Judgment | Satisfied | Conflicting | Feature | Required level | Candidate level |
|---|---|---|---|---|---|---|
| `af:cardCandidate` | `af:feasibleJudgment` | `af:cutEdgeThicknessRequirement` | — | `af:edgeThickness` | `af:low` | `af:low` |
| `af:cardCandidate` | `af:feasibleJudgment` | `af:cutRigidityRequirement` | — | `af:rigidity` | `af:high` | `af:high` |
| `af:spongeCandidate` | `af:infeasibleJudgment` | — | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:high` |
| `af:spongeCandidate` | `af:infeasibleJudgment` | — | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:low` |

Four rows are expected with inference; zero rows without it. A dash indicates that the `?satisfied` or `?conflicting` variable is unbound for that row.

#### Query 4.2: Identify requirements satisfied by the card but violated by the sponge

*Reasoning: OWL DL and SWRL inference (S1, S5, S6).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?decidingRequirement ?feature
WHERE {
  af:cardCarrotCutAssessment af:satisfiesRequirement ?decidingRequirement .
  af:spongeCarrotCutAssessment af:conflictsWithRequirement ?decidingRequirement .
  ?decidingRequirement af:concernsFeature ?feature .
}
ORDER BY ?decidingRequirement
```

#### Result 4.2: Expected deciding requirements

| Deciding requirement | Feature |
|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` |
| `af:cutRigidityRequirement` | `af:rigidity` |

Both CUT requirements distinguish the card from the sponge. Two rows are expected with inference and no rows without it.



<!-- ## Value Retrieval Query for Visualization 

### Star Plot Code

We present a query below that is used to retrieve the central value, and upper and lower bounds for continuous characteristics of a study arm. The characteristics are those that overlap with the patient features that we gather for diabetic patients in NHANES, i.e. age, body mass index, systolic blood pressure, diastolic blood pressure, Hemoglobin A1C. This query is triggered in the faceted browser to generate the visualization.
This query can flexibly retrieve values for both mean +/- standard deviation, median and interquartile range representations with being agnostic of the expression of the characteristic. Also, if we were to constrain the query for values of other parameters, we would just included them in the filter clause. Hence, this query is a generalized faceted browser query.

To run the code, please follow the steps as below:

1. `cd study-cohort-ontology`
1. `python3 -m venv env`
1. `source env/bin/activate`
1. `pip install -r ../requirements.txt`
1. `python3 starplot.py`

The star plot code can be browsed at: [https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Code/starplot.py](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Code/starplot.py)

```sparql
PREFIX sco: <small><https://idea.tw.rpi.edu/projects/heals/studycohort/></small>
PREFIX resource: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX chear: <http://hadatac.org/ont/chear#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX stato: <http://purl.obolibrary.org/obo/STATO_>
PREFIX ncit: <http://purl.obolibrary.org/obo/NCIT_>

SELECT DISTINCT ?studyTitle ?propType ?lowerBound ?propVal ?upperBound
WHERE {
  ?study a ncit:C71104 .
  ?study dct:title ?studyTitle .
  ?study sio:hasParticipant ?studyArm .
  ?studyArm sio:hasAttribute | sio:hasProperty ?prop .
  {
    ?prop a ?propType .
    ?prop sio:hasAttribute ?attr .
    ?attr a sio:Mean .
    ?attr sio:hasValue ?propVal .
    ?prop sio:hasAttribute ?attr2 .
    ?attr2 a sio:StandardDeviation .
    ?attr2 sio:hasValue ?propVal2 .
    BIND((?propVal2  + ?propVal) AS ?upperBound) .
    BIND((?propVal  - ?propVal2) AS ?lowerBound) .
  }
  UNION
  {
    ?prop a ?propType .
    ?prop sio:hasAttribute ?attr .
    ?attr a sio:Median .
    ?attr sio:hasValue ?propVal .
    ?prop sio:hasAttribute ?attr2 .
    ?attr2 a stato:0000164 .
    ?prop sio:hasAttribute sio:MaximalValue .
    ?attr2 sio:hasValue ?upperBound .
    ?prop sio:hasAttribute sio:MinimalValue .
    ?attr2 sio:hasValue ?lowerBound .
  }
  FILTER  (
    ?propType IN (
      sio:Age,
      ncit:C64796,
      sco:SystolicBloodPressure,
      sco:DiastolicBloodPressure
    )
  ) .
}
``` -->
