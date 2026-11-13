---
layout: default
title: getting involved
---

## Maintenance Policy

Our aim is that anything that refers to our ontology keeps working, and that every version of it stays available.

- **Stable IRIs.** The main ontology keeps the IRI `https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/`,
  which it has used since Assignment 8, and the individuals ontology keeps
  `https://tw.rpi.edu/ontology-engineering/oe2026/agentic-orchestration/agentic-orchestration-individuals/`. New
  versions do not change them.
- **Version information in the header.** Since version 4.1 (Assignment 11), the header of both ontologies gives the
  version number (`owl:versionInfo`), a version IRI made of the ontology IRI and the version number (`owl:versionIRI`,
  for example `.../agentic-orchestration/v4.1`), the version it replaces (`owl:priorVersion`), the date of the last
  change (`dct:modified`) and what changed (`skos:changeNote`). Each release updates all five.
- **Earlier versions stay online.** Earlier versions of the main ontology, the individuals and the queries are kept in
  the `archived` folder and linked from the [Concept Map & Ontology](ontology.html#ontology) page. The use case, term
  list and presentations pages, and the conceptual model section of the ontology page, link every earlier version as
  well. Recent versions of the use case, term list and conceptual model have a redlined copy that marks what changed.
- **Testing before release.** Before each release we check with Pellet and HermiT that the main ontology, and the main
  and individuals ontologies together, are consistent and have no unsatisfiable classes. We also run every query in the
  query file and compare its results with the expected answer, and we run the course hygiene check. The results go in a
  test log linked from the ontology page.
- **Making changes.** The whole team agrees on modeling changes, and instructor feedback on one version is addressed in
  the next. Every change, including a class or property that is renamed or removed, is listed in the change note of the
  release that makes it.

## Getting Involved

Our use case lists three directions for future work:

- **Personalized constraints:** extend the ontology to user-aware, personalized constraints.
- **Request parsing:** build the NLP parser that turns a user's request into the goals, information requirements and
  constraints that the ontology describes. In the current use case the NLP tool is a secondary actor, and its
  development is out of scope.
- **Explanations:** reuse the [Explanation Ontology](https://tetherless-world.github.io/explanation-ontology/) to
  explain why one orchestration plan was selected over the other candidate plans.

All of the project's files are in the
[agentic-orchestration branch](https://github.com/tetherless-world/ontology-engineering/tree/agentic-orchestration/oe2026/agentic-orchestration)
of the course repository on GitHub. If you are interested in contributing, or have other ideas or suggestions, please
contact us:

- Gia Oriana Santos, <santog@rpi.edu>
- Barbara Kotlan, <kotlab@rpi.edu>
- Jiaying (Michael) Wang, <wangj63@rpi.edu>
- Jialin (Gary) Fang, <fangj6@rpi.edu>
- Elioenai Lincon Guedes Alves, <guedee@rpi.edu>
