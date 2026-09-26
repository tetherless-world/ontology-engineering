[Concept Map](#conceptual-model) | [Ontology File](course-recommender.rdf)

## Conceptual Model

The conceptual model for our most recent ontology version can be seen as a [drawio file](https://drive.google.com/file/d/1b3JVHcvj6Lowty8aPcan0jGcSv3qkH0Z/view?usp=sharing).
![Overall Concept Map](images/concept_map_overall.png)
The concept map above shows an overview of the classses and relationships in our ontology. In the following sections we break down this view into related components.

### People
![People Sub-Concept Map](images/concept_map_people.png)

The types of people that we represent in the Course Recommender Ontology are students and faculty members. Faculty
members may be instructors or advisors. For students, we capture their topics of interest and class year, as well as
the courses they are registered in and their plan of study (shown in the Plans of Study Section).

### Courses
![Courses Sub-Concept Map](images/concept_map_courses.png)

For courses, we capture information including course codes, the number of credits the course
provides, the topic areas it covers, any special tags (corresponding to special
requirements that they might fulfill), and the department associated with that course. Courses also have
required- and recommended-prerequisite relations. 

Specific instances of courses are represented as ScheduledCourseSections. ScheduledCourseSections correspond to
actual course offerings that a student can register for, and include schedule and instructor information.

### Plans of Study
![Requirements Sub-Concept Map](images/concept_map_requirements.png)

A student's Plan of Study is meant to model the student's intended graduation degree and major along with their course
information. Relevant information about courses includes which courses the student has completed, which courses they
are currently registered in, and which courses they plan to take in future semesters.

Additionally, through the
Degree concept, we have relations to Requirements (or Graduation Requirements). Requirements can be fulfilled by
certain courses - specified by CourseCodeRestrictions - and have relations that are used to determine how different
graduation requirements interact with each other.  Requirements are an essential piece in enabling our intended
course recommendation system, as the courses that are recommended to students should help them make progress in 
fulfilling their remaining graduation requirements.

## Ontologies

- [Main Ontology][oe-current]
- [Individuals][oe-current-ind]

### Previous Versions

| Ontology                    | Individuals                  |
|-----------------------------|------------------------------|
| [OE 12][oe-12-ont]          | [OE 12][oe-12-ind]           |
| [OE 11][oe-11-ont]          | [OE 11][oe-11-ind]           |
| [OE 10][oe-10-ont]          | [OE 10][oe-10-ind]           |
| [OE 9][oe-9-ont]            | [OE 9][oe-9-ind]             |
| [OE 8][oe-8-ont]            | [OE 8][oe-8-ind]             |
| [OE 7][oe-7-ont]            |                              |

[oe-current]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/course-recommender/oe2020/course-recommender/course-recommender.rdf
[oe-current-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/course-recommender/oe2020/course-recommender/course-recommender-individuals.rdf

[oe-12-ont]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/7dd19e4a8a78e7143a5ff6002fd206ed4b20bf13/oe2020/course-recommender/course-recommender.rdf
[oe-12-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/7dd19e4a8a78e7143a5ff6002fd206ed4b20bf13/oe2020/course-recommender/course-recommender-individuals.rdf

[oe-11-ont]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/4316f30ca8a93fd652ff4d4861c7ba101e28c7fa/oe2020/course-recommender/course-recommender.rdf
[oe-11-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/4316f30ca8a93fd652ff4d4861c7ba101e28c7fa/oe2020/course-recommender/course-recommender-individuals.rdf

[oe-10-ont]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/f611a01bbe4915a8af9f6bfa2e8a11d371b7ed0e/oe2020/course-recommender/course-recommender.rdf
[oe-10-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/f611a01bbe4915a8af9f6bfa2e8a11d371b7ed0e/oe2020/course-recommender/course-recommender-individuals.rdf

[oe-9-ont]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/83366e952dae6beb86ddcd660f004076a31b81ea/oe2020/course-recommender/course-recommender.rdf
[oe-9-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/83366e952dae6beb86ddcd660f004076a31b81ea/oe2020/course-recommender/course-recommender-individuals.rdf

[oe-8-ont]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/1d4ed76076bb7bc6687dd92ace36fc8734f34995/oe2020/course-recommender/course-recommender.rdf
[oe-8-ind]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/83366e952dae6beb86ddcd660f004076a31b81ea/oe2020/course-recommender/course-recommender-individuals.rdf

[oe-7-ont]: https://raw.githubusercontent.com/tetherless-world/ontology-engineering/5f9f5249fb24d6367fbf894c1673205298ef0f96/oe2020/course-recommender/course-recommender.rdf
