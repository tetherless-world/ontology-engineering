---
layout: default
title: About
---

## When To Go Where

When to go where is a project that aims to promote outdoor exploration across the 63 National Parks in the United States. We would like to give people a tool that will allow them to find national parks that will fit any preferences that they may have. We want to give people as few excuses as possible for not pursing outdoor activities such as camping and hiking.

To achieve this we are creating a semantically enabled application that will leverage an OWL ontology to answer user questions. Our interface will give users options to input preferences and using semantics we will identify the best parks that match a users particular criteria.

## Developers

- [Samyuth Sagi](https://github.com/Samyuth)
- [Tyler Layton](https://github.com/TylerLayton123)
- [Ben Rodgers](https://github.com/benrodgers14)
- [Annabelle Choi](https://github.com/snoopy0328)

## Workflow Diagram
![](images/OE12_WhenToGoWhere_ConceptualModel.png)

The conceptual model above is a visual representation of the ontology that we developed in this project. In the above we can see that there are a set of concepts such as Animal, Activity, Accommodation, Facility, Park Statistics, Terrain, and Climate. All of these concepts are attached to a central concept National Park which is the focus of our ontology. They also have sets of other concepts that are connected to them such as Accommodation which is attached to Campground, Hotel, Capacity, Availability, and Amenities.
	
The conceptual model also shows how we have connected the different concepts in our ontology. Using the relations we have defined we are able to query our ontology to answer specific questions. For example, to find the longest trail in California, the system would look at parks in California, check which trails they have, and find the one with the greatest length. The conceptual model helps the system understand and process these connections efficiently.

## List of Resources

<table>
  <tr>
    <th>Resources</th>
    <th>Links</th>
  </tr>
  <tr>
    <td>1. Ontology</td>
    <td><a href="https://when-to-go-where--rpi-ontology-engineering.netlify.app/oe2024/when-to-go-where/ontology">When To Go Where</a></td>
  </tr>
  <tr>
    <td>2. Term List</td>
    <td><a href="https://when-to-go-where--rpi-ontology-engineering.netlify.app/oe2024/when-to-go-where/termlist">Curated Terms List</a> </td>
  </tr>
  <tr>
    <td>2. Competency Questions</td>
    <td><a href="https://when-to-go-where--rpi-ontology-engineering.netlify.app/oe2024/when-to-go-where/demo">SPARQL Queries</a> </td>
  </tr>
  <tr>
    <td>3. Presentations:</td>
    <td><a href="https://when-to-go-where--rpi-ontology-engineering.netlify.app/oe2024/when-to-go-where/presentations">Project presentations during class</a> </td>
  </tr>
</table>

## Acknowledgements

We would like to thank the following individuals for their guidance and support throughout this course:

- **Instructors**: Prof. Deborah L. McGuinness and Ms. Elisa Kendall, for their expertise and instruction.
- **Course Managers**: Jade Franklin, Vladia Pinheiro, Kelsey Rook, and Danielle Villa, for their dedicated coordination and assistance.