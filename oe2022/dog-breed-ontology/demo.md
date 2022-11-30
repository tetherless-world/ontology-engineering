
## Queries
These queries are meant to be run in the SNAP SPARQL tab in Protege. They can be run with normal SPARQL, but since that doesn't use the reasoner's inferences most of the queries will not return any results.

### Query 1: What dog breed would meet the needs of a large family with allergies in a large home?
Usage scenario covered: A large family consisting of 3 kids is looking for a dog.

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX cmns-cls: <https://www.omg.org/spec/Commons/Classifiers/>
PREFIX cmns-rt: <https://www.omg.org/spec/Commons/Ratings/>
PREFIX oe2022-dogs: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet/>
SELECT ?label ?popularityQuantitativeScore ?childfriendlinesslevel ?exerciseneedslevel 
	WHERE { ?breed a oe2022-dogs:GoodForChildrenBreed;
			rdfs:label ?label.
		?char_profile a oe2022-dogs:BreedCharacteristicProfile;
			cmns-cls:characterizes ?breed;
			oe2022-dogs:displaysChildFriendlinessLevel ?childfriendlinesslevel;
			oe2022-dogs:displaysExerciseNeedsLevel ?exerciseneedslevel.
        ?popularityRating a oe2022-dogs:BreedPopularityRating;
			cmns-rt:rates ?breed;
			cmns-rt:hasRatingScore ?ratingScore.
		?ratingScore cmns-rt:hasMeasureWithinScale ?popularityQuantitativeScore.
}
ORDER BY ?popularityQuantitativeScore
```

#### Result 1:
Top 5 results shown

| label | popularityQuantitativeScore | childfriendlinesslevel | exerciseneedslevel | 
| --- | --- | --- | --- |
| labrador retriever | 1.0 | 1.0 | 1.0 |
| golden retriever | 3.0 | 1.0 | 1.0|
| german shepherd dog | 4.0 | 1.0 | 0.6 |
| great dane | 17.0 | 0.6 | 0.4 |
| pomeranian | 24.0 | 0.2 | 0.4 |

#### Explanation:
This query is specifically using the family in competancy question 1. It returns whether or not the breed is a good fit based on some of the potential characteristic of the family: since it's a large family we use good with kids (inferred based on childfriendliness), and since there are multiple children the dog will need to have high activity level (inferred based on exercise level value).

### Query 2: What dog breeds are good for students living in apartments?
Usage scenario covered: A group of 4 college students is looking to adopt a dog.

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX cmns-cls: <https://www.omg.org/spec/Commons/Classifiers/>
PREFIX cmns-cols: <https://www.omg.org/spec/Commons/Collections/>
PREFIX cmns-rt: <https://www.omg.org/spec/Commons/Ratings/>
PREFIX cmns-pts: <https://www.omg.org/spec/Commons/PartiesAndSituations/>
PREFIX oe2022-dogs: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet/>
PREFIX oe2022-dogs-ind: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet-individuals/>
select ?breedLabel ?rating
where {
oe2022-dogs-ind:Question2Student a oe2022-dogs:Student ;
 cmns-pts:playsRole ?adopter .
?adopter a oe2022-dogs:PotentialAdopter ; 
 oe2022-dogs:primarilyResidesAt ?residence . 
?residence a oe2022-dogs:Residence ;
 cmns-cols:comprises ?space .
?space a oe2022-dogs:ApartmentIndoorSpace .

?breed a oe2022-dogs:LowMaintenanceBreed ;
 a oe2022-dogs:LowExpenseBreed ;
 a oe2022-dogs:ApartmentFriendlyBreed ;
 rdfs:label ?breedLabel .

?popularityRating a oe2022-dogs:BreedPopularityRating ;
 cmns-rt:rates ?breed ;
 cmns-rt:hasRatingScore ?ratingScore .
?ratingScore cmns-rt:hasMeasureWithinScale ?rating .
}
order by ?rating
```

#### Result 2:
| breedLabel | rating |
| --- | --- |
| japanese chin | 105.0 |

#### Explanation:
This query specifically uses the person in competancy question 2 and seeing which dogs are a good fit. It returns the dogs that are a good fit based on: apartment friendliness (based on size, barking value, and stranger friendliness value), ability to care for on a low budget (based on size, initial cost, and health susceptability values), and ability to care for on minimal time (based on mental stimulation needing value, exercise needing value, and grooming value). The query returns the japanese chin. 

### Query 3: What dog breeds are good for a farm environment in Texas? 
Usage scenario covered: A family with small kids are looking for a dog to help around their farm in Texas

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX cmns-cls: <https://www.omg.org/spec/Commons/Classifiers/>
PREFIX cmns-cols: <https://www.omg.org/spec/Commons/Collections/>
PREFIX cmns-rt: <https://www.omg.org/spec/Commons/Ratings/>
PREFIX cmns-pts: <https://www.omg.org/spec/Commons/PartiesAndSituations/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX oe2022-dogs: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet/>
PREFIX oe2022-dogs-ind: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet-individuals/>
select Distinct ?breedLabel ?barkingLevel ?barkingLevelSource ?rating
where {
oe2022-dogs-ind:Question3FarmOwner a oe2022-dogs:Person ;
 cmns-pts:playsRole ?adopter .
?adopter a oe2022-dogs:PotentialAdopter ; 
 oe2022-dogs:primarilyResidesAt ?residence . 
?residence a oe2022-dogs:Residence ;
 cmns-cols:comprises ?space ;
 oe2022-dogs:isLocatedIn ?state .
?space a oe2022-dogs:OutdoorSpace .
?state oe2022-dogs:hasClimateZone ?zone .
?zone oe2022-dogs:isHotterClimateZoneThan oe2022-dogs:ClimateZone5 .

?breed a oe2022-dogs:HotClimateAppropriateBreed ;
 a oe2022-dogs:TrainableBreed ;
 a oe2022-dogs:HighExerciseNeedingBreed ;
 a oe2022-dogs:DogFriendlyBreed ;
 a oe2022-dogs:CatFriendlyBreed ;
 rdfs:label ?breedLabel .

?profile a oe2022-dogs:BreedCharacteristicProfile;
 cmns-cls:characterizes ?breed;
 prov:wasAttributedTo ?source ;
 oe2022-dogs:displaysBarkingLevel ?barkingLevel .

?source rdfs:label ?barkingLevelSource .

?popularityRating a oe2022-dogs:BreedPopularityRating ;
 cmns-rt:rates ?breed ;
 cmns-rt:hasRatingScore ?ratingScore .
?ratingScore cmns-rt:hasMeasureWithinScale ?rating .
}
order by ?barkingLevel ?rating
```

#### Result 3: 
| breedLabel | barkingLevel | barkingLevelSource | rating |
| --- | --- | --- | --- |
| australian cattle dog | 0.2 | The American Kennel Club | 51.0 |
| australian cattle dog | 0.8 | cattle dog VetStreet | 51.0 |

#### Explanation:
This query specifically uses the person in competancy question 3 and seeing which dogs are a good fit. It returns the dogs that are a good fit based on: the location (since the home is in Texas, a warm climate, the dog must be tollerant to heat), good with other animals (such as cats and dogs which are inferred based on dog/cat friendliness values), able to be trained to be a herder (based on trainability value), and its ability to do a lot of physical work (based on exercise needing value). The query returns 2 results, both for australian cattle dog. This is because barking is important for herding, but the AKC and VetStreet give different values for how loud the dog is.

### Query 4: Is a greyhound a good breed for a large family with multiple pets, including cats and other dogs?
Usage scenario covered: A large family consisting of 3 kids is looking for a dog; A family just came into a pet store looking to get a new dog

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oe2022-dogs: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet/>
PREFIX oe2022-dogs-ind: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet-individuals/>
PREFIX cmns-col: <https://www.omg.org/spec/Commons/Collections/>
select ?breedLabel
where {
oe2022-dogs-ind:Question4Family a oe2022-dogs:FamilyWithSmallChildren ;
 oe2022-dogs:ownsPet ?dog ;
 oe2022-dogs:ownsPet ?cat .
?dog a oe2022-dogs:Dog .
?cat a oe2022-dogs:Cat .

oe2022-dogs-ind:Greyhound a oe2022-dogs:GoodForChildrenBreed ;
 a oe2022-dogs:DogFriendlyBreed ;
 a oe2022-dogs:CatFriendlyBreed ;
 rdfs:label ?breedLabel .
}
```

#### Result 4:
| breedLabel |
| --- |

Nothing is returned. This is expected behavior since a greyhound would not be a good fit for the family. 


#### Explanation:
This query is specifically using the family in competancy question 4 and seeing if a greyhound is an appropriate dog for them. It returns whether or not the breed is a good fit based on some of the potential characteristic of the family: since it's a large family we use good with kids (inferred based on playfullness and child safety values), good with other dogs (inferred based on dog friendliness value), and good with cats (inferred based on cat friendliness value). The query returns nothing, since a greyhound is not a good choice for this type of family.  


### Query 5: What is a cute dog breed that can do well in an apartment that doesn’t get cleaned very often?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX cmns-cls: <https://www.omg.org/spec/Commons/Classifiers/>
PREFIX cmns-rt: <https://www.omg.org/spec/Commons/Ratings/>
PREFIX oe2022-dogs: <https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet/>
SELECT ?label ?popularityQuantitativeScore ?barkinglevel ?strangerfriendlinesslevel ?sheddinglevel ?droolinglevel ?maxWeight
	WHERE { ?breed a oe2022-dogs:ApartmentFriendlyBreed;
			a oe2022-dogs:LowSheddingBreed;
			a oe2022-dogs:LowDroolingBreed;
			rdfs:label ?label.
		?char_profile a oe2022-dogs:BreedCharacteristicProfile;
			cmns-cls:characterizes ?breed;
			oe2022-dogs:displaysDroolingLevel ?droolinglevel;
			oe2022-dogs:displaysSheddingLevel ?sheddinglevel;
			oe2022-dogs:displaysBarkingLevel ?barkinglevel;
			oe2022-dogs:displaysStrangerFriendlinessLevel ?strangerfriendlinesslevel.
		?phys_profile a oe2022-dogs:BreedPhysicalProfile;
			cmns-cls:characterizes ?breed;
			oe2022-dogs:hasMaxWeight ?maxWeight.
		?popularityRating a oe2022-dogs:BreedPopularityRating;
			cmns-rt:rates ?breed;
			cmns-rt:hasRatingScore ?ratingScore.
		?ratingScore cmns-rt:hasMeasureWithinScale ?popularityQuantitativeScore.
}
ORDER BY ?popularityQuantitativeScore ?barkinglevel DESC(?strangerfriendlinesslevel) ?sheddinglevel ?droolinglevel 
```

#### Result 5: 
| label     | popularityQuantitativeScore | barkinglevel | strangerFriendliness | sheddinglevel | droolinglevel | maxWeight | 
| --- | --- | --- | --- | --- | --- | --- |
| poodle (standard) | 165.0 | 0.4 | 1.0 | 0.2 | 0.2 | 50.0 |


#### Explanation: 
Query first requires apartment friendly characteristics (which will require a low barking, high stranger friendliness level, and a small or medium sized breed). It also requires that the dog have low shedding and drooling to account for the lack of cleaning in this apartment. It prioritizes our hard apartment constraints (barking and stranger friendliness) but ranks by popularity to account for the "cuteness" expectation.

### Previous Versions
- [Version 3 (OE 12)](files/queries_v3.txt) CURRENT
- [Version 2 (OE 11)](files/queries_v2.txt)
- [version 1 (OE 10)](files/queries_v1.txt)
