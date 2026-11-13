---
layout: default
title: related work
---

## Related Work and References

These are the references of our [use case](usecase.html) (Section IX). When a definition in the ontology comes from one
of them, the ontology cites it with `dct:source`, and the [term list](termlist.html) gives the sources of every term.

### Ontologies and knowledge graphs for agentic AI

Our classes for capabilities, tools, constraints and workflow steps specialize those of AgentO, which we import (version
0.2). Mulang' et al. describe agent tools in a knowledge graph so that an agent can find the right tool among many; we
describe skills alongside tools, and the plans that combine them.

- I. O. Mulang’, J. Thaller, T. Trivedi, L. Heling, and F. Sasaki, "Representing agentic tools in knowledge graphs for
  structure-aware tool discovery under tool overload," in Proc. 2nd Workshop on Knowledge Graphs and Agentic Systems
  Interplay (NORA 2026), co-located with IJCAI-ECAI 2026, Bremen, Germany, 2026. [Online]. Available:
  <https://openreview.net/forum?id=7MVoH9Y3mi>
- A. Ekelhart, K. Kurniawan, F. J. Ekaputra, and E. Kiesling, "AgentO: An ontology for modeling agentic AI systems," in
  The Semantic Web: 23rd European Semantic Web Conference, ESWC 2026, Proceedings, Part II, Lecture Notes in Computer
  Science, vol. 16550, M. Acosta et al., Eds. Cham, Switzerland: Springer, 2026, pp. 298–320, doi:
  [10.1007/978-3-032-25159-6_16](https://doi.org/10.1007/978-3-032-25159-6_16).
- K. Kurniawan and F. J. Ekaputra, "AgentO: An ontology for modeling agentic AI systems," ontology release v0.2, Zenodo,
  Jan. 22, 2026, doi: [10.5281/zenodo.18342625](https://doi.org/10.5281/zenodo.18342625). [Online]. Available:
  <https://w3id.org/agentic-ai/onto>
- IBM Research, "AI Atlas Nexus: AI risk ontology." [Online]. Available: <https://ibm.github.io/ai-atlas-nexus/ontology/>

### Agent tools, skills and planning

Three of the four external servers in the use case are Model Context Protocol (MCP) servers; the fourth is a
command-line interface. SkillsBench is the source of our definitions of the parts of a skill: instructions, scripts,
templates, reference material and executable resources. The two surveys and the NIST article are background on how LLM
agents use tools and plan.

- Model Context Protocol Project, "Model Context Protocol specification," revision 2026-07-28, LF Projects, LLC, Jul. 28,
  2026. [Online]. Available: <https://modelcontextprotocol.io/specification/2026-07-28>
- X. Li, Y. Liu, W. Chen, B. You, Z. Di, Y. He, et al., "SkillsBench: Benchmarking how well agent skills work across
  diverse tasks," arXiv:2602.12670, Feb. 2026. [Online]. Available: <https://arxiv.org/abs/2602.12670>
- H. Xu, C. Li, X. Ma, X. Ou, Z. Zhang, T. He, et al., "The evolution of tool use in LLM agents: From single-tool call to
  multi-tool orchestration," arXiv:2603.22862, Mar. 2026. [Online]. Available: <https://arxiv.org/abs/2603.22862>
- X. Huang, W. Liu, X. Chen, X. Wang, H. Wang, D. Lian, Y. Wang, R. Tang, and E. Chen, "Understanding the planning of LLM
  agents: A survey," arXiv:2402.02716, Feb. 2024. [Online]. Available: <https://arxiv.org/abs/2402.02716>
- National Institute of Standards and Technology, "Lessons learned from the consortium: Tool use in agent systems," Aug.
  5, 2025. [Online]. Available:
  <https://www.nist.gov/news-events/news/2025/08/lessons-learned-consortium-tool-use-agent-systems>

### Reused ontologies and modeling references

We reuse OWL-S for the parameters and preconditions of tools, PROV-O for the provenance of invocations and information
artifacts, and P-Plan for plans, steps and the activities that carry them out. The W3C note on n-ary relations and the
OWL 2 quick reference guide are modeling references. The other ontologies we import (BEAM, the OMG Commons Ontology
Library and FIBO) are listed on the [Concept Map & Ontology](ontology.html#ontologies-reused) page.

- D. Martin et al., "OWL-S: Semantic markup for web services," W3C Member Submission, Nov. 22, 2004. [Online].
  Available: <https://www.w3.org/submissions/OWL-S/>
- T. Lebo, S. Sahoo, and D. McGuinness, Eds., "PROV-O: The PROV ontology," W3C Recommendation, Apr. 30, 2013. [Online].
  Available: <https://www.w3.org/TR/prov-o/>
- D. Garijo and Y. Gil, "The P-Plan ontology," version 1.3, Mar. 12, 2014. [Online]. Available:
  <http://purl.org/net/p-plan>
- N. Noy and A. Rector, Eds., "Defining N-ary relations on the Semantic Web," W3C Working Group Note, Apr. 12, 2006.
  [Online]. Available: <https://www.w3.org/TR/swbp-n-aryRelations/>
- J. Bao, E. F. Kendall, D. L. McGuinness, and P. F. Patel-Schneider, Eds., "OWL 2 Web Ontology Language quick reference
  guide (second edition)," W3C Recommendation, Dec. 11, 2012. [Online]. Available:
  <https://www.w3.org/TR/owl2-quick-reference/>
