---
layout: default
title: Getting Involved
---

## Maintenance Policy

Our maintenance policy focuses on keeping the Tracking Collective Judgment Formation (Tracking CJF) ontology, example individuals, and documentation available for continued use. Tracking CJF is a Fall 2026 Ontology Engineering course project at Rensselaer Polytechnic Institute. The team reviews feedback during the course, and future maintenance depends on contributor availability, with no fixed update schedule.

The [ontology page](ontology.html#ontologies) links to the current OE_12 schema and matching individuals. We document changes in Git history, the ontology headers, and the [version archive](ontology-versions.html#downloadable-versions). Each release has its own version IRI and RDF files, and earlier releases retain their matching import catalogs. The ontology namespace remains https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/.

Changes to terms and axioms receive team review against the [use case](usecase.html) and [curated terminology](termlist.html). Before releasing semantic changes, we check consistency with HermiT, validate state-assignment processing with SHACL, and rerun affected competency queries. Changes that alter an existing term's meaning receive a new term IRI or a documented migration. Superseded terms are marked with owl:deprecated and a replacement note where available. Earlier releases remain available at their archived URLs.

CJF class IRIs use UpperCamelCase, and CJF property IRIs use lowerCamelCase. The OE12 naming checks cover declarations in the schema and class and property use in both example files. Reused terms retain the identifiers assigned by their source vocabularies. The OOPS! P22 check also counts those identifiers, including SIO terms such as `SIO_000000` and `SIO_000206`.

Policy updated November 19, 2026. Project contributions are distributed under the [MIT License](license.html).

## Getting Involved

We welcome researchers, annotators, ontology developers, and other users interested in continuing or expanding Tracking CJF. Future work could include annotating more conversations, comparing state histories across discussions, extending the model to new deliberation settings, and developing additional competency questions.

Feedback on conversation moves, relationships, evidence, definitions, or inferred states helps us improve the model. Please identify the ontology version, relevant term or query, expected behavior, and a short conversation example or reproducible result. If you are interested in contributing or taking part in future maintenance, contact any team member using the email links below.

## Team Members

- [Devin De Silva](https://github.com/DevinDeSilva) · [TWC profile](https://tw.rpi.edu/person/devin-de-silva) · [desild@rpi.edu](mailto:desild@rpi.edu)
- [Tiziana Hernandez](https://github.com/thernandez7) · [TWC profile](https://tw.rpi.edu/person/tiziana-hernandez) · [hernat@rpi.edu](mailto:hernat@rpi.edu)
- [Matthew Lausev](https://github.com/mlau-hue) · [LinkedIn](https://www.linkedin.com/in/matthew-lausev-742691410) · [lausem@rpi.edu](mailto:lausem@rpi.edu)
- [Srihari Sridharan](https://github.com/sridhs3) · [TWC profile](https://tw.rpi.edu/person/srihari-sridharan) · [sridhs3@rpi.edu](mailto:sridhs3@rpi.edu)
