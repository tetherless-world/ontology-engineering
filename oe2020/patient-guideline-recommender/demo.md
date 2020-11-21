---
---

## Static Demo

### Query Prefix
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
PREFIX lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
```

## Competency Questions

### Competency Question 1
#### Question:

Related to Guideline 5.27:
> “5.27 All adults, and particularly those with type 2 diabetes, should decrease the amount of time spent in daily sedentary behavior. B Prolonged sitting should be interrupted every 30 min for blood glucose benefits, particularly in adults with type 2 diabetes. C.

How does this guideline recommendation apply to me?

#### Query:
In SPARQL, with reasoner run:
```sparql
SELECT DISTINCT ?userConstraint WHERE {
  pgo:Guideline-5.27 a ?restriction .
  
  # Find guideline restriction
	?restriction a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom/owl:hasValue ?cohort .
    
	# Find cohort restraint
	?cohort rdf:type ?p .
	?p a owl:Restriction ;
		owl:onProperty lcc-lr:hasMember ;
		owl:someValuesFrom ?userConstraint .
}
```

After matching `?userConstraint` values, we then run the following query in snap-SPARQL with the reasoner (substututing the values of the previous query for `?userConstraint`):
```sparql
SELECT ?match WHERE {
  BIND(EXISTS {
    individuals:JaneSmithUser a ?userConstraint .
  } as ?match) .
}
```
The value of `?match` for each query tells us whether that constraint of Guideline 5.27 is applicable to the user.

### Competency Question 2

#### Question:

If I ate 1800 calories today, with no calories burned from exercise, have I met my dietary goal of losing weight??

#### Query:
In Snap-SPARQL, with reasoner run:
```sparql
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
In SPARQL:
```sparql
SELECT DISTINCT ?guideline ?recommendation ?userConstraint ?eatTarget WHERE {
	?guideline a pgo:Guideline ;
		rdf:type ?restriction .

	# Find guideline restriction
	?restriction a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom/owl:hasValue ?cohort .

	# Find cohort restraint
	?cohort rdf:type ?p .
	?p a owl:Restriction ;
		owl:onProperty lcc-lr:hasMember ;
		owl:someValuesFrom ?userConstraint .
	?guideline pgo:recommends ?recommendation .

	# Match recommendations relevant to carbohydrates
	?recommendation a ?recommendationFilt1 .
	?recommendationFilt1 a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom pgo:Carbohydrate .
  
  # Match recommendations relevant to eating
	?recommendation a ?recommendationFilt2 .
	?recommendationFilt2 a owl:Restriction ;
		owl:onProperty pgo:recommends ;
		owl:someValuesFrom ?recTarget .
	?recTarget a owl:Restriction ;
		owl:onProperty pgo:eats ;
		owl:someValuesFrom ?eatTarget .
}
```
After running the above query, check whether the guideline applies to the user with the following query in snap-SPARQL+reasoner:
```sparql
SELECT ?match WHERE {
  BIND(EXISTS {
    individuals:JaneSmithUser a ?userConstraint .
  } as ?match) .
}
```
For each guideline that matches, find all items of food to eat with the following query in snap-SPARQL+reasoner:
```sparql
SELECT ?food WHERE {
  ?food a ?eatTarget .
}
```

## SPARQL query to retrieve matched guideline for patient


```sparql
SELECT DISTINCT ?user ?matchedGuideline ?recommendation WHERE {
  ?user a people:Adult .
  ?user a ?matchedGuideline .
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuideline rdfs:subClassOf ?recommendation .
  ?recommendation rdfs:subClassOf individuals:Recommendation .
}
```

```sparql
SELECT DISTINCT ?matchedGuideline ?object {
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuideline (rdfs:subClassOf|owl:equivalentClass) ?object .
}

SELECT DISTINCT ?user ?matchedGuideline ?object WHERE {
  ?user a people:Adult .
  ?user a ?matchedGuideline .
  ?matchedGuideline rdfs:subClassOf pgo:Guideline .
  ?matchedGuideline owl:equivalentClass ?object .
}

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
