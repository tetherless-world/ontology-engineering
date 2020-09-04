[Concept Map](#conceptmap) | [Ontology File](#ontologyfile) | [Ontologies Reused](#ontologyreused) 

 <article class="mb-5" id="conceptmap">
<content>
<h2>Conceptual Model</h2>
 
   <img src="images/ConceptMap_SubjectModel.png" width="100%" height="100%">
   <p style="text-align:center;">An overview of the main classes and their property associations. Some property associations exist only upon representation of the Table 1 data, and so we highlight instances in pink</p>
 </content>

<article class="mb-5" id="ontologyfile">
<content>
<h2>Ontologies</h2>
<ul>
<h3> Study Cohort Ontology (SCO) </h3>
 <h4>Link: <a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/studycohort.owl">https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/studycohort.owl</a></h4>
 <h4>View the ontology documentation at: <a href="https://tetherless-world.github.io/study-cohort-ontology/WidocoDocumentation/doc/index-en.html">https://tetherless-world.github.io/study-cohort-ontology/WidocoDocumentation/doc/index-en.html</a></h4>
 <h4> Primary Classes and Definitions </h4>
 <ol>
 <li>Research Study 
  <ul type = "circle">
  <li> Definition: A scientific investigation that involves testing a hypothesis </li>
  <li> Immediate Superclass: None </li>
  <li> Example: "10-Year Follow-up of Intensive Glucose Control in Type 2 Diabetes"</li>
  <li> Reused From: Hasco</li>
  </ul>
  </li>

  
  <li>Clinical Trial
  <ul type = "circle">
  <li> Definition: A prospective study designed to evaluate whether one or more interventions are associated with an outcome</li>
  <li> Immediate Superclass: Research Study</li>
  <li> Example: "10-Year Follow-up of Intensive Glucose Control in Type 2 Diabetes"</li>
  <li> Reused From: National Cancer Institute Thesarus (NCIT) </li>
  </ul>
  </li>
  
    
  <li>Cohort
  <ul type = "circle">
  <li> Definition: A cohort is the group of subjects enrolled in a study</li>
  <li> Immediate Superclass: None</li>
  <li> Example: Randomized Cohort in "10-Year Follow-up of Intensive Glucose Control in Type 2 Diabetes"</li>
  <li> Reused From: The Statistical Methods Ontology (STATO)</li>
  </ul>
  </li>
  
  
  <li>Study Arm
  <ul type = "circle">
  <li> Definition: A group or subgroup of participants in a clinical trial that receives a specific intervention/treatment, or no intervention, according to the trial's protocol</li>
  <li> Immediate Superclass: Cohort</li>
  <li> Example: Metformin Conventional Therapy Arm</li>
  <li> Reused From: None</li>
  </ul>
  </li>
  
  <li>Study Subject
  <ul type = "circle">
  <li> Definition: A person who receives medical attention, care, or treatment, or who is registered with medical professional or institution with the purpose to receive medical care when necessary</li>
  <li> Immediate Superclass: None</li>
  <li> Example: African American Male Subject in "10-Year Follow-up of Intensive Glucose Control in Type 2 Diabetes"</li>
  <li> Reused From: SemanticScience Integrated Ontology (SIO)</li>
  </ul>
  </li>
  
  <li>Study Intervention
  <ul type = "circle">
  <li> Definition: A process or action that is the focus of a clinical study. Interventions include drugs, medical devices, procedures, vaccines, and other products that are either investigational or already available</li>
  <li> Immediate Superclass: None</li>
  <li> Example: Metformin</li>
  <li> Reused From: ProvCaRe </li>
  </ul>
  </li>
  
  <li>Subject Characteristic
  <ul type = "circle">
  <li> Definition: Property that summarizes important attributes of the participants enrolled in a study</li>
  <li> Immediate Superclass: None</li>
  <li> Example: Age</li>
  <li> Reused From: None</li>
  </ul>
  </li>
  
  <li>Statistical Measure
  <ul type = "circle">
  <li> Definition: a standard unit used to express the size, amount, or degree of something</li>
  <li> Immediate Superclass: None</li>
  <li> Example: Mean</li>
  <li> Reused From: ProvCaRe</li>
  </ul>
  </li>
  
 </ol>
 
 
<h3> Accompanying Suite of Ontologies </h3>

<ul>
 <li><a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/diseases.owl"> Diseases</a></li>
 <li> <a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/labresults.owl">Lab results</a></li>
 <li><a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/medications.owl"> Medications</a></li>
 <li><a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/therapies.owl">Therapies</a></li>
 <li><a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/measures.owl"> Measures</a></li>
 <li> <a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/units.owl">Units</a></li>
     </ul>
  
 </ul>
 </content>
 
 
 <article class="mb-5" id="ontologyreused">
<content>
<h1> Ontologies Reused</h1>
 We group the ontologies we reuse by the purpose and the use-cases they are intended to serve, as vocabularies for.
 
 <h3>Study Design Ontologies</h3>
 <ul>
  <li><a href="https://provcare.case.edu/">Provenance for Healthcare + Clinical Research (ProvCaRe)</a></li>
  <li><a href="http://hadatac.org/ont/hasco/">Human-Aware Science Ontology</a></li>
</ul>
 <h3>Medical Ontologies</h3>
 <ul>
  <li><a href="https://provcare.case.edu/">National Cancer Institute Thesarus (NCIT)</a></li>
  <li><a href="https://bioportal.bioontology.org/ontologies/NCIT">Children's Health Exposure Analysis Resource Ontology (CHEAR)</a></li>
  <li><a href=https://www.ebi.ac.uk/ols/ontologies/doid">Human-Disease Ontology (DOID)</a></li>
</ul>
   <h3>Mid-Level Ontologies</h3>
 <ul>
  <li><a href="https://raw.githubusercontent.com/micheldumontier/semanticscience/master/ontology/sio/release/sio-subset-labels.owl">SemanticScience Integrated Ontology (SIO)</a></li>
</ul>
   <h3>Statistical Ontologies</h3>
 <ul>
  <li><a href="https://www.google.com/search?q=UO+ontology&rlz=1C5CHFA_enIN727IN729&oq=UO+ontology&aqs=chrome..69i57j69i60.3199j0j4&sourceid=chrome&ie=UTF-8">Units Ontology (UO)</a></li>
   <li><a href="https://www.ebi.ac.uk/ols/ontologies/stato">Statistical Methods Ontology (STATO)</a></li>
</ul>
 <h2><a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Code/MIREOT.py">MIREOT Script</a></h2>
  <p>Below we present a small Python script that can be used to fetch the child and parent hierarchy for a class, given its IRI. This script pulls in all the axioms defined on the classes as well. We leverage the powerful constructs of the <a href="https://www.w3.org/TR/rdf-sparql-query/#describe">SPARQL DESCRIBE</a> functionality to achieve this. This script outputs the RDF/XML version of the subset class tree.</p>
 <pre>
 from SPARQLWrapper import *
from owlready2 import *
import os

sparql_endpoint = "http://localhost:9999/bigdata/sparql"

query = '''
describe ?child ?superParent 
where {
   hint:Query hint:describeMode "CBD".
  ?child rdfs:subClassOf* ?super .
  ?super rdfs:subClassOf* ?superParent .
}
values ?super {<http://hadatac.org/ont/chear#ATIDU>}
'''

sparql_wrapper = SPARQLWrapper(sparql_endpoint)
sparql_wrapper.setQuery(query)
sparql_wrapper.setReturnFormat(RDF)
results = sparql_wrapper.query().convert()
results.serialize('output.owl', format="pretty-xml")
print("Writing results to a rdf-xml file")

 </pre>
 
 
 <h3> Ontology Prefixes </h3>
  <table style="width:100%">
    <tr>
    <th>Prefix</th>
    <th>Links</th> 
  </tr>
  <tr>
    <td>rdf</td>
    <td><a href="http://www.w3.org/1999/02/22-rdf-syntax-ns">Resource Description Framework</a></td> 
  </tr>
  <tr>
    <td>rdfs</td>
    <td><a href="http://www.w3.org/2000/01/rdf-schema"> RDF Schema</a> </td> 
  </tr>
  <tr>
    <td>owl</td>
    <td><a href="http://www.w3.org/2002/07/owl#">Web Ontology Language </a> </td> 
  </tr>
    <tr>
    <td> xsd</td>
    <td> <a href="http://www.w3.org/2001/XMLSchema#"></a> XML Schema Definition</td> 
  </tr>
    <tr>
    <td>dct</td>
    <td> <a href="http://purl.org/dc/terms/">Dublin Core Term</a> </td> 
  </tr>
   <tr>
    <td>skos</td>
    <td> <a href="http://www.w3.org/2004/02/skos/core#"></a>  Simple Knowledge Organization System</td> 
  </tr>
    <tr>
    <td>sco</td>
    <td> <a href="https://idea.tw.rpi.edu/projects/heals/studycohort/"> Study Cohort Ontology</a> </td> 
  </tr>
    <tr>
    <td>chear</td>
    <td> <a href="http://hadatac.org/ont/chear#"></a>  Children’s Health Exposure Analysis Resource</td> 
  </tr>
    <tr>
    <td>hasco</td>
    <td> <a href="http://hadatac.org/ont/hasco#"> Human-Aware Science Ontology</a> </td> 
  </tr>
    <tr>
    <td>fibo-fnd-utl-av</td>
    <td> <a href="http://www.omg.org/spec/EDMC-FIBO/FND/Utilities/AnnotationVocabulary/">Financial Industry Business Ontology</a> </td> 
  </tr>
    <tr>
    <td>sio</td>
    <td> <a href="http://semanticscience.org/resource/">SemanticScience Integrated Ontology</a> </td> 
  </tr>
     <tr>
    <td>obo</td>
    <td> <a href="http://purl.obolibrary.org/obo/">OBO Foundry</a> </td> 
  </tr>
    <tr>
    <td>stato</td>
    <td> <a href="http://purl.obolibrary.org/obo/STATO_">The Statistical Methods Ontolgy</a> </td> 
  </tr>
    <tr>
    <td>uo</td>
    <td><a href="http://purl.obolibrary.org/obo/UO_"> Units of Measurement Ontology</a> </td> 
  </tr>
    <tr>
    <td>pato</td>
    <td> <a href="http://purl.obolibrary.org/obo/PATO_"> Human Phenotypic Quality Ontology</a> </td> 
  </tr>
    <tr>
    <td>ncit</td>
    <td> <a href="http://purl.obolibrary.org/obo/NCI_">National Cancer Institute Thesarus</a> </td> 
  </tr>
     <tr>
    <td>provcare</td>
    <td> <a href="http://www.case.edu/ProvCaRe/provcare#">Provenance for Clinical + Healthcare Research</a> </td> 
  </tr>
     <tr>
    <td>ocre</td>
    <td> <a href="http://purl.org/net/OCRe/OCRe.owl/#"> Ontology of Clinical Research</a> </td> 
  </tr>
</table>
 </ul>
 </content>
 
