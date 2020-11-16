---
---

## Static Demo

### Competency Question 1 Demo Query

#### Question
What’s a quick movie I can watch given that I recently watched “The Farewell”?

#### Answer
The Miseducation of Cameron Post (2018), watch on Netflix

#### Query
```sparql
PREFIX movie: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/>
PREFIX movieind: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/>

SELECT DISTINCT ?movies ?service
WHERE {
	movieind:TheFarewell movie:hasProductionType ?productionType .
	?award movie:hasAwardProductionType ?productionType .
    ?movies movie:hasAward ?award .
	?movies movie:isAvailableNow ?service  
}
```

### Competency Question 3 Demo Query

#### Question
Given my watch history, what genres should I explore?

#### Answer
Physical Comedy

#### Query
```sparql
PREFIX movie: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/>
PREFIX movieind: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/>

SELECT DISTINCT ?subgenre
WHERE {
	movieind:JohnDoe movie:hasWatchList ?watchlist .
  	?watchlist movie:hasMovie ?movies .
  	?movies movie:hasGenre ?genres .
    ?subgenre rdfs:subClassOf ?genres
}
GROUP BY ?subgenre
HAVING (COUNT(?subgenre) > 1)
```

### Competency Question 4 Demo Query

#### Question
What movie should I watch if I like movies by Damien Chazelle?

#### Answer
A Star is Born (2018), watch on Hulu

#### Query
```sparql
PREFIX movie: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/>
PREFIX movieind: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/>
PREFIX fibo: <https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Parties/>

SELECT DISTINCT ?movies ?service
WHERE {
	movieind:DamienChazelle fibo:playsActiveRoleIn ?refMovies .
	?refMovies movie:hasProductionType ?productionType .
  	?movies movie:hasProductionType ?productionType .
  	?movies movie:isAvailableNow ?service
}
```
