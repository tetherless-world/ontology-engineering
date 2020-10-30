[Concept Map](#conceptual-model) | [Ontology File](#ontologies)

## Conceptual Model

The conceptual model for the ontology developed in this project is shown below. The figure presents the general idea of the ontology and, although it does not present details for many classes, it is an accurate simple guide for someone getting familiar with the beer-ontology and how it should be used in a beer-advisor application. 

![Concept Map Subject Model](images/UserDiagram.jpg)


Beer classification involves the attributes that are intrinsic and extrinsic to a certain beer. In order to address this issue, the class Beer has an attribute called Characteristic which is responsible for summarizing all important features that are related to a specific beer. For example, beer is made of a set of ingredients. Those ingridients are necessary for different types of classification such as Wheat beers which have, obviously, wheat as an ingredient. Moreover, each beer has a specific color, bitterness and alcohol content. These characteristic are also taken into account and, since they are measured with some scale, they are subclasses of a Quantity Value. Note that the characteristic color, for instance, is measured through the standard reference method while alcohol content is measured by alcohol by volume and bitterness is measured using the international bitterness unit. An overview of beer characteristics and its association with other attributes is shown below.

![Characteristic Model Diagram](images/Characteristic-Class-Diagram.jpg)


## Ontologies

**Link:**
[ontolgy-version1](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/OE_7_beer-advisor.rdf)

**View the ontology documentation at:**
