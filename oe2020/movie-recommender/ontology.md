[Concept Map](#conceptual-model) | [Ontology File](#ontologies)

## Conceptual Model

### General Model [(Full Size)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/movie-recommender/oe2020/movie-recommender/images/conceptualModel.jpg) [(Editable Version)](https://drive.google.com/file/d/1MSmUmnXD892Ia6nD116NB8nuCs-uXFc1/view?usp=sharing):

<img src="images/conceptualModel.jpg" width="100%">

The above model shows how most of the high level classes connect to each other in the Movie Recommender ontology. It shows the basic construction of a creative work, the various classes connected to it that serve as attributes, and how it breaks into movies and TV shows. The contributor class is also detailed in this general model.

### Genre Model [(Full Size)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/movie-recommender/oe2020/movie-recommender/images/genresConceptualModel.jpg) [(Editable Version)](https://drive.google.com/file/d/1SaZrs4M5MLkLHHiZZzHqiqZpFmZ0tR-z/view?usp=sharing):

<img src="images/genresConceptualModel(2).jpg" width="100%">

The above model shows how the concept of a genre is represented in the ontology. The genres are broken to 5 fundamental categories: Action, Comedy, Romance, Horror, and Drama. Each of these genres have many subgenres associated with them. For example, Martial Arts is a subgenre of Action. These subgenres can sometimes be subclasses of more than one genre. For example, RomanticComedy is a subgenre of Comedy and Romance. The number of subgenres displayed in the diagram is limited for the scope of this project.

### Style Model [(Full Size)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/movie-recommender/oe2020/movie-recommender/images/styleConceptualModel.jpg) [(Editable Version)](https://drive.google.com/file/d/1SaZrs4M5MLkLHHiZZzHqiqZpFmZ0tR-z/view?usp=sharing):

<img src="images/styleConceptualModel.jpg" width="100%">

The above model shows how the concept of a style is represented in the ontology. Style classifies movies outside of story elements. Rather is looks at the methods of actually producing a movie. Considerations for style include the artistic format of the movie. Artistic style is broken up between animated and live-action. From there there are many sub-categories such as 3D Animation or musicals. Budget used to produce a movie and intended audience is also a consideration. Large budget, general audience films are typically considered "Major Motion". Small budget films with very specific audiences typcially fall under art films or indie films.

### User Model [(Full Size)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/movie-recommender/oe2020/movie-recommender/images/userAccount.jpg) [(Editable Version)](https://drive.google.com/file/d/1daR8-y7vl6DvhiFOharI3-nsPbhf-V7K/view?usp=sharing):

<img src="images/userAccount.jpg" width="100%">

The above model shows how users using the ontology are represented within the ontology. This includes their watch data as well as personal preferences. The watch data includes information about how users rate the movies they watch. The user data also stores information about streaming services to which the user is subscribed to so as to limit reccomendations by the catalogs of those services.

## Ontologies

**Link to current version:**

- Current Version (OE 12)
    - [Ontology](https://github.com/tetherless-world/ontology-engineering/blob/movie-recommender/oe2020/movie-recommender/movie-recommender.rdf)
    - [Individuals](https://github.com/tetherless-world/ontology-engineering/blob/movie-recommender/oe2020/movie-recommender/movie-recommender-individuals.rdf)

**Link to past versions:**

- Version 6 (OE 11)
    - [Ontology](https://drive.google.com/file/d/1q2oJ2YW3Yzw8PPbANRtpocB7LS6cul-M/view?usp=sharing)
    - [Individuals](https://drive.google.com/file/d/15RFwmVgqy-QLh1YC1S2oIAgoXVNQOG4f/view?usp=sharing)
- Version 5 (OE 10)
    - [Ontology](https://drive.google.com/file/d/1cLP7i3rTDrrYxpbLjjhSQv2wUkFkUPAm/view?usp=sharing)
    - [Individuals](https://drive.google.com/file/d/1IoUp5YrV-CBFHxGFpdpjeGrsI0crbNDB/view?usp=sharing)
- Version 4 (OE 9)
    - [Ontology](https://drive.google.com/file/d/1XryOQJe_h0wOGZHPHF5ss-kCeKv5pent/view?usp=sharing)
    - [Individuals](https://drive.google.com/file/d/14YaUmhAJmDt_ItMQAYdlDIE79Ru_TKI3/view?usp=sharing)
- Version 3 (OE 8)
    - [Ontology](https://drive.google.com/file/d/1JN5Uro4wnQkYhcmj44V3rfWO6Cxc8iTu/view?usp=sharing)
    - [Individuals](https://drive.google.com/file/d/18tEkaSxnA0dXV7nk9A1JKYuWjcPkMSG6/view?usp=sharing)
- [Version 2 Ontology (OE 7)](https://drive.google.com/file/d/1lcfccbxgRu_YG590d4Lfwp3UPoziYQWA/view?usp=sharing)
- [Version 1 Ontology (OE 6)](https://drive.google.com/file/d/1YPB6cCIfXY1cSC047wm9jWTZ--pIk-kz/view?usp=sharing)
