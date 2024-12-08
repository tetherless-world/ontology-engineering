---
---

## Queries


### Competency Question 1

### What is a good workout routine I can follow if I want to lose fat and gain muscle given that I have a knee ligament injury? (Users will enter their physical condition, etc.. - for more info see scope above)

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

### Results

| exercisePlan       | exercise          |
|--------------------|-------------------|
| KLIASGBackDay      | Pullups           |
| KLIASGCardioDay    | Swimming          |
| KLIASGChestDay     | BenchPress        |
| KLIASGChestDay     | Dips              |
| KLIASGChestDay     | InclineDumbbellPress |
| KLIASGChestDay     | Pushups           |
| KLIASGLegDay       | AbCrunches        |
| KLIASGLegDay       | GluteBridge       |
| KLIASGLegDay       | RussianTwists     |
| KLIASGRecoveryDay  | AbCrunches        |
| KLIASGRecoveryDay  | BenchPress        |
| KLIASGRecoveryDay  | Dips              |
| KLIASGRecoveryDay  | GluteBridge       |
| KLIASGRecoveryDay  | InclineDumbbellPress |
| KLIASGRecoveryDay  | Plank             |
| KLIASGRecoveryDay  | Pullups           |
| KLIASGRecoveryDay  | Pushups           |
| KLIASGRecoveryDay  | Superman          |
| KLIASGRecoveryDay  | Swimming          |
| KLIASGRecoveryDay  | WallAngles        |




### Competency Question 2
###   What are good workouts to build strength? (Users will enter their physical condition, etc.. - for more info see scope above)

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

### Results

| plan      | exercise                |
|-----------|-------------------------|
| BackDay   | BentOverBarbellRows     |
| BackDay   | BicepCurls              |
| BackDay   | CableRows               |
| BackDay   | DumbbellRows            |
| BackDay   | FacePulls               |
| BackDay   | LatPulldowns            |
| BackDay   | LatPullovers            |
| BackDay   | Pullups                 |
| BackDay   | SeatedRows              |
| ChestDay  | BenchPress              |
| ChestDay  | Dips                   |
| ChestDay  | InclineDumbbellPress   |
| ChestDay  | LateralRaises          |
| ChestDay  | OverheadShoulderPress  |
| ChestDay  | Pushups                |
| ChestDay  | TricepPushdowns        |
| LegDay    | AbCrunches             |
| LegDay    | BarbellBackSquats      |
| LegDay    | BulgarianSplitSquats   |
| LegDay    | GluteBridge            |
| LegDay    | HeavyFrontSquat        |
| LegDay    | RomanianDeadlifts      |
| LegDay    | RussianTwists          |
| LegDay    | SeatedLegExtensions    |


### Competency Question 3
### I’m looking into enforcing my back. Can you provide me with a back workout given I have a back injury? (User has already stated that they have scoliosis when creating their profile. System knows that the user has this condition.)

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

### Results

| planner            | exercise                | strainValue
|--------------------|-------------------------|---------------
|BackDay              | DumbellRows            |  Moderate
|BackDay              | LatPulldowns           |  Moderate
|BackDay              | SeatedRows             |  Moderate
|BackDay              | BentOverBarbellRows    |  Strenuous
