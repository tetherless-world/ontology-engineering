---
layout: default
title: Static Demo
---

## Demonstration
### Static Demo

#### Note
To run the demo, load the Individuals ontology (which can be found [here](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/indoor-environment-manager/oe2022/indoor-environment-manager/indoor-environment-manager.rdf))
into your favorite triplestore that is able to run SPARQL queries. 
With the latest additions to our main ontology, some of these queries now require nontrivial reasoning. This means that they must be executed in “Snap SPARQL Query” instead of Protégé’s built-in SPARQL query feature. Additionally, we’re still investigating a problem with running Pellet on our ontology, so we recommend that you activate HermiT before executing a query.

### Static Demo
Full screen mode is available [here](https://docs.google.com/presentation/d/e/2PACX-1vQH2Dap7LI4H7aTQLuTJtaw_rCzSf4CGWNejClGBeN_tFJNbGVpfijwOSstbkRiCMU9bSoOOaxIXoaQ/pub?start=false&loop=false&delayms=3000)

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQH2Dap7LI4H7aTQLuTJtaw_rCzSf4CGWNejClGBeN_tFJNbGVpfijwOSstbkRiCMU9bSoOOaxIXoaQ/embed?start=false&loop=false&delayms=10000" frameborder="0" width="640" height="379" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>


## Query

### Query Prefix
```sparql

PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX iem: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager-individuals/>

```

### Competency Question 1

#### Question
How to meet all requirements of the multiple occupants’ comfort ranges in an office room? There are three occupants who prefer temperatures in the range of 73°F to 77°F, 74°F to 78°F, and 75° to 78°F, respectively. All other factors are already ideal. The outdoor temperature is 18°F. The current HVAC thermostat setting is 75°F, which is the current indoor temperature. An electric space heater is available but is currently switched off.

#### Description
This query shouldn’t return any results because in the relevant competency question, the current environment is already ideal. Therefore, no actions need to be suggested or taken.

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

| ?roomComponent | ?newState |
|----------------|-----------|
|                |           |

<div id="CQ2"></div>
### Competency Question 2 

#### Question
How should IEQ parameters, such as temperature, humidity, airflow, etc., be changed to make the multiple occupants feel comfortable in a living room during summer? The occupants’ profile is a 26-year-old son typing something on his laptop (metabolic rate: 1.1, Long-sleeve coveralls, t-shirt: 0.72 clo), a 59-year-old mother dancing (metabolic rate: 3.4, Long-sleeve coveralls, t-shirt: 0.72 clo), and a 32-year-old daughter cleaning the house (metabolic rate: 2.7, Long-sleeve coveralls, t-shirt: 0.72 clo). The outdoor weather is 89°F, relative humidity is 70%, and outdoor air quality index is 34, ‘Good’. Indoor temperature is 85°F and relative humidity is 67%. A fan and a dehumidifier are available.

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

| ?airSpeedRoomComponent | ?airSpeedNewState | ?relativeHumidityRoomComponent | ?relativeHumidityNewState |
|------------------------|-------------------|--------------------------------|---------------------------|
| ind:Question4Fan       | iem:On            | ind:Question4Dehumidifier      | iem:On                    |

<div id="CQ3"></div>
### Competency Question 3

#### Question
In a small gym, three people are working out. 22-year-old male Jason walking on a treadmill lifting 45kg bars (metabolic rate: 4.0, wearing shorts & short-sleeve shirt: 0.36 clo), 44-year-old male Bob seated with heavy limb movement (metabolic rate: 2.2, wearing typical summer indoor clothing: 0.5 clo), and 52-year-old female Sarah walking on a treadmill with 3 mph (metabolic rate: 3.8, wearing a short-sleeve shirt: 0.57 clo). How should IEQ parameters, such as temperature, humidity, airflow, etc., be changed to make the multiple occupants feel comfortable in a gym? Indoor air-speed is 0.3m/s, outdoor air-speed is 2m/s, and outdoor air quality index is 38, ‘Good’. An air conditioner is available, and windows are closed.

#### Description
This query looks for a single action to change the air speed. The action must be available for a particular room component that’s, in turn, part of the room individual that’s associated with the relevant competency question. The action is selected by ensuring that it produces a resultant environment with the same air speed environment attribute delta sign as the target environment. The query also requires that the resultant environment have a “good” air quality level, which is inferred by the reasoner from the fact that opening a window must produce a resultant environment with the same air quality level as the relevant outdoor environment.

#### Query
```sparql

SELECT DISTINCT ?airSpeedRoomComponent ?airSpeedNewState WHERE {
	?airSpeedRoomComponent iem:isComponentOf ind:Question5Room .
	?airSpeedRoomComponent iem:hasAvailableAction ?airSpeedAction .
	?airSpeedAction iem:causesNewState ?airSpeedNewState .
	?airSpeedAction iem:produces ?airSpeedResultantEnvironment .
	?airSpeedResultantEnvironment iem:hasAirQualityLevel iem:AirQualityLevelGood .
	?airSpeedResultantEnvironment iem:hasAirSpeedSign ?airSpeedSign .
	ind:Question5EnvironmentTarget iem:hasAirSpeedSign ?airSpeedSign .
}

```

#### Example Results

| ?airSpeedRoomComponent | ?airSpeedNewState |
|------------------------|-------------------|
| ind:Question5Window    | iem:Open          |


### Competency Question 4

#### Question
In a room, only one occupant sits on a chair. Is this occupant feel comfortable? The occupant has a preferred temperature range of 72°F to 80°F and a preferred humidity range of 28% to 40%. The room temperature is 75°F and the relative humidity is 55%.

#### Description
This query corresponds with competency question 6. Given a specific room, it returns the occupants whose corresponding comfort ranges include the environment values and who therefore currently feel comfortable. Since there are no currently comfortable occupants in competency question 6, this query intentionally returns no results.

#### Query
```sparql

SELECT ?occupant WHERE {
	?occupant iem:occupies ind:Question6Room .
	?occupant iem:hasAirTemperatureComfortRangeLowerBound ?airTemperatureLowerBound .
	?occupant iem:hasRelativeHumidityComfortRangeLowerBound ?relativeHumidityLowerBound .
	?occupant iem:hasAirTemperatureComfortRangeUpperBound ?airTemperatureUpperBound .
	?occupant iem:hasRelativeHumidityComfortRangeUpperBound ?relativeHumidityUpperBound .
	ind:Question6EnvironmentCurrent iem:hasAirTemperatureValue ?airTemperatureValue .
	ind:Question6EnvironmentCurrent iem:hasRelativeHumidityValue ?relativeHumidityValue .
	FILTER(?airTemperatureValue <= ?airTemperatureUpperBound) .
	FILTER(?airTemperatureValue >= ?airTemperatureLowerBound) .
	FILTER(?relativeHumidityValue <= ?relativeHumidityUpperBound) .
	FILTER(?relativeHumidityValue >= ?relativeHumidityLowerBound) .
}

```

#### Example Results

| ?occupant |
|-----------|
|           |


### Competency Question 5

#### Question
In a small office space with three occupants, who are currently comfortable? Occupant 1 has a preferred temperature range of 64°F to 68°F, prefers lower humidity (25% to 35%), and enjoys a light breeze (1 m/s to 2 m/s). Occupant 2 has a preferred temperature range of 70°F to 75°F, is comfortable in varied humidity (30% to 40%), and likes a light to moderate breeze (1 m/s to 3 m/s). Occupant 3 has a preferred temperature range of 68°F to 74°F, is comfortable in most humidity settings (30% to 50%), and prefers no breeze (0 m/s to 1 m/s). The office temperature is 70°F, the relative humidity is 30%, and the air speed is 2 m/s.

#### Description
This query corresponds with competency question 7. Given a specific room, it returns the occupants whose corresponding comfort ranges include the environment values and who therefore currently feel comfortable.

#### Query
```sparql

SELECT ?occupant WHERE {
	?occupant iem:occupies ind:Question7Room .
	?occupant iem:hasAirSpeedComfortRangeLowerBound ?airSpeedLowerBound .
	?occupant iem:hasAirTemperatureComfortRangeLowerBound ?airTemperatureLowerBound .
	?occupant iem:hasRelativeHumidityComfortRangeLowerBound ?relativeHumidityLowerBound .
	?occupant iem:hasAirSpeedComfortRangeUpperBound ?airSpeedUpperBound .
	?occupant iem:hasAirTemperatureComfortRangeUpperBound ?airTemperatureUpperBound .
	?occupant iem:hasRelativeHumidityComfortRangeUpperBound ?relativeHumidityUpperBound .
	ind:Question7EnvironmentCurrent iem:hasAirTemperatureValue ?airTemperatureValue .
	ind:Question7EnvironmentCurrent iem:hasAirSpeedValue ?airSpeedValue .
	ind:Question7EnvironmentCurrent iem:hasRelativeHumidityValue ?relativeHumidityValue .
	FILTER(?airTemperatureValue <= ?airTemperatureUpperBound) .
	FILTER(?airTemperatureValue >= ?airTemperatureLowerBound) .
	FILTER(?airSpeedValue <= ?airSpeedUpperBound) .
	FILTER(?airSpeedValue >= ?airSpeedLowerBound) .
	FILTER(?relativeHumidityValue <= ?relativeHumidityUpperBound) .
	FILTER(?relativeHumidityValue >= ?relativeHumidityLowerBound) .
}

```

#### Example Results

| ?occupant          |
|--------------------|
| Question7Occupant2 |


## Previous Versions

- [Version 3 (OE 12)](https://docs.google.com/document/d/e/2PACX-1vT6GlxiJcW366IP9Q9z8ll9hKZYGSwCQGsf3LUQsGIhDnA1J-5PNSHjzCqTdXFpHQ/pub)
- [Version 2 (OE 11)](https://docs.google.com/document/d/e/2PACX-1vS4y9207qJCeofMWqARRhKca6QTTlc-uFwEmmDvxB6ejVSF0k8LVK3YXE1qalDzsg/pub)
- [Version 1 (OE 10)](https://docs.google.com/document/d/e/2PACX-1vSia6C1iOhK7PO1pVppIlTEVVB7-Y7DabGDwYeMTdnhEVHru-PrsXzPd_GkEVOqXg/pub)