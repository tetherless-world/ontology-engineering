---
layout: default
title: Demo
---

## Queries -- Assignment 12

The following SPARQL queries address the team's six competency questions (CQ1–CQ6). Results are **expected or team-reported results documented in the supplied OE12 query source**, not newly executed results in this Markdown conversion. This includes the two supplemental checks, Q2.5 and Q4.2.

**Execution:** Load `OE_12_TeamAffordance_Individuals.rdf` with its import of `OE_12_TeamAffordance.rdf` (the files should be in the same folder). **STANDARD / Asserted RDF** queries use Protégé’s regular SPARQL Query tab. **SNAP / OWL/SWRL inference** queries require HermiT 1.4.x to be started in the Snap SPARQL Query view, or a graph containing the relevant inferred assertions. Schema terms use `af:`; test individuals use `ind:`.

**OE12 notes:** Q2.5 computes an independent SPARQL-side cross-check rather than retrieving an inferred judgment. Q4.2 is a supplemental reasoner-dependent check, not independently re-executed in the source notes. CQ3 knife/scissors judgment, requirement-satisfaction, and scissors class assertions are cached in the Individuals file, so their presence in the standard tab is not proof of fresh reasoning.

### Earlier Queries
- [Assignment 11 queries](files/OE_11_TeamAffordance_Queries.txt)
- [Assignment 10 queries](files/OE_10_TeamAffordance_Queries.txt)
- [Assignment 9 queries](files/OE_9_TeamAffordance_Queries.txt)

### CQ1: Can a rigid plastic card cut a carrot, and why?

The high-hardness carrot requires low edge thickness and high rigidity for CUT. The card has both represented feature levels.

#### Query 1.1: Retrieve the card’s inferred feasibility judgment

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT; rules `InferSatisfiedRequirementFromMappedFeatures`, `ClassifyTwoCUTRequirementsSatisfied`, and `AssignFeasibleJudgment`).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?judgment
WHERE {
    ind:cardCarrotCutAssessment af:hasJudgment ?judgment .
}
```

#### Result 1.1: Expected judgment (1 row)

| Judgment |
|---|
| `ind:feasibleJudgment` |

In the STANDARD tab without inferred triples, no row is expected: `hasJudgment` is inferred.

#### Query 1.2: Compare the card’s features with target-dependent CUT requirements

*Reasoning: Asserted RDF (STANDARD; no reasoner needed).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?requirement ?requiredFeature ?requiredLevel ?candidateLevel
WHERE {
  ind:cardCarrotCutAssessment af:hasCandidate ?candidate ;
                              af:hasTarget ?target ;
                              af:hasAction ?action .

  ?action af:hasRequirement ?requirement .

  ?target af:hasFeatureValue ?targetFV .
  ?targetFV af:hasFeatureType ?targetFeature ;
            af:hasLevel ?targetLevel .

  ?mapping af:usesTargetFeatureType ?targetFeature ;
           af:usesTargetLevel ?targetLevel ;
           af:affectsRequirement ?requirement ;
           af:specifiesRequiredLevel ?requiredLevel .

  ?requirement af:concernsFeature ?requiredFeature .

  OPTIONAL {
    ?candidate af:hasFeatureValue ?candidateFV .
    ?candidateFV af:hasFeatureType ?requiredFeature ;
                 af:hasLevel ?candidateLevel .
  }
}
ORDER BY ?requirement
```

#### Result 1.2: Expected feature matches (2 rows)

| Requirement | Required feature | Required level | Candidate level |
|---|---|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |

Both rows concern `ind:cardCandidate`, `ind:carrotTarget`, and `af:cut` with target condition `af:hardness = af:high`. The query reports levels; it does not itself return a feasibility judgment.

### CQ2: Which of a rigid plastic card, rolling pin, kitchen sponge, and metal spatula satisfy the CUT requirements for the same carrot?

For the high-hardness carrot, the modeled CUT requirements are low edge thickness and high rigidity. The metal spatula has an explicitly unspecified edge-thickness value.

#### Query 2.1: Retrieve inferred feasibility judgments for four candidates

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?candidate ?judgment
WHERE {
  ?assessment af:hasTarget ind:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
  FILTER (?candidate = ind:cardCandidate || ?candidate = ind:rollingPinCandidate ||
          ?candidate = ind:spongeCandidate || ?candidate = ind:spatulaCandidate)
}
ORDER BY ?candidate
```

#### Result 2.1: Expected judgments (4 rows)

| Candidate | Judgment |
|---|---|
| `ind:cardCandidate` | `ind:feasibleJudgment` |
| `ind:rollingPinCandidate` | `ind:infeasibleJudgment` |
| `ind:spatulaCandidate` | `ind:insufficientInformationJudgment` |
| `ind:spongeCandidate` | `ind:infeasibleJudgment` |

Without inference, the STANDARD tab is expected to return no rows for this query.

#### Query 2.2: Identify satisfied, conflicting, and unresolved CUT requirements

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?candidate ?satisfied ?conflicting ?unresolved
WHERE {
  ?assessment af:hasTarget ind:carrotTarget .
  ?assessment af:hasCandidate ?candidate .
  { ?assessment af:satisfiesRequirement ?satisfied . }
  UNION
  { ?assessment af:conflictsWithRequirement ?conflicting . }
  UNION
  { ?assessment af:hasUnresolvedRequirement ?unresolved . }
  FILTER (?candidate = ind:cardCandidate || ?candidate = ind:rollingPinCandidate ||
          ?candidate = ind:spongeCandidate || ?candidate = ind:spatulaCandidate)
}
ORDER BY ?candidate
```

#### Result 2.2: Expected requirement outcomes (8 rows)

| Candidate | Satisfied | Conflicting | Unresolved |
|---|---|---|---|
| `ind:cardCandidate` | `af:cutEdgeThicknessRequirement` | — | — |
| `ind:cardCandidate` | `af:cutRigidityRequirement` | — | — |
| `ind:rollingPinCandidate` | `af:cutRigidityRequirement` | — | — |
| `ind:rollingPinCandidate` | — | `af:cutEdgeThicknessRequirement` | — |
| `ind:spatulaCandidate` | `af:cutRigidityRequirement` | — | — |
| `ind:spatulaCandidate` | — | — | `af:cutEdgeThicknessRequirement` |
| `ind:spongeCandidate` | — | `af:cutEdgeThicknessRequirement` | — |
| `ind:spongeCandidate` | — | `af:cutRigidityRequirement` | — |

A dash indicates an unbound query variable. Row ordering within each candidate may vary. Without inference, no rows are expected in the STANDARD tab.

#### Query 2.3: Retrieve required versus actual candidate feature levels

*Reasoning: Asserted RDF (STANDARD; `OPTIONAL` retains unspecified candidate values).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?candidate ?feature ?requiredLevel ?candidateLevel
WHERE {
  ?assessment af:hasTarget ind:carrotTarget .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasAction ?action .
  ?action af:hasRequirement ?requirement .
  ?requirement af:concernsFeature ?feature .
  ind:carrotTarget af:hasFeatureValue ?targetValue .
  ?targetValue af:hasFeatureType ?targetFeature .
  ?targetValue af:hasLevel ?targetLevel .
  ?mapping af:affectsRequirement ?requirement .
  ?mapping af:usesTargetFeatureType ?targetFeature .
  ?mapping af:usesTargetLevel ?targetLevel .
  ?mapping af:specifiesRequiredLevel ?requiredLevel .
  OPTIONAL {
    ?candidate af:hasFeatureValue ?candidateValue .
    ?candidateValue af:hasFeatureType ?feature .
    ?candidateValue af:hasLevel ?candidateLevel .
  }
  FILTER (?candidate = ind:cardCandidate || ?candidate = ind:rollingPinCandidate ||
          ?candidate = ind:spongeCandidate || ?candidate = ind:spatulaCandidate)
}
ORDER BY ?candidate ?feature
```

#### Result 2.3: Expected feature-level comparisons (8 rows)

| Candidate | Feature | Required level | Candidate level |
|---|---|---|---|
| `ind:cardCandidate` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:cardCandidate` | `af:rigidity` | `af:high` | `af:high` |
| `ind:rollingPinCandidate` | `af:edgeThickness` | `af:low` | `af:high` |
| `ind:rollingPinCandidate` | `af:rigidity` | `af:high` | `af:high` |
| `ind:spatulaCandidate` | `af:edgeThickness` | `af:low` | — |
| `ind:spatulaCandidate` | `af:rigidity` | `af:high` | `af:high` |
| `ind:spongeCandidate` | `af:edgeThickness` | `af:low` | `af:high` |
| `ind:spongeCandidate` | `af:rigidity` | `af:high` | `af:low` |

The spatula’s missing candidate level is an unbound value, not proof of a conflicting level.

#### Query 2.4: Regression-check judgments for all carrot-cutting candidates

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?judgment ?candidate
WHERE {
  ?assessment af:hasTarget ind:carrotTarget .
  ?assessment af:hasAction af:cut .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
}
ORDER BY ?judgment ?candidate
```

#### Result 2.4: Expected judgments, including test candidates (9 rows)

| Judgment | Candidate |
|---|---|
| `ind:feasibleJudgment` | `ind:cardCandidate` |
| `ind:feasibleJudgment` | `ind:knifeCandidate` |
| `ind:feasibleJudgment` | `ind:scissorsCandidate` |
| `ind:feasibleJudgment` | `ind:testCandidateA` |
| `ind:infeasibleJudgment` | `ind:rollingPinCandidate` |
| `ind:infeasibleJudgment` | `ind:spongeCandidate` |
| `ind:infeasibleJudgment` | `ind:testCandidateB` |
| `ind:insufficientInformationJudgment` | `ind:spatulaCandidate` |
| `ind:insufficientInformationJudgment` | `ind:testCandidateC` |

In the STANDARD tab, the two cached knife/scissors judgment rows can still appear; the other seven outcomes require reasoning in this query.

#### Query 2.5: Cross-check verdicts using asserted feature evidence (supplemental)

*Reasoning: Asserted RDF with SPARQL `OPTIONAL`, `BIND`, aggregation, and conditions (STANDARD; no reasoner).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?candidate
       (GROUP_CONCAT(?detail; separator=" | ") AS ?explanation)
       (IF(SUM(?isConflict) > 0, "INFEASIBLE",
           IF(SUM(?isUnmarked) > 0, "UNDETERMINED (UNMARKED)",
              IF(SUM(?isUnresolved) > 0, "INSUFFICIENT INFORMATION", "FEASIBLE"))) AS ?verdict)
WHERE {
  VALUES ?candidate {
    ind:cardCandidate ind:rollingPinCandidate ind:spongeCandidate ind:spatulaCandidate
  }
  ?assessment af:hasCandidate ?candidate ;
              af:hasTarget ind:carrotTarget ;
              af:hasAction ?action .
  ind:carrotTarget af:hasFeatureValue ?targetValue .
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
  OPTIONAL {
    ?candidate af:hasUnspecifiedFeatureType ?unspecifiedFeature .
    FILTER (?unspecifiedFeature = ?feature)
  }
  BIND(IF(!BOUND(?candidateLevel) && BOUND(?unspecifiedFeature), 1, 0) AS ?isUnresolved)
  BIND(IF(!BOUND(?candidateLevel) && !BOUND(?unspecifiedFeature), 1, 0) AS ?isUnmarked)
  BIND(IF(BOUND(?candidateLevel) && ?candidateLevel != ?requiredLevel, 1, 0) AS ?isConflict)
  BIND(CONCAT(STRAFTER(STR(?feature), "physical-properties/"), ": required ",
              STRAFTER(STR(?requiredLevel), "physical-properties/"), ", has ",
              IF(BOUND(?candidateLevel), STRAFTER(STR(?candidateLevel), "physical-properties/"), "NO VALUE"),
              IF(?isUnresolved = 1, " (explicitly unresolved)",
                 IF(?isUnmarked = 1, " (not represented)",
                    IF(?isConflict = 1, " (conflict)", " (satisfied)")))) AS ?detail)
}
GROUP BY ?candidate
ORDER BY ?candidate
```

#### Result 2.5: Expected cross-check verdicts (4 rows)

| Candidate | Computed verdict |
|---|---|
| `ind:cardCandidate` | FEASIBLE |
| `ind:rollingPinCandidate` | INFEASIBLE |
| `ind:spatulaCandidate` | INSUFFICIENT INFORMATION |
| `ind:spongeCandidate` | INFEASIBLE |

The query also returns an `?explanation` string concatenating each feature check (feature order may vary). It distinguishes a feature explicitly marked with `hasUnspecifiedFeatureType` from an unrepresented, unmarked feature, for which it returns `UNDETERMINED (UNMARKED)`. This check computes a SPARQL verdict; it does not assert a SWRL-inferred `hasJudgment` relationship.

### CQ3: Can a knife and scissors both meet the CUT requirements for the same carrot, and how does the ontology represent their different part structures?

Both are feasible under the modeled CUT requirements. The knife has one represented blade; scissors have two explicitly different interacting blades. CQ3-A and CQ3-B return the same six evidence rows through different SPARQL views.

#### Query 3.A: Combine cutting requirements, blade evidence, and part structures (regular SPARQL view)

*Reasoning: Asserted RDF (STANDARD, using cached CQ3 conclusions in the Individuals file).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT DISTINCT ?candidate ?assessment ?judgment ?requirement
                ?part ?feature ?requiredLevel ?partLevel
                ?interactingPart ?multiPartType ?interactingType
WHERE {
  ?assessment a af:Assessment ;
              af:hasCandidate ?candidate ;
              af:hasTarget ind:carrotTarget ;
              af:hasAction af:cut ;
              af:hasJudgment ?judgment ;
              af:satisfiesRequirement ?requirement .
  FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate)
  af:cut af:hasRequirement ?requirement .
  ?requirement af:concernsFeature ?feature .
  ind:carrotTarget af:hasFeatureValue ?targetValue .
  ?targetValue af:hasFeatureType ?targetFeature ; af:hasLevel ?targetLevel .
  ?mapping a af:RequirementMapping ;
           af:affectsRequirement ?requirement ;
           af:usesTargetFeatureType ?targetFeature ;
           af:usesTargetLevel ?targetLevel ;
           af:specifiesRequiredLevel ?requiredLevel .
  ?candidate af:hasPart ?part .
  ?part af:hasFeatureValue ?partValue .
  ?partValue af:hasFeatureType ?feature ; af:hasLevel ?partLevel .
  FILTER (?partLevel = ?requiredLevel)
  OPTIONAL {
    ?candidate af:hasPart ?interactingPart .
    ?part af:interactsWith ?interactingPart .
    FILTER (?part != ?interactingPart)
  }
  OPTIONAL {
    ?candidate a ?multiPartType .
    FILTER (?multiPartType = af:MultiPartObject)
  }
  OPTIONAL {
    ?candidate a ?interactingType .
    FILTER (?interactingType = af:InteractingPartObject)
  }
}
ORDER BY ?candidate ?part ?requirement
```

#### Result 3.A: Expected blade/requirement evidence (6 distinct rows)

| Candidate | Part | Requirement | Feature | Required level | Part level | Judgment | Interacting part | Multi-part type | Interacting type |
|---|---|---|---|---|---|---|---|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | `ind:feasibleJudgment` | — | — | — |
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | `ind:feasibleJudgment` | — | — | — |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | `ind:feasibleJudgment` | `ind:scissorsBlade2` | `af:MultiPartObject` | `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | `ind:feasibleJudgment` | `ind:scissorsBlade2` | `af:MultiPartObject` | `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | `ind:feasibleJudgment` | `ind:scissorsBlade1` | `af:MultiPartObject` | `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | `ind:feasibleJudgment` | `ind:scissorsBlade1` | `af:MultiPartObject` | `af:InteractingPartObject` |

The assessments are `ind:knifeCarrotCutAssessment` for the two knife rows and `ind:scissorsCarrotCutAssessment` for the four scissors rows. Structural columns for the knife are unbound. Cached conclusions allow these rows in the regular view without running a reasoner.

#### Query 3.B: Combine the same cutting and structural evidence using Snap SPARQL

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT DISTINCT ?candidate ?assessment ?judgment ?requirement
                ?part ?feature ?requiredLevel ?partLevel
                ?interactingPart ?multiPartType ?interactingType
WHERE {
  ?assessment a af:Assessment ;
              af:hasCandidate ?candidate ;
              af:hasTarget ind:carrotTarget ;
              af:hasAction af:cut ;
              af:hasJudgment ?judgment ;
              af:satisfiesRequirement ?requirement .
  FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate)
  af:cut af:hasRequirement ?requirement .
  ?requirement af:concernsFeature ?feature .
  ind:carrotTarget af:hasFeatureValue ?targetValue .
  ?targetValue af:hasFeatureType ?targetFeature ; af:hasLevel ?targetLevel .
  ?mapping a af:RequirementMapping ;
           af:affectsRequirement ?requirement ;
           af:usesTargetFeatureType ?targetFeature ;
           af:usesTargetLevel ?targetLevel ;
           af:specifiesRequiredLevel ?requiredLevel .
  ?candidate af:hasPart ?part .
  ?part af:hasFeatureValue ?partValue .
  ?partValue af:hasFeatureType ?feature ; af:hasLevel ?partLevel .
  FILTER (?partLevel = ?requiredLevel)
  OPTIONAL {
    {
    ?candidate af:hasPart ?interactingPart .
    ?part af:interactsWith ?interactingPart .
    FILTER (?part != ?interactingPart)
    }
    UNION
    {
    ?candidate af:hasPart ?interactingPart .
    ?part af:interactsWith ?interactingPart .
    FILTER (?part != ?interactingPart)
    }
  }
  OPTIONAL {
    {
    ?candidate a ?multiPartType .
    FILTER (?multiPartType = af:MultiPartObject)
    }
    UNION
    {
    ?candidate a ?multiPartType .
    FILTER (?multiPartType = af:MultiPartObject)
    }
  }
  OPTIONAL {
    {
    ?candidate a ?interactingType .
    FILTER (?interactingType = af:InteractingPartObject)
    }
    UNION
    {
    ?candidate a ?interactingType .
    FILTER (?interactingType = af:InteractingPartObject)
    }
  }
}
ORDER BY ?candidate ?part ?requirement
```

#### Result 3.B: Expected blade/requirement evidence (6 distinct rows)

| Candidate | Part | Requirement | Feature | Required level | Part level | Judgment | Interacting part | Multi-part type | Interacting type |
|---|---|---|---|---|---|---|---|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | `ind:feasibleJudgment` | — | — | — |
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | `ind:feasibleJudgment` | — | — | — |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | `ind:feasibleJudgment` | `ind:scissorsBlade2` | `af:MultiPartObject` | `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | `ind:feasibleJudgment` | `ind:scissorsBlade2` | `af:MultiPartObject` | `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` | `ind:feasibleJudgment` | `ind:scissorsBlade1` | `af:MultiPartObject` | `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` | `ind:feasibleJudgment` | `ind:scissorsBlade1` | `af:MultiPartObject` | `af:InteractingPartObject` |

This query produces the same bindings as CQ3-A. Its duplicated `UNION` branches inside `OPTIONAL` blocks work around a reported Snap SPARQL execution exception; `SELECT DISTINCT` eliminates duplicate intermediate matches. The extra branches do not provide additional evidence.

#### CQ3 diagnostic queries

The following checks isolate structural assertions, class inferences, inverse properties, and requirement evidence. Counts for asserted RDF versus reasoning reflect the OE12 source.

#### Query 3.1: Retrieve represented parts of the knife, scissors, and structural test objects

*Reasoning: Asserted RDF (STANDARD).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part
WHERE {
 ?candidate a af:WholeObject .
 ?candidate af:hasPart ?part .
 ?part a af:ObjectPart .
 FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate || ?candidate = ind:testCandidate3 || ?candidate = ind:testCandidate4)
}
ORDER BY ?candidate ?part
```

#### Result 3.1: Expected represented parts (7 rows)

| Candidate | Part |
|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` |
| `ind:testCandidate3` | `ind:testCandidate3Part1` |
| `ind:testCandidate3` | `ind:testCandidate3Part2` |
| `ind:testCandidate4` | `ind:testCandidate4Part1` |
| `ind:testCandidate4` | `ind:testCandidate4Part2` |

These counts are of represented parts, not exact OWL cardinalities.

#### Query 3.2: Retrieve explicitly distinct pairs of parts

*Reasoning: Asserted RDF (STANDARD; avoid a broad inferred `owl:differentFrom` query in SNAP).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part1 ?part2
WHERE {
 ?part1 owl:differentFrom ?part2 .
 ?candidate af:hasPart ?part1 .
 ?candidate af:hasPart ?part2 .
}
ORDER BY ?candidate
```

#### Result 3.2: Expected distinct pairs (3 rows)

| Candidate | Part 1 | Part 2 |
|---|---|---|
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `ind:scissorsBlade2` |
| `ind:testCandidate3` | `ind:testCandidate3Part1` | `ind:testCandidate3Part2` |
| `ind:testCandidate4` | `ind:testCandidate4Part1` | `ind:testCandidate4Part2` |

The source notes that different IRIs alone do not imply OWL inequality. This query starts from explicit `owl:differentFrom` triples to avoid the earlier expensive pattern.

#### Query 3.3: Retrieve interactions among represented parts of the same object

*Reasoning: Asserted RDF (STANDARD); OWL inference adds symmetric interactions in SNAP.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?candidate ?part1 ?part2
WHERE {
 ?candidate af:hasPart ?part1 .
 ?candidate af:hasPart ?part2 .
 ?part1 af:interactsWith ?part2 .
 FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate || ?candidate = ind:testCandidate3 || ?candidate = ind:testCandidate4)
}
ORDER BY ?candidate ?part1 ?part2
```

#### Result 3.3: Expected interactions (3 asserted / 4 with reasoning)

| Candidate | Part 1 | Interacts with part 2 | Evidence |
|---|---|---|---|
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `ind:scissorsBlade2` | Asserted |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `ind:scissorsBlade1` | Asserted |
| `ind:testCandidate4` | `ind:testCandidate4Part1` | `ind:testCandidate4Part2` | Asserted |
| `ind:testCandidate4` | `ind:testCandidate4Part2` | `ind:testCandidate4Part1` | Inferred |

The inferred fourth row follows from symmetry. No interaction row for `ind:testCandidate3` does not establish that its parts cannot interact.

#### Query 3.4: Retrieve multi-part and interacting-part structural classifications

*Reasoning: OWL 2 DL inference (SNAP with HermiT; two scissors rows are also cached assertions).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?candidate ?structureClass
WHERE {
 ?candidate a ?structureClass .
 FILTER (?structureClass = af:MultiPartObject || ?structureClass = af:InteractingPartObject)
 FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate || ?candidate = ind:testCandidate3 || ?candidate = ind:testCandidate4)
}
ORDER BY ?candidate ?structureClass
```

#### Result 3.4: Expected structural classes (2 asserted / 5 with reasoning)

| Candidate | Structural class | Evidence |
|---|---|---|
| `ind:scissorsCandidate` | `af:MultiPartObject` | Cached assertion |
| `ind:scissorsCandidate` | `af:InteractingPartObject` | Cached assertion |
| `ind:testCandidate3` | `af:MultiPartObject` | Inferred |
| `ind:testCandidate4` | `af:MultiPartObject` | Inferred |
| `ind:testCandidate4` | `af:InteractingPartObject` | Inferred |

No structural class row for the knife does not establish nonmembership under the open-world assumption.

#### Query 3.5: Retrieve inferred inverse part relationships

*Reasoning: OWL 2 DL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part
WHERE {
 ?candidate af:hasPart ?part .
 ?part af:isPartOf ?candidate .
 FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate || ?candidate = ind:testCandidate3 || ?candidate = ind:testCandidate4)
}
ORDER BY ?candidate ?part
```

#### Result 3.5: Expected inverse links (0 asserted / 7 with reasoning)

| Whole object | Part with inferred `isPartOf` |
|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` |
| `ind:testCandidate3` | `ind:testCandidate3Part1` |
| `ind:testCandidate3` | `ind:testCandidate3Part2` |
| `ind:testCandidate4` | `ind:testCandidate4Part1` |
| `ind:testCandidate4` | `ind:testCandidate4Part2` |

Each returned row confirms the represented `hasPart` link and inferred inverse `isPartOf`.

#### Query 3.6: Retrieve satisfied CUT requirements and judgments for knife and scissors

*Reasoning: OWL 2 DL/SWRL inference (SNAP); four corresponding assertions are cached for STANDARD.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?assessment ?requirement ?judgment
WHERE {
 ?assessment a af:Assessment .
 ?assessment af:hasCandidate ?candidate .
 ?assessment af:hasTarget ind:carrotTarget .
 ?assessment af:hasAction af:cut .
 ?assessment af:satisfiesRequirement ?requirement .
 ?assessment af:hasJudgment ?judgment .
 FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate)
}
ORDER BY ?candidate ?requirement
```

#### Result 3.6: Expected requirement satisfaction and judgments (4 rows)

| Candidate | Assessment | Satisfied requirement | Judgment |
|---|---|---|---|
| `ind:knifeCandidate` | `ind:knifeCarrotCutAssessment` | `af:cutEdgeThicknessRequirement` | `ind:feasibleJudgment` |
| `ind:knifeCandidate` | `ind:knifeCarrotCutAssessment` | `af:cutRigidityRequirement` | `ind:feasibleJudgment` |
| `ind:scissorsCandidate` | `ind:scissorsCarrotCutAssessment` | `af:cutEdgeThicknessRequirement` | `ind:feasibleJudgment` |
| `ind:scissorsCandidate` | `ind:scissorsCarrotCutAssessment` | `af:cutRigidityRequirement` | `ind:feasibleJudgment` |

The source reports the same four rows on the asserted graph because the judgments and satisfaction links were cached for CQ3.

#### Query 3.7: Match part-level blade feature values against required CUT levels

*Reasoning: Asserted RDF (STANDARD).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?candidate ?part ?requirement ?feature ?requiredLevel ?partLevel
WHERE {
 ?assessment af:hasCandidate ?candidate .
 ?assessment af:hasTarget ind:carrotTarget .
 ?assessment af:hasAction af:cut .
 af:cut af:hasRequirement ?requirement .
 ind:carrotTarget af:hasFeatureValue ?targetValue .
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
 FILTER (?candidate = ind:knifeCandidate || ?candidate = ind:scissorsCandidate)
}
ORDER BY ?candidate ?part ?requirement
```

#### Result 3.7: Expected part-level matches (6 rows)

| Candidate | Part | Requirement | Feature | Required level | Part level |
|---|---|---|---|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |

Six matches show blade-level feature evidence, not a complete proof trace for an inferred assessment judgment. OWL open-world semantics prevent inferring exact part counts from represented rows alone.

### CQ4: Why is the rigid plastic card returned as qualifying while the kitchen sponge is excluded?

The card satisfies both CUT requirements (low edge thickness, high rigidity); the sponge has both feature levels recorded, but each conflicts with the required level.

#### Query 4.1: Compare the inferred judgments and deciding requirement levels

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?candidate ?judgment ?satisfied ?conflicting ?feature ?requiredLevel ?candidateLevel
WHERE {
  ?assessment af:hasTarget ind:carrotTarget .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
  { ?assessment af:satisfiesRequirement ?satisfied .
    ?satisfied af:concernsFeature ?feature .
    ?mapping af:affectsRequirement ?satisfied . }
  UNION
  { ?assessment af:conflictsWithRequirement ?conflicting .
    ?conflicting af:concernsFeature ?feature .
    ?mapping af:affectsRequirement ?conflicting . }
  ?mapping af:specifiesRequiredLevel ?requiredLevel .
  ?candidate af:hasFeatureValue ?candidateValue .
  ?candidateValue af:hasFeatureType ?feature .
  ?candidateValue af:hasLevel ?candidateLevel .
  FILTER (?candidate = ind:cardCandidate || ?candidate = ind:spongeCandidate)
}
ORDER BY ?candidate ?feature
```

#### Result 4.1: Expected card-versus-sponge comparisons (4 rows)

| Candidate | Judgment | Satisfied | Conflicting | Feature | Required level | Candidate level |
|---|---|---|---|---|---|---|
| `ind:cardCandidate` | `ind:feasibleJudgment` | `af:cutEdgeThicknessRequirement` | — | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:cardCandidate` | `ind:feasibleJudgment` | `af:cutRigidityRequirement` | — | `af:rigidity` | `af:high` | `af:high` |
| `ind:spongeCandidate` | `ind:infeasibleJudgment` | — | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:high` |
| `ind:spongeCandidate` | `ind:infeasibleJudgment` | — | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:low` |

All card rows are satisfied and all sponge rows conflict. Without inferred triples, this query returns no rows in STANDARD.

#### Query 4.2: Identify the requirements satisfied by the card but conflicted by the sponge (supplemental)

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?decidingRequirement ?feature
WHERE {
  ind:cardCarrotCutAssessment af:satisfiesRequirement ?decidingRequirement .
  ind:spongeCarrotCutAssessment af:conflictsWithRequirement ?decidingRequirement .
  ?decidingRequirement af:concernsFeature ?feature .
}
ORDER BY ?decidingRequirement
```

#### Result 4.2: Expected deciding requirements (2 rows)

| Deciding requirement | Feature |
|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` |
| `af:cutRigidityRequirement` | `af:rigidity` |

This supplemental query depends on inferred requirement outcomes. The source records the expected rows but states it was not independently re-executed for OE12.

### CQ5: If a candidate’s rigidity is known but its edge thickness is not represented, can the system decide feasibility and identify the missing information?

A high-rigidity object with explicitly unspecified edge thickness cannot receive a final feasible/infeasible decision within the modeled requirements. The spatula and test candidate C exemplify this case.

#### Query 5.1: Identify insufficient-information candidates and their unresolved requirement

*Reasoning: OWL 2 DL/SWRL inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?candidate ?judgment ?satisfied ?unresolved ?missingFeature
WHERE {
  ?assessment af:hasTarget ind:carrotTarget .
  ?assessment af:hasCandidate ?candidate .
  ?assessment af:hasJudgment ?judgment .
  ?assessment af:hasUnresolvedRequirement ?unresolved .
  ?unresolved af:concernsFeature ?missingFeature .
  ?assessment af:satisfiesRequirement ?satisfied .
}
ORDER BY ?candidate
```

#### Result 5.1: Expected unresolved assessments (2 rows)

| Candidate | Judgment | Satisfied | Unresolved | Missing feature |
|---|---|---|---|---|
| `ind:spatulaCandidate` | `ind:insufficientInformationJudgment` | `af:cutRigidityRequirement` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` |
| `ind:testCandidateC` | `ind:insufficientInformationJudgment` | `af:cutRigidityRequirement` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` |

Without inference, no rows are expected in STANDARD because `hasJudgment` and `hasUnresolvedRequirement` are inferred.

### CQ6: What feature levels must a candidate have to cut a target with high hardness?

The asserted CUT requirement mappings specify low edge thickness and high rigidity for a target whose hardness level is high. This question can be answered without assessing any particular candidate.

#### Query 6.1: Retrieve target-dependent feature requirements and their mappings

*Reasoning: Asserted RDF (STANDARD; same two rows with SNAP).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?requirement ?feature ?requiredLevel ?mapping
WHERE {
  af:cut af:hasRequirement ?requirement .
  ?requirement af:concernsFeature ?feature .
  ?mapping af:affectsRequirement ?requirement .
  ?mapping af:usesTargetFeatureType af:hardness .
  ?mapping af:usesTargetLevel af:high .
  ?mapping af:specifiesRequiredLevel ?requiredLevel .
}
ORDER BY ?requirement
```

#### Result 6.1: Expected requirement mappings (2 rows)

| Requirement | Feature | Required level | Mapping |
|---|---|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:cutEdgeThicknessMapping` |
| `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:cutRigidityMapping` |

Only reusable individuals in the main ontology are involved in this query: `af:cut`, mappings, requirements, features, and levels.

#### Query 6.2: Retrieve mappings inferred to be `HighHardnessRigidityMapping`

*Reasoning: OWL 2 DL equivalent-class inference (SNAP with HermiT).*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>

SELECT ?mapping
WHERE {
  ?mapping a af:HighHardnessRigidityMapping .
}
ORDER BY ?mapping
```

#### Result 6.2: Expected inferred mapping classification (1 row)

| Mapping |
|---|
| `af:cutRigidityMapping` |

The `HighHardnessRigidityMapping` class membership is inferred rather than asserted; the STANDARD tab without inference returns no rows.




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
