---
---

## Static Demo

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

*Note that the example URLs use a namespace prefix for ease-of-reading.*

| prerequisiteCourse           | prerequisiteCourseName          |
|------------------------------|---------------------------------|
| oe2020-crs-rec-ind:crs000102 | Computer Science I              |
| oe2020-crs-rec-ind:crs000138 | Data Structures                 |
| oe2020-crs-rec-ind:crs000188 | Foundations of Computer Science |
| oe2020-crs-rec-ind:crs000205 | Introduction to Algorithms      |

### Competency Question 2

#### Question
*This question will use the course history of Jacob Shomstein to produce an answer, but a full list of courses completed is omitted for privacy.*

I am a rising senior and I want to take the smallest number of courses required to complete my degree. I also want to take “easier” courses whenever possible to allow for more time to plan for a future career. What courses can fulfill my remaining requirements? 

> We don’t have a complete information encoded surrounding graduation requirements (since there doesn’t seem to be any convenient way for us to automate adding them, the only ones we have right now have been done by hand). Therefore for demonstrative purposes we will show how we can achieve this query by (1) getting all courses that can fulfill portions of the HASS core requirements (which we have mostly encoded, along with one Integrative Pathway option), (2) remove all courses that Jacob has already completed, and (3) filter out courses by course level to only choose “easy” courses (which we will define as being below the 4000 level, for this query example). 

#### Query
```sparql
prefix oe2020-crs-rec: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender/>
prefix oe2020-crs-rec-ind: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/>
prefix lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
SELECT DISTINCT ?recCourse ?recCourseName ?recCourseLabel
WHERE {
  # the URI for Jacob in our individuals ontology
  oe2020-crs-rec-ind:usr000929 oe2020-crs-rec:hasStudyPlan [ oe2020-crs-rec:hasCompletedCourse ?completedCourseSection ] .
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
*Note that the example URLs use a namespace prefix for ease-of-reading.*

| recCourse                    | recCourseName                     | recCourseLabel |
|------------------------------|-----------------------------------|----------------|
| oe2020-crs-rec-ind:crs000015 | Introduction to Cognitive Science | COGS-2120      |

### Competency Question 3
#### Question
I have taken CSCI 4340 Ontologies and CSCI 4020 Design and Analysis of Algorithms. What are some courses like CSCI 6340 Ontologies that I should take next fall?

#### Query
```sparql
prefix oe2020-crs-rec: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender/>
prefix oe2020-crs-rec-ind: <https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/>
prefix lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
SELECT DISTINCT ?validCourse
WHERE {
  VALUES ?completedCourseTag { "CSCI-4340" "CSCI-4020" }
  ?completedCourse oe2020-crs-rec:hasCourseCode [
    lcc-lr:hasTag ?completedCourseTag
  ] .
  ?completedCourse oe2020-crs-rec:hasRequiredPrerequisite* ?completedCourseInferred .
  ?validCourseSec a oe2020-crs-rec:CourseSection ;
                  oe2020-crs-rec:hasSchedule [
                   oe2020-crs-rec:hasTerm "fall" ;
                   oe2020-crs-rec:hasYear 2020
                 ] ;
                  oe2020-crs-rec:isCourseSectionOf ?validCourse .
  ?validCourse a oe2020-crs-rec:Course .
  FILTER NOT EXISTS {
    ?validCourse oe2020-crs-rec:hasRequiredPrerequisite+ ?filterPrereqs .
    FILTER(?filterPreqreqs != ?completedCourseInferred)
  }
  FILTER (?validCourse != ?completedCourseInferred)
}
LIMIT 10
```

#### Example Results
*Note that the example URLs use a namespace prefix for ease-of-reading.*

| validCourse              |
|--------------------------|
| oe2020-crs-rec:crs000045 |
| oe2020-crs-rec:crs000048 |
| oe2020-crs-rec:crs000484 |
| oe2020-crs-rec:crs000488 |
| oe2020-crs-rec:crs000491 |
| oe2020-crs-rec:crs000497 |
| oe2020-crs-rec:crs000082 |
| oe2020-crs-rec:crs000088 |
| oe2020-crs-rec:crs000102 |
| oe2020-crs-rec:crs000015 |

