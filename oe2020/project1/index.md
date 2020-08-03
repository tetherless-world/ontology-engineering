[Abstract](#abstract) | [Workflow](#workflow) | [Resource List](#resources) | [License](#license) | [Acknowledgements](#acknowledgements)

<article class="mb-5" id="note">
<content>
 <h2>Note</h2>
 <p>This website is organized as follows. The side navigation serves a static menu to navigate across pages on this website. However, the top navigation menu is updated on a per page basis, and serves as an in-page section navigation toool. </p>
 </content>
<article class="mb-5" id="authors">
<!-- <content>
<h2>Authors</h2>
 <ul>
 Shruthi Chari<sup>1</sup>, Miao Qi<sup>2</sup>, Nkcheniyere N. Agu<sup>1</sup>, Oshani Seneviratne<sup>2</sup>, James P. McCusker<sup>1</sup>, Kristin P. Bennett<sup>2</sup>, Amar K. Das<sup>3</sup> and Deborah L. McGuinness<sup>1</sup>
  <br>
 <strong><sup>1</sup><a href="https://tw.rpi.edu/">Tetherless World Constellation</a></strong>, Rensselaer Polytechnic Institute
 <br>
 <strong><sup>2</sup><a href="https://idea.rpi.edu/">Instiute for Data Exploration and Applications</a></strong>, Rensselaer Polytechnic Institute
 <br>
 <strong><sup>3</sup><a href="http://www.research.ibm.com/">IBM Research</a></strong>, Cambridge
 </ul>
 </content> -->
 
<article class="mb-5" id="abstract">
<content>
<h2>Abstract</h2>
 <p>Treatment recommendations within Clinical Practice Guidelines (CPGs) are largely based on findings from clinical trials, referred here as research studies, that are often based on highly selective clinical populations, referred here as study cohorts. In applying CPG recommendations in clinical practice, physicians will need to understand how well their patient population matches the characteristics of those in the study cohort, and thus are confronted with the challenges of locating the study cohort information and making the analytic comparison. To address these challenges, we develop an ontology-enabled prototype workflow, which exposes the population descriptions in research studies in a declarative manner, with the ultimate goal of allowing physicians to better understand the applicability and generalizability of treatment recommendations. We build a Study Cohort Ontology (SCO) to encode the vocabulary of descriptions of study populations, that are often reported in the first table in the published work, thus often referred to as Table 1. We leverage the well-used Semanticscience Integrated Ontology (SIO) for defining property associations between classes. Further, we model the key components of Table 1s, i.e., collections of study subjects, subject characteristics and statistical measures in RDF knowledge graphs. Utilizing a tool we developed, medical professional can perform population analysis and cohort similarity assessment to determine the applicability of a study population to the clinical population. Our semantic approach to make study populations visible by standardized representations of Table 1s, allows users to quickly derive clinically relevant inferences about study populations.</p>
<ul>
  
 </ul>
 </content>
 
 
<article class="mb-5" id="workflow">
<content>
<h2>Workflow Diagram</h2>
    <iframe src="images/CohortAnalyticsWorkflowDiagramISWCPaper.pdf" style="width:100%; height: 500px"></iframe>
<ul>
 <p>Our knowledge representation approach backed by our study cohort ontology and the knowledge graphs instantiating Table 1 data, are built to support analytical applications to determine applicability of a study population to a patient. Our <a href="./papers-used.html">data sources</a> include cited research studies from the pharmacologic and cardiovascular complications chapters of the ADA Standards of Medical Care guidelines, and patient records selected from the NHANES 2015-2016 questionnaire. Our population analysis scenarios are designed to determine if studies match, if there are limitations and to evaluate their quality. Additionally, we visualize similarity of a group of study subjects (arm) to a patient.</p>  
 </ul>
 </content>
 
  
<article class="mb-5" id="resources">
<content>
<h2>List of Resources </h2>
<ul>
 <table style="width:100%">
    <tr>
    <th>Resources</th>
    <th>Links</th> 
  </tr>
  <tr>
    <td>1. Ontologies</td>
    <td> (a) <a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/studycohort.owl">Study Cohort Ontology (SCO)</a></td> 
  </tr>
  <tr>
    <td>2. Knowledge Graphs:</td>
    <td>(a) <a href="./knowledge-graph.html">Table 1 Knowledge Graphs</a> </td> 
  </tr>
  <tr>
    <td>3. Source Code:</td>
    <td>(a) <a href="./ontology-resource.html#ontologyreused">MIREOT Script </a> </td> 
  </tr>
    <!--<tr>
    <td> </td>
    <td> (b) <a href="./application.html">Faceted Browser</a> </td> 
  </tr>-->
    <tr>
    <td></td>
    <td>(b) <a href="./application.html#visualization">Cohort Similarity Visualization</a> </td> 
  </tr>
   <tr>
    <td>4 .Data: </td>
    <td> (a) <a href="./papers-used.html">NHANES Patient Records</a> </td> 
  </tr>
</table>
  
 </ul>
 </content>
 
 <article class="mb-5" id="license">
<content>
<h2>License</h2>
 <ul> 
<iframe src="images/License.pdf" style="width: 100%;height: 700px;border: none;"></iframe>
  </ul>
 </content>
 
 <article class="mb-5" id="acknowledgements">
<content>
 <h2>Acknowledgements</h2>
 <p>This work is undertaken as a part of the <a href="https://science.rpi.edu/biology/news/ibm-and-rensselaer-team-research-chronic-diseases-cognitive-computing"> Health Empowerement by Analytics, Learning and Semantics (HEALS) </a> project , and is  partially supported by IBM Research AI through the AI Horizons Network. We thank our colleagues from IBM Research, Dan Gruen, Morgan Foreman and Ching-Hua Chen, and from RPI, John Erickson, Alexander New, Neha Keshan and Rebecca Cowan, who provided insight and expertise that greatly assisted the research.</p>
<ul>
    
  
 </ul>
 </content>


