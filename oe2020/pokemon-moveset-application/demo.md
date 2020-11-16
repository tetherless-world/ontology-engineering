---
---

## Static Demo
### Query Prefix:
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

### Competency Questions

#### Competency Question 1

- Question: 
How can the Pokémon species Noivern learn the moves Hurricane, Draco Meteor, Air Slash, and Defog?

- Query:
```sparql
SELECT DISTINCT ?move_name ?method_name ?method_info {
    pkm-mvs-ind:Noivern a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:rest*/rdf:first/owl:hasValue ?move.
    ?move a pkm-mvs:Move.
    ?move rdfs:label ?move_name.
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?method.
      ?method a owl:Class.
      ?method rdfs:label ?method_name.
    }
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?r2.
      ?r2 owl:onProperty pkm-mvs:hasAssociatedMoveSource.
      ?r2 owl:hasValue / rdfs:label ?method_info.
    }
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?r2.
      ?r2 owl:onProperty pkm-mvs:hasLevel.
      ?r2 owl:someValuesFrom / owl:intersectionOf / rdf:rest* / rdf:first / owl:hasValue ?method_info. 
    }
    FILTER (?move_name = "Hurricane" || ?move_name = "Draco Meteor" || ?move_name = "Air Slash" || ?move_name = "Defog")
}
```

#### Competency Question 2

- Question:
Are the Pokémon species Hydreigon and Braviary compatible breeding
partners?

- Query:
```sparql
SELECT DISTINCT ?move_name ?method_name ?method_info {
    pkm-mvs-ind:Noivern a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:rest*/rdf:first/owl:hasValue ?move.
    ?move a pkm-mvs:Move.
    ?move rdfs:label ?move_name.
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?method.
      ?method a owl:Class.
      ?method rdfs:label ?method_name.
    }
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?r2.
      ?r2 owl:onProperty pkm-mvs:hasAssociatedMoveSource.
      ?r2 owl:hasValue / rdfs:label ?method_info.
    }
    OPTIONAL {
      ?lis rdf:rest*/rdf:first ?r2.
      ?r2 owl:onProperty pkm-mvs:hasLevel.
      ?r2 owl:someValuesFrom / owl:intersectionOf / rdf:rest* / rdf:first / owl:hasValue ?method_info. 
    }
    FILTER (?move_name = "Hurricane" || ?move_name = "Draco Meteor" || ?move_name = "Air Slash" || ?move_name = "Defog")
}
```

#### Competency Question 3
- Question:
Is the move Fly a valid Egg Move for the Pokémon species Squirtle?

- Query:
```sparql
SELECT DISTINCT ?move_name {
    pkm-mvs-ind:Noivern a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:rest*/rdf:first/owl:hasValue ?move.
    ?move a pkm-mvs:Move.
    ?move rdfs:label ?move_name.
    ?lis rdf:rest*/rdf:first pkm-mvs:LearnByInheritance.
}
```

#### Competency Question 4
- Question:
From what Pokémon species can the Pokémon species Squirtle inherit the
move Fake Out as an Egg Move?

- Query:
```sparql
SELECT DISTINCT ?move_name ?pokemon_inherit_from {
    pkm-mvs-ind:Squirtle a ?r.
    ?r a owl:Restriction.
    ?r owl:onProperty pkm-mvs:hasLearnMethod.
    ?r owl:someValuesFrom / owl:intersectionOf ?lis.
    ?lis rdf:rest*/rdf:first/owl:hasValue ?move.
    ?move a pkm-mvs:Move.
    ?move rdfs:label ?move_name.
    ?lis rdf:rest*/rdf:first ?r2.
    ?r2 owl:onProperty pkm-mvs:inheritsMoveFrom.
    ?r2 owl:hasValue ?pokemon_inherit_from.
    FILTER (?move_name = "Fake Out")
}
```