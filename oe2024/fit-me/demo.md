---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

### Prefixes

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/Individuals/>
PREFIX ind2: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe/Individuals#>
PREFIX ex: <https://tw.rpi.edu/ontology-engineering/oe2024/FitMe#>
PREFIX ex2: <http://purl.obolibrary.org/obo/FOODON_0340079>
```
### Competency Question 1

### What is a good workout routine I can follow if I want to lose fat and gain muscle given that I have a knee injury? (Users will enter their age, weight, height, sex, physical condition, etc..)

#### Query 1: SPARQL Query to fetch workout cycle aimed for muscle gain with knee injury. Note that these have been separated for ease of viewing. These are put together using UNION.


if((targets back && strainValue light)) Put in Pull section Section(Limit to 2)

```sparql
select ?workout where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:hasStrainValue ind2:Light .
  ?workout ex:targets ind2:BackMuscles .
} LIMIT 2
```
if(targets bicep) put in Pull section(Limit to 2)
```sparql
select ?workout where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind2:Biceps .
} LIMIT 2

```
if(targets chest) Put in push section(limit to 2)
```sparql
select ?workout where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind2:ChestMuscles .
} LIMIT 2

```


if(targets tricep) Put in push section(Limit to 2)
```sparql
select ?workout where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind2:Triceps .
} LIMIT 2

```
If(targets quads) Put in legs(Limit to 2)
```
select ?workout where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind:Quadriceps .
} LIMIT 2
```

If(targets hamstrings || targets glutes) Put in legs(Limit to 2)
if(AerobicExercise) Put one in each group
if(targets abdominal muscle) Put one in each group
```
select ?workout where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind:Abs .
} LIMIT 2

```
if(AerobicExercise && strainValue light) Put in Active Recovery(Limit to 2)

```
select ?workout where{
  ?workout rdf:type ex:AerobicExercise .
  ?workout ex:hasStrainValue ind2:Light .
} LIMIT 2
```

if(targets back && !strainValue light) in the do not section(Limit to 4 exercises)

```
select ?workout ?strain where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind2:BackMuscles .
  ?workout ex:hasStrainValue ?strain .
  FILTER (?strain != ind2:Light)
}
```

### Competency Question 2
###  I’m looking into strengthening my back. Can you provide me with a back workout? (User has already stated that they have scoliosis when creating their profile. System knows that the user has this condition.)

#### Query 2: SPARQL Query to fetch workout plan aimed at strengthening back

PULL 1
```sparql
SELECT ?workout
WHERE {
  {
    SELECT ?workout WHERE {
      ?workout rdf:type ex:Exercise .
      ?workout ex:hasStrainValue ind2:Light .
      ?workout ex:targets ind2:BackMuscles .
    } LIMIT 2
  }
  UNION
  {
    SELECT ?workout {
  ?workout rdf:type ex:Exercise .
  {
    ?workout ex:targets ind2:Biceps .
     
  }MINUS{
     ?workout ex:targets ind2:BackMuscles .
  }
}LIMIT 2
  }
}
```
PULL 2
```sparql
SELECT ?workout
WHERE {
  {
    SELECT ?workout WHERE {
      ?workout rdf:type ex:Exercise .
      ?workout ex:hasStrainValue ind2:Light .
      ?workout ex:targets ind2:BackMuscles .
    } LIMIT 4
OFFSET 2
  }
  UNION
  {
    SELECT ?workout {
  ?workout rdf:type ex:Exercise .
  {
    ?workout ex:targets ind2:Biceps .
     
  }MINUS{
     ?workout ex:targets ind2:BackMuscles .
  }
}LIMIT 4
OFFSET 2
  }
}
```
DO NOT
```sparql
select ?workout ?strain where{
  ?workout rdf:type ex:Exercise .
  ?workout ex:targets ind2:BackMuscles .
  ?workout ex:hasStrainValue ?strain .
  FILTER (?strain != ind2:Light)
}
```

### Competency Question 3
### I’m looking to develop strong legs. Can you provide me with a leg workout? (User has already stated that they have a mild leg strain when creating their profile. The system knows that the user has this condition.)

#### Query 3: SPARQL query to fetch workout plan despite stated injury.

```sparql
SELECT ?workout
WHERE {
  {
    SELECT ?workout WHERE {
      ?workout rdf:type ex:Exercise .
      ?workout ex:hasStrainValue ?strain .
      FILTER (?strain != ind2:Light) .
      ?workout ex:targets ind2:Quadriceps .
    } LIMIT 2
  }
  UNION
  {
    SELECT ?workout {
  ?workout rdf:type ex:Exercise .
  {
    ?workout ex:targets ind2:GluteusMaximus .
     
  }MINUS{
     ?workout ex:targets ind2:Quadriceps .
  }
}LIMIT 2

  }
}

SELECT ?workout
WHERE {
  {
    SELECT ?workout WHERE {
      ?workout rdf:type ex:Exercise .
      ?workout ex:hasStrainValue ?strain .
      FILTER (?strain != ind2:Light) .
      ?workout ex:targets ind2:Quadriceps .
    } LIMIT 4
      OFFSET 2
  }
  UNION
  {
    SELECT ?workout {
  ?workout rdf:type ex:Exercise .
  {
    ?workout ex:targets ind2:GluteusMaximus .
     
  }MINUS{
     ?workout ex:targets ind2:Quadriceps .
  }
}LIMIT 4
OFFSET 2
  }
}
```