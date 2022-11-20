[Concept Map](#conceptual-model) | [Ontology File](#ontologies) | [Ontologies Reused](#ontologies-reused) | [Ontology Prefixes](#ontology-prefixes)

## Conceptual Model

<img src="images/ConceptualModel_BreedTypes.png" width="100%"/>
Our ontology models dog breeds and classifies them based on what potential adopters might require or prefer. These are the types of breeds that our system can infer. 
<img src="images/ConceptualModel_BreedCharacteristics.png" width="100%"/>
The above image describes our conceptual model with regards to how we model dog breeds. This includes the object properties that connect each breed with the classes that describe it.
<img src="images/ConceptualModel_BreedCharacteristicProfile.png" width="50%"/>
<img src="images/ConceptualModel_BreedCharacteristics.png" width="50%"/>
Each of these profiles are sets of data properties that describe a breed. Each object property in the breed characteristic profile is a value between 0 and 1 that indicate how much a breed embodies that characteristic.
<img src="images/ConceptualModel_ProfileProvenance.png" width="50%"/>
Each profile is attributed to the organization (eg. The American Kennel Club) that provided the information.
<img src="images/ConceptualModel_PetOwnership.png" width="50%"/>
<img src="images/ConceptualModel_MarkingColors.png" width="50%"/>
Potential adopters may have existing pets that a new dog would have to get along with, and this is how we model that. Markings are also broken up as a shape and its color(s). We use the 2022 AKC colors and marking names as instances. 
<img src="images/ConceptualModel_Ratings.png" width="100%"/>
Since we cannot model cuteness, since that's subjective, we model the popularity rankings for each breed, currently as reported by the AKC. This model shows how we do that. Since we allow for any organization could be the rating provider, additional rankings could be added.
<img src="images/ConceptualModel_Adopter.png" width="100%"/>
The above image describes our conceptual model with regards to how we model potential adopters. This includes the object properties that connect each adopter with the classes that describe it. It also shows how we model famililies and allergies (a dog allergy is an instance of the Allergy class).
<img src="images/ConceptualModel_FunctionalRoles.png" width="100%"/>
Some adopters may want a dog for a certain purpose, such as herding, and most breeds were bred for a certain purpose, such as hunting. We model that using roles.
<img src="images/ConceptualModel_Residences.png" width="100%"/>
We model an adopter's residence with its location so that we can recommend breeds that are well suited for the climate. We use the IECC climate zones. 
<img src="images/ConceptualModel_Spaces.png" width="50%"/>
Each residence is made up of a set of spaces, some indoors and some outdoors. Spaces that are covered but not temperature controlled, such as patios or screened-in porches, are considered outdoor spaces. 
<img src="images/ConceptualModel_Aspects.png" width="100%"/>
This model shows how the varous characteristics of other entities are organized. 

### Previous Versions

- [Version 5 (OE 10)](files/ConceptualModel_v5.pdf) [SVG](files/ConceptualModel_v5.svg) CURRENT
- [Version 4 (OE 9)](files/ConceptualModel_v4.pdf) [SVG](files/ConceptualModel_v4.svg)
- [Version 3 (OE 8)](files/ConceptualModel_v3.pdf)
- [Version 2 (OE 6)](files/ConceptualModel_v2.pdf)
- [Version 1 (OE 5)](files/ConceptualModel_v1.pdf)

## Ontologies

- [Version 6 (OE 11)](https://github.com/tetherless-world/ontology-engineering/blob/68ee5cc09ddc8a4af8b5d85b31565d2733f38613/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://github.com/tetherless-world/ontology-engineering/blob/68ee5cc09ddc8a4af8b5d85b31565d2733f38613/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf) CURRENT
- [Version 5 (OE 10)](https://github.com/tetherless-world/ontology-engineering/blob/c1f3e28aecb3212c01b1f88fa362049ae3272d31/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://github.com/tetherless-world/ontology-engineering/blob/c1f3e28aecb3212c01b1f88fa362049ae3272d31/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf)
- [Version 4 (OE 9)](https://github.com/tetherless-world/ontology-engineering/blob/006ce23f62757847531bcb106831490d4c43f14b/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://github.com/tetherless-world/ontology-engineering/blob/006ce23f62757847531bcb106831490d4c43f14b/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf)
- [Version 3 (OE 8)](https://github.com/tetherless-world/ontology-engineering/blob/c65013f0f13175273378c6a35a18031150a03e32/oe2022/dog-breed-ontology/find-a-pet.rdf) [Individuals](https://github.com/tetherless-world/ontology-engineering/blob/c65013f0f13175273378c6a35a18031150a03e32/oe2022/dog-breed-ontology/find-a-pet-individuals.rdf) 
- [Version 2 (OE 7)](https://github.com/tetherless-world/ontology-engineering/blob/3ffedc3e1063ee3ddeb0f233c9d43d29989e17bc/oe2022/dog-breed-ontology/find-a-pet.rdf)
- [Version 1 (OE 6)](https://github.com/tetherless-world/ontology-engineering/blob/40b9433c732a6adc31d5fb0dd1c953f172dbd228/oe2022/dog-breed-ontology/find-a-pet.rdf) 

## Ontologies Reused
- [OMG Annotation Vocabulary v.20220801](https://www.omg.org/spec/Commons/AnnotationVocabulary/)
- [OMG Classifiers v.20220801](https://www.omg.org/spec/Commons/Classifiers/)
- [OMG Collections v.20220801](https://www.omg.org/spec/Commons/Collections/)
- [OMG Documents v.20220601](https://www.omg.org/spec/Commons/Documents/)
- [OMG Dates & Times v.20220801](https://www.omg.org/spec/Commons/DatesAndTimes/)
- [OMG Products & Services v.20220701](https://www.omg.org/spec/Commons/ProductsAndServices/)
- [OMG Parties & Situations v.20220901](https://www.omg.org/spec/Commons/PartiesAndSituations/)
- [OMG Ratings v.20221001](https://www.omg.org/spec/Commons/Ratings/)
- [Purl DC Terms v.20200120](http://purl.org/dc/terms/)
- [LCC Country Representation v.20221101](https://www.omg.org/spec/LCC/Countries/CountryRepresentation/)
- [LCC ISO3166-2 US Subdivision Codes v.20221101](https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-US/)
- [PROVO v.20130430](http://www.w3.org/ns/prov#)
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


