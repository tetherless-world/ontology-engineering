---
---

## Queries

The following SPARQL queries address the team’s **five competency questions (CQ1–CQ5)** in `OE_11_TeamAffordance_Queries.txt`. The results are transcribed from the source’s **final, checked submission**; the queries were **not independently re-executed** when preparing this Markdown version.

**Execution:** Load `OE_11_TeamAffordance_Individuals.rdf` together with its import of `OE_11_TeamAffordance.rdf` in Protégé 5.6.x. **STANDARD** means the ordinary SPARQL Query tab over asserted RDF. **SNAP** means Snap SPARQL Query with HermiT started to use OWL 2 DL and SWRL inference. If querying an exported graph instead, include the relevant inferred assertions. The `af:` namespace holds ontology terms; the `ind:` namespace holds test individuals, a change introduced in OE11.

**Note on inferred versus cached results:** CQ3’s updated Individuals file includes eight cached conclusions (two feasibility judgments, four satisfied-requirement assertions, and two structural class assertions). A result retrieved from those assertions alone is not proof of fresh inference; the source describes a separate HermiT test with the cached conclusions removed.

### Earlier Queries
- [Assignment 10 queries](files/OE_10_TeamAffordance_Queries.txt)
- [Assignment 9 queries](files/OE_9_TeamAffordance_Queries.txt)

### CQ1: Can a rigid plastic card cut a carrot, and why?

For the represented carrot, hardness is high. CUT therefore requires low edge thickness and high rigidity. The card has both feature levels and is assessed as feasible under the two modeled requirements.

#### Query 1.1: Can a rigid plastic card be used to cut a carrot?

*Reasoning: SNAP; OWL/SWRL inference via `InferSatisfiedRequirementFromMappedFeatures`, `ClassifyTwoCUTRequirementsSatisfied`, and `AssignFeasibleJudgment`.*

```sparql
PREFIX af: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2026/physical-properties/individuals/>

SELECT ?judgment
WHERE {
    ind:cardCarrotCutAssessment af:hasJudgment ?judgment .
}
```

#### Result 1.1: Card–carrot feasibility judgment

| Judgment |
|---|
| `ind:feasibleJudgment` |

One row is reported with HermiT. The standard asserted-only tab returns no rows because `af:hasJudgment` is inferred for this assessment.

#### Query 1.2: Why does the card satisfy the modeled CUT requirements?

*Reasoning: STANDARD; asserted RDF, no reasoner required.*

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

#### Result 1.2: Required and actual feature levels

| Requirement | Required feature | Required level | Candidate level |
|---|---|---|---|
| `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |

Both rows refer to candidate `ind:cardCandidate`, target `ind:carrotTarget`, action `af:cut`, and target condition `af:hardness = af:high`. This query retrieves comparisons and does not itself return the feasibility judgment.

### CQ2: Given the same carrot, which of a rigid plastic card, a rolling pin, a kitchen sponge, and a metal spatula can satisfy the CUT requirements?

For a carrot with high hardness, the modeled requirements are `af:edgeThickness = af:low` and `af:rigidity = af:high`. The card meets both; the rolling pin and sponge conflict with at least one; the spatula has no supplied edge-thickness value.

#### Query 2.1: Which of the four candidates can cut the carrot?

*Reasoning: SNAP; inferred feasibility judgments with HermiT.*

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

#### Result 2.1: Feasibility judgments for four candidates

| Candidate | Judgment |
|---|---|
| `ind:cardCandidate` | `ind:feasibleJudgment` |
| `ind:rollingPinCandidate` | `ind:infeasibleJudgment` |
| `ind:spatulaCandidate` | `ind:insufficientInformationJudgment` |
| `ind:spongeCandidate` | `ind:infeasibleJudgment` |

Four rows are reported with reasoning; the standard asserted-only tab returns no rows for these CQ2 assessments. **Only the card is classified feasible** among the four.

#### Query 2.2: Which CUT requirements does each object satisfy, conflict with, or leave unresolved?

*Reasoning: SNAP; reads inferred `af:satisfiesRequirement`, `af:conflictsWithRequirement`, and `af:hasUnresolvedRequirement`.*

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

#### Result 2.2: Requirement-level explanations

| Candidate | Satisfied (`?satisfied`) | Conflicting (`?conflicting`) | Unresolved (`?unresolved`) |
|---|---|---|---|
| `ind:cardCandidate` | `af:cutEdgeThicknessRequirement` | — | — |
| `ind:cardCandidate` | `af:cutRigidityRequirement` | — | — |
| `ind:rollingPinCandidate` | `af:cutRigidityRequirement` | — | — |
| `ind:rollingPinCandidate` | — | `af:cutEdgeThicknessRequirement` | — |
| `ind:spatulaCandidate` | `af:cutRigidityRequirement` | — | — |
| `ind:spatulaCandidate` | — | — | `af:cutEdgeThicknessRequirement` |
| `ind:spongeCandidate` | — | `af:cutEdgeThicknessRequirement` | — |
| `ind:spongeCandidate` | — | `af:cutRigidityRequirement` | — |

Eight rows are reported with HermiT; order within each candidate may vary. An em dash indicates an unbound variable. This rewritten OE11 query returns no rows in the standard tab.

#### Query 2.3: What feature levels does CUT require, and what levels are recorded for each object?

*Reasoning: STANDARD; asserted RDF with an `OPTIONAL` pattern to retain missing feature values.*

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

#### Result 2.3: Required levels versus represented candidate levels

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

Eight rows are reported without a reasoner. The spatula’s edge thickness is unbound, not asserted to be high or low. In OE11, this query no longer uses `CONCAT`, `BIND`, `IF`, or aggregation.

#### Query 2.4: What judgment does every object assessed against the carrot receive?

*Reasoning: SNAP for the complete inferred judgment set; regression check across all candidates.*

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

#### Result 2.4: Judgments including neutral-name test candidates

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

Nine rows are reported with HermiT. In the standard tab, only the two knife/scissors judgment rows appear, because the updated Individuals file also stores those conclusions as cached assertions.

### CQ3: Can a knife and a pair of scissors both meet the CUT requirements for the same carrot, and how does the ontology represent their different part structures?

Both knife and scissors meet the modeled CUT requirements through matching **blade-part** feature values. CQ3 provides two equivalent combined queries—one for the regular SPARQL view and one for Snap SPARQL with HermiT—plus seven smaller diagnostic queries. Structural columns are optional so that the knife remains in the results even though its structural class values are not returned.

#### Query 3-A: Combined assessment, blade-feature, interaction, and structural evidence (regular SPARQL view)

*Reasoning: STANDARD on the updated Individuals file with cached CQ3 assertions (or an asserted-plus-inferred graph).*

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

#### Result 3-A: Six combined evidence rows

| Candidate | Part | Feature / CUT requirement | Required / part level | Interacting part | Structural classes |
|---|---|---|---|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:edgeThickness` / `af:cutEdgeThicknessRequirement` | `af:low` / `af:low` | — | — |
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:rigidity` / `af:cutRigidityRequirement` | `af:high` / `af:high` | — | — |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:edgeThickness` / `af:cutEdgeThicknessRequirement` | `af:low` / `af:low` | `ind:scissorsBlade2` | `af:MultiPartObject`, `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:rigidity` / `af:cutRigidityRequirement` | `af:high` / `af:high` | `ind:scissorsBlade2` | `af:MultiPartObject`, `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:edgeThickness` / `af:cutEdgeThicknessRequirement` | `af:low` / `af:low` | `ind:scissorsBlade1` | `af:MultiPartObject`, `af:InteractingPartObject` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:rigidity` / `af:cutRigidityRequirement` | `af:high` / `af:high` | `ind:scissorsBlade1` | `af:MultiPartObject`, `af:InteractingPartObject` |

The actual query also selects `?assessment` and `?judgment`; **all six rows have `ind:feasibleJudgment`** and correspond to two assessments, not six independent assessments. Class names in the table represent two separate selected columns (`?multiPartType` and `?interactingType`). The original unmaterialized graph without inference returns no combined rows in the regular view.

#### Query 3-B: Combined assessment and structural evidence with Snap SPARQL and HermiT

*Reasoning: SNAP; OWL/SWRL inference, using a compatibility workaround for `OPTIONAL` patterns.*

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

#### Result 3-B: Same six combined evidence rows as Query 3-A

The source reports the same six rows and the same eleven selected variables as Query 3-A. This version intentionally repeats each optional match in two identical `UNION` branches to work around an `UnsupportedOperationException` in Snap SPARQL. `SELECT DISTINCT` removes the duplicate matches and **must be retained**. For a fresh inference test, remove the eight cached CQ3 assertions from a copy of the Individuals file before running HermiT.

#### Query 3.1: Which parts are represented for the knife, scissors, and two structural test candidates?

*Reasoning: STANDARD; asserted RDF.*

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

#### Result 3.1: Represented part counts

| Candidate | Represented parts |
|---|---|
| `ind:knifeCandidate` | 1 |
| `ind:scissorsCandidate` | 2 |
| `ind:testCandidate3` | 2 |
| `ind:testCandidate4` | 2 |

Seven part rows in total. These are counts of represented assertions, **not exact OWL cardinalities**.

#### Query 3.2: Which pairs of parts are explicitly stated to be different individuals?

*Reasoning: STANDARD; asserted `owl:differentFrom` links. This query was simplified in OE11 to avoid slow OWL pair enumeration.*

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

#### Result 3.2: Three explicitly distinct part pairs

| Candidate | Part 1 | Part 2 |
|---|---|---|
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `ind:scissorsBlade2` |
| `ind:testCandidate3` | `ind:testCandidate3Part1` | `ind:testCandidate3Part2` |
| `ind:testCandidate4` | `ind:testCandidate4Part1` | `ind:testCandidate4Part2` |

The source reports three rows. Different individual IRIs by themselves do not establish inequality in OWL. The source recommends the standard tab, **not** Snap SPARQL, for this check.

#### Query 3.3: Which represented parts of the same object interact with one another?

*Reasoning: Asserted RDF in STANDARD; OWL entailment in SNAP for inferred symmetric interactions.*

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

#### Result 3.3: Directed interaction links

| Mode | Directed interactions | Rows |
|---|---|---|
| Asserted | Both directions between the two scissors blades; `ind:testCandidate4Part1` → `ind:testCandidate4Part2` | 3 |
| With inference | The three asserted rows plus `ind:testCandidate4Part2` → `ind:testCandidate4Part1` | 4 |

No row for `ind:testCandidate3` is expected. That absence is not a proof of noninteraction under the open-world assumption.

#### Query 3.4: Which objects are inferred to be multi-part or interacting-part objects?

*Reasoning: SNAP; OWL DL classification. The two scissors class assertions are also cached in the updated Individuals file.*

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

#### Result 3.4: Inferred structural classifications

| Candidate | Structural class |
|---|---|
| `ind:scissorsCandidate` | `af:MultiPartObject` |
| `ind:scissorsCandidate` | `af:InteractingPartObject` |
| `ind:testCandidate3` | `af:MultiPartObject` |
| `ind:testCandidate4` | `af:MultiPartObject` |
| `ind:testCandidate4` | `af:InteractingPartObject` |

Five rows are reported with inference. The updated asserted-only file returns **two** cached scissors classification rows; the original unmaterialized file returned zero. A missing knife row does not imply nonmembership.

#### Query 3.5: For each represented part, is `isPartOf` inferred as the inverse of `hasPart`?

*Reasoning: SNAP; OWL DL inference of inverse properties.*

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

#### Result 3.5: Inferred inverse relationships

| Candidate | Number of `af:isPartOf` links |
|---|---|
| `ind:knifeCandidate` | 1 |
| `ind:scissorsCandidate` | 2 |
| `ind:testCandidate3` | 2 |
| `ind:testCandidate4` | 2 |

Seven inferred rows are reported, corresponding to the seven represented `af:hasPart` links. The standard tab returns no rows.

#### Query 3.6: Which CUT requirements do the knife and scissors satisfy, and what judgment does each receive?

*Reasoning: OWL/SWRL inference, or STANDARD on the updated file with cached CQ3 judgments and satisfaction links.*

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

#### Result 3.6: Requirement satisfaction and feasible judgments

| Candidate | Satisfied CUT requirement | Judgment |
|---|---|---|
| `ind:knifeCandidate` | `af:cutEdgeThicknessRequirement` | `ind:feasibleJudgment` |
| `ind:knifeCandidate` | `af:cutRigidityRequirement` | `ind:feasibleJudgment` |
| `ind:scissorsCandidate` | `af:cutEdgeThicknessRequirement` | `ind:feasibleJudgment` |
| `ind:scissorsCandidate` | `af:cutRigidityRequirement` | `ind:feasibleJudgment` |

Four rows are reported. The query also selects `?assessment`. The updated standard asserted-only file also yields four rows because the relevant results were cached; the original uncached file did not.

#### Query 3.7: Which blade feature values match the levels required to CUT the carrot?

*Reasoning: STANDARD; asserted part-level feature values and target-dependent requirement mappings.*

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

#### Result 3.7: Matching blade-part features

| Candidate | Part | Requirement | Feature | Required level | Part level |
|---|---|---|---|---|---|
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:knifeCandidate` | `ind:knifeBlade` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:scissorsCandidate` | `ind:scissorsBlade1` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:scissorsCandidate` | `ind:scissorsBlade2` | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:high` |

Six matching rows are reported: two for the knife blade and two for each scissors blade. These matches support part-level evidence; this query does not by itself infer a feasibility judgment.

**CQ3 interpretation:** Feasibility is relative to the two modeled CUT requirements. Neither a feasible judgment nor the part-level evidence constitutes an empirical cutting or safety claim. A represented knife blade does not entail that the knife has exactly one part under OWL’s open-world semantics.

### CQ4: Why is the rigid plastic card returned as a qualifying candidate while the kitchen sponge is excluded?

The card satisfies both CUT requirements; the sponge’s recorded feature values conflict with both. The sponge’s result is **infeasible**, not missing information.

#### Query 4.1: What is each object’s judgment, and which requirements explain the difference?

*Reasoning: SNAP; inferred judgment and requirement statuses joined to asserted feature levels.*

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

#### Result 4.1: Card versus sponge, requirement by requirement

| Candidate | Judgment | Satisfied | Conflicting | Feature | Required level | Candidate level |
|---|---|---|---|---|---|---|
| `ind:cardCandidate` | `ind:feasibleJudgment` | `af:cutEdgeThicknessRequirement` | — | `af:edgeThickness` | `af:low` | `af:low` |
| `ind:cardCandidate` | `ind:feasibleJudgment` | `af:cutRigidityRequirement` | — | `af:rigidity` | `af:high` | `af:high` |
| `ind:spongeCandidate` | `ind:infeasibleJudgment` | — | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` | `af:low` | `af:high` |
| `ind:spongeCandidate` | `ind:infeasibleJudgment` | — | `af:cutRigidityRequirement` | `af:rigidity` | `af:high` | `af:low` |

Four rows are reported with inference. Both CUT requirements distinguish the card from the sponge. In the standard tab, the source reports no rows.

### CQ5: If a candidate’s rigidity is known but its edge thickness is not represented, can the system decide whether it can cut the carrot, and what information is missing?

The modeled system cannot make a final feasible/infeasible decision for a candidate with high rigidity but unknown edge thickness. The remaining unresolved condition is the edge-thickness requirement; both the spatula and neutral-name test candidate C demonstrate the case.

#### Query 5.1: Which candidates have insufficient information, what do they satisfy, and which feature is missing?

*Reasoning: SNAP; inferred `af:hasJudgment`, `af:satisfiesRequirement`, and `af:hasUnresolvedRequirement`.*

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

#### Result 5.1: Insufficient-information cases

| Candidate | Judgment | Satisfied requirement | Unresolved requirement | Missing feature |
|---|---|---|---|---|
| `ind:spatulaCandidate` | `ind:insufficientInformationJudgment` | `af:cutRigidityRequirement` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` |
| `ind:testCandidateC` | `ind:insufficientInformationJudgment` | `af:cutRigidityRequirement` | `af:cutEdgeThicknessRequirement` | `af:edgeThickness` |

Two rows are reported with reasoning. The standard asserted-only tab returns none. **Insufficient information is not equivalent to infeasibility** in this model.



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
