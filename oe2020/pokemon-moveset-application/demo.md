---
layout: default
title: Demo
---

## Static Demo
### Competency Questions
- Download the SPARQL Queries [Here](https://docs.google.com/document/d/e/2PACX-1vTb4omkqTUynXymTeJoXFfCMVGgHn8uaWEtyWHdxQpGRgj2FLY9uo-Wf1lDME4C1ruiZvYSFEjnKJEi/pub)

#### Query Prefix:
```sparql 
PREFIX uo: <http://purl.obolibrary.org/obo/UO_> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX sio: <http://semanticscience.org/resource/> 
PREFIX dct: <http://purl.org/dc/terms/> 
PREFIX xml: <http://www.w3.org/XML/1998/namespace> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX valo: <http://purl.org/ontology/validation/ont#> 
PREFIX val-kb: <http://purl.org/ontology/validation/kb#> 
PREFIX fibo-fnd-aap-agt: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/Agents/>
PREFIX fibo-fnd-aap-ppl: <https://spec.edmcouncil.org/fibo/ontology/FND/AgentsAndPeople/People/>
PREFIX fibo-fnd-arr-cls: <https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/ClassificationSchemes/>
PREFIX fibo-fnd-arr-lif: <https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Lifecycles/>
PREFIX fibo-fnd-dt-fd: <https://spec.edmcouncil.org/fibo/ontology/FND/DatesAndTimes/FinancialDates/>
PREFIX fibo-fnd-dt-oc: <https://spec.edmcouncil.org/fibo/ontology/FND/DatesAndTimes/Occurrences/>
PREFIX fibo-fnd-gao-obj: <https://spec.edmcouncil.org/fibo/ontology/FND/GoalsAndObjectives/Objectives/>
PREFIX fibo-fnd-org-fm: <https://spec.edmcouncil.org/fibo/ontology/FND/Organizations/FormalOrganizations/>
PREFIX fibo-fnd-plc-loc: <https://spec.edmcouncil.org/fibo/ontology/FND/Places/Locations/>
PREFIX fibo-fnd-pty-pty: <https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Parties/>
PREFIX fibo-fnd-pty-rl: <https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Roles/>
PREFIX fibo-fnd-qt-qtu: <https://spec.edmcouncil.org/fibo/ontology/FND/Quantities/QuantitiesAndUnits/>
PREFIX fibo-fnd-rel-rel: <https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/>
PREFIX fibo-fnd-utl-alx: <https://spec.edmcouncil.org/fibo/ontology/FND/Utilities/Analytics/>
PREFIX fibo-fnd-utl-av: <https://spec.edmcouncil.org/fibo/ontology/FND/Utilities/AnnotationVocabulary/>
PREFIX lcc-cr: <https://www.omg.org/spec/LCC/Countries/CountryRepresentation/>
PREFIX lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
PREFIX sm: <http://www.omg.org/techprocess/ab/SpecificationMetadata/>
PREFIX pkm-mvs: <https://tw.rpi.edu/ontology-engineering/oe2020/pokemon-moveset/>
PREFIX pkm-mvs-ind:  <https://tw.rpi.edu/ontology-engineering/oe2020/pokemon-moveset-individuals/>
```

#### Competency Question 1

- **Question:** 
*How can the Pokémon species Noivern learn the moves Hurricane, Draco Meteor, Air Slash, and Defog?*

- **Query:**
```sparql
SELECT DISTINCT ?move ?method_name ?method_info WHERE {
    pkm-mvs-ind:Noivern a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:first / rdfs:label ?method_name.
    ?lis rdf:rest/rdf:first ?e1.
    {
        ?e1 owl:onProperty pkm-mvs:isLearnMethodFor.
        ?e1 owl:hasValue ?move.
    } UNION {
        ?lis rdf:rest/rdf:rest/rdf:first ?e2.
        ?e2 owl:onProperty pkm-mvs:isLearnMethodFor.
        ?e2 owl:hasValue ?move.
        OPTIONAL {
            {
                ?e1 owl:onProperty pkm-mvs:hasAssociatedMoveSource.
                ?e1 owl:hasValue / rdfs:label ?method_info.
            }
            UNION {
                ?e1 owl:onProperty pkm-mvs:hasLevel.
                ?e1 owl:someValuesFrom / owl:intersectionOf / rdf:rest* / rdf:first / owl:hasValue ?method_info.
             }
        }
    }
    FILTER (?move = pkm-mvs-ind:Hurricane || ?move = pkm-mvs-ind:DracoMeteor || ?move = pkm-mvs-ind:AirSlash || ?move = pkm-mvs-ind:Defog)
}
```
- **Results:**

|      move     |      method_name      |        method_info     |
|:-------------:|:---------------------:|:----------------------:|
| Hurricane     |"learn by level up"    |56                      |
| Hurricane     |"learn from item"      |"technical record #89"  |
| Draco Meteor  |"learn from move tutor"|"Ace Trainer"           |
| Air Slash     |"learn from item"      |"technical record #95"  |
| Defog         |"learn by inheritance" |                        |


#### Competency Question 2

- **Question:**
*Are the Pokémon species Hydreigon and Noivern compatible breeding
partners?*

- **Query:**
```sparql
SELECT DISTINCT ?breeding_partner_name ?egg_group_name WHERE {
    pkm-mvs-ind:Hydreigon pkm-mvs:hasEggGroup ?egg_group.
    ?breeding_partner pkm-mvs:hasEggGroup ?egg_group.
    ?breeding_partner rdfs:label ?breeding_partner_name.
    ?egg_group rdfs:label ?egg_group_name.
}
```

- **Results:**

|      breeding_partner_name     |      egg_group_name      | 
|:------------------------------:|:------------------------:|
| "Deino"                        |"Dragon egg group"        |
| "Hydreigon"                    |"Dragon egg group"        |
| "Noibat"                       |"Dragon egg group"        |
| "Zweilous"                     |"Dragon egg group"        |
| "Noivern"                      |"Dragon egg group"        |


#### Competency Question 3
- **Question:**
*Is the move Transform a valid Egg Move for the Pokémon species Noivern?*

- **Query:**
```sparql
SELECT DISTINCT ?move WHERE {
    pkm-mvs-ind:Noivern a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:rest*/rdf:first/owl:hasValue ?move.
    ?move a pkm-mvs:Move.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis2.
    ?lis2 rdf:rest*/rdf:first pkm-mvs:LearnByInheritance.
}
```

- **Results:**

|    move    |
|:----------:|
|Defog       |
|Dragon Rush |

#### Competency Question 4
- **Question:**
*How can you obtain the Pokémon Rufflet?*

- **Query:**
```sparql
SELECT DISTINCT ?method_name ?method_info WHERE {
    pkm-mvs-ind:Rufflet a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasObtainMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:first ?method.
    ?method a owl:Class.
    ?method rdfs:label ?method_name.
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?r2.
      ?r2 owl:hasValue / rdfs:label ?method_info.
    }
}
```

- **Results:**

|method_name       |method_info      |
|:----------------:|:---------------:|
|"obtain from wild"|"Lake of Outrage"|
|"obtain from wild"|"Bridge Field"   |
