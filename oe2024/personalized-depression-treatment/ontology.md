[Concept Map](#conceptual-model) | [Ontology File](#ontologies) | [Ontologies Reused](#ontologies-reused) | [Ontology Prefixes](#ontology-prefixes)

## Conceptual Model

Current Version:
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vR3rd-kLnItLnUuyke0WYLSg1r3EFvpfMv6HpKgcabQk5wHXIJD9I3Axge5UCZSvWNLPuQRcgbA1PM4/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>


Week 8 Version:
[Week 8 Concept Model](images/ConceptModel/OE8_PTDO_ConceptModel.pdf)

Week 6 Versions:
[Patient / Illness Model](images/ConceptModel/w6PatientModel.png)

[Treatment Model](images/ConceptModel/w6TreatmentModel.png)

[Genetics Model](images/ConceptModel/w6GeneticModel.png)


## Ontologies

### Personalized Depression Treatment Ontology

**Link:**
[https://github.com/tetherless-world/ontology-engineering/blob/personalized-depression-treatment/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatmentWeek10.rdf](https://github.com/tetherless-world/ontology-engineering/blob/personalized-depression-treatment/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatmentWeek10.rdf)

## **View the ontology documentation at:**
## [https://tetherless-world.github.io/study-cohort-ontology/WidocoDocumentation/doc/index-en.html](https://tetherless-world.github.io/study-cohort-ontology/WidocoDocumentation/doc/index-en.html)

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

## - [Diseases](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/diseases.owl)
## - [Lab results](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/labresults.owl)
## - [Medications](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/medications.owl)
## - [Therapies](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/therapies.owl)
## - [Measures](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/measures.owl)
## - [Units](https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Ontologies/units.owl)

## Ontologies Reused

IDMP - Identification of Medicinal Products Ontology

[Link](https://spec.edmcouncil.org/idmp/)

QV - Commons "Quantity and Units"
[Link](https://www.omg.org/spec/Commons/QuantitiesAndUnits/)

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
    <td>skos</td>
    <td> <a href="https://spec.edmcouncil.org/idmp/">Identification of Medicinal Products</a></td>
  </tr>
  <tr>
    <td>skos</td>
    <td> <a href="https://www.omg.org/spec/Commons/QuantitiesAndUnits/">Commons Quantities and Units</a></td>
  </tr>
</table>
