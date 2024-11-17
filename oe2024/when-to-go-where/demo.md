---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

### Question: What are the hikes in Arches National Park?

#### Query 1: SPARQL query to fetch hikes in Arches National Park

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
SELECT ?hike
WHERE { 
    ?hike oe-wtgw:isHikeOf oe-wtgw-ind:ArchesNationalPark
}
```

#### Result 1: Hike retrieved

| Hike         |
|--------------|
| DoubleOArch  |

---

### Question: What is the park's location using longitude and latitude?

#### Query 2: SPARQL query to fetch parks and their latitude

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
PREFIX Locations: <https://www.omg.org/spec/Commons/Locations/>

SELECT ?park ?latitude
WHERE  { 
    ?park Locations:hasLocation ?location .
    ?location Locations:hasLatitude ?latitude .
    FILTER(datatype(?latitude) = xsd:decimal)
}
ORDER BY DESC(?latitude)
```

#### Result 2: Parks and latitudes retrieved

| Park                    | Latitude |
|-------------------------|----------|
| Rocky Mountain National | 44.33    |
| Arches National Park    | 37.2982  |

---

### Question: What parks are in Maine?

#### Query 3: SPARQL query to fetch parks in Maine

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>

SELECT ?park
WHERE { 
    ?park rdf:type oe-wtgw:NationalPark .
    ?park oe-wtgw:hasState oe-wtgw-ind:Maine .
}
```

#### Result 3: Park retrieved

| Park                   |
|------------------------|
| Acadia National Park   |

---

### Question: Which national park has the coolest summer temperatures in the Midwest?

#### Query 4: SPARQL query to fetch parks with summer temperatures in the Midwest

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX oe-wtgw: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/>
PREFIX oe-wtgw-ind: <https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/>
PREFIX Locations: <https://www.omg.org/spec/Commons/Locations/>

SELECT ?park ?longitude ?summerTemp
WHERE {
    ?park rdf:type oe-wtgw:NationalPark .
    ?park Locations:hasLocation ?location .
    ?location Locations:hasLongitude ?longitude .
    ?park oe-wtgw:hasAvgSeasonalTemperature ?tempInd .
    ?tempInd rdf:type oe-wtgw:AvgSeasonalTemperature .
    ?tempInd oe-wtgw:temperatureHasSeason oe-wtgw-ind:Summer .
    ?tempInd oe-wtgw:hasTemperature ?summerTemp .
    FILTER(?longitude >= -110 && ?longitude <= -82)
}
ORDER BY ASC(?summerTemp)
```

#### Result 4: Park with the coolest summer temperature

| Park                   | Summer Temperature |
|------------------------|---------------------|
| Rocky Mountain National| 70°F               |

---

### Question: I am new to hiking. Which national park has cool summer temperatures and hikes less than 2 miles?

#### Query 5: SPARQL query to fetch parks with short hikes and cool summer temperatures

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

#### Result 5: Park and hike retrieved

| Park                   | Temp  | Hike              | Distance |
|------------------------|-------|-------------------|----------|
| Crater Lake National   | 65°F  | Watchman Peak Trail| 1.7 mi   |

---

### Question: What are the longest hikes in California's national parks?

#### Query 6: SPARQL query to fetch longest hikes in California

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

#### Result 6: Longest hike retrieved

| Hike              | Distance |
|-------------------|----------|
| Lakes Trail       | 12.2 mi  |
```