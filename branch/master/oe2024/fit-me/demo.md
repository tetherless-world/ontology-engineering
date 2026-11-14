---
---

## Queries

### How to Run 

- Please note that all queries were executed using Blazegraph
- To run the queries yourself please use our inferred reasoner axiom ontology at the following link: [FitMeReasonerAxioms](https://github.com/tetherless-world/ontology-engineering/blob/fit-me/oe2024/fit-me/FitMeReasonerAxioms.rdf).


### Competency Question 1

### What is a good workout routine I can follow if I want to lose fat and gain muscle given that I have a knee ligament injury? (Users will enter their physical condition, etc.. - for more info see scope above)

```
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>

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
PREFIX rdf: <http://www.w3.org/1999/02/22/rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>

select ?exercise where { 
  ?exercise a ex:EnforceBackPlan.
}
```

### Results

| Exercise |
|---|
|CableRows|
|FacePulls|
|LatPullovers|
|Pullups|


### Competency Question 4
### I’m looking to start gaining muscle. Provide me with a workout cycle. (Users will enter their physical condition, etc.. - for more info see scope above)

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>

select ?exercise where {
    ?exercise a ex:StrengthExercise. 
}
```

### Results

| Exercise |
|---|
| AbCrunches |
| Barbell Back Squats |
| Bench Press |
| Bent-Over Barbell Rows |
| Bicep Curls |
| Bulgarian Split Squats |
| Cable Rows |
| Deadlifts |
| Dips |
| Dumbbell Rows |
| Face Pulls |
| Glute Bridge |
| Heavy Front Squat |
| Incline Dumbbell Press |
| Lateral Raises |
| Lat Pulldowns |
| Lat Pullovers |
| Overhead Shoulder Press |
| Plank |
| Pullups |
| Pushups |
| Romanian Deadlifts |
| Russian Twists |
| Seated Leg Extensions |
| Seated Rows |
| Superman |
| Tricep Pushdowns |
| Wall Sit |


### Competency Question 5
### I’m looking to develop strong legs. Can you provide me with a leg workout? (Users will enter their physical condition, etc.. - for more info see scope above)

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/FitMe/>

select ?exercise where {
    ?exercise a ex:LegStrengtheningExercise. 
}
```

### Results

| Exercise |
|---|
| Barbell Back Squats |
| Bulgarian Split Squats |
| Deadlifts |
| Heavy Front Squat |
| Romanian Deadlift |
| Seated Leg Extensions |