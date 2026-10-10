---
---

## Static Demo

To run the demo, load the Individuals ontology (which can be found [here](https://raw.githubusercontent.com/tetherless-world/ontology-engineering/course-recommender/oe2020/course-recommender/course-recommender-individuals.rdf))
into your favorite triplestore that is able to run SPARQL queries. 
We have tested the following queries using [Blazegraph](https://blazegraph.com/).

## Competency Questions
### Competency Question 1

#### Question

What are all the prerequisite courses need to take the CSCI 4340 Ontologies course?

#### Query

```sparql
prefix oe2020-crs-rec: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender/>
prefix oe2020-crs-rec-ind: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/>
prefix lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
SELECT DISTINCT ?prerequisiteCourse ?prerequisiteCourseName
WHERE {
  VALUES ?targetCourseTag { "CSCI-4340" }
  ?targetcourse oe2020-crs-rec:hasCourseCode [ lcc-lr:hasTag ?targetCourseTag ] ;
                oe2020-crs-rec:hasRequiredPrerequisite+ ?prerequisiteCourse .
  ?prerequisiteCourse oe2020-crs-rec:hasName ?prerequisiteCourseName .
}
```

#### Example Results

*Note that the example URIs use a namespace prefix for ease-of-reading.*

We obtain a number of prerequisites that correctly match our expected results.
The only direct prerequisite for CSCI-4340 is Computer Science I, but Computer Science I
has its own prerequisites, which we also see in our results.

| prerequisiteCourse           | prerequisiteCourseName          |
|------------------------------|---------------------------------|
| oe2020-crs-rec-ind:crs000102 | Computer Science I              |
| oe2020-crs-rec-ind:crs000138 | Data Structures                 |
| oe2020-crs-rec-ind:crs000188 | Foundations of Computer Science |
| oe2020-crs-rec-ind:crs000205 | Introduction to Algorithms      |

### Competency Question 2

#### Question

*This question will use the course history of Jacob Shomstein to produce an
answer, but a full list of courses completed is omitted for privacy.*

I am a rising senior and I want to take the smallest number of courses required
to complete my degree. I also want to take “easier” courses whenever possible
to allow for more time to plan for a future career. What courses can fulfill my
remaining requirements?

#### Note

> We don’t have a complete information encoded surrounding graduation
> requirements (since there doesn’t seem to be any convenient way for us to
> automate adding them, the only ones we have right now have been done by
> hand). Therefore for demonstrative purposes we will show how we can achieve
> this query by (1) getting all courses that can fulfill portions of the HASS
> core requirements (which we have mostly encoded, along with one Integrative
> Pathway option), (2) remove all courses that Jacob has already completed, and
> (3) filter out courses by course level to only choose “easy” courses (which
> we will define as being below the 4000 level, for this query example).

#### Query

```sparql
prefix oe2020-crs-rec: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender/>
prefix oe2020-crs-rec-ind: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/>
prefix lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
SELECT DISTINCT ?recCourse ?recCourseName ?recCourseLabel
WHERE {
  # the URI for Jacob in our individuals ontology
  ?usrUri oe2020-crs-rec:hasName "jacob" ;
          oe2020-crs-rec:hasStudyPlan [ oe2020-crs-rec:hasCompletedCourse ?completedCourseSection ] .
  ?completedCourseSection oe2020-crs-rec:isCourseSectionOf ?completedCourse .
  ?requirement a oe2020-crs-rec:Requirement ;
               oe2020-crs-rec:hasCourseCodeRestriction ?ccRest .
  OPTIONAL { ?ccRest oe2020-crs-rec:hasValidCourseCodeTag ?validTag }
  OPTIONAL { ?ccRest oe2020-crs-rec:hasValidDepartmentCodeTag ?validDeptTag }
  OPTIONAL { ?ccRest oe2020-crs-rec:hasValidLevelMax ?validLevelMax }
  OPTIONAL { ?ccRest oe2020-crs-rec:hasValidLevelMin ?validLevelMin }
  ?recCourse a oe2020-crs-rec:Course ;
             oe2020-crs-rec:hasCourseCode ?recCourseCode ;
             oe2020-crs-rec:hasName ?recCourseName ;
             rdfs:label ?recCourseLabel .
  ?recCourseCode oe2020-crs-rec:hasLevel ?recCourseLevel ;
                 lcc-lr:hasTag ?recCCTag ;
                 oe2020-crs-rec:hasDepartmentCode [ lcc-lr:hasTag ?recCCDeptTag ] .
  FILTER (?recCourse != ?completedCourse ) # filter out courses that have already been completed
  FILTER (?recCourseLevel < 4000) # only select "easy" courses
  FILTER ( (?recCCTag = ?validTag) || (?recCCDeptTag = ?validDeptTag && ?validLevelMin <= ?recCourseLevel && ?validLevelMax >= ?recCourseLevel)) # check that the course can satisfy restrictions
}
```

#### Example Results
*Note that the example URIs use a namespace prefix for ease-of-reading.*

Due to the limited scope of our implementation, only 1 result is returned. This result is based on one of
the graduation requirements which captures specific courses (which include COGS courses) and levels
(restricting the valid levels to over 2000), which this course matches. 

| recCourse                    | recCourseName                     | recCourseLabel |
|------------------------------|-----------------------------------|----------------|
| oe2020-crs-rec-ind:crs000015 | Introduction to Cognitive Science | COGS-2120      |

### Competency Question 3

#### Question

I have taken CSCI 4340 Ontologies and CSCI 4020 Design and Analysis of
Algorithms. What are some courses like CSCI 6340 Ontologies that I should take
next fall?

#### Query

```sparql
prefix oe2020-crs-rec: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender/>
prefix oe2020-crs-rec-ind: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/>
prefix lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
SELECT DISTINCT ?validCourse ?validCourseName
WHERE {
  VALUES ?completedCourseTag { "CSCI-4340" "CSCI-4020" }
  ?completedCourse oe2020-crs-rec:hasCourseCode [
    lcc-lr:hasTag ?completedCourseTag
  ] .
  ?completedCourse oe2020-crs-rec:hasRequiredPrerequisite* ?completedCourseInferred .
  ?validCourseSec a oe2020-crs-rec:ScheduledCourseSection ;
                  oe2020-crs-rec:hasSemester [
                   oe2020-crs-rec:hasTerm "fall" ;
                   oe2020-crs-rec:hasYear 2020
                 ] ;
                  oe2020-crs-rec:isCourseSectionOf ?validCourse .
  ?validCourse a oe2020-crs-rec:Course .
  ?validCourse oe2020-crs-rec:hasName ?validCourseName .
  FILTER NOT EXISTS {
    ?validCourse oe2020-crs-rec:hasRequiredPrerequisite+ ?filterPrereqs .
    FILTER(?filterPreqreqs != ?completedCourseInferred)
  }
  FILTER (?validCourse != ?completedCourseInferred)
}
LIMIT 10
```

#### Example Results

*Note that the example URs use a namespace prefix for ease-of-reading.*

This query may have varying results, since we include a LIMIT in the query. We use inference to
determine which course prerequisites have been fulfilled based on the fact that two advanced courses
have already been completed. Based on the prerequisites that are inferred from these courses,
candidate courses to recommend are generated by checking that they have not already been completed
and checking that they do not overlap with any of the inferred completed courses.

| validCourse              | validCourseName |
|--------------------------|-----------------|
| oe2020-crs-rec:crs000015 | Introduction to Cognitive Science |
| oe2020-crs-rec:crs000023 | Introduction to Linguistics |
| oe2020-crs-rec:crs000037 | Introduction to Cognitive Neuroscience |
| oe2020-crs-rec:crs000687 | Programming for Cognitive Science and Artificial Intelligence |
| oe2020-crs-rec:crs000692 | Game AI |
| oe2020-crs-rec:crs000696 | Learning and Advanced Game AI |
| oe2020-crs-rec:crs000059 | Topics in Cognitive Science |
| oe2020-crs-rec:crs000063 | Undergraduate Thesis |
| oe2020-crs-rec:crs000103 | Master's Project |
| oe2020-crs-rec:crs000113 | Master's Thesis |

## SPARQL Query Document Links

-[Week 13 SPARQL Queries](https://github.com/tetherless-world/ontology-engineering/blob/628bd433e492f5a76d6346face7d6d59c0122f78/oe2020/course-recommender/queries/OE_13_CourseRecommender_SPARQLQueries.sparql)

-[Week 11 SPARQL Queries](https://docs.google.com/document/d/e/2PACX-1vSNBvI4Ea8cJPNZj-vL0r0344MjT63iemZSwAxOHSkA8jPIZuhoMUOMdQSX8AMXO-u7RGMwOjabhXke/pub)

-[Week 10 SPARQL Queries](https://docs.google.com/document/d/e/2PACX-1vRNPjW90hb4S7h_uGvDivmLV2UHkhO4m70CiVk5skBZLGZSUQijGRPn3WHoj85zZ6Ur3tH-IXMP55Hl/pub)

