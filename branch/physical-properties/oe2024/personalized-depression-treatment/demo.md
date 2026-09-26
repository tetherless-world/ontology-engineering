---
---

## Queries

#### Query 1: SPARQL Query to fetch treatments with high effectiveness in patients with the SLC64A-L allele

This query gets all polymorphisms of each gene, then finds the one requested in our
competency question, the SLC6A4 long allele (allele name: 5-HTTLPR_L). It then gets all
treatment responses that the allele has, all the treatments and their effectivenesses and
displays the group of the drugs with the highest effectiveness that exists.

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>

SELECT ?treatment ?effectiveness
WHERE {
  ?gene rdf:type pdt:SLC6A4 .
  FILTER (?gene = pdt:5-HTTLPR_L)
  ?gene pdt:hasResponse ?treatmentResponse .
  ?treatmentResponse pdt:isResponseTo ?treatment .
  ?treatmentResponse pdt:hasTreatmentEffectiveness ?effectiveness .
  BIND(
    IF(?effectiveness = pdt:high, 1,
      IF(?effectiveness = pdt:medium, 2,
        IF(?effectiveness = pdt:low, 3, 4)
      )
    ) AS ?priority
  )
}
ORDER BY ?priority
```

#### Result 1: Effective Treatments for SLC64A-L

|Treatment| Effectiveness |
|-----------|-------------|
| Citalopram | High |
| Escitalopram | High |
| Fluoxetine | High |
| Fluvoxamine | High |
| Paroxetine | High |
| Sertraline | High |
| Vilazodone | High |


#### Query 2: What treatments are effective against depression in 35 year olds?

This query gets all age based therapeutic indications and the treatments that have the
corresponding therapeutic indications. It then checks which therapeutic indications are for
groups that contain the age from our competency question (35) in the age range for that group.
It then outputs all treatments that match these parameters

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>
PREFIX qv: <https://www.omg.org/spec/Commons/QuantitiesAndUnits/>

SELECT ?treatment
WHERE {
  ?treatment rdf:type/rdfs:subClassOf* pdt:MedicinalProduct .
  ?treatment pdt:hasTherapeuticIndication/pdt:hasTargetPopulation/qv:hasQuantityValueRange/qv:hasLowerBound/rdfs:label ?lowerBound .
  ?treatment pdt:hasTherapeuticIndication/pdt:hasTargetPopulation/qv:hasQuantityValueRange/qv:hasUpperBound/rdfs:label ?upperBound .
  FILTER(xsd:decimal(?upperBound) >= 35 && xsd:decimal(?lowerBound) <= 35)
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

This query finds all example patients that have shown poor response to the group of SSRIs as
the question does not specify specific medications. It then finds the treatment response of the
example patient to other treatments. It then outputs the treatments with the best effectiveness
and their corresponding effectiveness.

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>

SELECT ?treatment ?effectiveness
WHERE {
  ?patient rdf:type pdt:Patient .
  ?patient pdt:hasResponse ?response .
  FILTER(?response = pdt:SSRI-Low)
  ?treatmentResponse rdf:type pdt:TreatmentResponse .
  ?treatmentResponse pdt:isResponseOf ?patient .
  ?treatmentResponse pdt:hasTreatmentEffectiveness ?effectiveness .
  ?treatmentResponse pdt:isResponseTo ?treatment . 
 BIND(
    IF(?effectiveness = pdt:high, 1,
      IF(?effectiveness = pdt:medium, 2,
        IF(?effectiveness = pdt:low, 3, 4)
      )
    ) AS ?priority
  )
}
ORDER BY ?priority
```

#### Result 3: Treatments effective on patients who resist SSRIs

| Treatment | Effectiveness |
| -------------- | ---------- |
| Bupropion | High |

#### Query 4: Which gene alleles impact the effectiveness of SSRIs and what are their impact?

This query finds all gene alleles, finds all the treatments they have responses to, 
finds the effectiveness of each of those treatments, and then only displays those that are specifically SSRIs

```sparql
PREFIX pdt: <https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/PersonalizedDepressionTreatment/>

SELECT ?gene ?treatment ?effectiveness
WHERE {
  ?gene rdf:type/rdfs:subClassOf* pdt:Gene .
  ?gene pdt:hasResponse/pdt:isResponseTo ?treatment .
  ?gene pdt:hasResponse/pdt:hasTreatmentEffectiveness ?effectiveness .
  ?treatment rdf:type/rdfs:subClassOf* pdt:SelectiveSerotoninReuptakeInhibitor .
}
```

#### Result 4: Effective Treatments for SLC64A-L (Showing 21 out of 100 results)

| Gene | Treatment| Effectiveness |
|-----------|-------------|-----------|
| SLC6A4-L | Citalopram | High |
| SLC6A4-L | Escitalopram | High |
| SLC6A4-L | Fluoxetine | High |
| SLC6A4-L | Fluvoxamine | High |
| SLC6A4-L | Paroxetine | High |
| SLC6A4-L | Sertraline | High |
| SLC6A4-L | Vilazodone | High |
| Val66Met_Met | Citalopram | Low |
| Val66Met_Met | Escitalopram | Low |
| Val66Met_Met | Fluoxetine | Low |
| Val66Met_Met | Fluvoxamine | Low |
| Val66Met_Met | Paroxetine | Low |
| Val66Met_Met | Sertraline | Low |
| Val66Met_Met | Vilazodone | Low |
| rs165599_A | Citalopram | Low |
| rs165599_A | Escitalopram | Low |
| rs165599_A | Fluoxetine | Low |
| rs165599_A | Fluvoxamine | Low |
| rs165599_A | Paroxetine | Low |
| rs165599_A | Sertraline | Low |
| rs165599_A | Vilazodone | Low |
