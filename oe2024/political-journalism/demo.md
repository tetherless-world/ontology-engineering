---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

#### Question 1: 
What federal senate elections in 2022 that had a narrow victory margin for a Republican candidate were mentioned in articles published by a right-wing news outlet?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
SELECT DISTINCT ?e WHERE {
?e pj:isElectionFor pj:FederalSenator;
   pj:hasElectionMargin pj:NarrowMargin;
   pj:hasElectionWinner ?c;
   xsd:hasExplicitDate ?d.
?c rdf:type pj:RepublicanPoliticalCandidate;
   pj:isSubjectOf ?a.
?a rdf:type pj:Article;
   pj:hasPublisher ?p.
?p rdf:type pj:RightWingPublisher.
FILTER(?d >= "2022-01-01"^^xsd:date && ?d <= "2022-12-31"^^xsd:date) }
```

#### Result 1:


#### Query 2: 
Which journalists wrote articles about Senator Bernie Sanders in both the New York Times and Fox News from 2020–2022?

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
SELECT DISTINCT ?j WHERE {
?a1 rdf:type pj:Article;
    pj:hasAuthor ?j;
    pj:hasPublisher pj:NewYorkTimes;
    pj:hasPublishDate ?d1;
    pj:hasPersonSubject pj:BernieSanders.
?a2 rdf:type pj:Article;
    pj:hasAuthor ?j;
    pj:hasPublisher pj:FoxNews;
    pj:hasPublishDate ?d2;
    pj:hasPersonSubject pj:BernieSanders.
FILTER(?d1 >= "2022-01-01"^^xsd:date && ?d1 <= "2022-12-31"^^xsd:date)
FILTER(?d2 >= "2022-01-01"^^xsd:date && ?d2 <= "2022-12-31"^^xsd:date) }
```

#### Result 2: 
None

#### Question 3:
What articles have the New York Times and Fox News published about Democratic candidates in relation to the economy in 2022? 

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rc:  <https://www.omg.org/spec/Commons/RolesAndCompositions/>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
SELECT ?p ?a WHERE {
?p rdf:type pj:Publisher.
?a rdf:type pj:EconomicArticle;
   pj:hasPublishDate ?d;
   pj:hasPublisher ?p;
   pj:hasSubject ?p.
?p rc:playsRole ?c
?c rdf:type pj:DemocratPoliticalCandidate.
FILTER(?d >= "2022-01-01"^^xsd:date && ?d <= "2022-12-31"^^xsd:date)
FILTER(?p = pj:FoxNews || ?p = pj:NewYorkTimes) }
```

#### Result 3: 

#### Question 4:
What journalists wrote an article published by the New York Times in 2022 mentioning a Democratic candidate who lost in a landslide in a state election in 2022?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
SELECT ?j ?a WHERE {
?a rdf:type pj:Article;
   pj:hasAuthor :j;
   pj:hasPublishDate ?d1;
   pj:hasPublisher :NewYorkTimes;
   pj:hasSubject ?p.
?p rc:playsRole ?c.
?c rdf:type pj:DemocratPoliticalCandidate;
   pj:isElectionLoserIn ?e.
?e rdf:type :StateElection;
   pj:hasElectionMargin :LandslideMargin;
   pj:hasDate ?d2.
FILTER(?d1 >= "2024-01-01"^^xsd:date && ?d1 <= "2024-12-31"^^xsd:date) 
FILTER(?d2 >= "2024-01-01"^^xsd:date && ?d2 <= "2024-12-31"^^xsd:date)
FILTER(?p = pj:FoxNews || ?p = pj:NewYorkTimes) }
```

#### Result 4: 

#### Question 5:
What other topics in articles published in 2024 are covered by journalists who have published articles on immigration and Kamala Harris for right-wing news outlets also in 2024?

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX pj: <https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#>
SELECT DISTINCT ?t ?a2 ?j  WHERE {
?a1 rdf:type pj:Article;
    pj:hasAuthor ?j;
    pj:hasPublisher ?p;
    pj:hasPersonSubject :KamalaHarris;
    pj:hasTopic ?t;
    pj:hasPublishDate ?d1.
?t rdf:type pj:ImmigrationTopic.
?p rdf:type pj:RightWingPublisher.
?j pj:isAuthorOf ?a2.
?a2 pj:hasTopic ?t;
    pj:hasPublishDate ?d2.
FILTER(?d1 >= "2024-01-01"^^xsd:date && ?d1 <= "2024-12-31"^^xsd:date) 
FILTER(?d2 >= "2024-01-01"^^xsd:date && ?d2 <= "2024-12-31"^^xsd:date) }
```

#### Result 5: 