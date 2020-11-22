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
	?awards movie:hasAwardProductionType ?productionType .
    ?movies movie:hasAward ?awards .
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
	{
		SELECT ?genres (count(?genres) as ?count)
		WHERE {
			movieind:JohnDoe movie:hasWatchList ?watchlist .
		  	?watchlist movie:hasMovie ?movies .
		  	?movies movie:hasGenre ?genres .
		}
		GROUP BY ?genres
		ORDER BY DESC(?count) LIMIT 2
	}
    ?subgenre rdfs:subClassOf ?genres
}
GROUP BY ?subgenre
HAVING (COUNT(?subgenre) > 1)
```

#### Description
This query is looking for genres it thinks that this user will enjoy. It will do this by looking at this user's 2 most frequent genres and recommending any subgenres that fall under those genres. The first subquery's goal is to find the user's top 2 genres. The subquery's first line under the WHERE clause gets John's watch list, an individual. The second line gets the movies within the watch list and puts them under the variable ?movies. The last line gets all of the genres of these movies. This subquery is grouped by and ordered by the genres, limited to just 2. This makes the subquery only return the top two genres in the user's watch list. Finally, the outer query finds all subgenres of those top two genres, and returns the ones that appear twice. The implication of this is that any subgenre that appears twice is a subgenre of both of the two genres inputted, meaning that this particular subgenre will combine the user's top two genres, and thus be a solid recommendation.

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

SELECT  DISTINCT ?movies ?service
WHERE {
	{
		SELECT ?productionType (count(?productionType) as ?count)
		WHERE {
			movieind:DamienChazelle fibo:playsActiveRoleIn ?refMovies .
        	?refMovies movie:hasProductionType ?productionType
		}
		GROUP BY ?productionType
		ORDER BY DESC(?count) LIMIT 1
  	}
  	?movies movie:hasProductionType ?productionType .
	?movies movie:isAvailableNow ?service
}
```

#### Description
This query is looking for movies that the user may enjoy given that they like the director Damien Chazelle, which it will do by finding movies that share the same production type as Damien Chazelle movies. The subquery under the WHERE clause finds production types of movies that Damien Chazelle has contributed to. It loads the most common production type into the ?productionType variable. That variable is then used in the next line to find movies that share that production type, loading said movies into the ?movies variable. Finally, the associated streaming sites are found and returned alongside the movies.


## Past Queries

- [Version 1 (OE 10)](https://drive.google.com/file/d/1e3-frVlfwR_ziNd705hhe3taYXnW639k/view?usp=sharing)
