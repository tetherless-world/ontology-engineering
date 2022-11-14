---
layout: default
title: Static Demo
---

## Static Demo

To run the demo, load the Individuals ontology (which can be found [here](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/indoor-environment-manager/oe2022/indoor-environment-manager/indoor-environment-manager.rdf))
into your favorite triplestore that is able to run SPARQL queries. 
We have tested the following queries using [Blazegraph](https://blazegraph.com/).

## Competency Questions
### Competency Question 1

#### Question
What IEQ parameters, such as temperature, humidity, airflow, etc., make the multiple occupants feel comfortable in an office room? There are three occupants who prefer temperatures in the range of 73°F to 77°F, 74°F to 78°F, and 75° to 78°F, respectively. All other factors are already ideal. The outdoor temperature is 18°F. The current HVAC thermostat setting is 75°F, which is the current indoor temperature. An electric space heater is available but currently switched off.

#### Query
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX iem: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager-individuals/>

SELECT ?roomComponent ?newState WHERE {
        ?roomComponent iem:hasAvailableAction ?action .
        ?action iem:causesNewState ?newState .
        ?action iem:produces ?resultantEnvironment .
        ?resultantEnvironment iem:hasAirTemperatureSign ?airTemperatureSign .
        ind:Question2EnvironmentTarget iem:hasAirTemperatureSign ?airTemperatureSign .
}
```

#### Example Results
Keep the thermostat setting at 75°F


### Competency Question 2

#### Question
What IEQ parameters, such as temperature, humidity, airflow, etc., make the multiple occupants feel comfortable in a living room during summer? The occupants’ profile is a 26-year-old son typing something on his laptop (metabolic rate: 1.1, Long-sleeve coveralls, t-shirt: 0.72 clo), a 59-year-old mother dancing (metabolic rate: 3.4, Long-sleeve coveralls, t-shirt: 0.72 clo), and a 32-year-old daughter cleaning the house (metabolic rate: 2.7, Long-sleeve coveralls, t-shirt: 0.72 clo). The outdoor weather is 89°F, relative humidity is 70%, air-speed is 1.2m/s, and outdoor air quality index is 34, ‘Good’. Indoor temperature is 85°F, relative humidity is 67%, and air-speed is 0.8m/s. Air-conditioner, a fan, and a dehumidifier are available. 

#### Query
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX iem: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager-individuals/>

SELECT ?airTemperatureRoomComponent ?airTemperatureNewState ?relativeHumidityRoomComponent ?relativeHumidityNewState WHERE {
        ?airTemperatureRoomComponent iem:hasAvailableAction ?airTemperatureAction .
        ?airTemperatureAction iem:causesNewState ?airTemperatureNewState .
        ?airTemperatureAction iem:produces ?airTemperatureResultantEnvironment .
        ?airTemperatureResultantEnvironment iem:hasAirTemperatureSign ?airTemperatureSign .
        ind:Question4EnvironmentTarget iem:hasAirTemperatureSign ?airTemperatureSign .       

        ?relativeHumidityRoomComponent iem:hasAvailableAction ?airHumidityAction .
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

#### Query
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX iem: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager/>
PREFIX ind: <https://tw.rpi.edu/ontology-engineering/oe2022/indoor-environment-manager-individuals/>

SELECT ?airSpeedRoomComponent ?airSpeedNewState WHERE {
        ?airSpeedRoomComponent iem:hasAvailableAction ?airSpeedAction .
        ?airSpeedAction iem:causesNewState ?airSpeedNewState .
        ?airSpeedAction iem:produces ?airSpeedResultantEnvironment .
        ?airSpeedResultantEnvironment iem:hasAirSpeedSign ?airSpeedSign .
        ind:Question5EnvironmentTarget iem:hasAirSpeedSign ?airSpeedSign .
}
```

#### Example Results
Open windows