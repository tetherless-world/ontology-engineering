---
---

## Queries

<p class="message-highlight">List your SPARQL queries to your competency questions along with answers retrieved from your ontology/KG such as the below.</p>

### Study Match: Is there a study that matches this patient on a feature (s)?

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

## Result 2: 
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

