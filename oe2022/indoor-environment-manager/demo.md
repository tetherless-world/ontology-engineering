---
layout: default
title: Static Demo
---

## Static Demo

To run the demo, load the Individuals ontology (which can be found [here](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/indoor-environment-manager/oe2022/indoor-environment-manager/indoor-environment-manager.rdf))
into your favorite triplestore that is able to run SPARQL queries. 
We have tested the following queries using [Blazegraph](https://blazegraph.com/).

### Query Prefix
```sparql

PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX iem: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager-individuals/>

```

## Competency Questions
### Competency Question 1

#### Question
What IEQ parameters, such as temperature, humidity, airflow, etc., make the multiple occupants feel comfortable in an office room? There are three occupants who prefer temperatures in the range of 73°F to 77°F, 74°F to 78°F, and 75° to 78°F, respectively. All other factors are already ideal. The outdoor temperature is 18°F. The current HVAC thermostat setting is 75°F, which is the current indoor temperature. An electric space heater is available but currently switched off.

#### Description
 Our individuals ontology has been updated such that these queries should work properly with just Protégé’s built-in SPARQL query feature. If, for some reason, this method doesn’t actually work, then we recommend that you install “Snap SPARQL Query” and use that to execute the queries instead after activating a reasoner. In our testing, Snap SPARQL Query sometimes doesn’t work without a reasoner even in situations in which the built-in SPARQL query feature works without a reasoner.

#### Query
```sparql

SELECT DISTINCT ?roomComponent ?newState WHERE {
    ?roomComponent iem:isComponentOf ind:Question2Room .
    ?roomComponent iem:hasAvailableAction ?action .
  	?action iem:causesNewState ?newState .
  	?action iem:produces ?resultantEnvironment .
  	?resultantEnvironment iem:hasAirTemperatureSign ?airTemperatureSign .
  	ind:Question2EnvironmentTarget iem:hasAirTemperatureSign ?airTemperatureSign .
}

```

#### Example Results
This query shouldn’t return any results because in the relevant competency question, the current environment is already ideal. Therefore, no actions need to be suggested or taken.


### Competency Question 2

#### Question
What IEQ parameters, such as temperature, humidity, airflow, etc., make the multiple occupants feel comfortable in a living room during summer? The occupants’ profile is a 26-year-old son typing something on his laptop (metabolic rate: 1.1, Long-sleeve coveralls, t-shirt: 0.72 clo), a 59-year-old mother dancing (metabolic rate: 3.4, Long-sleeve coveralls, t-shirt: 0.72 clo), and a 32-year-old daughter cleaning the house (metabolic rate: 2.7, Long-sleeve coveralls, t-shirt: 0.72 clo). The outdoor weather is 89°F, relative humidity is 70%, air-speed is 1.2m/s, and outdoor air quality index is 34, ‘Good’. Indoor temperature is 85°F, relative humidity is 67%, and air-speed is 0.8m/s. Air-conditioner, a fan, and a dehumidifier are available. 

#### Description
This query looks for two different actions: one to change the air speed and one to change the relative humidity. Each action must be available for a particular room component that’s, in turn, part of the room individual that’s associated with the relevant competency question. The actions are selected by ensuring that they produce respective resultant environments with the same environment attribute delta signs as the target environment.

#### Query
```sparql

SELECT DISTINCT ?airSpeedRoomComponent ?airSpeedNewState ?relativeHumidityRoomComponent ?relativeHumidityNewState WHERE {
  	?airSpeedRoomComponent iem:isComponentOf ind:Question4Room .
    ?airSpeedRoomComponent iem:hasAvailableAction ?airSpeedAction .
    ?airSpeedAction iem:causesNewState ?airSpeedNewState .
    ?airSpeedAction iem:produces ?airSpeedResultantEnvironment .
    ?airSpeedResultantEnvironment iem:hasAirSpeedSign ?airSpeedSign .
  	ind:Question4EnvironmentTarget iem:hasAirSpeedSign ?airSpeedSign .
  	
  	?relativeHumidityRoomComponent iem:isComponentOf ind:Question4Room .
    ?relativeHumidityRoomComponent iem:hasAvailableAction ?relativeHumidityAction .
  	?relativeHumidityAction iem:causesNewState ?relativeHumidityNewState .
  	?relativeHumidityAction iem:produces ?relativeHumidityResultantEnvironment .
  	?relativeHumidityResultantEnvironment iem:hasRelativeHumiditySign ?relativeHumiditySign .
  	ind:Question4EnvironmentTarget iem:hasRelativeHumiditySign ?relativeHumiditySign .
}

```

#### Example Results
Turned on the fan and dehumidifier


### Competency Question 3

#### Question
In a small gym, three people are working out. 22-year-old male Jason walking on a treadmill lifting 45kg bars (metabolic rate: 4.0, wearing shorts & short-sleeve shirt: 0.36 clo), 44-year-old male Bob seated with heavy limb movement (metabolic rate: 2.2, wearing typical summer indoor clothing: 0.5 clo), and 52-year-old female Sarah walking on a treadmill with 3 mph (metabolic rate: 3.8, wearing a short-sleeve shirt: 0.57 clo). What IEQ parameters, such as temperature, humidity, airflow, etc., make the multiple occupants feel comfortable in a gym? Indoor temperature is 82°F, relative humidity is 38%, air-speed is 0.3m/s, and air quality index is 38, ‘Good’. Outdoor temperature is 80°F, relative humidity is 34%, and air-speed is 2m/s. An air conditioner is available, and windows are closed. 

#### Description
This query looks for a single action to change the air speed. The action must be available for a particular room component that’s, in turn, part of the room individual that’s associated with the relevant competency question. The action is selected by ensuring that it produces a resultant environment with the same air speed environment attribute delta sign as the target environment.

#### Query
```sparql

SELECT DISTINCT ?airSpeedRoomComponent ?airSpeedNewState WHERE {
  	?airSpeedRoomComponent iem:isComponentOf ind:Question5Room .
  	?airSpeedRoomComponent iem:hasAvailableAction ?airSpeedAction .
  	?airSpeedAction iem:causesNewState ?airSpeedNewState .
  	?airSpeedAction iem:produces ?airSpeedResultantEnvironment .
  	?airSpeedResultantEnvironment iem:hasAirSpeedSign ?airSpeedSign .
  	ind:Question5EnvironmentTarget iem:hasAirSpeedSign ?airSpeedSign .
}

```

#### Example Results
Open windows


### Competency Question 4

#### Question
In a room, only one occupant sits on a chair. Is this occupant feel comfortable? The occupant has a preferred temperature range of 72°F to 80°F and a preferred humidity range of 28% to 40%. The room temperature is 75°F and the relative humidity is 55%.

#### Description
This query corresponds with competency question 6. Given Question6Room, it returns an occupant whose corresponding comfort ranges include the environment values and who currently feels comfortable.

#### Query
```sparql

SELECT ?occupant WHERE {
	?occupant iem:occupies ind:Question6Room .
	?occupant iem:hasAirTemperatureComfortRangeLowerBound ?AirTemperatureLowerBound .
    ?occupant iem:hasRelativeHumidityComfortRangeLowerBound ?RelativeHumidityLowerBound .
	?occupant iem:hasAirTemperatureComfortRangeUpperBound ?AirTemperatureUpperBound .
	?occupant iem:hasRelativeHumidityComfortRangeUpperBound ?RelativeHumidityUpperBound .
	ind:Question6EnvironmentCurrent iem:hasAirTemperatureValue ?AirTemperatureValue .
	ind:Question6EnvironmentCurrent iem:hasRelativeHumidityValue ?RelativeHumidityValue .
	FILTER(?AirTemperatureValue <= ?AirTemperatureUpperBound) .
    FILTER(?AirTemperatureValue >= ?AirTemperatureLowerBound) .
	FILTER(?RelativeHumidityValue <= ?RelativeHumidityUpperBound) .
	FILTER(?RelativeHumidityValue >= ?RelativeHumidityLowerBound) .
 }

```

#### Example Results
he occupant don’t feel comfortable


### Competency Question 5

#### Question
In a small office space with three occupants, who is currently comfortable? Occupant 1 has a preferred temperature range of 64°F to 68°F, prefers lower humidity (25% to 35%), and enjoys a light breeze (1 m/s to 2 m/s). Occupant 2 has a preferred temperature range of 70°F to 75°F, is comfortable in varied humidity (30% to 40%), and likes a light to moderate breeze (1 m/s to 3 m/s). Occupant 3 has a preferred temperature range of 68°F to 74°F, is comfortable in most humidity settings (30% to 50%), and prefers no breeze (0 m/s to 1 m/s). The office temperature is 70°F, the relative humidity is 30%, and the air speed is 2 m/s.

#### Description
This query corresponds with competency question 7. Given Question7Room, it returns all occupants of said room that are currently comfortable, e.g. the environment values are all within an occupant’s corresponding comfort ranges.

#### Query
```sparql

SELECT ?occupant WHERE {
	?occupant iem:occupies ind:Question7Room .
	?occupant iem:hasAirSpeedComfortRangeLowerBound ?AirSpeedLowerBound .
	?occupant iem:hasAirTemperatureComfortRangeLowerBound ?AirTemperatureLowerBound .
    ?occupant iem:hasRelativeHumidityComfortRangeLowerBound ?RelativeHumidityLowerBound .
	?occupant iem:hasAirSpeedComfortRangeUpperBound ?AirSpeedUpperBound .
	?occupant iem:hasAirTemperatureComfortRangeUpperBound ?AirTemperatureUpperBound .
	?occupant iem:hasRelativeHumidityComfortRangeUpperBound ?RelativeHumidityUpperBound .
	ind:Question7EnvironmentCurrent iem:hasAirTemperatureValue ?AirTemperatureValue .
	ind:Question7EnvironmentCurrent iem:hasAirSpeedValue ?AirSpeedValue .
	ind:Question7EnvironmentCurrent iem:hasRelativeHumidityValue ?RelativeHumidityValue .
	FILTER(?AirTemperatureValue <= ?AirTemperatureUpperBound) .
    FILTER(?AirTemperatureValue >= ?AirTemperatureLowerBound) .
	FILTER(?AirSpeedValue <= ?AirSpeedUpperBound) .
	FILTER(?AirSpeedValue >= ?AirSpeedLowerBound) .
	FILTER(?RelativeHumidityValue <= ?RelativeHumidityUpperBound) .
	FILTER(?RelativeHumidityValue >= ?RelativeHumidityLowerBound) .
 }

```

#### Example Results
Occupant 2 is comfortable


## Previous Versions

- [Version 2 (OE 11)](https://docs.google.com/document/d/e/2PACX-1vQmp9z2kZzc8exMiONkRynBHpT4CQ1Jzr70PcYHPggBXrvBiSJe7M078M75pGt7Vw/pub)
- [Version 1 (OE 10)](https://docs.google.com/document/d/e/2PACX-1vSia6C1iOhK7PO1pVppIlTEVVB7-Y7DabGDwYeMTdnhEVHru-PrsXzPd_GkEVOqXg/pub)