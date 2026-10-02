[Concept Map](#conceptual-model) | [Ontology File](#ontologies) | [Ontologies Reused](#ontologies-reused) | [Ontology Prefixes](#ontology-prefixes)

## Conceptual Model

The most recent full version of our conceptual model is available as a [drawio file](files/ConceptualModel_v7.drawio).
The ontology is split into two main parts: describing the breeds, and describing the potential adopters. Our scope is limited to the United States, so we only consider breeds that are recognized by the American Kennel Club and are only model characteristics of dog adopters in the United States. Below is an overview of our conceptual model.

In our conceptual models the colors denote different type of entities:
- white: class that we created
- grey: class that we imported from another ontology
- light blue: object property that we created, connected to the arrow that show the classes in the relation and any cardinality restrictions
- dark blue: object property that we imported from another ontology
- red: data value, shown is its datatype

The names without boxes along arrows are data properties.

#### Breeds

<img style="float: center;" src="images/ConceptualModel_BreedTypes.png"/>
Our ontology models dog breeds and classifies them based on what potential adopters might require or prefer. These are the types of breeds that our system can infer. Some of these are disjoint so help with reasoning speed (hypoallergenic vs. likely allergenic) and others are disjoint because their definitions do not allow for overlap (cold climate appropriate vs. hot climate appropriate).  Since each of these subclasses are defined, they can be inferred from a breed's relation to various breed aspects. Every breed will be inferred to be either hypoallergenic or likely allergenic, and either hairy or hairless. 
<img style="float: center;" src="images/ConceptualModel_BreedCharacteristics.png"/>
While every dog is unique, those that are the same breed share many characteristics. Breeds tend to look very similar and often act in similar ways as well. We consider physical characteristics such as weight (included in breed physical profile), behavioral characteristics such as playfulness (included in breed characteristic profile), and extrinsic characteristics such as popularity. Some characteristics such as coat type and coat length are used to infer other aspects of the breed, such as if it's hot or cold tolerant. Other relations, such as a breed's relation to an allergy, allow us to determine whether a breed is considered hypoallergenic. The allergy that we were most concerned about was an allergy to dog dander or fur, which is an instance in our system. We also consider some characteristics of breeds that the system considers optional, such as if an adopter has a preferred color of dog. Many of these are considered breed aspects since they describe the tendencies of the breed as a group. 
<img style="float: center;" src="images/ConceptualModel_Ratings.png"/>
We cannot model cuteness, since that's subjective. We instead model the popularity rankings for each breed. Popularity is not based just on how cute people find a dog, since dogs may also be popular because they are easy to care for and have a lot of information available on them, but dogs that are largely considered 'ugly' are less likely to be popular. We reuse the Commons Ratings ontology to model this. Due to scope we only include rankings from the AKC in 2021, with the smaller rankings (1st, 2nd) being more popular than larger rankings (40th, 41st).  

#### Potential Adopter

<img style="float: center;" src="images/ConceptualModel_Adopter.png"/>
The above diagram shows how we model potential adopters. We chose the name 'potential adopter' because while they may want to adopter a new dog, they have not done so yet and may change their mind. Potential adopter is a role that either a family or an individual can play. Some aspects are related to the individual adopter/members of the adopter family, such as exercise level, while others are related to the party that is playing the role of potential adopter, such as budget. We separated those families that included children under 5 years old from those that do not. People may be small children, students, or elderly. People may also have an allergy, but we consider the entire party having a single primary residence that a dog would spend most of its time.  
<img style="float: center;" src="images/ConceptualModel_FunctionalRoles.png"/>
Some adopters may want a dog for a certain purpose, such as herding, and most breeds were bred for a certain purpose, such as hunting. Additionally, breeds are sorted into breed groups that describe the primary purpose the breed was bred to serve. We modeled those purposes as functional roles, and added categories for the most common purposes that dogs were bred for and serve. Due to scope limitations we only included the official AKC breed groups as instances. Since it’s not guaranteed to be good at the purpose it’s bred for (since most dogs are not working dogs in the US) this is an optional requirement of the system and overall trainability is prioritized.

### Previous Versions

- [Version 7 (OE 13)](files/ConceptualModel_v7.pdf) [SVG](files/ConceptualModel_v7.svg) CURRENT
- [Version 6 (OE 12)](files/ConceptualModel_v6.pdf) [SVG](files/ConceptualModel_v6.svg)
- [Version 5 (OE 10)](files/ConceptualModel_v5.pdf) [SVG](files/ConceptualModel_v5.svg) 
- [Version 4 (OE 9)](files/ConceptualModel_v4.pdf) [SVG](files/ConceptualModel_v4.svg)
- [Version 3 (OE 8)](files/ConceptualModel_v3.pdf)
- [Version 2 (OE 6)](files/ConceptualModel_v2.pdf)
- [Version 1 (OE 5)](files/ConceptualModel_v1.pdf)

## Ontologies

- [Version 8 (OE 13)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/3db93d1b10911829c64fb1d1fda0dd4b033ac006/oe2022/dog-breed-ontology/find-a-pet.rdf) [Large Individuals](https://github.com/tetherless-world/ontology-engineering/raw/c78b8c60b6f6687c8d719997c7fe1d45fb20c664/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf) [Small Individuals](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/411a147b864f13eecf2c84701550626bf3190622/oe2022/dog-breed-ontology/find-a-pet-individuals-small.rdf) CURRENT
- [Version 7 (OE 12)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/c4c5af171820eedcb7108cc069a69637fe25a02a/oe2022/dog-breed-ontology/find-a-pet.rdf) [Large Individuals](https://github.com/tetherless-world/ontology-engineering/raw/c4c5af171820eedcb7108cc069a69637fe25a02a/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf) [Small Individuals](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/c4c5af171820eedcb7108cc069a69637fe25a02a/oe2022/dog-breed-ontology/find-a-pet-individuals-small.rdf) 
- [Version 6 (OE 11)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/68ee5cc09ddc8a4af8b5d85b31565d2733f38613/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://github.com/tetherless-world/ontology-engineering/raw/68ee5cc09ddc8a4af8b5d85b31565d2733f38613/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf) 
- [Version 5 (OE 10)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/c1f3e28aecb3212c01b1f88fa362049ae3272d31/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/c1f3e28aecb3212c01b1f88fa362049ae3272d31/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf)
- [Version 4 (OE 9)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/006ce23f62757847531bcb106831490d4c43f14b/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/006ce23f62757847531bcb106831490d4c43f14b/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf)
- [Version 3 (OE 8)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/c65013f0f13175273378c6a35a18031150a03e32/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/c65013f0f13175273378c6a35a18031150a03e32/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf) 
- [Version 2 (OE 7)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/3ffedc3e1063ee3ddeb0f233c9d43d29989e17bc/oe2022/dog-breed-ontology/find-a-pet.rdf)
- [Version 1 (OE 6)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/40b9433c732a6adc31d5fb0dd1c953f172dbd228/oe2022/dog-breed-ontology/find-a-pet.rdf) 

## Ontologies Reused
- [OMG Annotation Vocabulary v.2022-08-01](https://www.omg.org/spec/Commons/20220801/AnnotationVocabulary/)
- [OMG Classifiers v.2022-08-01](https://www.omg.org/spec/Commons/20220801/Classifiers/)
- [OMG Collections v.2022-08-01](https://www.omg.org/spec/Commons/20220801/Collections/)
- [OMG Documents v.2022-06-01](https://www.omg.org/spec/Commons/20220601/Documents/)
- [OMG Dates & Times v.2022-08-01](https://www.omg.org/spec/Commons/20220801/DatesAndTimes/)
- [OMG Products & Services v.2022-07-01](https://www.omg.org/spec/Commons/20220701/ProductsAndServices/)
- [OMG Parties & Situations v.2022-09-01](https://www.omg.org/spec/Commons/20220901/PartiesAndSituations/)
- [OMG Ratings v.2022-10-01](https://www.omg.org/spec/Commons/20221001/Ratings/)
- [Purl DC Terms v.2020-01-20](http://purl.org/dc/terms/)
- [LCC Country Representation v.2022-11-01](https://www.omg.org/spec/LCC/20221101/Countries/CountryRepresentation/)
- [LCC ISO3166-2 US Subdivision Codes v.2022-11-01](https://www.omg.org/spec/LCC/20221101Countries/Regions/ISO3166-2-SubdivisionCodes-US/)
- [PROVO v.2013-04-30](http://www.w3.org/ns/prov-o-20130430/)
- [W3C OWL v.2002](http://www.w3.org/2002/07/owl#)
- [W3C RDF v.1999](http://www.w3.org/1999/02/22-rdf-syntax-ns#)
- [W3C RDFS v.2000](http://www.w3.org/2000/01/rdf-schema#)
- [W3C SKOS v.2004](http://www.w3.org/2004/02/skos/core#)
- [W3C XSD v.2001](http://www.w3.org/2001/XMLSchema#)

## Ontology Prefixes
- cmns-av="https://www.omg.org/spec/Commons/AnnotationVocabulary/"
- cmns-cls="https://www.omg.org/spec/Commons/Classifiers/"
- cmns-col="https://www.omg.org/spec/Commons/Collections/"
- cmns-doc="https://www.omg.org/spec/Commons/Documents/"
- cmns-dt="https://www.omg.org/spec/Commons/DatesAndTimes/"
- cmns-prd="https://www.omg.org/spec/Commons/ProductsAndServices/"
- cmns-pts="https://www.omg.org/spec/Commons/PartiesAndSituations/"
- cmns-rt="https://www.omg.org/spec/Commons/Ratings/"
- dct="http://purl.org/dc/terms/"
- lcc-3166-2-us="https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-US/"
- lcc-cr="https://www.omg.org/spec/LCC/Countries/CountryRepresentation/"
- prov="http://www.w3.org/ns/prov#"
- oe2022-dogs="https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet/"
- oe2022-dogs-ind="https://tw.rpi.edu/ontology-engineering/oe2022/find-a-pet-individuals/"
- owl="http://www.w3.org/2002/07/owl#"
- rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
- rdfs="http://www.w3.org/2000/01/rdf-schema#"
- skos="http://www.w3.org/2004/02/skos/core#"
- xsd="http://www.w3.org/2001/XMLSchema#"


