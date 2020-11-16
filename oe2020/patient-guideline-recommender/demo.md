---
---

## Static Demo
## Competency Questions

### Competency Question 1
#### Question:

Related to Guideline 5.27:
> “5.27 All adults, and particularly those with type 2 diabetes, should decrease the amount of time spent in daily sedentary behavior. B Prolonged sitting should be interrupted every 30 min for blood glucose benefits, particularly in adults with type 2 diabetes. C.

How does this guideline recommendation apply to me?

#### Query:
In Snap-SPARQL, with reasoner run:
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>
PREFIX fiboRoles: <https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Roles/>
PREFIX fiboRelations: <https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/>


SELECT DISTINCT ?user ?typicalPatient WHERE {
  ?user a people:Adult .
  ?user fiboRoles:playsRole ?userPatient .
  ?userPatient pgo:hasCondition ?condition .
  ?user a ?typicalPatient.
  ?typicalPatient rdfs:subClassOf pgo:TypicalPatient .
  ?typicalPatInst a ?typicalPatient .
  ?guideline rdfs:subClassOf pgo:Guideline .
  ?guidelineInst a ?guideline .
  ?guidelineInst fiboRelations:appliesTo ?typicalPatInst .
}
```

In SPARQL:
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>


SELECT DISTINCT ?typicalPatient ?object {
  ?typicalPatient rdfs:subClassOf pgo:TypicalPatient.
  ?typicalPatient (rdfs:subClassOf|owl:equivalentClass) ?object .
} 
```

### Competency Question 2

#### Question:

If I ate 1800 calories today, with no calories burned from exercise, have I met my dietary goal of losing weight??

#### Query:
In Snap-SPARQL, with reasoner run:
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>
PREFIX fiboRelations: <https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/>

SELECT DISTINCT ?user ?goalMet WHERE {
  ?user a people:Adult .
  ?user pgo:hasWeightGoal ?weightloss .
  ?user a ?typicalPatient .
  ?typicalPatient rdfs:subClassOf pgo:TypicalPatient .
  ?typicalPatInst a ?typicalPatient .
  ?guideline rdfs:subClassOf pgo:Guideline .
  ?guidelineInst a ?guideline .
  ?guidelineInst fiboRelations:appliesTo ?typicalPatInst .
  ?guidelineInst pgo:recommends ?recommendation .
  ?recommendation a pgo:Recommendation .
  ?recommendationInst a pgo:Recommendation .
  FILTER(?recommendationInst = ?user) .
  BIND (IF (?recommendationInst = ?user, True, False) as ?goalMet) .
}
```

### Competency Question 3.

#### Context:
 - Has Type-2 diabetes

#### Question:

What carbohydrates should I be eating?

#### Query:
In Snap-SPARQL:
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>
PREFIX fiboRelations: <https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/>

SELECT DISTINCT ?user ?recommendationInst WHERE {
  ?user a people:Adult .
  ?user pgo:eats ?food .
  ?user a ?typicalPatient .
  ?typicalPatient rdfs:subClassOf pgo:TypicalPatient .
  ?typicalPatInst a ?typicalPatient .
  ?guideline rdfs:subClassOf pgo:Guideline .
  ?guidelineInst a ?guideline .
  ?guidelineInst fiboRelations:appliesTo ?typicalPatInst .
  ?guidelineInst pgo:recommends ?recommendation .
  ?recommendation a pgo:Recommendation .
  ?recommendationInst a pgo:Recommendation .
  ?recommendationInst a pgo:Food .
}
```

## SPARQL query to retrieve matched guideline for patient


```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/>
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/>
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/> 

SELECT DISTINCT ?user ?matchedGuideline ?recommendation WHERE {
  ?user a people:Adult .
  ?user a ?matchedGuideline .
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuideline rdfs:subClassOf ?recommendation .
  ?recommendation rdfs:subClassOf individuals:Recommendation .
}
```

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>
SELECT DISTINCT ?matchedGuideline ?object {
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuideline (rdfs:subClassOf|owl:equivalentClass) ?object .
} 


PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>
SELECT DISTINCT ?user ?matchedGuideline ?object WHERE {
  ?user a people:Adult .
  ?user a ?matchedGuideline .
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuideline owl:equivalentClass ?object .
} 



PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX people: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/> 
PREFIX individuals: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender-individuals/> 
PREFIX pgo: <https://tw.rpi.edu/ontology-engineering/oe2020/patient-guideline-recommender/>
SELECT DISTINCT ?actionInstances WHERE {
  ?matchedGuidelineInstance a ?matchedGuideline .
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuidelineInstance pgo:recommends ?recommendationInstance .
  ?recommendationInstance a ?recommendation .
  ?recommendation rdfs:subClassOf pgo:Recommendation .
  ?recommendation owl:equivalentClass ?action .
  ?actionInstances a ?action .
} 

```
