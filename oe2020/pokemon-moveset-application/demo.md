---
layout: default
title: Demo
---

## Static Demo
### Competency Questions
- Download the SPARQL Queries [Here](https://docs.google.com/document/d/e/2PACX-1vTb4omkqTUynXymTeJoXFfCMVGgHn8uaWEtyWHdxQpGRgj2FLY9uo-Wf1lDME4C1ruiZvYSFEjnKJEi/pub)

#### Query Prefixes:
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

Assembling a team of Pokémon that know specific moves is the core idea of the Pokémon Moveset Ontology, but it is not always straightfoward to get a Pokémon that knows certain moves, as there are multiple ways a Pokémon can learn a move. This query returns information on how Noivern can learn each one of these moves, for each one it can:

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

The most complex method of learning a move is the "learning through inheritance" method. In order for a Pokémon to learn a Move through inheritance, specific parent Pokémon must be bred together--and in order for two Pokémon to breed, they must be compatible breeding partners (in the same egg group). To be as applicable as possible, we designed this query to return all compatible breeding partners of Hydreigon:

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

The above query answers the more general question of *“What are the compatible breeding partners of Hydreigon?”*, as we think it useful to demonstrate how to do this, and since Noivern is included in the list, it answers the question of whether Hydreigon and Noivern can breed. Alternatively, to only return true or false if Hydreigon and Noivern can breed, we can use the following query:

- **Query:**
```sparql
SELECT ?can_breed WHERE {
    BIND(EXISTS{
        pkm-mvs-ind:Hydreigon pkm-mvs:hasEggGroup ?egg_group.
        pkm-mvs-ind:Noivern pkm-mvs:hasEggGroup ?egg_group.
    } AS ?can_breed)
}
```

- **Results:**

| can_breed  |
|:----------:|
|True        |

#### Competency Question 3
- **Question:**
*Is the move Defog a valid Egg Move for the Pokémon species Noivern?*

An Egg Move is a move which is learned through inheritance and breeding. This query returns *all* valid Egg Moves for the Pokémon species Noivern:

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

We can add a filter to the above query to return *just* Defog if it is a valid Egg Move for the Pokémon species Noivern:

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
FILTER (?move = pkm-mvs-ind:Defog)
}
```

- **Results:**

|    move    |
|:----------:|
|Defog       |

#### Competency Question 4

- **Question:**
*From what Pokémon species can the Pokémon species Noibat inherit the move Defog as an Egg Move?*

An Egg Move is a move which is learned through inheritance and breeding. This query returns chains of different Pokémon that you can breed successively in order to eventually get a Noibat which knows the move Defog.

- **Query:**
```sparql
SELECT DISTINCT ?move_name ?PSTART ?p1 ?p2 ?p_end WHERE {
    BIND(pkm-mvs-ind:Noibat AS ?PSTART) #PSTART == starting pokemon
    BIND(pkm-mvs-ind:Defog AS ?MOVE)     #MOVE == move to learn  
  
    #Confirm that PSTART can learn this MOVE by inheritance
    ?PSTART a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:rest*/rdf:first/owl:hasValue ?MOVE. 
    ?MOVE rdfs:label ?move_name.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis2.
    ?lis2 rdf:rest*/rdf:first pkm-mvs:LearnByInheritance.
  
    # Try to end chain here; if cannot, start making chain
    # (Can end chain if p_end learns MOVE via level-up)
    {
      ?PSTART pkm-mvs:hasEggGroup /^ pkm-mvs:hasEggGroup ?p_end.
      ?p_end a ?r_pend.
      ?r_pend a owl:Restriction.
      ?r_pend owl:onProperty pkm-mvs:hasLearnMethod.
      ?r_pend owl:someValuesFrom / owl:intersectionOf ?lis_pend.
      ?lis_pend rdf:rest*/rdf:first/owl:hasValue ?MOVE. 
      ?MOVE rdfs:label ?move_name.
      ?r_pend owl:someValuesFrom / owl:intersectionOf ?lis_pend2.
      ?lis_pend2 rdf:rest*/rdf:first pkm-mvs:LearnByLevelUp.
    } UNION {
      #Get p1 (First link in chain)
      ?PSTART pkm-mvs:hasEggGroup /^ pkm-mvs:hasEggGroup ?p1.
      ?p1 a ?r1.
      ?r1 a owl:Restriction.
      ?r1 owl:onProperty pkm-mvs:hasLearnMethod.
      ?r1 owl:someValuesFrom / owl:intersectionOf ?lis1.
      ?lis1 rdf:rest*/rdf:first/owl:hasValue ?MOVE. 
      ?MOVE rdfs:label ?move_name.
      ?r1 owl:someValuesFrom / owl:intersectionOf ?lis_1.
      ?lis_1 rdf:rest*/rdf:first pkm-mvs:LearnByInheritance.
      
      # Try to end chain here; if cannot, start making chain
      # (Can end chain if p_end learns MOVE via level-up)
      {
        ?p1 pkm-mvs:hasEggGroup /^ pkm-mvs:hasEggGroup ?p_end.
        ?p_end a ?r_pend.
        ?r_pend a owl:Restriction.
        ?r_pend owl:onProperty pkm-mvs:hasLearnMethod.
        ?r_pend owl:someValuesFrom / owl:intersectionOf ?lis_pend.
        ?lis_pend rdf:rest*/rdf:first/owl:hasValue ?MOVE. 
        ?MOVE rdfs:label ?move_name.
        ?r_pend owl:someValuesFrom / owl:intersectionOf ?lis_pend2.
        ?lis_pend2 rdf:rest*/rdf:first pkm-mvs:LearnByLevelUp.
      } UNION {
        #Get p1 (First link in chain)
        ?p1 pkm-mvs:hasEggGroup /^ pkm-mvs:hasEggGroup ?p2.
        ?p2 a ?r2.
        ?r2 a owl:Restriction.
        ?r2 owl:onProperty pkm-mvs:hasLearnMethod.
        ?r2 owl:someValuesFrom / owl:intersectionOf ?lis2__.
        ?lis2__ rdf:rest*/rdf:first/owl:hasValue ?MOVE. 
        ?MOVE rdfs:label ?move_name.
        ?r2 owl:someValuesFrom / owl:intersectionOf ?lis_2.
        ?lis_2 rdf:rest*/rdf:first pkm-mvs:LearnByInheritance.

        ?p2 pkm-mvs:hasEggGroup /^ pkm-mvs:hasEggGroup ?p_end.
        ?p_end a ?r_pend.
        ?r_pend a owl:Restriction.
        ?r_pend owl:onProperty pkm-mvs:hasLearnMethod.
        ?r_pend owl:someValuesFrom / owl:intersectionOf ?lis_pend.
        ?lis_pend rdf:rest*/rdf:first/owl:hasValue ?MOVE. 
        ?MOVE rdfs:label ?move_name.
        ?r_pend owl:someValuesFrom / owl:intersectionOf / rdf:rest*/rdf:first pkm-mvs:LearnByLevelUp.
        
        FILTER (?p1 != ?p2 && ?PSTART != ?p2).
      }
      
      FILTER (?PSTART != ?p1).
    }
}
```

- **Results:**

|    move_name    |   PSTART    |    p1    |    p2    |    p_end    |
|:---------------:|:-----------:|:--------:|:--------:|:-----------:|
|Defog            |Noibat       |          |          |Rufflet      |
|Defog            |Noibat       |          |          |Braviary     |
|Defog            |Noibat       |Noivern   |          |Rufflet      |
|Defog            |Noibat       |Noivern   |          |Braviary     |

p2 is empty, but we still return it here to show that we can return longer and longer chains of Pokemon to inherit from.

#### Competency Question 5
- **Question:**
*How can you obtain the Pokémon Rufflet?*

In order to get a Pokémon with moves you want, you first need to get the Pokémon. There are usually multiple different ways to obtain a member of a specific Pokémon species--this query returns all methods to obtain Rufflet:

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
