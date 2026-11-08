---
layout: default
title: getting involved
---

[Maintenance Policy](#maintenance-policy) | [Planned Extensions](#planned-extensions) | [How to Contribute](#how-to-contribute) | [Contact](#contact)

## Maintenance Policy

CareAir was built as a class project, but the team intends to carry it past the end of the semester, and the modelling choices were made with later extension in mind (see the *extensibility* decision in the [use case](usecase)). The policy below is meant to keep the ontology usable by anyone who starts depending on it.

- **Stable identifiers.** The ontology IRI `https://tw.rpi.edu/ontology-engineering/oe2026/ventilation-compliance/ventilation-compliance/` and the IRIs of its terms will not change. Terms that are superseded will be deprecated with `owl:deprecated` and a pointer to their replacement rather than deleted, so existing data and queries keep resolving.
- **Versioning.** Each release carries an `owl:versionIRI` and a change note in the ontology header. Releases that break compatibility (a renamed property, a changed domain or range, a changed rule conclusion) will be published under a new version IRI, and the previous version will stay available, in the same way earlier use case, term list and presentation versions are kept under `archived/`.
- **Reused vocabularies are pinned.** The four imports (PROV-O 2013-04-30, SAREF4BLDG 2.1.1, RealEstateCore Core 3.3, OMG Commons Quantities and Units) are resolved to local copies through `catalog-v001.xml`, so a change upstream cannot silently change what the ontology entails. Upgrading an import is treated as a release.
- **Rules and axioms are tested against the individuals file.** Any change to the ontology must still return the expected rows for the six competency questions on the [demo page](demo) in Protégé with Pellet. New reasoning features come with a new competency question and expected result.
- **Documentation follows the ontology.** The [concept map and ontology page](ontology), the [terminology list](termlist) and the demo page are updated in the same change as the RDF, and every new term gets an `rdfs:label`, a `skos:definition` written to ISO 704 and a source in the term list's reference sheet.
- **Licence.** All resources are released under the [Apache 2.0 licence](license).

## Planned Extensions

The current release is deliberately the smallest version that completes the three use cases. The items below are the extensions already identified, roughly in the order the team expects to take them. Each one fits the existing policy and assessment pattern without changing the architecture, which is the point of having kept policies, measurements and assessments as separate modules.

**Reasoning and validation**

- **Unknown status under the closed world.** A policy assessment with no logged measurement should be classed `UnknownPolicyAssessment`, and a room with any unknown policy should never be reported as compliant. OWL cannot conclude this from an absence, so a SHACL (and SHACL-AF) validation step over each assessment context is planned; the `sh:` annotation properties are already declared in the ontology for it.
- **Mixed assessment states.** An assessment that mixes unsatisfied and unknown policy assessments currently falls into none of the four compliance classes. Defining the precedence between the states (unknown over partially satisfied, for instance) is the next modelling decision in the assessment module.
- **Unit conversion.** The SWRL rules only compare a measurement and a bound that share a unit. Adding declared conversions between, for example, m³/h and m³/s, or a pre-processing step that normalises units, would let a bound be matched against any sensor that reports the same quantity kind.

**Coverage of the domain**

- **The remaining CDC policies and other frameworks.** Only the minimum outdoor-air-change and relative-humidity policies are instantiated. The other four CDC policy kinds are modelled as classes and need instances, measurements and test rooms. ASHRAE 170 Table 7.1 can be added as a second `ComplianceFramework` with its own policies and room applicability without any new rule.
- **Clinical designation as a role.** Requirement R1 asks for the clinical function of a space to be a time-bounded role rather than a permanent class, so that re-designating a room (an ICU room becoming an airborne infection isolation room) changes which framework applies without rewriting the room. The present release types rooms directly.
- **Pressure relationships and adjacent areas.** The `neighbor` relation and the `recordedInNeighbor` chain are in place for the air-movement-relationship policy, which needs differential pressure readings between a room and its corridor. Test data and a worked competency question for it are the next step.
- **Additional space types.** Protective environment rooms, sterile processing and bronchoscopy rooms each add requirement kinds to the taxonomy without changing the architecture.

**Operation**

- **Live data.** Replace the hand-written test ABox with a building model exported from the DOE / PNNL prototype hospital (via ASHRAE 223P) and measurements logged from a sensor API, so the topology and readings in the graph come from the systems of record.
- **Nanopublication store and query service.** Publish each sensor reading and each assessment as a nanopublication with its provenance, and implement the retrieval and reasoning flows in the [architecture and activity diagrams](index#system-architecture), including the freshness policy for "latest" results.
- **Deferred triggers.** Scheduled re-evaluation (T2), measurement-driven re-evaluation when a reading crosses a bound (T3), and model-change re-evaluation when a room is re-designated or a new edition of a standard is adopted (T4) all need running infrastructure that the class project did not build.
- **Staleness window.** A measurement should only count as evidence for a bounded period after it was taken, and a sensor should carry an expected reporting frequency; both are deferred until measurements are collected rather than logged at request.
- **Explanation and a natural-language interface.** Render the evidence behind a verdict (measurement, bound, policy, components) as a human-readable explanation, and explore natural-language-to-SPARQL over the graph for the three actor groups.

Out of scope on principle, and not planned: actuation or control of equipment (the system must stay read-only and must never become a dependency of a life-safety loop), fault diagnosis that asserts a confirmed cause, and any patient data.

## How to Contribute

The ontology, test individuals, queries and this website live in the course repository on GitHub: [tetherless-world/ontology-engineering](https://github.com/tetherless-world/ontology-engineering), under `oe2026/ventilation-compliance`.

- **Report a problem or suggest a term.** Open an issue, or email the team, with the term or axiom concerned, the CDC or ASHRAE clause it comes from, and if possible a competency question that the change would answer.
- **Propose a change.** Fork the repository, edit `ventilation-compliance.rdf` in Protégé (the catalog file resolves the imports offline), add or update individuals and a query so the change is testable, confirm the six existing queries still return their expected rows with Pellet, update the term list and the ontology page, and open a pull request.
- **Contribute data.** Anonymised building topology (systems, components, connections, room volumes) and sensor logs from a healthcare facility would let the team validate the model beyond the prototype hospital. No patient data is accepted.
- **Reuse the ontology.** If you apply it to another facility or framework, tell us: the goal is for a new framework, room type or sensor to require only new data, not new rules, and reports of where that breaks down are the most useful feedback.

## Contact

Team HVCC, Ontologies (CSCI 4340 / 6340), Rensselaer Polytechnic Institute, Fall 2026.

- Ahosan Habib – <habiba5@rpi.edu>
- Nipun Deelaka – <pathin@rpi.edu>
- Andy Cheng – <cheng11@rpi.edu>
- Carina Liu – <liuc17@rpi.edu>

Advised by Dr. Deborah McGuinness and Ms. Elisa Kendall, with mentoring from Jade Franklin, Danielle Villa and Kelsey Rook.
