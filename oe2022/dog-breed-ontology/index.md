---
layout: default
title: About
---

## Abstract

This application recommends dog breeds to households given some specific characteristics of the homeowners. Additionally, the recommendation would provide a list of other potential dog breeds that may suit the family’s needs to account for any potential subjective factors like cuteness.

<img src="images/dog1.jpg"/>

## Project Overview Diagrams

The Dog Breed Ontology is intended to be used with external resouces, primarily dog breed information sources, to recommend dog breeds to potential adopters. Below is the imagined system's architecture which shows how our ontology would be used. A user interface would ingest information about the potential adopter, potentially using natural language processing on a given description of the adopter. Several potential sources of dog breed information are also shown.

<img style="float: center;" src="images/SystemArchDiagram.png"/>

Below is an activity diagram of the basic flow of the system. A user enters household and individual information, and any personal preferences, which are used by the ontology to reason what requirements a breed needs to fulfill. After the user confirms that any assumptions made by the system are correct, the recommender uses the reasoning capabilities of the ontology to classify each dog breed and determine which breeds are the best fit. These are then returned to the user. 

<img style="float: center;" src="images/ActivityDiagramBasic.png"/>

It may be that the user is unsatisfied with the results, either because they do not like a specific breed that was recommended or because they realized they needed to give the system more information about their needs and preferences. The below activity diagram shows that process. 

<img style="float: center;" src="images/ActivityDiagramAlt.png"/>

## Point of Contact

Ashley Choi: <choia5@rpi.edu>

Debjani Ray-Majumder: <raymad@rpi.edu>

Danielle Villa: <villad4@rpi.edu>

## List of Resources

<table>
  <tr>
    <th>Resources</th>
    <th>Links</th>
  </tr>
  <tr>
    <td>1. Ontology</td>
    <td>(a) <a href="https://github.com/tetherless-world/ontology-engineering/tree/dog-breed-ontology/oe2022/dog-breed-ontology">Base Ontology</a> <br> (b) <a href="https://github.com/tetherless-world/ontology-engineering/tree/dog-breed-ontology/oe2022/dog-breed-ontology">Small Individuals Ontology</a> <br> (c) <a href="https://github.com/tetherless-world/ontology-engineering/tree/dog-breed-ontology/oe2022/dog-breed-ontology">Large Individuals</a> </td>
  </tr>
  <tr>
    <td>2. Term List</td>
    <td> <a href="https://dog-breed-ontology--rpi-ontology-engineering.netlify.app/oe2022/dog-breed-ontology/termlist">Mapped Vocabularies</a> </td>
  </tr>
  <tr>
    <td>2. Competency Questions</td>
    <td> <a href="https://dog-breed-ontology--rpi-ontology-engineering.netlify.app/oe2022/dog-breed-ontology/demo">Demonstrations and SPARQL Queries</a> </td>
  </tr>
  <tr>
    <td>3. Presentations:</td>
    <td> <a href="https://dog-breed-ontology--rpi-ontology-engineering.netlify.app/oe2022/dog-breed-ontology/presentations">Project presentations during class</a> </td>
  </tr>
</table>

## Acknowledgements

This work is undertaken as a part of Fall 2022 CSCI 4340 Ontologies. We would like to thank our professors Dr. Deborah McGuinness and Ms. Elisa Kendall for their teaching and guidance. We would also like to thank our mentors Jade Franklin and Sola Shirai for their help and feedback, and Sabbir Rashid for his advice on query writing. 

<img src="images/dog2.jpg"/>
