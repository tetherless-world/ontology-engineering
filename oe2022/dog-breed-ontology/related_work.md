---
layout: default
title: related_work
---

## Related Work

### Ontologies

The Dog Breed Ontology was developed with the help of several published ontologies. Below are the ontologies that were used a significant amount in the design and implementation of the system. All ontologies used are listed on the [Concept Map & Ontology](https://dog-breed-ontology--rpi-ontology-engineering.netlify.app/oe2022/dog-breed-ontology/ontology#ontologies-reused) page of our website.

- [Languages, Countries and Codes (LCC)](https://www.omg.org/spec/LCC/Countries/CountryRepresentation/) This ontology provides a model to represent countries and country subdivisions, as well as providing individuals for each state in the USA in [LCC ISO3166-2 US Subdividion Codes](https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-US/). 
- [The Provenance Ontology (PROV-O)](http://www.w3.org/ns/prov#) This ontology provides a model for tracking provenance throughout a system, which we use to connect breed characteristic values with the organization that gave them.
- [OMG Ratings](https://www.omg.org/spec/Commons/Ratings/) This ontology provides a model for organizations to provide ratings and rankings, which we used to model the popularity rankings of dog breeds.

Several other ontologies exist that aim to describe the characteristics of animals that were not used in this project. They are listed below.

- [Pet Ontology](https://w3id.org/MON/pet.owl) While limited in scope, this ontology does describe the basic characteristics of pets, including dogs. However, due to a lack of license or copyright information we were unwilling to reuse it.
- [Animal Trait Ontology for Livestock](http://opendata.inra.fr/ATOL/atol_ontology) This ontology does include many physical and behavioral traits of animals that could be applied to dog breeds. It has a very different use case though, and the vast majority of the ontology is specific to livestock (e.g. meat production, necessary nutrients, reproductive features). Because of this, we chose not to include it in our ontology, though if future work wanted to focus on dog breeds for breeding purposes this ontology may be of use. 
- [Vertebrate Breed Ontology](http://purl.obolibrary.org/obo/vbo.owl) This ontology was created to be a source of animal breeds for data standardization and integration. However, its scope is much larger than ours and as of Nov. 2022 it does not include information on dog breeds (only livestock and cats) so we were unable to use it in our system. In the future if dog breeds are added, it may be worth integrating with the ontology to increase interoperability. 

### Other Breed Recommendation Systems

Many other systems exist for recommending dog breeds. Our project was inspired by these quizes/questionnaires and aimed to combine the best aspects of each systems with semantic technology. 

- [The American Kennel Club Breed Selector Tool](https://www.akc.org/breed-selector-tool/) This tool asks 6 questions about desired dog characteristics and 7 about individual/household characteristics, then returns the top 5 breeds that match.
- [Bow Wow Meow Breed Selector](https://www.selectadogbreed.com/) This tool asks 18 total questions, with the option to select multiple or no preferences on many questions. It returns the top 6 results, but does not give details on what characteristics do or do not match the user's input.
- [IAMS Dog Breed Selector Quiz](https://www.iams.com/dog-breed-selector) This tool asks 13 questions and asks the user to rank which characteristics are most important to them. It shows only the top match with compatibility percentages on various characteristics. It was the only one of the recommendation systems we looked at that did not ask about dog allergies in the household.

There were some questions that other recommenders asked about that our system does not account for. Our system has no way to model an experienced vs inexperienced dog owner, and no way to model pets that are not cats and dogs. Other recommenders asked about level of experience in dog ownership and usually allowed for a catch-all category of pets such as 'other small mammal' or 'other small animal.' It was unclear what data was being used to categorize breeds as 'good for inexperienced owners' or 'good for small animal' so we did not include those categories.

We ran an experiment to compare the results of our recommender with the other recommenders. We used the same situation for each:
*Adopter already has a dog and multiple small children, one of whom is mildly allergic to dogs. They live in an apartment and don't have much time to clean, but is willing to give the dog basic obedience training.*
We encoded this as the following characteristics that we wanted in a dog:
- hypoallergenic
- apartment friendly
- low barking
- stranger friendly
- dog friendly
- small or medium size (or extra small size when offered)
- low shedding
- low drooling
- dog friendly
- child friendly
- playful/affectionate
- trainable

When the recommenders asked about preferences that are not included in the above description, no preference or the most neutral option was selected. The top results from each recommender were:
- AKC Breed Selector: **Mastif**, extra large size, not hypoallergenic, very high shedding
- BWM Breed Selector: **German Spitz**, not hypoallergenic, high shedding, high barking, not stranger friendly
- IAMS Dog Breed Quiz: **Soft-Coated Wheaten Terrier**, slightly higher barking tendencies than desired, though the quiz did not ask about hypoallergenic status so we suspect it was coincidence that this dog meets that requirement
- Find a Friend (Our System): **Coton de Tulear**, met all of the preferences (we wrote a custom [SNAP SPARQL query](files/customQuery.txt) since we do not have a proper UI)

## References

- "Answer These 5 Questions to Find the Right Dog For You." The American Kennel Club. https://www.akc.org/expert-advice/lifestyle/answer-5-questions-find-right-dog/.
- Babineau, J R. “Understanding the IECC's New Climate Zone Map.” Johns Manville, Berkshire Hathaway, 17 Mar. 2021, https://www.jm.com/en/blog/2021/march/understanding-the-iecc-s-new-climate-zone-map/.
- "Dictionary by Merriam-Webster: America's most-trusted online dictionary." Merriam-Webster Dictionary. https://www.merriam-webster.com.
- "Dog Breed Information Ultimate Resource: Listing of All Dog Breeds." Vetstreet, http://www.vetstreet.com/dogs/breeds.
- "Dog Breeds - Types of Dogs." American Kennel Club, https://www.akc.org/dog-breeds/.
- "Dog Breeds ." Dogbreedslist.info, https://www.dogbreedslist.info/.
- "iDog." China National Center for Bioinformation: National Genomics Data Center. https://ngdc.cncb.ac.cn/idog/breed/getAllBreed.action
- K.E. Holland, "Acquiring a pet dog: A review of factors affecting the decision-making of prospective dog owners," Animals, vol. 9, no. 124, Mar. 2019 , doi: 10.3390/ani9040124
- Kendall, Elisa F., and Deborah L. McGuinness. Ontology Engineering. Morgan & Claypool Publishers, 2019. 
- "Oxford English Dictionary." Oxford Dictionary. https://www.oed.com/.
- "SKOS Simple Knowledge Organization System RDF Schema." W3C. https://www.w3.org/TR/2008/WD-skos-reference-20080829/skos.html
