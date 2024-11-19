---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

### Study Match: Is there a study that matches this patient on a feature (s)?

#### Query 1: SPARQL Query to fetch treatments with high effectiveness in patients with the SLC64A-L allele

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>

SELECT ?treatment ?effectiveness
WHERE {
  ?gene rdf:type pdt:Gene .
  ?gene rdfs:label "SLC6A4-L" .
  ?gene pdt:hasResponse ?treatmentResponse .
  ?treatmentResponse pdt:isResponseTo ?treatment .
  ?treatmentResponse pdt:hasTreatmentEffectiveness ?effectiveness .
  ?effectiveness rdfs:label "high" .
}

```

#### Result 1: Effective Treatments for SLC64A-L

|Treatment Name|
|-----------|
| Citalopram |
| Escitalopram |
| Fluoxetine |
| Fluvoxamine |
| Paroxetine |
| Sertraline |
| Vilazodone |


#### Query 2: What treatments are effective against depression in 35 year olds?

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>
PREFIX qv: <https://www.omg.org/spec/Commons/QuantitiesAndUnits/>

SELECT ?medicinalProduct
WHERE {
  ?indication rdf:type pdt:TherapeuticIndication .
  ?indication pdt:hasTargetPopulation ?population .
  ?population rdf:type pdt:AgePopulationCharacteristic .
  ?population qv:hasQuantityValueRange ?range .
  ?range qv:hasLowerBound ?lb .
  ?lb rdfs:label ?lowerBound .
  ?range qv:hasUpperBound ?ub .
  ?up rdfs:label ?upperBound .
  ?medicinalProduct rdf:type pdt:MedicinalProduct .
  ?medicinalProduct pdt:hasTherapeuticIndication ?indication .
  FILTER(?upperBound >= 35 && ?lowerBound <= 35) 
}
```

#### Result 2: Effective treatments for 35 year olds

|Treatment Name|
|-----------|
| Citalopram |
| Escitalopram |
| Fluoxetine |
| Paroxetine |
| Sertraline |


#### Query 3: What treatments are effective in patients who resist SSRIs?

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>

SELECT ?treatment
WHERE {
  ?patient rdf:type pdt:Patient .
  ?patient pdt:hasResponse ?response .
  ?response rdfs:label "SSRI-Low" .
  ?treatmentResponse rdf:type pdt:TreatmentResponse .
  ?treatmentResponse pdt:isResponseOf ?patient .
  ?treatmentResponse pdt:hasTreatmentEffectiveness ?treatmentEffectiveness .
  ?treatmentEffectiveness rdfs:label "high" .
  ?treatmentResponse pdt:isResponseTo ?treatment . 
}
```

#### Result 3: Treatments effective on patients who resist SSRIs

| Treatment Name | 
| -------------- | 
| Bupropion |

