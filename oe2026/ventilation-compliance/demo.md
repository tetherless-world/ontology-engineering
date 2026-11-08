---
layout: default
title: demo
---

[How to run](#how-to-run-the-queries) | [Test scenario](#test-scenario) | [Use case 1](#use-case-1--locating-the-systems-and-sensor-readings-that-relate-to-a-room) | [Use case 2](#use-case-2--verifying-the-ventilation-compliance-of-critical-care-rooms) | [Use case 3](#use-case-3--tracing-compliance-failures-to-hvac-systems-and-components) | [Coverage](#what-the-queries-cover)

## Demonstration and Queries

This page lists the SPARQL queries that answer the project's competency questions, the reasoning each one depends on, and the rows each returns over the test individuals. There are two competency questions per [use case](usecase), six in total. The queries are also available as a single file, [OE 9 Team HVCC SPARQL Queries.txt](OE%209%20Team%20HVCC%20SPARQL%20Queries.txt), and in the shared [Google document](https://docs.google.com/document/d/17PMngIgp1zkGrxAJy3VSjCbdqSPk6pXczj8IaPUhMn4/edit?usp=sharing).

A recurring theme: **most of the answer columns below are never asserted in the data.** Which system serves a room, whether a policy was satisfied, how a room's assessment is classed and which components are implicated are all worked out by the reasoner, as described on the [ontology page](ontology#how-the-ontology-works). Running the same queries without a reasoner returns no rows for CQ 1.1, 3.1 and 3.2, which is the intended demonstration rather than a fault.

## How to run the queries

1. Keep [ventilation-compliance.rdf](ventilation-compliance.rdf), [individuals.rdf](individuals.rdf) and [catalog-v001.xml](catalog-v001.xml) in one folder together with `files/imports/`, and open **individuals.rdf** in Protégé. It declares `owl:imports` on the ontology, so both files load.
2. Start the **Pellet** reasoner (Reasoner → Pellet → Start reasoner). HermiT will not work: it rejects the SWRL built-ins `swrlb:lessThan` and `swrlb:greaterThanOrEqual` that classify the policy assessments.
3. Run the queries in the **Snap SPARQL Query** tab, which evaluates against the reasoner so OWL entailments and SWRL conclusions are visible. Snap SPARQL supports a subset of SPARQL (no property paths, `VALUES`, `BIND`, `EXISTS`, aggregates or sub-queries); the queries below respect that. CQ 1.2 uses the imported `prov:generatedAtTime` property, which the strict Snap SPARQL parser rejects, so run that one in the built-in **SPARQL Query** tab with Pellet started.

All queries share these prefixes:

```sparql
PREFIX v:    <https://tw.rpi.edu/ontology-engineering/oe2026/ventilation-compliance/ventilation-compliance/>
PREFIX test: <https://tw.rpi.edu/ontology-engineering/oe2026/ventilation-compliance/test-individuals/>
PREFIX core: <https://w3id.org/rec/core/>
PREFIX qu:   <https://www.omg.org/spec/Commons/QuantitiesAndUnits/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
```

## Test scenario

The test individuals describe one ventilation test of three ICU rooms on 9 October 2026. Each reading keeps its value, unit and timestamp.

**Rooms and readings**

| Room | Outdoor air change rate | Relative humidity |
|---|---|---|
| ICU-01 (room 4E-12) | 1.4 ACH at 14:25 (M-0412, derived) | 45 %RH at 14:30 |
| ICU-02 | 2.6 ACH at 14:30 | 40 %RH at 14:30 |
| ICU-03 | 3.1 ACH at 14:30 | 50 %RH at 14:30 |

ICU-01 also has two raw airflow readings from sensor AF-412 (12.4 m³/h at 14:20 and 12.1 m³/h at 14:10), a supply airflow reading M-0411 at 14:25, and the derivation chain M-0412 ← M-0413 (outdoor air flow rate to room) ← M-0411 (supply air flow rate), M-0414 (outdoor air fraction) and V-ICU-01 (room volume).

**HVAC topology**

| System | Service components | Connected rooms |
|---|---|---|
| HVAC-3 | AHU-3 (with filter FL-3 as a nested part), supply duct SD-3, VAV box VAV-412, diffuser DF-412 | all connect to ICU-01 |
| HVAC-4 | VAV-421, VAV-431 | ICU-02, ICU-03 |

VAV-412, DF-412, SD-3 and FL-3 each act on the supply airflow reading M-0411. VAV-421 and VAV-431 act on the ACH readings of ICU-02 and ICU-03.

**Compliance policies** (CDC framework, applied to all three rooms; CDC *Environmental Infection Control* 2003, Appendix B, critical and intensive care)

| Policy | Kind | Bound |
|---|---|---|
| min outdoor air changes per hour (`P_ACH_min`) | minimum outdoor air changes per hour, min-bounded | ≥ 2.0 ACH |
| relative humidity range (`P_RH`) | relative humidity, range-bounded | 30 to 60 %RH |

Only these two of the six CDC policy kinds are instantiated; the other CDC requirements are outside this test.

## Use case 1 – Locating the systems and sensor readings that relate to a room

*Actor: system maintenance technician. A work order reports room 4E-12 as stuffy.*

### CQ 1.1 – Which building service systems and connected service components serve room 4E-12?

```sparql
SELECT DISTINCT ?roomName ?systemName ?componentName
WHERE {
  ?room rdf:type core:Room ;
        rdfs:label ?roomName .
  FILTER(CONTAINS(STR(?roomName), "4E-12"))

  ?component v:connectsTo ?room ;
             rdfs:label ?componentName .

  ?system v:hasServiceComponent ?component ;
          rdfs:label ?systemName ;
          rdf:type ?systemType .
  ?systemType rdfs:subClassOf v:BuildingServiceSystem .
}
```

**Reasoning needed.** OWL DL. The relation between a system and a room is not asserted anywhere in the individuals file; the property chain `hasServiceComponent ∘ connectsTo ⊑ servesRoom` derives it, and this query exposes the two halves of that chain side by side. Run in Snap SPARQL with Pellet started.

**Result (4 rows).** HVAC-4 is correctly absent because it serves ICU-02 and ICU-03, not 4E-12.

| roomName | systemName | componentName |
|---|---|---|
| ICU-01 (room 4E-12) | HVAC-3 | AHU-3 |
| ICU-01 (room 4E-12) | HVAC-3 | DF-412 |
| ICU-01 (room 4E-12) | HVAC-3 | SD-3 |
| ICU-01 (room 4E-12) | HVAC-3 | VAV-412 |

### CQ 1.2 – What is the complete compliance assessment history (standard, evaluated policy and overall status) for room 4E-12?

```sparql
SELECT DISTINCT ?roomName ?time ?standardName ?policyName ?complianceStatus
WHERE {
  ?room rdf:type core:Room ;
        rdfs:label ?roomName .
  FILTER(CONTAINS(STR(?roomName), "4E-12"))

  ?context v:forRoom ?room ;
           v:usesFramework ?standard ;
           v:usesMeasurement ?measurement .
  ?standard rdfs:label ?standardName .
  ?measurement prov:generatedAtTime ?time .

  ?assessment v:hasContext ?context ;
              rdf:type ?complianceStatus ;
              v:hasPolicyAssessment ?policyAssessment .
  FILTER(CONTAINS(STR(?complianceStatus), "ComplianceAssessment"))

  ?policyAssessment v:evaluatedPolicy ?policy .
  ?policy rdfs:label ?policyName .
}
```

**Reasoning needed.** OWL DL with SWRL. Not one compliance fact in this answer is asserted. Rules S1 to S7 classify each policy assessment as satisfied or unsatisfied, and the class definitions then classify the room-level assessment; here `A_ICU_01` is inferred to be a `PartiallySatisfiedComplianceAssessment`. The query carries no date filter because the individuals file records exactly one test; a second test day would make one necessary. Run in the built-in SPARQL Query tab with Pellet started.

**Result (8 rows).** Both the asserted class `ComplianceAssessment` and the inferred class `PartiallySatisfiedComplianceAssessment` appear, for each of the two measurement times and the two policies. Satisfied policies are included because the question asks for the full history.

| roomName | time | standardName | policyName | complianceStatus |
|---|---|---|---|---|
| ICU-01 (room 4E-12) | 2026-10-09T14:25:00 | CDC framework | min outdoor air changes per hour | v:ComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:25:00 | CDC framework | min outdoor air changes per hour | v:PartiallySatisfiedComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:25:00 | CDC framework | relative humidity range | v:ComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:25:00 | CDC framework | relative humidity range | v:PartiallySatisfiedComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:30:00 | CDC framework | min outdoor air changes per hour | v:ComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:30:00 | CDC framework | min outdoor air changes per hour | v:PartiallySatisfiedComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:30:00 | CDC framework | relative humidity range | v:ComplianceAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:30:00 | CDC framework | relative humidity range | v:PartiallySatisfiedComplianceAssessment |

## Use case 2 – Verifying the ventilation compliance of critical care rooms

*Actor: healthcare administrator or nurse, ahead of an infection-control review.*

### CQ 2.1 – Which ICU rooms met the CDC ventilation standard in the test on 9 October 2026?

```sparql
SELECT DISTINCT ?roomName ?time ?standardName ?policyName ?status
WHERE {
  ?assessment v:hasContext ?context .
  ?assessment v:hasPolicyAssessment ?pa .
  ?context v:forRoom ?room .
  ?context v:usesFramework ?standard .
  ?context v:usesMeasurement ?measurement .
  ?measurement v:isEvaluatedAt ?pa .
  ?measurement prov:generatedAtTime ?time .
  ?pa v:evaluatedPolicy ?policy .
  ?pa rdf:type ?status .
  ?room rdfs:label ?roomName .
  ?standard rdfs:label ?standardName .
  ?policy rdfs:label ?policyName .
  FILTER (
    ?status = v:SatisfiedPolicyAssessment ||
    ?status = v:UnsatisfiedPolicyAssessment ||
    ?status = v:UnknownPolicyAssessment
  )
}
ORDER BY ?roomName ?policyName
```

**Reasoning needed.** OWL DL with SWRL. Each `?status` is a SWRL conclusion: S2 fires for ICU-01's ACH (1.4 < 2.0), S1 for the other two rooms' ACH, and S5 for all three humidity readings. The query deliberately returns every tested policy, satisfied or not, with its room, time, standard and measurement, so that the compliance decision is explainable instead of filtering only for failures.

**Result (6 rows).** ICU-02 and ICU-03 met both tested policies; ICU-01 failed outdoor-air ACH but passed relative humidity.

| roomName | time | standardName | policyName | status |
|---|---|---|---|---|
| ICU-01 (room 4E-12) | 2026-10-09T14:25:00 | CDC framework | min outdoor air changes per hour | v:UnsatisfiedPolicyAssessment |
| ICU-01 (room 4E-12) | 2026-10-09T14:30:00 | CDC framework | relative humidity range | v:SatisfiedPolicyAssessment |
| ICU-02 | 2026-10-09T14:30:00 | CDC framework | min outdoor air changes per hour | v:SatisfiedPolicyAssessment |
| ICU-02 | 2026-10-09T14:30:00 | CDC framework | relative humidity range | v:SatisfiedPolicyAssessment |
| ICU-03 | 2026-10-09T14:30:00 | CDC framework | min outdoor air changes per hour | v:SatisfiedPolicyAssessment |
| ICU-03 | 2026-10-09T14:30:00 | CDC framework | relative humidity range | v:SatisfiedPolicyAssessment |

### CQ 2.2 – For room ICU-01, which compliance policies were not satisfied in that test, and which measurements show it?

```sparql
SELECT DISTINCT ?roomName ?policyName ?status ?measurementName
                ?actual ?minimum ?maximum ?unit ?time
WHERE {
  test:A_ICU_01 v:hasContext ?context ;
                v:hasPolicyAssessment ?pa .
  ?context v:forRoom ?room ;
           v:usesFramework ?standard ;
           v:usesMeasurement ?measurement .
  ?pa v:evaluatedPolicy ?policy ;
      rdf:type ?status .
  ?measurement v:isEvaluatedAt ?pa ;
               qu:hasQuantityValue ?quantity ;
               prov:generatedAtTime ?time ;
               rdfs:label ?measurementName .
  ?quantity qu:hasNumericValue ?actual ;
            qu:hasMeasurementUnit ?unit .
  ?room rdfs:label ?roomName .
  ?policy rdfs:label ?policyName .
  OPTIONAL {
    ?policy qu:hasLowerBound ?lower .
    ?lower qu:hasNumericValue ?minimum .
  }
  OPTIONAL {
    ?policy qu:hasUpperBound ?upper .
    ?upper qu:hasNumericValue ?maximum .
  }
  FILTER (
    ?status = v:SatisfiedPolicyAssessment ||
    ?status = v:UnsatisfiedPolicyAssessment ||
    ?status = v:UnknownPolicyAssessment
  )
}
ORDER BY ?policyName
```

**Reasoning needed.** The status of each policy assessment is inferred by the SWRL rules; everything else (measured value, unit, time, policy bounds) is retrieved from asserted triples. The `OPTIONAL` blocks keep whichever bounds a policy has, so min-bounded and range-bounded policies come back in the same shape. The satisfied humidity row is included on purpose so the failed policy can be read against a passing one.

**Result (2 rows).** The ACH policy is unsatisfied: 1.4 air changes per hour at 14:25, below the 2.0 lower bound. Relative humidity is satisfied at 45 %RH inside 30 to 60 %RH.

| roomName | policyName | status | measurementName | actual | minimum | maximum | unit | time |
|---|---|---|---|---|---|---|---|---|
| ICU-01 (room 4E-12) | min outdoor air changes per hour | v:UnsatisfiedPolicyAssessment | M-0412 | 1.4 | 2.0 | | v:airChangesPerHour | 2026-10-09T14:25:00 |
| ICU-01 (room 4E-12) | relative humidity range | v:SatisfiedPolicyAssessment | measurement ICU-01 RH | 45 | 30 | 60 | v:percentRelativeHumidity | 2026-10-09T14:30:00 |

## Use case 3 – Tracing compliance failures to HVAC systems and components

*Actor: system administrator responsible for the building systems, starting from the failed rooms of use case 2.*

### CQ 3.1 – Which HVAC system served the rooms that did not meet the standard in the test on 9 October 2026?

```sparql
SELECT DISTINCT ?systemName ?roomName ?outcome
WHERE {
  ?assessment rdf:type ?outcome .
  ?assessment v:hasContext ?context .
  FILTER ( ?outcome = v:PartiallySatisfiedComplianceAssessment ||
           ?outcome = v:UnsatisfiedComplianceAssessment )
  ?context v:forRoom ?room .
  ?system v:servesRoom ?room .
  ?system rdfs:label ?systemName .
  ?room rdfs:label ?roomName .
}
```

**Reasoning needed.** OWL DL with SWRL. Every column is inferred:

1. Rules S1 to S7 classify each policy assessment as satisfied or unsatisfied.
2. The OWL definition of `PartiallySatisfiedComplianceAssessment` (some satisfied *and* some unsatisfied policy assessment) classifies `A_ICU_01`. The closure axiom each assessment carries on `hasPolicyAssessment` is what makes the `only`-based sibling definitions usable.
3. The property chain `hasServiceComponent ∘ connectsTo ⊑ servesRoom` derives which system serves which room; `servesRoom` is asserted zero times in the individuals file.

Run in Snap SPARQL with Pellet started; the built-in tab without reasoning returns 0 rows.

**Result (1 row).** HVAC-4 is correctly absent: it serves ICU-02 and ICU-03, both of which classify as `SatisfiedComplianceAssessment`.

| systemName | roomName | outcome |
|---|---|---|
| HVAC-3 | ICU-01 (room 4E-12) | v:PartiallySatisfiedComplianceAssessment |

### CQ 3.2 – Which components of which HVAC system may be causing a room to fall short of the minimum outdoor air changes per hour policy?

The room is a variable rather than a fixed individual, so this answer joins directly onto the room column of CQ 1.1 and CQ 1.2.

```sparql
SELECT DISTINCT ?roomName ?policyName ?unitName ?componentName ?systemName
WHERE {
  ?assessment v:hasContext ?context .
  ?assessment v:hasPolicyAssessment ?pa .
  ?context v:forRoom ?room .
  ?room rdfs:label ?roomName .
  ?pa rdf:type v:UnsatisfiedPolicyAssessment .
  ?pa v:evaluatedPolicy ?policy .
  ?pa v:wasAssociatedWithComponent ?component .
  ?pa v:wasAssociatedWithSystem ?system .
  ?policy rdf:type v:MinimumAirChangesOfOutdoorAirPerHour .
  ?policy qu:hasLowerBound ?lb .
  ?policy rdfs:label ?policyName .
  ?lb qu:hasMeasurementUnit ?unit .
  ?unit rdfs:label ?unitName .
  ?component rdfs:label ?componentName .
  ?system rdfs:label ?systemName .
}
ORDER BY ?componentName
```

**Reasoning needed.** OWL DL with SWRL. Every column except the policy name is inferred, in five steps:

1. Rule S2 marks the policy assessment unsatisfied, because 1.4 ACH is below the 2.0 ACH lower bound. The rule binds one variable for both units, so a comparison across mismatched units cannot fire.
2. `prov:wasDerivedFrom` is a sub-property of the transitive `v:isTransitivelyDerivedFrom`, so the reasoner closes the provenance chain: M-0412 derives from M-0413, which derives from the supply airflow M-0411.
3. Rule S9 attaches every component that acts on any measurement in that chain to the policy assessment as `wasAssociatedWithComponent`.
4. `cmns-col:hasPart` is transitive and the inverse of `isPartOf`, and `hasServiceComponent` is a sub-property of it, so FL-3 is a part of HVAC-3 even though it is only asserted as part of AHU-3.
5. Rule S10 lifts the association from the component to the system containing it as `wasAssociatedWithSystem`, which is why the query needs no hard-coded reference to HVAC-3.

Run in Snap SPARQL with Pellet started; without the reasoner it returns 0 rows.

**Result (4 rows).** ICU-02 and ICU-03 are absent because they satisfied the policy, so S2 never fires for them and nothing is associated. AHU-3 is absent from the component column: it is part of HVAC-3 but acts on no measurement in the failing derivation chain. These are candidates linked to the failing evidence, not a confirmed cause (use case requirement R7): the system narrows the search for a facilities engineer, it does not diagnose.

| roomName | policyName | unitName | componentName | systemName |
|---|---|---|---|---|
| ICU-01 (room 4E-12) | min outdoor air changes per hour | air changes per hour | DF-412 | HVAC-3 |
| ICU-01 (room 4E-12) | min outdoor air changes per hour | air changes per hour | FL-3 | HVAC-3 |
| ICU-01 (room 4E-12) | min outdoor air changes per hour | air changes per hour | SD-3 | HVAC-3 |
| ICU-01 (room 4E-12) | min outdoor air changes per hour | air changes per hour | VAV-412 | HVAC-3 |

## What the queries cover

| Competency question | Inference exercised |
|---|---|
| CQ 1.1 | property chain `servesRoom`; sub-class reasoning over `BuildingServiceSystem` |
| CQ 1.2 | SWRL S1–S7; classification of the compliance assessment; measurement time via PROV-O |
| CQ 2.1 | SWRL S1–S7 over all rooms, min-bounded and range-bounded policies |
| CQ 2.2 | SWRL status plus asserted evidence: value, unit, bounds, time |
| CQ 3.1 | compliance classification with closure axioms, plus the `servesRoom` chain |
| CQ 3.2 | SWRL S2, S9 and S10; transitive derivation; transitive part-of |

The six questions use the room, service, measurement and compliance modules of the ontology. They do not exercise `Building`, `BuildingSystem`, `hasBuildingSystem`, `hasServiceSystem` or `hasRoom`, and they instantiate only two of the six CDC policy kinds; questions about a whole building, or about the other policies, follow the same pattern without new rules. Policy assessments that would be *unknown* (no measurement logged) are not produced in this release, because that requires the closed-world SHACL step described under [known limitations](ontology#known-limitations-and-open-points).
