---
---

## Static Demo
## Competency Questions
Competency Question 1.


Question:


Related to Guideline 5.27 - “5.27 All adults, and particularly those with type 2 diabetes, should decrease the amount of time spent in daily sedentary behavior. B Prolonged sitting should be interrupted every 30 min for blood glucose benefits, particularly in adults with type 2 diabetes. C.


How does this guideline recommendation apply to me?


Competency Question 2.


Question:


If I ate a burrito, pad thai, and a slice of cheesecake today, with no calories burned exercise, how should I work towards my dietary goal of losing weight?


Competency Question 3.


Context:
Has Type-2 diabetes


Question:


What carbohydrates should I be eating?

## SPARQL query to retrieve matched guideline for patient

<code>
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

  </code>
