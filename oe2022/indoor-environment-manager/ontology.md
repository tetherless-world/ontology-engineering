[Concept Map](#conceptual-model) | [Ontology File](#ontologies) 

## Conceptual Model

We aim to create a system that, given a small room containing specified environment-affecting components as well as the demographic information for up to several occupants, will suggest an action to take that will increase the overall comfort of the occupants. Our ontology supports this reasoning by connecting a room and its components, occupants, and environment.


### Ontology Overview

![Ontology Overview Diagram](images/OE_13_IEQ_Management_System_ConceptualModel_1.PNG)

This concept map shows how the most important high-level resources are connected in our ontology. Central to our project is a Room, which has Room Components— objects in the room that have some effect on the room’s environment— and one or more Occupants, which have various characteristics from which we may calculate a comfort range. Room components are either Power Consuming or Non-Power Consuming, with priority given to actions that use Non-Power Consuming Components during action recommendation. Each Room Component has multiple possible Component States and Component Actions; each action produces a new component state, as well as a different Environment. Additionally, each Room has one or more associated environments, including Indoor Environments, which refer to the Current Indoor Environment and some set of possible indoor environments, and Delta-Defined Environments, which are Environments defined by their difference from some other Environment. The Current Indoor Environment is defined in absolutes, while Resultant Indoor Environments are also Delta-Defined Environments. One Ideal Environment should exist, representing some environment that satisfies the comfort needs of the occupants as closely and possible. An Outdoor Environment is some environment associated with an Indoor Environment such that there is some influence on the Indoor Environment that can be exerted by opening a Window. This Outdoor Environment is expressed as the difference from the Current Indoor Environment, as its effect on the Indoor Environment is dependent on whether it has a negative or positive difference from the Indoor Environment’s attributes.

### Room Component
![Room Component Diagram](images/OE_13_IEQ_Management_System_ConceptualModel_2.PNG)

This diagram shows, in more detail, what Room Components are considered in our system as well as their possible states. Each Room Component Action is associated with a particular Room Component, causes the component to have a new Component State, and produces a new Environment— specifically a Resultant Environment, defined in terms of the change the Room Component Action produces.

### Environment
![Environment Diagram](images/OE_13_IEQ_Management_System_ConceptualModel_3.PNG)

This diagram reiterates the various subclasses of Environment created in our ontology, as well as a clarification of the attributes each type of Environment should have. The Current Indoor Environment is defined in absolute terms of air speed, relative humidity, and air temperature. The Outdoor Environment associated with an Indoor Environment has its air speed, humidity, and temperature defined in relative terms, but also has two absolute attributes, air quality and daylight intensity, which are so defined because of the assumption that the default Indoor Environment air quality is Good, and lack of daylight will never affect air speed and humidity, or decrease indoor temperature. The remainder of Outdoor Environment attributes, as well as Resultant and Ideal Indoor Environment attributes, are, for the scope of this project, described in general terms as having a Positive or Negative difference from the Current Indoor Environment.

### Air Quality
![Air Quality Diagram](images/OE_13_IEQ_Management_System_ConceptualModel_4.PNG)

This diagram shows how our ontology models the relationship between outdoor and indoor air quality, which is a special case: while turning some component on and off will be one-to-one with an increase or decrease in some environment attribute, actions that allow an Outdoor Environment to start or stop affecting the Current Indoor Environment depend on the status of the Outdoor Environment to determine what the Resultant Indoor Environment will be. To infer such a result, we use a specific Outdoor Affected Action, which takes into account some Outdoor Environment to produce a Resultant Indoor Environment with an inferred Air Quality Level.

### Occupants
![Occupant Diagram](images/OE_13_IEQ_Management_System_ConceptualModel_5.PNG)

This occupant shows the attributes associated with an Occupant in our ontology. Each Occupant occupies exactly one room, and has associated data attributes from which their ideal environments can be calculated, externally to the ontology, in multiple optional ways.

### Ontology Prefixes
- cmns-cls="https://www.omg.org/spec/Commons/Classifiers/"
- cmns-col="https://www.omg.org/spec/Commons/Collections/"
- cmns-pts="https://www.omg.org/spec/Commons/PartiesAndSituations/"

### Previous Versions

- [Version 6 (OE 13)](https://docs.google.com/document/d/e/2PACX-1vQylY9mn8MdmqGYpoH_aO8xqncU3q8qgM0bVfN_cicqdNd_aeedkyW_PFIrupZSy_AX94yfTG0xE-EJ/pub) CURRENT
- [Version 5 (OE 12)](https://docs.google.com/document/d/e/2PACX-1vSw7lUhroHhFwmxZBdyKkvm6LnfRIOyQBr9keHI-LKNRx5j0NTQQxeY5LHw033ltmrAoSu5JqzxsjZ2/pub)
- [Version 4 (OE 10)](https://drive.google.com/file/d/1KBWr0WCVRvt_qdKMcTlZXjD_QgQer4YE/view?usp=sharing)
- [Version 3 (OE 8)](https://drive.google.com/file/d/1TKyZMECKkrVbj1IumNUA7Mr-ySvIPOyF/view?usp=sharing)
- [Version 2 (OE 6)](https://drive.google.com/file/d/1flNzd0NzZzrsa6nSemaQal0lpTnElB1l/view?usp=sharing)
- [Version 1 (OE 5)](https://drive.google.com/file/d/1yJqxKVTRcumLYXdhePVD13OTwe4al6JT/view?usp=sharing)


## Ontologies
- [Main Ontology][oe-current]
- [Individuals][oe-current-ind]

### Previous Versions

| Ontology                   | Individuals        |
|----------------------------|--------------------|
| [OE 13][oe-13-ont] CURRENT | [OE 13][oe-13-ind] CURRENT |
| [OE 12][oe-12-ont]         | [OE 12][oe-12-ind] |
| [OE 11][oe-11-ont]         | [OE 11][oe-11-ind] |
| [OE 10][oe-10-ont]         | [OE 10][oe-10-ind] |
| [OE 9][oe-9-ont]           | [OE 9][oe-9-ind]   |
| [OE 8][oe-8-ont]           | [OE 8][oe-8-ind]   |
| [OE 7][oe-7-ont]           |                    |
| [OE 6][oe-6-ont]           |                    |

[oe-current]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/indoor-environment-manager/oe2022/indoor-environment-manager/indoor-environment-manager.rdf
[oe-current-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/indoor-environment-manager/oe2022/indoor-environment-manager/indoor-environment-manager-individuals.rdf

[oe-13-ont]: https://drive.google.com/file/d/1h9NlJgBPecFV3bnhgzx_Z4ZnwIR8DevD/view?usp=sharing
[oe-13-ind]: https://drive.google.com/file/d/1P3N7OYgSOJvUAa04GMwaPEmxjXh11Q8j/view?usp=sharing
[oe-12-ont]: https://drive.google.com/file/d/163wP6_7lnsurJFzRiVUyjKO954ZL0PIa/view?usp=sharing
[oe-12-ind]: https://drive.google.com/file/d/1OOd6jBaszlkFgTx0_n9utCOoqBs2COxM/view?usp=sharing
[oe-11-ont]: https://drive.google.com/file/d/1XtraM1W_y4D_L-pubxanNSri4vryW80t/view?usp=sharing
[oe-11-ind]: https://drive.google.com/file/d/1BlrUgyI8UzMUdmbOg-BKcu15iROlOkXJ/view?usp=sharing
[oe-10-ont]: https://drive.google.com/file/d/1BtQrXq5zChT-ZGwCXyW8THV615Ppe5o8/view?usp=sharing
[oe-10-ind]: https://drive.google.com/file/d/17Ie0SSndCoWPiWMl3wj7VhdtMU0AvML6/view?usp=sharing
[oe-9-ont]: https://drive.google.com/file/d/13iBBe-5aJmbTNVseWYV-ZhUIzVuZ3SMb/view?usp=sharing
[oe-9-ind]: https://drive.google.com/file/d/1XO-PXqexPTZ2O4cIBCV2Ccc0bhMNhBoE/view?usp=sharing
[oe-8-ont]: https://drive.google.com/file/d/1X9NW2gPrfn2bKI22yidyKDglUxtjOJCO/view?usp=sharing
[oe-8-ind]: https://drive.google.com/file/d/1qLbnwGmGNuiXDlMiTI534nDgBdnLOVHK/view?usp=sharing
[oe-7-ont]: https://drive.google.com/file/d/1y_wbfqx8kfL1v-gwhOmNouOI81pz6AY8/view?usp=sharing
[oe-6-ont]: https://drive.google.com/file/d/1xO0Oi_e_AuzzqE3LZpJdHwQkIVfQtHPt/view?usp=sharing
