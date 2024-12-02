---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

### Prefixes

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMeIndividual/>
```
### Competency Question 1

### What is a good workout routine I can follow if I want to lose fat and gain muscle given that I have a knee ligament injury? (Users will enter their physical condition, etc.. - for more info see scope above)


```sparql
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
### Results
| Planner  | Exercise                | StrainValue  |
|----------|--------------------------|--------------|
| BackDay  | DumbbellRows            | Moderate     |
| BackDay  | LatPulldowns            | Moderate     |
| BackDay  | BentOverBarbellRows     | Strenuous    |
| BackDay  | SeatedRows              | Moderate     |
| ChestDay | InclineDumbbellPress    | Moderate     |
| ChestDay | BenchPress              | Strenuous    |
| ChestDay | LateralRaises           | Moderate     |
| ChestDay | OverheadShoulderPress   | Moderate     |
| LegDay   | RomanianDeadlifts       | Moderate     |
| LegDay   | HeavyFrontSquat         | Strenuous    |
| LegDay   | BarbellBackSquats       | Strenuous    |
| LegDay   | BulgarianSplitSquats    | Moderate     |

### Competency Question 2
###   What are good workouts to build strength? (Users will enter their physical condition, etc.. - for more info see scope above)

```sparql
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
### Results
| Planner  | Exercise                | StrainValue  |
|----------|--------------------------|--------------|
| BackDay  | DumbbellRows            | Moderate     |
| BackDay  | LatPulldowns            | Moderate     |
| BackDay  | SeatedRows              | Moderate     |
| BackDay  | BentOverBarbellRows     | Strenuous    |
| ChestDay | InclineDumbbellPress    | Moderate     |
| ChestDay | LateralRaises           | Moderate     |
| ChestDay | OverheadShoulderPress   | Moderate     |
| ChestDay | BenchPress              | Strenuous    |
| LegDay   | RomanianDeadlifts       | Moderate     |
| LegDay   | BulgarianSplitSquats    | Moderate     |
| LegDay   | HeavyFrontSquat         | Strenuous    |
| LegDay   | BarbellBackSquats       | Strenuous    |


### Competency Question 3
### I’m looking into enforcing my back. Can you provide me with a back workout given I have a back injury? (User has already stated that they have scoliosis when creating their profile. System knows that the user has this condition.)

```sparql
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

### Results
| Planner  | Exercise            | StrainValue  |
|----------|----------------------|--------------|
| BackDay  | DumbbellRows        | Moderate     |
| BackDay  | LatPulldowns        | Moderate     |
| BackDay  | SeatedRows          | Moderate     |
| BackDay  | BentOverBarbellRows | Strenuous    |
