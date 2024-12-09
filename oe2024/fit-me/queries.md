# Competency Question 1
```
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMeIndividuals/>

# Routine for fat loss, muscle gain for a user having Knee ligament injury
select DISTINCT ?exercisePlan ?exercise where {
  BIND (ex:KneeLigamentInjuryAgnosticStrengthGainPlan AS ?plan).
  ?exercisePlan rdfs:subClassOf ?plan.
  ?exercise a ?exercisePlan.
}
```

# Competency Question 2

```
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMeIndividuals/>


# workouts and plan to build strength 
select ?plan ?exercise where { 
	?plan a ex:StrengthGainPlan .
  	?exercise ex:exerciseContainedIn ?plan .
}
```
# Competency Question 3

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMeIndividuals/>


PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>


# Routine for fat loss, muscle gain for a user having Knee ligament injury
select ?exercise where { ?exercise a ex:EnforceBackPlan. }
```

# Competency Question 4
```
# Start gaining muscle

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMeIndividuals/>

select ?exercise where {
    ?exercise a ex:StrengthExercise. 
}

```

# Competency Question 5
```
# looking to develop strong legs

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMeIndividuals/>

select ?exercise where {
    ?exercise a ex:LegStrengtheningExercise. 
}
```