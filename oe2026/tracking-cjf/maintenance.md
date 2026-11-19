---
layout: default
title: Maintenance Policy
---

## Maintenance Policy

Tracking Collective Judgment Formation (Tracking CJF) is a Fall 2026 Ontology Engineering course project at Rensselaer Polytechnic Institute. Our maintenance policy focuses on keeping released ontologies, example individuals, and documentation available and making revisions traceable.

Policy updated November 19, 2026. The current ontology release is OE_12.

### Availability and Releases

The [ontology page](ontology.html#ontologies) links to the current schema and matching individuals. We retain earlier releases and their import catalogs in the [version archive](ontology-versions.html#downloadable-versions). The ontology namespace is `https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/`.

Each release has a version-specific ontology IRI and RDF filename. Its header records the release version, modification date, preceding version, license, copyright, and a link to this policy. We update the current download links and catalogs together so that the schema and individuals resolve to the same release.

### Changes and Compatibility

We record accepted changes in Git history and summarize release changes in the ontology headers and version history. Corrections to labels, definitions, examples, and documentation receive review against the use case and curated terminology.

Changes to classes, properties, state-transition axioms, or query behavior require review of their effects on existing annotations and competency-question results. We check RDF parsing and ontology consistency with HermiT, validate state-assignment processing with SHACL, and rerun affected queries before releasing semantic changes.

Changes that alter the meaning of an existing term receive a new term IRI or an explicitly documented migration. Superseded terms are marked with `owl:deprecated` and a replacement or migration note where one is available. Previous release files remain available at their archived paths.

### Maintenance After the Course

During the course, the team reviews feedback as part of its development work. After the course, maintenance depends on contributor availability, with no fixed update schedule. Users interested in continuing the project can contact the team to discuss contributions or future stewardship.

### Community Feedback

We welcome feedback from dialogue researchers, annotators, ontology developers, and users applying the model to new conversations. Useful contributions include additional annotated conversations, clearer definitions, new competency questions, and reports of unexpected inferred states or query results.

Please identify the ontology version, relevant term or query, expected behavior, and a short conversation example or reproducible result. Contact any team member through the email links below. The [Getting Involved page](gettinginvolved.html) provides further project and contact information.

- [Tiziana Hernandez](mailto:hernat@rpi.edu)
- [Devin De Silva](mailto:desild@rpi.edu)
- [Srihari Sridharan](mailto:sridhs3@rpi.edu)
- [Matthew Lausev](mailto:lausem@rpi.edu)

Project contributions are distributed under the [MIT License](license.html).
