---
---

## Queries

#### Question 1: 
What federal senate elections in 2022 that had a narrow victory margin for a Republican candidate were mentioned in articles published by a right-wing news outlet?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rc:  <https://www.omg.org/spec/Commons/RolesAndCompositions/>
PREFIX dt:  <https://www.omg.org/spec/Commons/DatesAndTimes/>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
SELECT DISTINCT ?e WHERE {
?e rdf:type pj:NarrowMarginElection;
   pj:isElectionFor ?o;
   pj:hasElectionWinner ?c;
   pj:hasElectionDate ?d.
?o rdf:type pj:FederalSenator.
?c rdf:type pj:RepublicanCandidate;
   rc:isPlayedBy ?i.
?i pj:isSubjectOf ?a.
?a rdf:type pj:RightWingPublishedArticle.
?d dt:hasDateTimeValue ?dt.
FILTER(?dt >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?dt < "2023-01-01T00:00:00Z"^^xsd:dateTime) }
```

#### Query 2: 
Which journalists wrote articles about Senator Bernie Sanders in both the New York Times and Fox News from 2020–2022?

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dt:  <https://www.omg.org/spec/Commons/DatesAndTimes/>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
PREFIX pje: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism-individuals-example#>
SELECT DISTINCT ?j WHERE {
?a1 rdf:type pj:Article;
	pj:hasAuthor ?j;
	pj:hasPublisher pje:NewYorkTimes;
	pj:hasPublishDate ?d1;
	pj:hasPersonSubject pje:BernieSanders.
?a2 rdf:type pj:Article;
	pj:hasAuthor ?j;
	pj:hasPublisher pje:FoxNews;
	pj:hasPublishDate ?d2;
	pj:hasPersonSubject pje:BernieSanders.
?d1 dt:hasDateTimeValue ?dt1.
?d2 dt:hasDateTimeValue ?dt2.
FILTER(?dt1 >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?dt1 < "2023-01-01T00:00:00Z"^^xsd:dateTime)
FILTER(?dt2 >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?dt2 < "2023-01-01T00:00:00Z"^^xsd:dateTime) }
```


#### Question 3:
What articles have the New York Times and Fox News published about Democratic candidates in relation to the economy in 2022? 

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rc:  <https://www.omg.org/spec/Commons/RolesAndCompositions/>
PREFIX dt:  <https://www.omg.org/spec/Commons/DatesAndTimes/>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
PREFIX pje: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism-individuals-example#>
SELECT ?p ?a WHERE {
?p rdf:type pj:Publisher.
?a rdf:type pj:EconomicArticle;
   pj:hasPublishDate ?d;
   pj:hasPublisher ?p;
   pj:hasPersonSubject ?i.
?i rc:playsRole ?c.
?c rdf:type pj:DemocratCandidate.
?d dt:hasDateTimeValue ?dt.
FILTER(?dt >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?dt < "2023-01-01T00:00:00Z"^^xsd:dateTime)
FILTER(?p = pje:FoxNews || ?p = pje:NewYorkTimes) }
```

#### Question 4:
What journalists wrote an article published by the New York Times in 2022 mentioning a Democratic candidate who lost in a landslide in a state election in 2022?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rc:  <https://www.omg.org/spec/Commons/RolesAndCompositions/>
PREFIX dt:  <https://www.omg.org/spec/Commons/DatesAndTimes/>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
PREFIX pje: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism-individuals-example#>
SELECT ?a ?d1 WHERE {
?a rdf:type pj:Article;
   pj:hasPublishDate ?d1;
   pj:hasPublisher pje:NewYorkTimes;
   pj:hasPersonSubject ?p.
?p rc:playsRole ?c.
?c rdf:type pj:DemocratCandidate;
   pj:isElectionLoserIn ?e.
?e rdf:type pj:StateElection;
   pj:hasElectionMargin pj:LandslideMargin;
   pj:hasElectionDate ?d2.
?d1 dt:hasDateTimeValue ?dt1.
?d2 dt:hasDateTimeValue ?dt2.
FILTER(?dt1 >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?dt1 < "2023-01-01T00:00:00Z"^^xsd:dateTime)
FILTER(?dt2 >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?dt2 < "2023-01-01T00:00:00Z"^^xsd:dateTime) }
```


#### Question 5:
What other topics in articles published in 2024 are covered by journalists who have published articles on immigration and Kamala Harris for right-wing news outlets also in 2024?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dt:  <https://www.omg.org/spec/Commons/DatesAndTimes/>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
PREFIX pje: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism-individuals-example#>
SELECT DISTINCT ?t ?a2 ?j  WHERE {
?a1 rdf:type pj:RightWingPublishedArticle;
    pj:hasAuthor ?j;
    pj:hasPersonSubject pje:KamalaHarris;
    pj:hasTopic ?t;
    pj:hasPublishDate ?d1.
?t rdf:type pj:ImmigrationTopic.
?j pj:isAuthorOf ?a2.
?a2 pj:hasTopic ?t;
    pj:hasPublishDate ?d2.
?d1 dt:hasDateTimeValue ?dt1.
?d2 dt:hasDateTimeValue ?dt2.
FILTER(?dt1 >= "2024-01-01T00:00:00Z"^^xsd:dateTime && ?dt1 < "2025-01-01T00:00:00Z"^^xsd:dateTime)
FILTER(?dt2 >= "2024-01-01T00:00:00Z"^^xsd:dateTime && ?dt2 < "2025-01-01T00:00:00Z"^^xsd:dateTime) }
```
