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

### Note
The following queries require the results of the reasoner. If using progege, you can do File>Export inferred axioms as ontology..., then select all axioms to export. Open the exported file, and run the SPARQL queries on that.

### Competency Question 1
#### Question:

Related to Guideline 5.27:
> “5.27 All adults, and particularly those with type 2 diabetes, should decrease the amount of time spent in daily sedentary behavior. B Prolonged sitting should be interrupted every 30 min for blood glucose benefits, particularly in adults with type 2 diabetes. C.

How does this guideline recommendation apply to me?

#### Query:
In this query, we find the associated cohort to Guideline 5.27 and extract the type of its members (`?userConstraint`), then check if each matches the current user (`?match`).

In SPARQL on the inferred ontology, run:
```sparql
SELECT DISTINCT ?userConstraint ?match WHERE {
	pgo:Guideline-5.27 a ?restriction .
  
	# Find guideline restriction (Guideline-5.27 appliesTo some ?cohort)
	?restriction a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom/owl:hasValue ?cohort .
    
	# Find cohort restraint (?cohort 'has member' some ?userConstraint)
	?cohort rdf:type ?p .
	?p a owl:Restriction ;
		owl:onProperty lcc-lr:hasMember ;
		owl:someValuesFrom ?userConstraint .
	
	# The following part requires the inferred axioms
	BIND(EXISTS {
		individuals:JaneSmithUser a ?userConstraint .
	} as ?match) .
}
```

The value of `?match` tells us whether each constraint of Guideline 5.27 is applicable to the user.

### Competency Question 2

#### Context:
 - Dietary goal of 2000 calories
 - Weight loss goal

#### Question:

If I ate 1800 calories today (net -200), with no calories burned from exercise, have I met my dietary goal of losing weight??

#### Query:
In this query, we first find the guideline candidates (`?guideline`) to answer this question. After that, we find the associated cohort, and the type of its members. Because of the question ('...have I met my dietary goal...'), we only consider guidelines that are have some restriction based on `pgo:hasWeightGoal`. We then test if guideline is applicable to the current user (in this example, `individuals:NamirXiaUser`). Finally, we find the target of the recommendation (`?recTarget`) and test if the user has satisfied the recommendation.

In SPARQL on the inferred ontology, run:
```sparql
SELECT DISTINCT ?guideline ?recommendation ?goalMet WHERE {
	?guideline a pgo:Guideline ;
		rdf:type ?restriction .

	# Find guideline restriction (?guideline appliesTo some ?cohort)
	?restriction a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom/owl:hasValue ?cohort .

	# Find cohort restraint (?cohort 'has member' some ?userConstraint)
	?cohort rdf:type ?p .
	?p a owl:Restriction ;
		owl:onProperty lcc-lr:hasMember ;
		owl:someValuesFrom ?userConstraint .

	# Only consider user constraints that restrict based on weight goal (?userConstraint 'equivalent to' hasWeightGoal *)
	?userConstraint owl:equivalentClass ?userFilt .
	?userFilt a owl:Restriction ;
		owl:onProperty pgo:hasWeightGoal .

	# Find target of recommendation
	?guideline pgo:recommends ?recommendation .
	# (recommendation recommends some ?recTarget)
	?recommendation a ?recRestriction .
	?recRestriction a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom ?recTarget .
	
	# The following part requires the inferred axioms
	# Only consider guidelines that are applicable to the user
	individuals:NamirXiaUser a ?userConstraint .

	# Find if the user has satisfied the recommendation
	BIND(EXISTS {
		individuals:NamirXiaUser a ?recTarget .
	} as ?goalMet) .
}
```

After running the above query, `?goalMet` will be bound to whether or not the user has satisfied the recommendation.

### Competency Question 3.

#### Context:
 - Has Type-2 diabetes

#### Question:

What carbohydrates should I be eating?

#### Query:
To answer this, we first find guideline candidates (`?guideline`) to answer the question. We then find the associated cohort, and the type of its members, and check if the current user (`individuals:JaneSmithUser`) matches. Because of the question ('what carbohydrates'), we only consider guidelines that recommend something marked as applying to `pgo:Carbohydrate`. Finally, we use other parts of the question ('eating') to only consider guidelines that recommend eating something, and extract the things that it suggests to eat (`?food`).

In SPARQL:
```sparql
SELECT DISTINCT ?guideline ?recommendation ?food WHERE {
	?guideline a pgo:Guideline ;
		rdf:type ?restriction .

	# Find guideline restriction (?guideline appliesTo some ?cohort)
	?restriction a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom/owl:hasValue ?cohort .

	# Find cohort restraint (?cohort 'has member' some ?userConstraint)
	?cohort rdf:type ?p .
	?p a owl:Restriction ;
		owl:onProperty lcc-lr:hasMember ;
		owl:someValuesFrom ?userConstraint .
	?guideline pgo:recommends ?recommendation .

	# Match recommendations relevant to carbohydrates (?recommendation appliesTo Carbohydrate)
	?recommendation a ?recommendationFilt1 .
	?recommendationFilt1 a owl:Restriction ;
		owl:onProperty fiboRelations:appliesTo ;
		owl:someValuesFrom pgo:Carbohydrate .
  
	# Match recommendations relevant to eating (?recommendation recommends some (eats some ?eatTarget))
	?recommendation a ?recommendationFilt2 .
	?recommendationFilt2 a owl:Restriction ;
		owl:onProperty pgo:recommends ;
		owl:someValuesFrom ?recTarget .
	?recTarget a owl:Restriction ;
		owl:onProperty pgo:eats ;
		owl:someValuesFrom ?eatTarget .
	
	# The following part requires the inferred axioms
	# Only consider guidelines that apply to the user
	individuals:JaneSmithUser a ?userConstraint .
	
	# Find food items that are being recommended to eat
	?food a ?eatTarget .
}
```

After running the above query, (`?food`) is bound to the food items that the guidelines suggest eating.
