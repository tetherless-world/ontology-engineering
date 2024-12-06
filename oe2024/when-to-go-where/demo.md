---
---

## Queries

The following queries were run using Snap SPARQL with a Pellit Reasoner

### Compentency Question 1
#### Question: 
Which national park has the coolest summer temperatures in the Midwest?

#### Query: 
SPARQL query to fetch parks with summer temperatures in the Midwest

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
PREFIX Locations: <https://www.omg.org/spec/Commons/Locations/>
SELECT ?park ?summerTemp
WHERE {
    ?park rdf:type oe-wtgw:NationalPark .
    ?park Locations:hasLocation ?location .
    ?location Locations:hasLongitude ?longitude .
    ?location Locations:hasLatitude ?latitude .
    ?park oe-wtgw:hasAvgSeasonalTemperature ?tempInd .
    ?tempInd rdf:type oe-wtgw:AvgSeasonalTemperature .
    ?tempInd oe-wtgw:temperatureHasSeason oe-wtgw-ind:Summer .
    ?tempInd oe-wtgw:hasTemperature ?summerTemp .
    FILTER(?longitude >= -110 && ?longitude <= -82)
    FILTER(?latitude >= 36 && ?latitude <= 49)
}
ORDER BY ASC(?summerTemp)
```

#### Result: Park with the coolest summer temperature

| Park                                         | Summer Temperature |
|----------------------------------------------|--------------------|
| Isle Royale National Park                   | 65                 |
| Rocky Mountain National Park                | 70                 |
| Voyageurs National Park                     | 70                 |
| Black Canyon Of The Gunnison National Park  | 70                 |
| Indiana Dunes National Park                 | 75                 |
| Wind Cave National Park                     | 75                 |
| Theodore Roosevelt National Park            | 75                 |
| Gateway Arch National Park                  | 80                 |
| Great Sand Dunes National Park              | 80                 |
| Mesa Verde National Park                    | 80                 |
| Mammoth Cave National Park                  | 80                 |
| Badlands National Park                      | 80                 |
| Canyonlands National Park                   | 95                 |
| Arches National Park                        | 95                 |

#### Description:
---


### Compentency Question 2
#### Question: I am new to hiking. Which national park has cool summer temperatures and hikes less than 2 miles?

#### Query: SPARQL query to fetch parks with short and easy hikes and cool summer temperatures

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
SELECT ?park ?summerTemp ?hike ?distance
WHERE {
    ?park rdf:type oe-wtgw:NationalPark .
    ?park oe-wtgw:hasAvgSeasonalTemperature ?tempInd .
    ?tempInd rdf:type oe-wtgw:AvgSeasonalTemperature .
    ?tempInd oe-wtgw:temperatureHasSeason oe-wtgw-ind:Summer .
    ?tempInd oe-wtgw:hasTemperature ?summerTemp .
    ?park oe-wtgw:hasHike ?hike .
    ?hike oe-wtgw:hasDistance ?distance .
    FILTER(?distance <= 2)
}
ORDER BY ASC(?summerTemp)
```

#### Result: Park and hike retrieved

| Park                           | Summer Temperature | Trail                     | Distance (miles) |
|--------------------------------|--------------------|---------------------------|------------------|
| Cuyahoga Valley National Park  | 75                 | Brandywine Gorge Trail     | 1.5              |
| Gateway Arch National Park     | 80                 | Gateway Arch Trail         | 1.8              |
| Mammoth Cave National Park     | 80                 | Extended Historic Tour     | 2.0              |
| Dry Tortugas National Park     | 85                 | Fort Jefferson Loop        | 0.5              |
| Carlsbad Caverns National Park| 85                 | Big Room Trail             | 1.25             |
| Biscayne National Park         | 90                 | Elliott Key Loop           | 1.1              |
| Everglades National Park       | 90                 | Anhinga Trail              | 0.8              |
| Petrified Forest National Park | 90                 | Blue Mesa Trail            | 1.0              |
| Canyonlands National Park      | 95                 | Grand View Point           | 1.8              |
| White Sands National Park      | 95                 | Dune Life Nature Trail     | 1.0              |


#### Description:
---

### Compentency Question 3
#### Question: What are the longest hikes in California's national parks?

This last query was run in the normal SPARQL window

#### Query: SPARQL query to fetch longest hikes in California

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
SELECT ?park ?hike ?distance
WHERE {
    ?park rdf:type oe-wtgw:NationalPark .
    ?park oe-wtgw:hasState oe-wtgw-ind:California .
    ?park oe-wtgw:hasHike ?hike .
    ?hike oe-wtgw:hasDistance ?distance .
    FILTER(datatype(?distance) = xsd:decimal)
}
ORDER BY DESC(?distance)
```

#### Result: Longest hike retrieved

| Hike              | Distance |
|-------------------|----------|
| Lakes Trail       | 12.2 mi  |

#### Description:

---

### Compentency Question 4
#### Question:
#### Result:
#### Query:
#### Description:
---

### Compentency Question 5
#### Question:
#### Result:
#### Query:
#### Description:
---
