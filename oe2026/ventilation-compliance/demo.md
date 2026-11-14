---
layout: default
title: demo
---

[How to run](#how-to-run-the-queries) | [Test scenario](#test-scenario) | [Use case 1](#use-case-1--locating-the-systems-and-sensor-readings-that-relate-to-a-room) | [Use case 2](#use-case-2--verifying-the-ventilation-compliance-of-critical-care-rooms) | [Use case 3](#use-case-3--tracing-compliance-failures-to-hvac-systems-and-components) | [Coverage](#what-the-queries-cover)

## Demonstration and Queries

This page lists the SPARQL queries that answer the project's competency questions, the reasoning each one depends on, and the rows each returns over the test individuals in [individuals copy.rdf](individuals%20copy.rdf). There are three questions per [use case](usecase).

The queries are deliberately short. They return individuals rather than their labels, which Protégé displays by name anyway. They name a fixed individual directly, such as `test:ICU_01`, instead of searching labels. And they ask for the one status class the question is about instead of filtering a list of classes. The original, longer versions of the first six questions are kept in [OE 9 Team HVCC SPARQL Queries.txt](OE%209%20Team%20HVCC%20SPARQL%20Queries.txt) and in the shared [Google document](https://docs.google.com/document/d/17PMngIgp1zkGrxAJy3VSjCbdqSPk6pXczj8IaPUhMn4/edit?usp=sharing).

**Most answers are never asserted in the data.** Which system serves a room, which readings were recorded in it, whether a policy was satisfied, how a room's assessment is classed and which components are implicated are all worked out by the reasoner, as described on the [ontology page](ontology#how-the-ontology-works). Without a reasoner, every query below except CQ 2.4 returns no rows.

**How the results were checked.** The rows below were produced by running each query with rdflib over the test data with its inferences materialised: an OWL-RL reasoner supplied the property chains, sub-properties, inverses and transitive closures, and the project's [reference implementation](code/careair/reference.py) supplied the SWRL rules S1 to S11 and the outcome classes that need the closure axioms. The earlier, longer versions of the ICU queries were validated in Protégé with Pellet; the shortened queries on the expanded data still need that confirmation.

## How to run the queries

1. Keep [ventilation-compliance.rdf](ventilation-compliance.rdf), [individuals copy.rdf](individuals%20copy.rdf) and [catalog-v001.xml](catalog-v001.xml) in one folder together with `files/imports/`, and open **individuals copy.rdf** in Protégé. It declares `owl:imports` on the ontology, so both files load.
2. Start the **Pellet** reasoner (Reasoner → Pellet → Start reasoner). HermiT will not work: it rejects the SWRL built-ins `swrlb:lessThan` and `swrlb:greaterThanOrEqual` that classify the policy assessments.
3. Run the queries in the **Snap SPARQL Query** tab, which evaluates against the reasoner so OWL entailments and SWRL conclusions are visible. Snap SPARQL supports a subset of SPARQL (no property paths, `VALUES`, `BIND`, `EXISTS`, aggregates or sub-queries), and the queries below stay within it. CQ 1.2 and CQ 2.2 read the imported `prov:generatedAtTime` property; if Snap SPARQL reports a signature error for it, remove the `?time` variable and its triple, and the rest of the answer is unchanged.

All queries share these prefixes:

```sparql
PREFIX v:    <https://tw.rpi.edu/ontology-engineering/oe2026/ventilation-compliance/>
PREFIX test: <https://tw.rpi.edu/ontology-engineering/oe2026/ventilation-compliance/test-individuals/>
PREFIX qu:   <https://www.omg.org/spec/Commons/QuantitiesAndUnits/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
```

## Test scenario

The test individuals describe ventilation tests of seven rooms on 9 October 2026. Each reading keeps its value, unit and timestamp. All policy bounds come from the CDC *Guidelines for Environmental Infection Control in Health-Care Facilities* (2003), Appendix B, Table B.2, with temperatures converted to °C; where that table gives no relative-humidity value, the ASHRAE 170 maximum of 60 %RH is used, and the source is recorded on each policy individual.

**The ICU scenario (one test, 14:25 to 14:30)**

| Room | Outdoor air change rate | Relative humidity |
|---|---|---|
| ICU-01 (room 4E-12) | 1.4 ACH at 14:25 (M-0412, derived) | 45 %RH at 14:30 |
| ICU-02 | 2.6 ACH at 14:30 | 40 %RH at 14:30 |
| ICU-03 | 3.1 ACH at 14:30 | 50 %RH at 14:30 |

ICU-01 also has two raw airflow readings from sensor AF-412 (12.4 m³/h at 14:20 and 12.1 m³/h at 14:10), a supply airflow reading M-0411 at 14:25, and the derivation chain M-0412 ← M-0413 (outdoor air flow rate to room) ← M-0411 (supply air flow rate), M-0414 (outdoor air fraction) and V-ICU-01 (room volume). HVAC-3 (AHU-3 with nested filter FL-3, supply duct SD-3, VAV-412, DF-412) serves ICU-01; HVAC-4 (VAV-421, VAV-431) serves ICU-02 and ICU-03. The ICU policies are a minimum of 2.0 outdoor ACH and a 30 to 60 %RH range.

**The expanded scenario (three tests: 08:00, 14:30, 20:00)**

| Room (type, volume) | System | Policies applied |
|---|---|---|
| OR-01 (operating room, 120 m³) | HVAC-5: AHU-5 (fan SF-5, filter FL-5, coils CC-5 and HC-5, outdoor-air damper OAD-5), SD-5, RD-5, VAV-204, DF-204, CTRL-5 | outdoor ACH ≥ 3; total ACH ≥ 15; RH 30 to 60 %; temperature 20 to 23 °C; air movement *out* (incoming transfer airflow ≤ −212 m³/h) |
| AII-01 (airborne infection isolation room, 45 m³) | HVAC-6: AHU-6 (SF-6, FL-6, CC-6, HC-6, OAD-6), SD-6, RD-6, VAV-620, DF-620, exhaust system EXR-6 (inlet EI-620, duct ED-6, fan EF-6, discharge OD-6), CTRL-6 | outdoor ACH ≥ 2; total ACH ≥ 12; air movement *in* (incoming transfer ≥ 212 m³/h); RH ≤ 60 %; temperature 21 to 24 °C |
| PE-01 (protective environment room, 45 m³) | HVAC-6 via VAV-630, DF-630, EI-630 | outdoor ACH ≥ 2; total ACH ≥ 12; air movement *out* (≤ −212 m³/h); RH ≤ 60 %; temperature 21 to 24 °C |
| PR-01 (patient room, 40 m³) | HVAC-6 via VAV-640, DF-640, EI-640 | outdoor ACH ≥ 2; total ACH ≥ 6; temperature 21 to 24 °C |
| corridor 4E (patient corridor) | none | no framework applies, so the room is never assessed |

Each room has supply, return, exhaust (except the operating room), temperature and humidity sensors; each air handler has outdoor-air and supply airflow sensors. The derived measurements (outdoor air fraction per air handler; outdoor airflow to room, outdoor and total air changes per hour, and incoming transfer airflow per room) are asserted in the file with their provenance: `prov:wasDerivedFrom` their inputs, `prov:wasGeneratedBy` a derivation run of the software agent `ALG_DERIVATION`, and a comment showing the calculation. In practice these individuals are created by a derivation algorithm, whose reference implementation is in [code/](code/README.md).

| Room | 08:00 | 14:30 | 20:00 |
|---|---|---|---|
| OR-01 | all five policies satisfied | **temperature 24.1 °C above 23 °C** | **AHU-5 outdoor-air reading missing: outdoor ACH cannot be derived, policy unknown**; other four satisfied |
| AII-01 | all satisfied | **exhaust fan degraded: incoming transfer 50 m³/h, below the 212 m³/h offset** | **outdoor ACH 1.6, below 2** |
| PE-01 | **humidity reading missing: policy unknown**; other four satisfied | all satisfied | **outdoor ACH 1.73, below 2** |
| PR-01 | all satisfied | all satisfied | **outdoor ACH 0.9, below 2** |

The three failures on AHU-6 at 20:00 share one cause in the data: its outdoor-air damper OAD-6 is partly closed, so the outdoor air fraction drops from 0.30 to 0.12. Nothing in the data says so; CQ 3.2 and 3.3 recover it through the derivation chain.

The two unknown cases differ in where the evidence went missing. In PE-01 the room's own humidity sensor did not answer. In OR-01 every room sensor answered, but the air handler's outdoor-air sensor did not, so no outdoor air change rate could be derived for the room. Both policy assessments are typed `UnknownPolicyAssessment` in the file; in practice that type comes from the closed-world SHACL check in [code/shacl/](code/shacl/unknown-policy-assessment.ttl), because OWL cannot conclude that a measurement is absent. The room-level verdicts are left to the reasoner.

## Use case 1 – Locating the systems and sensor readings that relate to a room

*Actor: system maintenance technician. A work order reports room 4E-12 (ICU-01) as stuffy.*

### CQ 1.1 – Which building service systems serve room 4E-12, and through which connected components?

```sparql
SELECT ?system ?component WHERE {
  ?system v:servesRoom test:ICU_01 ;
          v:hasServiceComponent ?component .
  ?component v:connectsTo test:ICU_01 .
}
ORDER BY ?component
```

**Reasoning.** `servesRoom` is asserted nowhere; the property chain `hasServiceComponent ∘ connectsTo ⊑ servesRoom` derives it. The second and third triples return the components that support the conclusion.

**Result (4 rows).** HVAC-4 is correctly absent because it serves ICU-02 and ICU-03. The filter FL-3 also connects to the room, but it is part of AHU-3 rather than a direct service component, so the chain does not use it.

| system | component |
|---|---|
| test:HVAC_3 | test:AHU_3 |
| test:HVAC_3 | test:DF_412 |
| test:HVAC_3 | test:SD_3 |
| test:HVAC_3 | test:VAV_412 |

### CQ 1.2 – Which sensor readings have been recorded in room 4E-12, and which sensors produced them?

```sparql
SELECT ?sensor ?measurement ?value ?unit ?time WHERE {
  ?sensor v:measures ?measurement .
  ?measurement v:recordedIn test:ICU_01 ;
               qu:hasQuantityValue ?q ;
               prov:generatedAtTime ?time .
  ?q qu:hasNumericValue ?value ;
     qu:hasMeasurementUnit ?unit .
}
ORDER BY ?time
```

**Reasoning.** The readings are asserted with `measuredIn`; `measuredIn` is a sub-property of `recordedIn`, so the reasoner returns them for the more general relation. This question follows the use case document (version 10). The compliance history of a room, which an earlier version asked here, is now CQ 2.3.

**Result (2 rows).** Only logged readings with a value are returned; the gap between 14:10 and 14:20 means nobody requested a reading in between. The supply airflow reading M-0411 has no value recorded and is not listed.

| sensor | measurement | value | unit | time |
|---|---|---|---|---|
| test:AF_412 | test:M_0410b | 12.1 | v:cubicMetrePerHour | 2026-10-09T14:10:00 |
| test:AF_412 | test:M_0410a | 12.4 | v:cubicMetrePerHour | 2026-10-09T14:20:00 |

## Use case 2 – Verifying the ventilation compliance of critical care rooms

*Actor: healthcare administrator or nurse, ahead of an infection-control review.*

### CQ 2.1 – Which ICU rooms met the CDC ventilation standard in the test on 9 October 2026?

```sparql
SELECT ?room WHERE {
  ?assessment a v:SatisfiedComplianceAssessment ;
              v:hasContext ?context .
  ?context v:forRoom ?room .
  ?room a v:ICU .
}
ORDER BY ?room
```

**Reasoning.** SWRL rules S1 and S5 mark each policy assessment of ICU-02 and ICU-03 satisfied. With the closure axiom each assessment carries, the definition `hasPolicyAssessment only SatisfiedPolicyAssessment` then classifies the room's assessment as satisfied. No date filter is needed because the ICU rooms were tested once.

**Result (2 rows).** ICU-01 is absent: its outdoor-air policy failed, so its assessment is partially satisfied. CQ 2.2 shows why.

| room |
|---|
| test:ICU_02 |
| test:ICU_03 |

### CQ 2.2 – For room ICU-01, which compliance policies were not satisfied, and which measurements show it?

```sparql
SELECT ?policy ?measurement ?value ?unit ?lower ?upper ?time WHERE {
  test:A_ICU_01 v:hasPolicyAssessment ?pa .
  ?pa a v:UnsatisfiedPolicyAssessment ;
      v:evaluatedPolicy ?policy .
  ?measurement v:isEvaluatedAt ?pa ;
               qu:hasQuantityValue ?q ;
               prov:generatedAtTime ?time .
  ?q qu:hasNumericValue ?value ;
     qu:hasMeasurementUnit ?unit .
  OPTIONAL { ?policy qu:hasLowerBound ?lb . ?lb qu:hasNumericValue ?lower . }
  OPTIONAL { ?policy qu:hasUpperBound ?ub . ?ub qu:hasNumericValue ?upper . }
}
```

**Reasoning.** Rule S2 marks the outdoor-air policy assessment unsatisfied because 1.4 is below 2.0 and both are in air changes per hour. Everything else in the row is asserted evidence. The two `OPTIONAL` blocks return whichever bounds the policy has, so the same query works for min-, max- and range-bounded policies.

**Result (1 row).** The satisfied humidity policy is not returned, because the question asks only for policies that were not satisfied.

| policy | measurement | value | unit | lower | upper | time |
|---|---|---|---|---|---|---|
| test:P_ACH_min | test:M_0412 | 1.4 | v:airChangesPerHour | 2.0 | | 2026-10-09T14:25:00 |

### CQ 2.3 – How did the compliance of the operating room OR-01 change across the three tests?

```sparql
SELECT ?assessment ?outcome WHERE {
  ?assessment v:hasContext ?context ;
              a ?outcome .
  ?context v:forRoom test:OR_01 .
  ?outcome rdfs:subClassOf v:ComplianceAssessment .
  FILTER(?outcome != v:ComplianceAssessment)
}
ORDER BY ?assessment
```

**Reasoning.** The `rdfs:subClassOf` triple keeps only the outcome classes; the filter removes `ComplianceAssessment` itself, which the reasoner also returns as a sub-class of itself. At 08:00 all policies are satisfied. At 14:30 rule S7 marks the temperature policy unsatisfied, giving a partially satisfied assessment. At 20:00 the outdoor-air policy assessment is unknown, and the definition `hasPolicyAssessment some UnknownPolicyAssessment` makes the whole assessment unknown although its other four policies are satisfied.

**Result (3 rows).** One outcome per test, three different outcomes. The room is never reported satisfied on the strength of an absent reading.

| assessment | outcome |
|---|---|
| test:A_OR_01_0800 | v:SatisfiedComplianceAssessment |
| test:A_OR_01_1430 | v:PartiallySatisfiedComplianceAssessment |
| test:A_OR_01_2000 | v:UnknownComplianceAssessment |

### CQ 2.4 – Which policy assessments could not be decided because no measurement was available?

```sparql
SELECT ?room ?assessment ?policy WHERE {
  ?pa a v:UnknownPolicyAssessment ;
      v:evaluatedPolicy ?policy .
  ?assessment v:hasPolicyAssessment ?pa ;
              v:hasContext ?context .
  ?context v:forRoom ?room .
}
ORDER BY ?room
```

**Reasoning.** None in OWL: "no evidence" is a closed-world conclusion. The type is asserted in the test data; in practice the SHACL rule U1 in [code/shacl/unknown-policy-assessment.ttl](code/shacl/unknown-policy-assessment.ttl) asserts it for every policy assessment that evaluates no measurement. This is the use case's alternate flow (steps 4a to 4e): such rooms are reported as not verified rather than merged with the compliant ones.

**Result (2 rows).** OR-01 is the indirect case, where an air-handler reading was missing; PE-01 is the direct case, where the room's own sensor gave no reading.

| room | assessment | policy |
|---|---|---|
| test:OR_01 | test:A_OR_01_2000 | test:P_OR_OACH |
| test:PE_01 | test:A_PE_01_0800 | test:P_PE_RH |

## Use case 3 – Tracing compliance failures to HVAC systems and components

*Actor: system administrator responsible for the building systems, starting from the failed rooms of use case 2.*

### CQ 3.1 – Which HVAC systems served the rooms that did not meet the standard?

```sparql
SELECT DISTINCT ?system ?room WHERE {
  ?pa a v:UnsatisfiedPolicyAssessment .
  ?assessment v:hasPolicyAssessment ?pa ;
              v:hasContext ?context .
  ?context v:forRoom ?room .
  ?system v:servesRoom ?room .
}
ORDER BY ?system ?room
```

**Reasoning.** A room "did not meet the standard" when one of its policy assessments is unsatisfied (rules S1 to S7). The system comes from the same `servesRoom` property chain as CQ 1.1. Testing the policy assessment rather than the room-level class also catches an assessment that mixes unsatisfied and unknown results.

**Result (5 rows).** HVAC-4 is correctly absent: ICU-02 and ICU-03 satisfied every policy. Rooms whose only problem is an unknown policy, such as PE-01 at 08:00, do not add rows; PE-01 and OR-01 appear because of their failures at other times. `DISTINCT` collapses repeated tests to one row per room.

| system | room |
|---|---|
| test:HVAC_3 | test:ICU_01 |
| test:HVAC_5 | test:OR_01 |
| test:HVAC_6 | test:AII_01 |
| test:HVAC_6 | test:PE_01 |
| test:HVAC_6 | test:PR_01 |

### CQ 3.2 – Which components of which HVAC system may be causing a room to fall short of its minimum outdoor air changes per hour?

```sparql
SELECT ?room ?component ?system WHERE {
  ?pa a v:UnsatisfiedPolicyAssessment ;
      v:evaluatedPolicy ?policy ;
      v:wasAssociatedWithComponent ?component ;
      v:wasAssociatedWithSystem ?system .
  ?policy a v:MinimumAirChangesOfOutdoorAirPerHour .
  ?assessment v:hasPolicyAssessment ?pa ;
              v:hasContext ?context .
  ?context v:forRoom ?room .
}
ORDER BY ?room ?component
```

**Reasoning.** Every column except the room is inferred:

1. Rule S2 marks the outdoor-air policy assessment unsatisfied. The rule binds one variable for both units, so a comparison across mismatched units cannot fire.
2. `prov:wasDerivedFrom` is a sub-property of the transitive `v:isTransitivelyDerivedFrom`, so the reasoner closes each derivation chain back to the raw readings.
3. Rule S9 associates every component that acts on any measurement in that chain with the policy assessment.
4. `cmns-col:hasPart` is transitive, and `hasServiceComponent` is a sub-property of it, so a nested part such as FL-3 inside AHU-3 is a part of HVAC-3.
5. Rule S10 lifts the association from the component to the system containing it, so the query names no system.

**Result (22 rows).** ICU-02, ICU-03 and the satisfied tests are absent because rule S2 never fires for them. OR-01 is absent at 20:00 because that policy is unknown, not failed. AHU-3 and AHU-6 are absent because they act on no measurement in a failing chain. For the HVAC-6 rooms the chain runs back through the outdoor air fraction of AHU-6 to its own airflow readings, which is how the damper OAD-6, the fan SF-6 and the filter FL-6 appear for rooms they are not connected to. These are candidates linked to the failing evidence, not a confirmed cause (use case requirement R7).

| room | component | system |
|---|---|---|
| test:AII_01 | test:DF_620 | test:HVAC_6 |
| test:AII_01 | test:FL_6 | test:HVAC_6 |
| test:AII_01 | test:OAD_6 | test:HVAC_6 |
| test:AII_01 | test:SD_6 | test:HVAC_6 |
| test:AII_01 | test:SF_6 | test:HVAC_6 |
| test:AII_01 | test:VAV_620 | test:HVAC_6 |
| test:ICU_01 | test:DF_412 | test:HVAC_3 |
| test:ICU_01 | test:FL_3 | test:HVAC_3 |
| test:ICU_01 | test:SD_3 | test:HVAC_3 |
| test:ICU_01 | test:VAV_412 | test:HVAC_3 |
| test:PE_01 | test:DF_630 | test:HVAC_6 |
| test:PE_01 | test:FL_6 | test:HVAC_6 |
| test:PE_01 | test:OAD_6 | test:HVAC_6 |
| test:PE_01 | test:SD_6 | test:HVAC_6 |
| test:PE_01 | test:SF_6 | test:HVAC_6 |
| test:PE_01 | test:VAV_630 | test:HVAC_6 |
| test:PR_01 | test:DF_640 | test:HVAC_6 |
| test:PR_01 | test:FL_6 | test:HVAC_6 |
| test:PR_01 | test:OAD_6 | test:HVAC_6 |
| test:PR_01 | test:SD_6 | test:HVAC_6 |
| test:PR_01 | test:SF_6 | test:HVAC_6 |
| test:PR_01 | test:VAV_640 | test:HVAC_6 |

### CQ 3.3 – In which rooms and tests is the outdoor-air damper OAD-6 associated with a failed policy?

```sparql
SELECT ?room ?assessment ?policy WHERE {
  ?pa v:wasAssociatedWithComponent test:OAD_6 ;
      a v:UnsatisfiedPolicyAssessment ;
      v:evaluatedPolicy ?policy .
  ?assessment v:hasPolicyAssessment ?pa ;
              v:hasContext ?context .
  ?context v:forRoom ?room .
}
ORDER BY ?room
```

**Reasoning.** The same inferences as CQ 3.2, read from the component's side. OAD-6 is connected to none of the three rooms and is asserted only as part of AHU-6; it is reached through the derivation chain and rule S9.

**Result (3 rows).** One component appears behind the simultaneous failure of three rooms served by the same air handler, which is the signal a facilities engineer would act on first. The 08:00 and 14:30 tests are absent because the damper was open and no outdoor-air policy failed.

| room | assessment | policy |
|---|---|---|
| test:AII_01 | test:A_AII_01_2000 | test:P_AII_OACH |
| test:PE_01 | test:A_PE_01_2000 | test:P_PE_OACH |
| test:PR_01 | test:A_PR_01_2000 | test:P_PR_OACH |

## What the queries cover

| Competency question | Inference exercised |
|---|---|
| CQ 1.1 | property chain `servesRoom` |
| CQ 1.2 | sub-property `measuredIn ⊑ recordedIn`; measurement time via PROV-O |
| CQ 2.1 | SWRL S1 and S5; `only`-based outcome class with closure axioms |
| CQ 2.2 | SWRL S2 plus asserted evidence: value, unit, bounds, time |
| CQ 2.3 | three outcome classes over time, including unknown from a missing upstream reading |
| CQ 2.4 | closed-world unknown status (asserted; produced in practice by SHACL rule U1) |
| CQ 3.1 | SWRL S1 to S7 plus the `servesRoom` chain |
| CQ 3.2 | SWRL S2, S9 and S10; transitive derivation across a shared air handler; transitive part-of |
| CQ 3.3 | the same, read from the component's side |

The questions use the room, service, measurement and compliance modules of the ontology, five of the seven CDC policy kinds (outdoor and total air changes, air movement relationship, relative humidity, design temperature) in all three bound shapes, and five room types. They do not exercise `Building`, `BuildingSystem`, `hasBuildingSystem`, `hasServiceSystem` or `hasRoom`, nor the two yes/no CDC requirements (all air exhausted directly to outdoors, recirculation by room units), which have no measurement behind them yet. The corridor has no applicable framework and is correctly never assessed.
