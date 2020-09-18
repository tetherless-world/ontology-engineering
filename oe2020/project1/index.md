---
layout: default
title: About
---

## Note to students

This website is organized as follows.
The side navigation serves a static menu to navigate across pages on this website.
We provide you with a template of what we want to see from your project pages, the contents can be edited on a per project basis.

## Abstract

<p class="message-highlight">Overview of project goes here, an example is below</p>

Treatment recommendations within Clinical Practice Guidelines (CPGs) are largely based on findings from clinical trials, referred here as research studies, that are often based on highly selective clinical populations, referred here as study cohorts. In applying CPG recommendations in clinical practice, physicians will need to understand how well their patient population matches the characteristics of those in the study cohort, and thus are confronted with the challenges of locating the study cohort information and making the analytic comparison. To address these challenges, we develop an ontology-enabled prototype workflow, which exposes the population descriptions in research studies in a declarative manner, with the ultimate goal of allowing physicians to better understand the applicability and generalizability of treatment recommendations. We build a Study Cohort Ontology (SCO) to encode the vocabulary of descriptions of study populations, that are often reported in the first table in the published work, thus often referred to as Table 1. We leverage the well-used Semanticscience Integrated Ontology (SIO) for defining property associations between classes. Further, we model the key components of Table 1s, i.e., collections of study subjects, subject characteristics and statistical measures in RDF knowledge graphs. Utilizing a tool we developed, medical professional can perform population analysis and cohort similarity assessment to determine the applicability of a study population to the clinical population. Our semantic approach to make study populations visible by standardized representations of Table 1s, allows users to quickly derive clinically relevant inferences about study populations.</p>

## Workflow Diagram

<iframe src="files/CohortAnalyticsWorkflowDiagramISWCPaper.pdf" style="width:100%; height: 500px"></iframe>

<p class="message-highlight">Add a representative diagram of your project such as the below workflow diagram illustrating the flow between the components.</p>

Our knowledge representation approach backed by our study cohort ontology and the knowledge graphs instantiating Table 1 data, are built to support analytical applications to determine applicability of a study population to a patient. Our [data sources](./papers-used.html) include cited research studies from the pharmacologic and cardiovascular complications chapters of the ADA Standards of Medical Care guidelines, and patient records selected from the NHANES 2015-2016 questionnaire. Our population analysis scenarios are designed to determine if studies match, if there are limitations and to evaluate their quality. Additionally, we visualize similarity of a group of study subjects (arm) to a patient.

## List of Resources

List resources you think a reader would benefit from to use your project. We list some examples you could make available below.

<table>
  <tr>
    <th>Resources</th>
    <th>Links</th>
  </tr>
  <tr>
    <td>1. Ontology</td>
    <td>(a) <a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/studycohort.owl">Your Ontology</a></td>
  </tr>
  <tr>
    <td>2. Term List</td>
    <td>(a) <a href="./knowledge-graph.html">Mapped Vocabularies</a> </td>
  </tr>
  <tr>
    <td>2. Competency Questions</td>
    <td>(a) <a href="./knowledge-graph.html">SPARQL Queries</a> </td>
  </tr>
  <tr>
    <td>3. Presentations:</td>
    <td>(a) <a href="./ontology-resource.html#ontologyreused">Project presentations during class</a> </td>
  </tr>
</table>

## License

<iframe src="files/License.pdf" style="width: 100%;height: 700px;border: none;"></iframe>

## Acknowledgements

<p class="message-highlight">Please acknowledge people who have helped you in this work. An example is below</p><br/>
This work is undertaken as a part of the [Health Empowerement by Analytics, Learning and Semantics (HEALS)](https://science.rpi.edu/biology/news/ibm-and-rensselaer-team-research-chronic-diseases-cognitive-computing) project , and is partially supported by IBM Research AI through the AI Horizons Network. We thank our colleagues from IBM Research, Dan Gruen, Morgan Foreman and Ching-Hua Chen, and from RPI, John Erickson, Alexander New, Neha Keshan and Rebecca Cowan, who provided insight and expertise that greatly assisted the research.
