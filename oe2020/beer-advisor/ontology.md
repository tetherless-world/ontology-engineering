[Concept Map](#conceptual-model) | [Ontology File](#ontologies)

## Conceptual Model

#### Overview
[(Figure 1 - Full Image)](images/OverviewDiagram.jpg)
![Concept Map Model](images/OverviewDiagram.jpg)
The first diagram captures a broad overview of our ontology and focuses upon the beer classes. In our ontology, a beer is defined by having a set of characteristics and being produced by a brewery. This can be seen in the above diagram. Underneath the main beer class is a variety of different beer styles. Each style is a subclass of beer and its ancestors above them. Each beer has its own set of characteristics that differentiate itself from other styles. In the upper right is the brewery class, which is a subclass of the functional business entity class found in the fibo ontology. Next to it is the bar class and the brewpub class, which is a subclass of both. The beer class connects to the characteristics through a property, "has characteristic", and to the user through preferences. 


#### Beer Characteristics
[(Figure 2 - Full Image)](images/Characteristic-Class-Diagram.jpg)
![Qualitative Characteristic Model Diagram](images/Characteristic-Class-Diagram.jpg)
Above is a diagram that looks at the main portion of our characteristics class, the measurements. The four measurements we are currently using are alcohol content, original gravity, the sweetness of a beer, color, and bitterness units. Each of these units is a subclass of the quantity value, which allows us to give it a numerical value. However, we also need to differ between the units of each class. This is where the measurement unit class comes into play. The four classes that inherit from this class are custom measurement units. Alcohol by volume is for alcohol content, degree plato for original gravity, standard reference method for color, and international bitterness unit for bitterness. This allows us to provide a different instance for each range of a specific style, which helps us to properly differentiate styles.


[(Figure 3 - Full Image)](images/Characteristic-one.jpg)
![Ingredient Characteristic Model Diagram](images/Characteristic-one.jpg)
In addition to the measurements, the following characteristics are attached. These include the style, ingredient, brand, season, and alcohol. Alcohol relates to whether or not a beer is alcoholic, which we can tell through it’s abv. Each beer also has a given style based upon its characteristics. There is then a brand for the name and a season. The main class that is expanded upon here is the ingredients. A beer can be made of a variety of different kinds of grains, hops, and yeasts. This is another way in which beers with similar measurements can be differentiated, as they may not share ingredients. Underneath the 3 main ingredients, the ontology gets a bit more specific. Finally we move on to the 3rd main class, the user class.

#### User
[(Figure 4 - Full Image)](images/UserDiagram.jpg)
![User Model Diagram](images/UserDiagram.jpg)
Our third major class is our user class, which connects to the beer class through the preferences class. In order to differentiate our ontology with other existing ontologies, we decided that we would log the search results and preferences of users in our ontology. The user is a subclass of the party in role class, allowing us to give it the identity of a person. Each user then has a user profile, which is a subclass of the record class. Each profile consists of a search history, which is a subclass of the dated structured collection class and contains a series of beers that a user has searched for, and the date they searched for said beer. In addition to this, each user has a preference, which is also a subclass of the record class. Preferences are made of different beers and characteristics. This will allow us to compare other users not only based up on their search history, but also based upon preferences we have stored.

- [Explanation pdf](files/OE_12_Conceptual_Models.pdf)
## Conceptual Model Raw Files

**Links:**
- [Figure 1 - Version 1](files/overview.uml)
- [Figures 2, 3 - Version 1](files/characteristic.uml)
- [Figure 4 - Version 1](files/updated.uml)
- [Figure 5 - Version 1](files/property_overview.uml)

## Ontologies

**Links:**
- [main-ontology](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/beer-advisor.rdf)
- [individuals-ontology](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/beer-advisor-individuals.rdf)

**View the ontology documentation at:**


## Previous Versions of Ontologies
**Links:**

- [ontology-version6 (OE-11)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-11-beer-advisor.rdf)
- [ontology-version5 (OE-10)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-10-beer-advisor.rdf)
- [ontology-version4 (OE-9)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-9-beer-advisor.rdf)
- [ontology-version3 (OE-8)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE_8_beer-advisor.rdf)
- [ontology-version2 (OE-7)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE_7_beer-advisor.rdf)
- [ontology-version1 (OE-6)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-6-beer-advisor.rdf)
- [individuals-ontology-version4 (OE-11)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-11-beer-advisor-individuals.rdf)
- [individuals-ontology-version3 (OE-10)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-10-beer-advisor-individuals.rdf)
- [individuals-ontology-version2 (OE-9)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE-9-beer-advisor-individuals.rdf)
- [individuals-ontology-version1 (OE-8)](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/beer-advisor/oe2020/beer-advisor/archived/OE_8_beer-advisor-individuals.rdf)