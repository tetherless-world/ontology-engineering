# CC1
```
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMeIndividual/>

# Routine for fat loss, muscle gain for a user having Knee ligament injury
select DISTINCT ?exercisePlan ?exercise where {
  BIND (ex:KneeLigamentInjuryAgnosticStrengthGainPlan AS ?plan).
  ?exercisePlan rdfs:subClassOf ?plan.
  ?exercise a ?exercisePlan.
}
```

# CC2

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
# CC3

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMeIndividual/>


SELECT DISTINCT ?planner ?exercise ?strainValue
WHERE { 
  # Get all plan the user is focused on
  ind:User3 ex:focus ?planner .

  ?planner ex:containsExercise ?exercise .

  # Get the strain value for each exercise
  ?exercise ex:hasStrainValue ?strainValue .

  # Get the preferred strain from the current Goal
  ind:StrengthGain ex:preferredStrain ?preferredStrain .

  # Filter exercises whose strain matches the prefered
  FILTER(?strainValue = ?preferredStrain)
}
```