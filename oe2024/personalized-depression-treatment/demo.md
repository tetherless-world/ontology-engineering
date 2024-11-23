---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

### Study Match: Is there a study that matches this patient on a feature (s)?

#### Query 1: SPARQL Query to fetch treatments with high effectiveness in patients with the SLC64A-L allele

This query gets all polymorphisms of each gene, then finds the one requested in our
competency question, the SLC6A4 long allele (allele name: 5-HTTLPR_L). It then gets all
treatment responses that the allele has, all the treatments and their effectivenesses and
displays the group of the drugs with the highest effectiveness that exists.

```sparql
PREFIX pdt:
<https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/Personalize
dDepressionTreatment/>
SELECT ?treatment ?effectiveness
WHERE {
?gene rdf:type pdt:SLC6A4 .
FILTER (?gene = pdt:5-HTTLPR_L)
?gene pdt:hasResponse ?treatmentResponse .
?treatmentResponse pdt:isResponseTo ?treatment .
?treatmentResponse pdt:hasTreatmentEffectiveness ?effectiveness .
BIND(
IF(?effectiveness = "high", 1,
IF(?effectiveness = "medium", 2,
IF(?effectiveness = "low", 3, 4)
)
) AS ?priority
)
}
ORDER BY ?priority

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

This query gets all age based therapeutic indications and the treatments that have the
corresponding therapeutic indications. It then checks which therapeutic indications are for
groups that contain the age from our competency question (35) in the age range for that group.
It then outputs all treatments that match these parameters

```sparql
PREFIX pdt:
<https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/Personalize
dDepressionTreatment/>
PREFIX qv: <https://www.omg.org/spec/Commons/QuantitiesAndUnits/>
SELECT ?treatment
WHERE {
?indication rdf:type pdt:TherapeuticIndication .
?indication pdt:hasTargetPopulation ?population .
?population rdf:type pdt:AgePopulationCharacteristic .
?population qv:hasQuantityValueRange ?range .
?range qv:hasLowerBound ?lb .
?lb rdfs:label ?lowerBound .
?range qv:hasUpperBound ?ub .
?up rdfs:label ?upperBound .
?treatment rdf:type pdt:MedicinalProduct .
?treatment pdt:hasTherapeuticIndication ?indication .
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

This query finds all example patients that have shown poor response to the group of SSRIs as
the question does not specify specific medications. It then finds the treatment response of the
example patient to other treatments. It then outputs the treatments with the best effectiveness
and their corresponding effectiveness.

```sparql
PREFIX pdt:
<https://tw.rpi.edu/ontology-engineering/oe2024/personalized-depression-treatment/Personalize
dDepressionTreatment/>
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
IF(?effectiveness = "high", 1,
IF(?effectiveness = "medium", 2,
IF(?effectiveness = "low", 3, 4)
)
) AS ?priority
)
}
ORDER BY ?priority```

#### Result 3: Treatments effective on patients who resist SSRIs

| Treatment Name | 
| -------------- | 
| Bupropion |

