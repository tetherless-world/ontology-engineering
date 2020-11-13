---
---

## Static Demo

- Competency Question 1 Demo Query
```
SELECT DISTINCT ?movies ?service
WHERE
{
	<https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/TheFarewell> <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasProductionType> ?productionType .
	?award <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasAwardProductionType> ?productionType .
    ?movies <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasAward> ?award .
	?movies <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/isAvailableNow> ?service  
}
```
- Competency Question 3 Demo Query
```
SELECT DISTINCT ?subgenre
WHERE
{
	<https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/JohnDoe> <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasWatchList> ?watchlist .
  	?watchlist <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasMovie> ?movies .
  	?movies <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasGenre> ?genres .
    ?subgenre rdfs:subClassOf ?genres
}
GROUP BY ?subgenre
HAVING (COUNT(?subgenre) > 1)
```
- Competency Question 4 Demo Query
```
SELECT DISTINCT ?movies ?service
WHERE
{
	<https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/DamienChazelle> <https://spec.edmcouncil.org/fibo/ontology/FND/Parties/Parties/playsActiveRoleIn> ?refMovies .
	?refMovies <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasProductionType> ?productionType .
  	?movies <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/hasProductionType> ?productionType .
  	?movies <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/isAvailableNow> ?service
}
```
