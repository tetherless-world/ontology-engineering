---
---

## Static Demo

[Link to queries as text file](https://drive.google.com/file/d/1mKtpEp7tK0hTFoiK2vOG5S2LMqf4WQKo/view?usp=sharing)

### Competency Question 1 Demo Query

#### Question
What’s a movie I can watch given that I recently watched “The Farewell”?

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

#### Description
This query is looking for movies that the user may enjoy given that they enjoyed "The Farewell". This particular query aims to achieve that goal by finding award winning movies of the same production type. The first line in the WHERE clause determines the production type of "The Farewell" and puts it into the ?productionType variable. The second line uses that variable to find all awards that share that particular production type, putting it into the ?awards variable. Those awards are then used in the third line to find the movies that are associated with those awards, as each award is associated with one movie (the award refers to one instance of an award, not the general award). Finally, the last line takes the movies that have been queried and finds the services they are streaming on in order to make watching them faster for the user.

### Competency Question 2 Demo Query

#### Question
What action movie can I watch that Alexis enjoyed?

#### Answer
Captain America (2010), watch on Disney Plus

#### Query
```sparql
PREFIX movie: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/>
PREFIX movieind: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/>
PREFIX fibo-fnd-arr-arr: <https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Arrangements/>
PREFIX fibo-fnd-arr-rt: <https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Ratings/>

SELECT ?movies ?service
WHERE {
    {
        SELECT ?movies ?scores
        WHERE {
            movieind:AlexisFord movie:hasWatchList ?watchlist .
            ?watchlist fibo-fnd-arr-arr:hasConstituent ?entries .
            ?entries fibo-fnd-arr-rt:hasRating ?reviews .
            ?reviews fibo-fnd-arr-rt:rates ?movies .
            ?reviews fibo-fnd-arr-rt:hasRatingScore ?scoresRaw .
            ?scoresRaw fibo-fnd-arr-rt:hasMeasureWithinScale ?scores .
            FILTER(?scores > 8)
        }
    }
    ?movies movie:hasGenre movie:Action .
    ?movies movie:isAvailableNow ?service .
    movieind:JohnDoe movie:hasWatchList ?userWatchlist .
    FILTER NOT EXISTS {
        ?userWatchlist movie:hasMovie ?movies
    }
}
```

#### Description
This query will look at Alexis's watched movies and find high rated movies that John can watch. The first subquery is based around finding high rated movies from Alexis, with the first line obtaining her watchlist, the second line obtaining the entries, the third line obtaining the reviews, and the last ones obtaining a measurable metric for the score. Only movies that have been rated higher than an 8 are returned. The first line in the outer query ensures that returned movies are of the "action" genre, and the second one finds the services that the returned movies are available on. Finally, John's watchlist is retrieved and the previously return movies are filtered to ensure that they don't have any repeats with John's watchlist.

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

### Competency Question 5 Demo Query

#### Question
What movie should I watch given that I just watched "Captain America" and "Thor: Ragnarok"?

#### Answer
Iron Man (2008), watch on Disney Plus

#### Query
```sparql
PREFIX movie: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender/>
PREFIX movieind: <https://tw.rpi.edu/ontology-engineering/oe2020/movie-recommender-individuals/>
PREFIX lcc-cr: <https://www.omg.org/spec/LCC/Countries/CountryRepresentation/>

SELECT ?recMovies ?service
WHERE {
    {
        SELECT ?universes
        WHERE {
            movieind:AlexisFord movie:hasWatchList ?watchlist .
            ?watchlist movie:hasMovie ?movies .
            ?movies lcc-cr:isPartOf ?universes
        }
        GROUP BY ?universes
        ORDER BY DESC(COUNT(?universes)) LIMIT 1
    }
    ?recMovies lcc-cr:isPartOf ?universes .
    ?recMovies movie:isAvailableNow ?service
    FILTER NOT EXISTS {
        ?watchlist movie:hasMovie ?recMovies
    }
}
```

#### Description
This query is looking for movies that the user may enjoy given that they have watched some Marvel movies recently. To simulate this, we have placed two Marvel movies into the watchlist for Alexis Ford. The first line of the first subquery obtains Alexis's watchlist, and keeps it as the ?watchlist variable. The second line of the first subquery extracts all movies in Alexis's watchlist and puts them under the ?movies variable. Finally, the third line gets all cinematic universes that the returned movies are part of. The subquery only returns the most popular universe, being that it orders by the number of appearances and limits it to one. The outer query then takes that universe and finds all movies that are a part of that universe. Finally, the query determines which of those movies have not been watched by the user already, and returns those.

## Past Queries

- [Version 2 (OE 11)](https://drive.google.com/file/d/1u_zF-2vJrH20QNwAfoO6fqJ8zfzp7tVN/view?usp=sharing)
- [Version 1 (OE 10)](https://drive.google.com/file/d/1e3-frVlfwR_ziNd705hhe3taYXnW639k/view?usp=sharing)
