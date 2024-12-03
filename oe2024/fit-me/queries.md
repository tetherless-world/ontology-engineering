# CC1
```
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMeIndividual/>

SELECT DISTINCT ?planner ?exercise ?strainValue
WHERE { 
  # Get all plan the user is focused on
  ind:User2 ex:focus ?planner .

  # Match exercises associated with the users plan
  ?planner ex:containsExercise ?exercise .

  # Get the strain value for each exercise
  ?exercise ex:hasStrainValue ?strainValue .

  # Get the preferred strain from the current Goal
  ind:StrengthGain ex:preferredStrain ?preferredStrain .

  # Get the user's injury
  ind:User1 ex:hasInjury ?injury .

  # Get the muscle group affected by the injury
  ?injury ex:affects ?affectedMuscleGroup .

  # Get the muscle group targeted by the exercise
  ?exercise ex:targets ?targetedMuscleGroup .

  # Filter exercises whose strain matches the prefered
  FILTER(?strainValue = ?preferredStrain)

  # Exclude exercises targeting affected muscle groups
  FILTER NOT EXISTS { 
    ?exercise ex:targets ?targetedMuscleGroup . 
    ?injury ex:affects ?targetedMuscleGroup 
  }
}
GROUP BY ?planner ?exercise ?strainValue
```

# CC2

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
  ind:User2 ex:focus ?planner .

  ?planner ex:containsExercise ?exercise .

  # Get the strain value for each exercise
  ?exercise ex:hasStrainValue ?strainValue .

  # Get the preferred strain from the current Goal
  ind:StrengthGain ex:preferredStrain ?preferredStrain .

  # Filter exercises whose strain matches the prefered
  FILTER(?strainValue = ?preferredStrain)
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