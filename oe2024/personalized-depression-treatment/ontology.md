[Concept Map](#conceptual-model) | [Ontology File](#ontologies) | [Ontologies Reused](#ontologies-reused) | [Ontology Prefixes](#ontology-prefixes)

## Conceptual Model

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTKf97PhTPJl4P0H46J_9uDp2wto6eaxaNrJXGjX7lq0z0CeHO45ZNemQx3ewr1_qie1A_kiVNid19G/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

Week 6 Versions:
[Patient / Illness Model](images/ConceptModel/w6PatientModel.png)

[Treatment Model](images/ConceptModel/w6TreatmentModel.png)

[Genetics Model](images/ConceptModel/w6GeneticModel.png)


## Ontologies

### Personalized Depression Treatment Ontology

**Link:**
[https://github.com/tetherless-world/ontology-engineering/blob/personalized-depression-treatment/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatmentWeek7.rdf](https://github.com/tetherless-world/ontology-engineering/blob/personalized-depression-treatment/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatmentWeek8.rdf)

**View the ontology documentation at:**
[https://tetherless-world.github.io/study-cohort-ontology/WidocoDocumentation/doc/index-en.html](https://tetherless-world.github.io/study-cohort-ontology/WidocoDocumentation/doc/index-en.html)

#### Primary Classes and Definitions

1. Patient
    - Definition: role of a person receiving or registered to receive medical treatment
    - Immediate Superclass: party role
    - Example: John Doe, a 45-year-old man admitted to the hospital for suicidal ideations.
    - Reused From: None
2. Treatment
    - Definition: something used to manage, alleviate, or cure a medical condition or disease
    - Immediate Superclass: functional role
    - Example: Cognitive Behavioral Therapy
    - Reused From: None
3. Condition
    - Definition: state of being, such as a state of health
    - Immediate Superclass: situation
    - Example: Major Depressive Disorder 
    - Reused From: Identification of Medicinal Products (IDMP)
4. Diagnosis
    - Definition: disorder with which a patient has been identified as having
    - Immediate Superclass: specification
    - Example: persistent depressive disorder
    - Reused From: None
5. Medicinal Product
    - Definition: specification for a pharmaceutical product or combination of pharmaceutical products that may be administered to human beings (or animals) for treating or preventing disease, with the aim/purpose of making a medical diagnosis or to restore, correct or modify physiological functions
    - Immediate Superclass: specification
    - Example: Fluoxetine
    - Reused From: Identification of Medicinal Products (IDMP)
6. Gene
    - Definition: distinct sequence of nucleotides forming part of a chromosome, the order of which determines the order of monomers in a polypeptide or nucleic acid molecule which a cell (or virus) may synthesize
    - Immediate Superclass: constituent
    - Example: SLC6A4
    - Reused From: None
7. Symptom
    - Definition: physical or mental feature which is regarded as indicating a condition of disease
    - Immediate Superclass: aspect
    - Example: anhedonia
    - Reused From: None
8. Undesirable Effect
    - Definition: specification of any potential undesirable side effect, adverse reaction or event, complication, or other similar potential consequence associated with the medicinal product as authorized or under investigation
    - Immediate Superclass: specification
    - Example: Nausea
    - Reused From: Identification of Medicinal Products (IDMP)


### Accompanying Suite of Ontologies

- [Diseases](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/diseases.owl)
- [Lab results](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/labresults.owl)
- [Medications](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/medications.owl)
- [Therapies](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/therapies.owl)
- [Measures](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/measures.owl)
- [Units](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/units.owl)

## Ontologies Reused

We group the ontologies we reuse by the purpose and the use-cases they are intended to serve, as vocabularies for.

### Study Design Ontologies

- [Provenance for Healthcare + Clinical Research (ProvCaRe)](https://provcare.case.edu/)
- [Human-Aware Science Ontology](http://hadatac.org/ont/hasco/)

### Medical Ontologies

- [National Cancer Institute Thesarus (NCIT)](https://provcare.case.edu/)
- [Children's Health Exposure Analysis Resource Ontology (CHEAR)](https://bioportal.bioontology.org/ontologies/NCIT)
- [Human-Disease Ontology (DOID)](https://www.ebi.ac.uk/ols/ontologies/doid")

### Mid-Level Ontologies

- [SemanticScience Integrated Ontology
  (SIO)](https://raw.githubusercontent.com/micheldumontier/semanticscience/master/ontology/sio/release/sio-subset-labels.owl)

### Statistical Ontologies

- [Units Ontology
  (UO)](https://www.google.com/search?q=UO+ontology&rlz=1C5CHFA_enIN727IN729&oq=UO+ontology&aqs=chrome..69i57j69i60.3199j0j4&sourceid=chrome&ie=UTF-8)
- [Statistical Methods Ontology (STATO)](https://www.ebi.ac.uk/ols/ontologies/stato)

### Ontology Prefixes

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
    <td> <a href="http://www.w3.org/2001/XMLSchema#">XML Schema Definition</a></td>
  </tr>
  <tr>
    <td>dct</td>
    <td> <a href="http://purl.org/dc/terms/">Dublin Core Term</a> </td>
  </tr>
  <tr>
    <td>skos</td>
    <td> <a href="http://www.w3.org/2004/02/skos/core#">Simple Knowledge Organization System</a></td>
  </tr>
  <tr>
    <td>sco</td>
    <td> <a href="https://idea.tw.rpi.edu/projects/heals/studycohort/"> Study Cohort Ontology</a> </td>
  </tr>
  <tr>
    <td>chear</td>
    <td> <a href="http://hadatac.org/ont/chear#">Children’s Health Exposure Analysis Resource</a></td>
  </tr>
  <tr>
    <td>hasco</td>
    <td> <a href="http://hadatac.org/ont/hasco#"> Human-Aware Science Ontology</a> </td>
  </tr>
  <tr>
    <td>fibo-fnd-utl-av</td>
    <td> <a href="http://www.omg.org/spec/EDMC-FIBO/FND/Utilities/AnnotationVocabulary/">Financial Industry Business
        Ontology</a> </td>
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
