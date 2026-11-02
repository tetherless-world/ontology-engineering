---
---

## Queries

The following SPARQL queries address the team's three competency questions. Results are **expected results specified in the supplied query source**, not independently executed outputs.

**Execution:** Load `OE_9_TeamAffordance_Individuals.rdf` with its import of `OE_9_TeamAffordance.rdf`. Queries marked **Asserted RDF** run in the standard SPARQL Query tab; queries marked **OWL/SWRL inference** require a reasoner-aware query environment or an exported graph containing inferred assertions.

### CQ1: Can a rigid plastic card cut a carrot, and why?

#### Query 1: Identify applicable CUT requirements and compare them with the card's features

*Reasoning: Asserted RDF.*

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

#### Result 1: Expected requirement matches

| Requirement | Required feature | Required level | Candidate level | Status |
|---|---|---|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | Satisfied |
| `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | Satisfied |

Both rows concern `af:cardCandidate`, `af:carrotTarget`, and `af:cut` under `af:hardness = af:high`. Both modeled requirements are satisfied; the query itself returns requirement statuses rather than an inferred feasibility judgment.

### CQ2: Which of a rigid plastic card, a rolling pin, and a kitchen sponge satisfy the CUT requirements for the same carrot?

#### Query 2.1: Retrieve inferred feasibility judgments for the three candidates

*Reasoning: OWL/SWRL inference.*

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
  FILTER (?candidate = af:cardCandidate || ?candidate = af:rollingPinCandidate || ?candidate = af:spongeCandidate)
}
ORDER BY ?candidate
```

#### Result 2.1: Expected judgments

| Candidate | Judgment |
|---|---|
| `af:cardCandidate` | `af:feasibleJudgment` |
| `af:rollingPinCandidate` | `af:infeasibleJudgment` |
| `af:spongeCandidate` | `af:infeasibleJudgment` |

#### Query 2.2: Retrieve satisfied and conflicting CUT requirements

*Reasoning: OWL/SWRL inference.*

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate ?satisfiedRequirement ?conflictingRequirement
WHERE {
  ?assessment af:hasTarget af:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  { ?assessment af:satisfiesRequirement ?satisfiedRequirement . }
  UNION
  { ?assessment af:conflictsWithRequirement ?conflictingRequirement . }
  FILTER (?candidate = af:cardCandidate || ?candidate = af:rollingPinCandidate || ?candidate = af:spongeCandidate)
}
ORDER BY ?candidate ?satisfiedRequirement ?conflictingRequirement
```

#### Result 2.2: Expected requirement explanations

| Candidate | Satisfied requirement | Conflicting requirement |
|---|---|---|
| `af:cardCandidate` | `af:cutEdgeThicknessRequirement` | — |
| `af:cardCandidate` | `af:cutRigidityRequirement` | — |
| `af:rollingPinCandidate` | — | `af:cutEdgeThicknessRequirement` |
| `af:rollingPinCandidate` | `af:cutRigidityRequirement` | — |
| `af:spongeCandidate` | — | `af:cutEdgeThicknessRequirement` |
| `af:spongeCandidate` | — | `af:cutRigidityRequirement` |

#### Query 2.3: Cross-check verdicts from asserted feature levels

*Reasoning: Asserted RDF, with SPARQL aggregation and conditional expressions.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?candidate
       (GROUP_CONCAT(?detail; separator=" | ") AS ?explanation)
       (IF(SUM(?isConflict) > 0, "INFEASIBLE",
           IF(SUM(?isUnresolved) > 0, "INSUFFICIENT INFORMATION", "FEASIBLE")) AS ?verdict)
WHERE {
  VALUES ?candidate { af:cardCandidate af:rollingPinCandidate af:spongeCandidate }
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

#### Result 2.3: Expected verdicts

| Candidate | Explanation | Verdict |
|---|---|---|
| `af:cardCandidate` | Edge thickness: low required, low present; rigidity: high required, high present | FEASIBLE |
| `af:rollingPinCandidate` | Edge thickness: low required, high present; rigidity: high required, high present | INFEASIBLE |
| `af:spongeCandidate` | Edge thickness: low required, high present; rigidity: high required, low present | INFEASIBLE |

The `?explanation` column includes the feature names and `(satisfied)` or `(conflict)` labels; concatenation order can vary.

#### Query 2.4: Validate inferred judgments across all carrot-cutting candidates

*Reasoning: OWL/SWRL inference.*

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

#### Result 2.4: Expected judgments for test individuals

| Judgment | Candidate |
|---|---|
| `af:feasibleJudgment` | `af:cardCandidate` |
| `af:feasibleJudgment` | `af:knifeCandidate` |
| `af:feasibleJudgment` | `af:scissorsCandidate` |
| `af:feasibleJudgment` | `af:testCandidateA` |
| `af:infeasibleJudgment` | `af:rollingPinCandidate` |
| `af:infeasibleJudgment` | `af:spongeCandidate` |
| `af:infeasibleJudgment` | `af:testCandidateB` |
| `af:insufficientInformationJudgment` | `af:testCandidateC` |

### CQ3: Can a knife and scissors both meet the CUT requirements for the same carrot, and how does the ontology represent their different part structures?

#### Query 3.1: Retrieve represented object parts

*Reasoning: Asserted RDF.*

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

Seven part rows in total. These are counts of represented parts, not exact OWL cardinalities.

#### Query 3.2: Retrieve explicitly distinct part pairs

*Reasoning: Asserted RDF.*

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

#### Query 3.3: Retrieve interactions between represented parts

*Reasoning: Asserted RDF; OWL inference also retrieves inverse interaction for `testCandidate4`.*

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

#### Result 3.3: Expected interactions

Three directed asserted rows: both directions between the scissors blades, plus `testCandidate4Part1` to `testCandidate4Part2`. With inference, a fourth row adds the reverse interaction for `testCandidate4`. No interaction row is expected for `testCandidate3`.

#### Query 3.4: Retrieve inferred structural classifications

*Reasoning: OWL inference.*

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

The absence of a knife row does not establish non-membership in those classes.

#### Query 3.5: Retrieve inferred inverse part relationships

*Reasoning: OWL inference.*

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

Seven `af:isPartOf` rows, corresponding to the seven represented `af:hasPart` links: one for the knife and two each for scissors, `testCandidate3`, and `testCandidate4`.

#### Query 3.6: Retrieve knife/scissors requirement satisfaction and feasibility

*Reasoning: OWL/SWRL inference.*

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

#### Query 3.7: Retrieve part-level feature matches against target-dependent CUT requirements

*Reasoning: Asserted RDF.*

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

Six rows: two matched requirements for the knife blade and two for each of the scissors blades. This establishes matching feature values at part level, not an inferred feasibility judgment by itself.


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
