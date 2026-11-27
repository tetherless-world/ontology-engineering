// Worked examples and diagram coordinates from the supplied CJF Classroom OE12 Query Studio.
const classroomGraphs = {
  "release": "OE12",
  "commit": "759aa580456f8d3272bfcdacfc222ac98667b014",
  "questions": [
    {
      "id": 1,
      "question": "Which CJF conversation moves have occurred in the conversation, and what are their identifiers, types, summaries, and current recorded state(s), where applicable?",
      "query": "CQAnswers/CQ1/CQ1.conversation-moves.current-states.snap.rq",
      "csv": "CQAnswers/CQ1/CQ1.conversation-moves.current-states.answers.csv",
      "size": [
        830,
        590
      ],
      "nodes": [
        {
          "id": "move",
          "x": 18,
          "y": 175,
          "w": 168,
          "h": 94,
          "title": "Conversation move"
        },
        {
          "id": "branchClass",
          "x": 18,
          "y": 341,
          "w": 168,
          "h": 93,
          "title": "Move type"
        },
        {
          "id": "moveClass",
          "x": 18,
          "y": 474,
          "w": 168,
          "h": 83,
          "title": "Move-class name"
        },
        {
          "id": "summary",
          "x": 312,
          "y": 321,
          "w": 239,
          "h": 159,
          "title": "Move summary"
        },
        {
          "id": "state",
          "x": 312,
          "y": 58,
          "w": 175,
          "h": 96,
          "title": "Current State"
        },
        {
          "id": "stateClass",
          "x": 624,
          "y": 58,
          "w": 181,
          "h": 96,
          "title": "Specific state class"
        },
        {
          "id": "schemaState",
          "x": 624,
          "y": 252,
          "w": 181,
          "h": 81,
          "title": "Superclass"
        },
        {
          "id": "stateResult",
          "x": 614,
          "y": 452,
          "w": 197,
          "h": 100,
          "title": "Displayed state"
        }
      ],
      "edges": [
        {
          "id": "moveType",
          "predicate": "rdf:type",
          "d": "M100 269 V341",
          "x": 99,
          "y": 309,
          "ends": [
            "move",
            "branchClass"
          ]
        },
        {
          "id": "summary",
          "predicate": "hasSummary",
          "d": "M186 245 H223 Q237 245 237 259 V393 H312",
          "x": 252,
          "y": 317,
          "ends": [
            "move",
            "summary"
          ]
        },
        {
          "id": "state",
          "predicate": "hasState",
          "d": "M186 197 H218 Q232 197 232 183 V119 Q232 106 246 106 H312",
          "x": 256,
          "y": 93,
          "ends": [
            "move",
            "state"
          ]
        },
        {
          "id": "stateType",
          "predicate": "rdf:type",
          "d": "M487 106 H624",
          "x": 555,
          "y": 94,
          "ends": [
            "state",
            "stateClass"
          ]
        },
        {
          "id": "subclass",
          "predicate": "rdfs:subClassOf",
          "d": "M715 154 V252",
          "x": 715,
          "y": 209,
          "ends": [
            "stateClass",
            "schemaState"
          ]
        }
      ],
      "steps": [
        {
          "title": "Find moves of each of the six types.",
          "nodes": [
            "move",
            "branchClass",
            "moveClass"
          ],
          "edges": [
            "moveType"
          ],
          "code": "SELECT * WHERE {\n  { ?move a cjf:Issue . BIND(STR(\"Issue\") AS ?moveClass) . } UNION\n  { ?move a cjf:Claim . BIND(STR(\"Claim\") AS ?moveClass) . } UNION\n  { ?move a cjf:Option . BIND(STR(\"Option\") AS ?moveClass) . } UNION\n  { ?move a cjf:InformationRequest .\n    BIND(STR(\"InformationRequest\") AS ?moveClass) . } UNION\n  { ?move a cjf:ExpressedPosition .\n    BIND(STR(\"ExpressedPosition\") AS ?moveClass) . } UNION\n  { ?move a cjf:Outcome . BIND(STR(\"Outcome\") AS ?moveClass) . }\n}"
        },
        {
          "title": "Get the summary for the same move.",
          "nodes": [
            "move",
            "summary"
          ],
          "edges": [
            "summary"
          ],
          "code": "SELECT * WHERE {\n  { ?move a cjf:Issue . BIND(STR(\"Issue\") AS ?moveClass) . } UNION\n  { ?move a cjf:Claim . BIND(STR(\"Claim\") AS ?moveClass) . } UNION\n  { ?move a cjf:Option . BIND(STR(\"Option\") AS ?moveClass) . } UNION\n  { ?move a cjf:InformationRequest .\n    BIND(STR(\"InformationRequest\") AS ?moveClass) . } UNION\n  { ?move a cjf:ExpressedPosition .\n    BIND(STR(\"ExpressedPosition\") AS ?moveClass) . } UNION\n  { ?move a cjf:Outcome . BIND(STR(\"Outcome\") AS ?moveClass) . }\n  ?move cjf:hasSummary ?summary .\n}"
        },
        {
          "title": "Follow the move to its current State, if it has one.",
          "nodes": [
            "move",
            "state"
          ],
          "edges": [
            "state"
          ],
          "code": "SELECT * WHERE {\n  { ?move a cjf:Issue . BIND(STR(\"Issue\") AS ?moveClass) . } UNION\n  { ?move a cjf:Claim . BIND(STR(\"Claim\") AS ?moveClass) . } UNION\n  { ?move a cjf:Option . BIND(STR(\"Option\") AS ?moveClass) . } UNION\n  { ?move a cjf:InformationRequest .\n    BIND(STR(\"InformationRequest\") AS ?moveClass) . } UNION\n  { ?move a cjf:ExpressedPosition .\n    BIND(STR(\"ExpressedPosition\") AS ?moveClass) . } UNION\n  { ?move a cjf:Outcome . BIND(STR(\"Outcome\") AS ?moveClass) . }\n  ?move cjf:hasSummary ?summary .\n  OPTIONAL { ?move cjf:hasState ?state .\n  }\n}"
        },
        {
          "title": "Read the specific class of that State.",
          "nodes": [
            "state",
            "stateClass",
            "schemaState"
          ],
          "edges": [
            "stateType",
            "subclass"
          ],
          "code": "SELECT * WHERE {\n  { ?move a cjf:Issue . BIND(STR(\"Issue\") AS ?moveClass) . } UNION\n  { ?move a cjf:Claim . BIND(STR(\"Claim\") AS ?moveClass) . } UNION\n  { ?move a cjf:Option . BIND(STR(\"Option\") AS ?moveClass) . } UNION\n  { ?move a cjf:InformationRequest .\n    BIND(STR(\"InformationRequest\") AS ?moveClass) . } UNION\n  { ?move a cjf:ExpressedPosition .\n    BIND(STR(\"ExpressedPosition\") AS ?moveClass) . } UNION\n  { ?move a cjf:Outcome . BIND(STR(\"Outcome\") AS ?moveClass) . }\n  ?move cjf:hasSummary ?summary .\n  OPTIONAL { ?move cjf:hasState ?state .\n    ?state a ?stateClass . ?stateClass rdfs:subClassOf cjf:State .\n    MINUS { ?state a ?stateClass .\n            FILTER (?stateClass = cjf:State) } }\n}"
        },
        {
          "title": "Return the state class, or show N/A.",
          "nodes": [
            "stateClass",
            "stateResult"
          ],
          "edges": [],
          "code": "SELECT DISTINCT ?move ?moveClass\n  (IF(BOUND(?stateClass), ?stateClass, \"N/A\") AS ?stateResult)\n  ?summary WHERE {\n  { ?move a cjf:Issue . BIND(STR(\"Issue\") AS ?moveClass) . } UNION\n  { ?move a cjf:Claim . BIND(STR(\"Claim\") AS ?moveClass) . } UNION\n  { ?move a cjf:Option . BIND(STR(\"Option\") AS ?moveClass) . } UNION\n  { ?move a cjf:InformationRequest .\n    BIND(STR(\"InformationRequest\") AS ?moveClass) . } UNION\n  { ?move a cjf:ExpressedPosition .\n    BIND(STR(\"ExpressedPosition\") AS ?moveClass) . } UNION\n  { ?move a cjf:Outcome . BIND(STR(\"Outcome\") AS ?moveClass) . }\n  ?move cjf:hasSummary ?summary .\n  OPTIONAL { ?move cjf:hasState ?state .\n    ?state a ?stateClass . ?stateClass rdfs:subClassOf cjf:State .\n    MINUS { ?state a ?stateClass .\n            FILTER (?stateClass = cjf:State) } }\n} ORDER BY ?move ?moveClass"
        }
      ],
      "examples": [
        {
          "label": "M0010 · Resolved",
          "rowIndex": 11,
          "terms": {
            "move": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "branchClass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "moveClass": {
              "value": "Issue",
              "origin": "computed"
            },
            "summary": {
              "value": "Platform A may exceed the team's current tooling budget.",
              "origin": "recorded"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_3cfe4fcd6c82b91ca5d0",
              "origin": "inferred",
              "display": "State_3cfe4fcd…"
            },
            "stateClass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Resolved",
              "origin": "inferred",
              "display": "Resolved"
            },
            "schemaState": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/State",
              "origin": "recorded",
              "display": "State"
            },
            "stateResult": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Resolved",
              "origin": "computed",
              "display": "Resolved"
            }
          },
          "edges": {
            "moveType": "recorded",
            "summary": "recorded",
            "state": "inferred",
            "stateType": "inferred",
            "subclass": "recorded"
          },
          "note": "The funding issue’s current State has two matching classes.",
          "answer": {
            "move": "cjf:CQSample/Move_OCT21_A-M0010",
            "moveClass": "Issue",
            "stateResult": "cjf:Resolved",
            "summary": "Platform A may exceed the team's current tooling budget."
          }
        },
        {
          "label": "M0010 · Addressed",
          "rowIndex": 10,
          "terms": {
            "move": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "branchClass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "moveClass": {
              "value": "Issue",
              "origin": "computed"
            },
            "summary": {
              "value": "Platform A may exceed the team's current tooling budget.",
              "origin": "recorded"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_3cfe4fcd6c82b91ca5d0",
              "origin": "inferred",
              "display": "State_3cfe4fcd…"
            },
            "stateClass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Addressed",
              "origin": "inferred",
              "display": "Addressed"
            },
            "schemaState": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/State",
              "origin": "recorded",
              "display": "State"
            },
            "stateResult": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Addressed",
              "origin": "computed",
              "display": "Addressed"
            }
          },
          "edges": {
            "moveType": "recorded",
            "summary": "recorded",
            "state": "inferred",
            "stateType": "inferred",
            "subclass": "recorded"
          },
          "note": "Addressed and Resolved describe the same current State record.",
          "answer": {
            "move": "cjf:CQSample/Move_OCT21_A-M0010",
            "moveClass": "Issue",
            "stateResult": "cjf:Addressed",
            "summary": "Platform A may exceed the team's current tooling budget."
          }
        },
        {
          "label": "M0061 · N/A",
          "rowIndex": 63,
          "terms": {
            "move": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0061",
              "origin": "recorded",
              "display": "M0061"
            },
            "branchClass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/ExpressedPosition",
              "origin": "recorded",
              "display": "ExpressedPosition"
            },
            "moveClass": {
              "value": "ExpressedPosition",
              "origin": "computed"
            },
            "summary": {
              "value": "D agrees with choosing Platform A.",
              "origin": "recorded"
            },
            "stateResult": {
              "value": "N/A",
              "origin": "computed"
            }
          },
          "edges": {
            "moveType": "recorded",
            "summary": "recorded"
          },
          "note": "The optional State pattern has no binding. IF supplies the text N/A.",
          "answer": {
            "move": "cjf:CQSample/Move_OCT21_A-M0061",
            "moveClass": "ExpressedPosition",
            "stateResult": "N/A",
            "summary": "D agrees with choosing Platform A."
          }
        }
      ]
    },
    {
      "id": 2,
      "question": "Which issues are currently addressed or resolved, and what evidence supports each current state?",
      "query": "CQAnswers/CQ2/CQ2.issues-currently-addressed-or-resolved.snap.rq",
      "csv": "CQAnswers/CQ2/CQ2.issues-currently-addressed-or-resolved.answers.csv",
      "size": [
        850,
        610
      ],
      "nodes": [
        {
          "id": "issues",
          "x": 18,
          "y": 26,
          "w": 167,
          "h": 91,
          "title": "An issue"
        },
        {
          "id": "issueType",
          "x": 18,
          "y": 201,
          "w": 167,
          "h": 94,
          "title": "Issue class"
        },
        {
          "id": "stateassignment",
          "x": 348,
          "y": 26,
          "w": 178,
          "h": 96,
          "title": "Current assignment"
        },
        {
          "id": "state",
          "x": 663,
          "y": 26,
          "w": 163,
          "h": 96,
          "title": "Assigned State"
        },
        {
          "id": "stateclass",
          "x": 663,
          "y": 216,
          "w": 163,
          "h": 87,
          "title": "Specific class"
        },
        {
          "id": "schemaState",
          "x": 663,
          "y": 415,
          "w": 163,
          "h": 84,
          "title": "Superclass"
        },
        {
          "id": "relation",
          "x": 348,
          "y": 213,
          "w": 178,
          "h": 100,
          "title": "Triggering relationship"
        },
        {
          "id": "text_span",
          "x": 348,
          "y": 421,
          "w": 178,
          "h": 95,
          "title": "Evidence span"
        },
        {
          "id": "evidence",
          "x": 16,
          "y": 382,
          "w": 215,
          "h": 174,
          "title": "Supporting words"
        }
      ],
      "edges": [
        {
          "id": "issueType",
          "predicate": "rdf:type",
          "d": "M102 117 V201",
          "x": 102,
          "y": 164,
          "ends": [
            "issues",
            "issueType"
          ]
        },
        {
          "id": "current",
          "predicate": "hasCurrentStateAssignment",
          "d": "M185 72 H348",
          "x": 267,
          "y": 58,
          "ends": [
            "issues",
            "stateassignment"
          ]
        },
        {
          "id": "assigned",
          "predicate": "assignedState",
          "d": "M526 73 H663",
          "x": 594,
          "y": 59,
          "ends": [
            "stateassignment",
            "state"
          ]
        },
        {
          "id": "type",
          "predicate": "rdf:type",
          "d": "M744 122 V216",
          "x": 744,
          "y": 175,
          "ends": [
            "state",
            "stateclass"
          ]
        },
        {
          "id": "subclass",
          "predicate": "rdfs:subClassOf",
          "d": "M744 303 V415",
          "x": 744,
          "y": 363,
          "ends": [
            "stateclass",
            "schemaState"
          ]
        },
        {
          "id": "trigger",
          "predicate": "hasTriggeringRelationship",
          "d": "M437 122 V213",
          "x": 438,
          "y": 176,
          "ends": [
            "stateassignment",
            "relation"
          ]
        },
        {
          "id": "evidenceSpan",
          "predicate": "SIO_000206",
          "d": "M437 313 V421",
          "x": 437,
          "y": 370,
          "ends": [
            "relation",
            "text_span"
          ]
        },
        {
          "id": "words",
          "predicate": "hasConversationText",
          "d": "M348 465 H231",
          "x": 289,
          "y": 451,
          "ends": [
            "text_span",
            "evidence"
          ]
        }
      ],
      "steps": [
        {
          "title": "Start with the issues raised in the conversation.",
          "nodes": [
            "issues",
            "issueType"
          ],
          "edges": [
            "issueType"
          ],
          "code": "SELECT * WHERE {\n    ?issues a cjf:Issue .\n}"
        },
        {
          "title": "Find the current assignment and its State.",
          "nodes": [
            "issues",
            "stateassignment",
            "state"
          ],
          "edges": [
            "current",
            "assigned"
          ],
          "code": "SELECT * WHERE {\n    ?issues a cjf:Issue .\n    ?issues cjf:hasCurrentStateAssignment ?stateassignment .\n    ?stateassignment cjf:assignedState ?state .\n}"
        },
        {
          "title": "Read the specific state class.",
          "nodes": [
            "state",
            "stateclass",
            "schemaState"
          ],
          "edges": [
            "type",
            "subclass"
          ],
          "code": "SELECT * WHERE {\n    ?issues a cjf:Issue .\n    ?issues cjf:hasCurrentStateAssignment ?stateassignment .\n    ?stateassignment cjf:assignedState ?state .\n    ?state a ?stateclass .\n    ?stateclass rdfs:subClassOf cjf:State .\n    FILTER (?stateclass != cjf:State)\n}"
        },
        {
          "title": "Find the relationship that triggered the assignment.",
          "nodes": [
            "stateassignment",
            "relation"
          ],
          "edges": [
            "trigger"
          ],
          "code": "SELECT * WHERE {\n    ?issues a cjf:Issue .\n    ?issues cjf:hasCurrentStateAssignment ?stateassignment .\n    ?stateassignment cjf:assignedState ?state .\n    ?state a ?stateclass .\n    ?stateclass rdfs:subClassOf cjf:State .\n    FILTER (?stateclass != cjf:State)\n    ?stateassignment cjf:hasTriggeringRelationship ?relation .\n}"
        },
        {
          "title": "Read the evidence on that relationship.",
          "nodes": [
            "relation",
            "text_span",
            "evidence"
          ],
          "edges": [
            "evidenceSpan",
            "words"
          ],
          "code": "SELECT * WHERE {\n    ?issues a cjf:Issue .\n    ?issues cjf:hasCurrentStateAssignment ?stateassignment .\n    ?stateassignment cjf:assignedState ?state .\n    ?state a ?stateclass .\n    ?stateclass rdfs:subClassOf cjf:State .\n    FILTER (?stateclass != cjf:State)\n    ?stateassignment cjf:hasTriggeringRelationship ?relation .\n    ?relation sio:SIO_000206 ?text_span .\n    ?text_span cjf:hasConversationText ?evidence .\n}"
        }
      ],
      "examples": [
        {
          "label": "Training concern · M0014",
          "rowIndex": 24,
          "terms": {
            "issues": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0014",
              "origin": "recorded",
              "display": "M0014"
            },
            "issueType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "stateassignment": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Assignment_b6b48dc43eacd2283461",
              "origin": "shacl",
              "display": "Assignment_b6b48dc4…"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_b6b48dc43eacd2283461",
              "origin": "recorded",
              "display": "State_b6b48dc4…"
            },
            "stateclass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Addressed",
              "origin": "inferred",
              "display": "Addressed"
            },
            "schemaState": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/State",
              "origin": "recorded",
              "display": "State"
            },
            "relation": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_d7f3b9a8f9136e0a4cbb",
              "origin": "recorded",
              "display": "Relationship_d7f3b9a8…"
            },
            "text_span": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_acbd55774438f91e9eb8",
              "origin": "recorded",
              "display": "Span_acbd5577…"
            },
            "evidence": {
              "value": "We could use Monday’s five-to-six training slot for a vendor-led session, then give developers the recording and a practice environment.",
              "origin": "recorded"
            }
          },
          "edges": {
            "issueType": "recorded",
            "current": "shacl",
            "assigned": "recorded",
            "type": "inferred",
            "subclass": "recorded",
            "trigger": "recorded",
            "evidenceSpan": "recorded",
            "words": "recorded"
          },
          "note": "The current assignment is at turn 20. Its Address relationship supplies the evidence span.",
          "answer": {
            "issues": "sample:Move_OCT21_A-M0014",
            "stateclass": "cjf:Addressed",
            "evidence": "We could use Monday’s five-to-six training slot for a vendor-led session, then give developers the recording and a practice environment."
          }
        },
        {
          "label": "Funding concern · M0010",
          "rowIndex": 16,
          "terms": {
            "issues": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "issueType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "stateassignment": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Assignment_3cfe4fcd6c82b91ca5d0",
              "origin": "shacl",
              "display": "Assignment_3cfe4fcd…"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_3cfe4fcd6c82b91ca5d0",
              "origin": "recorded",
              "display": "State_3cfe4fcd…"
            },
            "stateclass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Resolved",
              "origin": "inferred",
              "display": "Resolved"
            },
            "schemaState": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/State",
              "origin": "recorded",
              "display": "State"
            },
            "relation": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_82a82bdcdde25eb3e956",
              "origin": "recorded",
              "display": "Relationship_82a82bdc…"
            },
            "text_span": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_9dba47deb827f27a7021",
              "origin": "recorded",
              "display": "Span_9dba47de…"
            },
            "evidence": {
              "value": "Agreed. Let’s move the $6,000 into the platform budget. We’ve all agreed to that, so the funding gap for Platform A is covered.",
              "origin": "recorded"
            }
          },
          "edges": {
            "issueType": "recorded",
            "current": "shacl",
            "assigned": "recorded",
            "type": "inferred",
            "subclass": "recorded",
            "trigger": "recorded",
            "evidenceSpan": "recorded",
            "words": "recorded"
          },
          "note": "The Address and Resolve triggers both support this projected answer. This example follows the Resolve record.",
          "answer": {
            "issues": "sample:Move_OCT21_A-M0010",
            "stateclass": "cjf:Resolved",
            "evidence": "Agreed. Let’s move the $6,000 into the platform budget. We’ve all agreed to that, so the funding gap for Platform A is covered."
          }
        }
      ]
    },
    {
      "id": 3,
      "question": "Which Claims support or challenge Platform A, what are their summaries and current recorded states, and which of these Claims have been assigned a Supported state?",
      "query": "CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.snap.rq",
      "csv": "CQAnswers/CQ3/CQ3.claims-that-support-challenges-platform-a.answers.csv",
      "size": [
        800,
        510
      ],
      "nodes": [
        {
          "id": "move",
          "x": 20,
          "y": 35,
          "w": 190,
          "h": 104,
          "title": "The same move"
        },
        {
          "id": "option",
          "x": 310,
          "y": 35,
          "w": 200,
          "h": 106,
          "title": "Platform A"
        },
        {
          "id": "claimType",
          "x": 20,
          "y": 278,
          "w": 175,
          "h": 88,
          "title": "Claim class"
        },
        {
          "id": "relation",
          "x": 320,
          "y": 192,
          "w": 179,
          "h": 66,
          "title": "Relation name"
        },
        {
          "id": "state_ind",
          "x": 596,
          "y": 36,
          "w": 181,
          "h": 100,
          "title": "Claim’s current State"
        },
        {
          "id": "stateclass",
          "x": 596,
          "y": 286,
          "w": 181,
          "h": 96,
          "title": "State class"
        },
        {
          "id": "summary",
          "x": 289,
          "y": 292,
          "w": 253,
          "h": 163,
          "title": "Recorded summary"
        }
      ],
      "edges": [
        {
          "id": "direction",
          "predicate": "supports / challenges",
          "d": "M210 85 H310",
          "x": 260,
          "y": 70,
          "ends": [
            "move",
            "option"
          ]
        },
        {
          "id": "claimType",
          "predicate": "rdf:type",
          "d": "M91 139 V278",
          "x": 91,
          "y": 211,
          "ends": [
            "move",
            "claimType"
          ]
        },
        {
          "id": "current",
          "predicate": "hasState",
          "d": "M210 114 H226 Q240 114 240 128 V163 Q240 177 254 177 H552 Q565 177 565 163 V121 Q565 107 579 107 H596",
          "x": 420,
          "y": 178,
          "ends": [
            "move",
            "state_ind"
          ]
        },
        {
          "id": "type",
          "predicate": "rdf:type",
          "d": "M685 136 V286",
          "x": 685,
          "y": 215,
          "ends": [
            "state_ind",
            "stateclass"
          ]
        },
        {
          "id": "summary",
          "predicate": "hasSummary",
          "d": "M157 139 V213 H246 Q260 213 260 227 V355 H289",
          "x": 219,
          "y": 243,
          "ends": [
            "move",
            "summary"
          ]
        }
      ],
      "steps": [
        {
          "title": "Find moves that support or challenge Platform A.",
          "nodes": [
            "move",
            "option",
            "relation"
          ],
          "edges": [
            "direction"
          ],
          "code": "SELECT * WHERE {\n    { ?move cjf:supports sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"supports\") AS ?relation) . }\n    UNION\n    { ?move cjf:challenges sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"challenges\") AS ?relation) . }\n}"
        },
        {
          "title": "Keep the moves that are Claims.",
          "nodes": [
            "move",
            "claimType"
          ],
          "edges": [
            "claimType"
          ],
          "code": "SELECT * WHERE {\n    { ?move cjf:supports sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"supports\") AS ?relation) . }\n    UNION\n    { ?move cjf:challenges sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"challenges\") AS ?relation) . }\n    ?move a cjf:Claim .\n}"
        },
        {
          "title": "Find the Claim’s current State.",
          "nodes": [
            "move",
            "state_ind"
          ],
          "edges": [
            "current"
          ],
          "code": "SELECT * WHERE {\n    { ?move cjf:supports sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"supports\") AS ?relation) . }\n    UNION\n    { ?move cjf:challenges sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"challenges\") AS ?relation) . }\n    ?move a cjf:Claim .\n    ?move cjf:hasState ?state_ind .\n}"
        },
        {
          "title": "Read the specific State class.",
          "nodes": [
            "state_ind",
            "stateclass"
          ],
          "edges": [
            "type"
          ],
          "code": "SELECT * WHERE {\n    { ?move cjf:supports sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"supports\") AS ?relation) . }\n    UNION\n    { ?move cjf:challenges sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"challenges\") AS ?relation) . }\n    ?move a cjf:Claim .\n    ?move cjf:hasState ?state_ind .\n    ?state_ind a ?stateclass .\n    FILTER (?stateclass != cjf:State &&\n            ?stateclass != sio:SIO_000000 &&\n            ?stateclass != owl:Thing)\n}"
        },
        {
          "title": "Get the Claim’s summary, if one is recorded.",
          "nodes": [
            "move",
            "summary"
          ],
          "edges": [
            "summary"
          ],
          "code": "SELECT * WHERE {\n    { ?move cjf:supports sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"supports\") AS ?relation) . }\n    UNION\n    { ?move cjf:challenges sample:Move_OCT21_A-M0003 .\n      BIND(STR(\"challenges\") AS ?relation) . }\n    ?move a cjf:Claim .\n    ?move cjf:hasState ?state_ind .\n    ?state_ind a ?stateclass .\n    FILTER (?stateclass != cjf:State &&\n            ?stateclass != sio:SIO_000000 &&\n            ?stateclass != owl:Thing)\n    OPTIONAL { ?move cjf:hasSummary ?summary . }\n}"
        }
      ],
      "examples": [
        {
          "label": "M0013 · challenges A",
          "rowIndex": 0,
          "terms": {
            "move": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0013",
              "origin": "recorded",
              "display": "M0013"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "claimType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Claim",
              "origin": "recorded",
              "display": "Claim"
            },
            "relation": {
              "value": "challenges",
              "origin": "computed"
            },
            "state_ind": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_a7fafbb4c4190122ee2c",
              "origin": "inferred",
              "display": "State_a7fafbb4…"
            },
            "stateclass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Supported",
              "origin": "inferred",
              "display": "Supported"
            },
            "summary": {
              "value": "Using Platform A would require covering a $6,000 funding shortfall.",
              "origin": "recorded"
            }
          },
          "edges": {
            "direction": "inferred",
            "claimType": "recorded",
            "current": "inferred",
            "type": "inferred",
            "summary": "recorded"
          },
          "edgeLabels": {
            "direction": "challenges"
          },
          "note": "The funding-gap Claim challenges the Option and its own State is Supported.",
          "answer": {
            "move": "sample:Move_OCT21_A-M0013",
            "relation": "challenges",
            "stateclass": "cjf:Supported",
            "summary": "Using Platform A would require covering a $6,000 funding shortfall."
          }
        },
        {
          "label": "M0004 · supports A",
          "rowIndex": 3,
          "terms": {
            "move": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0004",
              "origin": "recorded",
              "display": "M0004"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "claimType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Claim",
              "origin": "recorded",
              "display": "Claim"
            },
            "relation": {
              "value": "supports",
              "origin": "computed"
            },
            "state_ind": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_7de8b4a5d0de7ec78981",
              "origin": "inferred",
              "display": "State_7de8b4a5…"
            },
            "stateclass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Supported",
              "origin": "inferred",
              "display": "Supported"
            },
            "summary": {
              "value": "Platform A seems like the better fit for the delivery schedule.",
              "origin": "recorded"
            }
          },
          "edges": {
            "direction": "inferred",
            "claimType": "recorded",
            "current": "inferred",
            "type": "inferred",
            "summary": "recorded"
          },
          "edgeLabels": {
            "direction": "supports"
          },
          "answer": {
            "move": "sample:Move_OCT21_A-M0004",
            "relation": "supports",
            "stateclass": "cjf:Supported",
            "summary": "Platform A seems like the better fit for the delivery schedule."
          }
        },
        {
          "label": "M0015 · Unassessed",
          "rowIndex": 1,
          "terms": {
            "move": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0015",
              "origin": "recorded",
              "display": "M0015"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "claimType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Claim",
              "origin": "recorded",
              "display": "Claim"
            },
            "relation": {
              "value": "challenges",
              "origin": "computed"
            },
            "state_ind": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_76bd14219c7492bc3d0c",
              "origin": "inferred",
              "display": "State_76bd1421…"
            },
            "stateclass": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Unassessed",
              "origin": "recorded",
              "display": "Unassessed"
            },
            "summary": {
              "value": "Most developers have not used Platform A.",
              "origin": "recorded"
            }
          },
          "edges": {
            "direction": "inferred",
            "claimType": "recorded",
            "current": "inferred",
            "type": "recorded",
            "summary": "recorded"
          },
          "edgeLabels": {
            "direction": "challenges"
          },
          "answer": {
            "move": "sample:Move_OCT21_A-M0015",
            "relation": "challenges",
            "stateclass": "cjf:Unassessed",
            "summary": "Most developers have not used Platform A."
          }
        }
      ]
    },
    {
      "id": 4,
      "question": "Which Issues challenge Platform A, how have their states changed throughout the conversation, and what evidence supports these changes?",
      "query": "CQAnswers/CQ4/CQ4.issues-platform-a-historical-states.snap.rq",
      "csv": "CQAnswers/CQ4/CQ4.issues-platform-a-historical-states.answers.csv",
      "size": [
        860,
        645
      ],
      "nodes": [
        {
          "id": "issue",
          "x": 13,
          "y": 20,
          "w": 175,
          "h": 91,
          "title": "Issue about A"
        },
        {
          "id": "challenge",
          "x": 351,
          "y": 20,
          "w": 181,
          "h": 87,
          "title": "Challenge record"
        },
        {
          "id": "option",
          "x": 675,
          "y": 20,
          "w": 170,
          "h": 89,
          "title": "Platform A"
        },
        {
          "id": "issueType",
          "x": 225,
          "y": 116,
          "w": 145,
          "h": 94,
          "title": "Issue class"
        },
        {
          "id": "assignment",
          "x": 13,
          "y": 217,
          "w": 182,
          "h": 94,
          "title": "One assignment"
        },
        {
          "id": "state",
          "x": 351,
          "y": 216,
          "w": 181,
          "h": 94,
          "title": "State at this point"
        },
        {
          "id": "stateType",
          "x": 675,
          "y": 215,
          "w": 170,
          "h": 94,
          "title": "State class"
        },
        {
          "id": "trigger",
          "x": 13,
          "y": 419,
          "w": 189,
          "h": 103,
          "title": "Triggering relationship"
        },
        {
          "id": "sourceMove",
          "x": 351,
          "y": 419,
          "w": 181,
          "h": 94,
          "title": "Source move"
        },
        {
          "id": "textSpan",
          "x": 675,
          "y": 415,
          "w": 170,
          "h": 95,
          "title": "Evidence span"
        },
        {
          "id": "evidence",
          "x": 480,
          "y": 544,
          "w": 345,
          "h": 90,
          "title": "Evidence text"
        }
      ],
      "edges": [
        {
          "id": "makesChallenge",
          "predicate": "makesChallenges",
          "d": "M188 60 H351",
          "x": 270,
          "y": 47,
          "ends": [
            "issue",
            "challenge"
          ]
        },
        {
          "id": "target",
          "predicate": "isAimedAtChallenges",
          "d": "M532 60 H675",
          "x": 605,
          "y": 47,
          "ends": [
            "challenge",
            "option"
          ]
        },
        {
          "id": "issueType",
          "predicate": "rdf:type",
          "d": "M177 111 L225 141",
          "x": 235,
          "y": 109,
          "ends": [
            "issue",
            "issueType"
          ]
        },
        {
          "id": "history",
          "predicate": "hasStateAssignment",
          "d": "M92 111 V217",
          "x": 95,
          "y": 172,
          "ends": [
            "issue",
            "assignment"
          ]
        },
        {
          "id": "assigned",
          "predicate": "assignedState",
          "d": "M195 263 H351",
          "x": 272,
          "y": 250,
          "ends": [
            "assignment",
            "state"
          ]
        },
        {
          "id": "type",
          "predicate": "rdf:type",
          "d": "M532 262 H675",
          "x": 602,
          "y": 248,
          "ends": [
            "state",
            "stateType"
          ]
        },
        {
          "id": "trigger",
          "predicate": "hasTriggeringRelationship",
          "d": "M100 311 V419",
          "x": 103,
          "y": 373,
          "ends": [
            "assignment",
            "trigger"
          ]
        },
        {
          "id": "sourceAddress",
          "predicate": "makesAddresses",
          "d": "M351 463 H202",
          "x": 276,
          "y": 449,
          "ends": [
            "sourceMove",
            "trigger"
          ]
        },
        {
          "id": "span",
          "predicate": "SIO_000206",
          "d": "M532 460 H675",
          "x": 603,
          "y": 447,
          "ends": [
            "sourceMove",
            "textSpan"
          ]
        },
        {
          "id": "words",
          "predicate": "hasConversationText",
          "d": "M767 510 V544",
          "x": 703,
          "y": 533,
          "ends": [
            "textSpan",
            "evidence"
          ]
        }
      ],
      "steps": [
        {
          "title": "Find the Issues that challenge Platform A.",
          "nodes": [
            "issue",
            "challenge",
            "option",
            "issueType"
          ],
          "edges": [
            "makesChallenge",
            "target",
            "issueType"
          ],
          "code": "SELECT * WHERE {\n    ?issue cjf:makesChallenges ?challenge .\n    ?challenge cjf:isAimedAtChallenges sample:Move_OCT21_A-M0003 .\n    OPTIONAL { ?issue rdf:type ?issueType . }\n    FILTER (?issueType = cjf:Issue)\n}"
        },
        {
          "title": "Follow each recorded state assignment.",
          "nodes": [
            "issue",
            "assignment",
            "state"
          ],
          "edges": [
            "history",
            "assigned"
          ],
          "code": "SELECT * WHERE {\n    ?issue cjf:makesChallenges ?challenge .\n    ?challenge cjf:isAimedAtChallenges sample:Move_OCT21_A-M0003 .\n    OPTIONAL { ?issue rdf:type ?issueType . }\n    FILTER (?issueType = cjf:Issue)\n    ?issue cjf:hasStateAssignment ?assignment .\n    ?assignment cjf:assignedState ?state .\n}"
        },
        {
          "title": "Read its Open, Addressed, or Resolved state.",
          "nodes": [
            "state",
            "stateType"
          ],
          "edges": [
            "type"
          ],
          "code": "SELECT * WHERE {\n    ?issue cjf:makesChallenges ?challenge .\n    ?challenge cjf:isAimedAtChallenges sample:Move_OCT21_A-M0003 .\n    OPTIONAL { ?issue rdf:type ?issueType . }\n    FILTER (?issueType = cjf:Issue)\n    ?issue cjf:hasStateAssignment ?assignment .\n    ?assignment cjf:assignedState ?state .\n    OPTIONAL { ?state rdf:type ?stateType . }\n    FILTER (?stateType = cjf:Open || ?stateType = cjf:Addressed ||\n            ?stateType = cjf:Resolved)\n}"
        },
        {
          "title": "Find the trigger and its source move, if recorded.",
          "nodes": [
            "assignment",
            "trigger",
            "sourceMove"
          ],
          "edges": [
            "trigger",
            "sourceAddress"
          ],
          "code": "SELECT * WHERE {\n    ?issue cjf:makesChallenges ?challenge .\n    ?challenge cjf:isAimedAtChallenges sample:Move_OCT21_A-M0003 .\n    OPTIONAL { ?issue rdf:type ?issueType . }\n    FILTER (?issueType = cjf:Issue)\n    ?issue cjf:hasStateAssignment ?assignment .\n    ?assignment cjf:assignedState ?state .\n    OPTIONAL { ?state rdf:type ?stateType . }\n    FILTER (?stateType = cjf:Open || ?stateType = cjf:Addressed ||\n            ?stateType = cjf:Resolved)\n    OPTIONAL { ?assignment cjf:hasTriggeringRelationship ?trigger .\n        OPTIONAL { ?sourceMove cjf:makesAddresses ?trigger .\n        } }\n}"
        },
        {
          "title": "Read the words on the source move.",
          "nodes": [
            "sourceMove",
            "textSpan",
            "evidence"
          ],
          "edges": [
            "span",
            "words"
          ],
          "code": "SELECT * WHERE {\n    ?issue cjf:makesChallenges ?challenge .\n    ?challenge cjf:isAimedAtChallenges sample:Move_OCT21_A-M0003 .\n    OPTIONAL { ?issue rdf:type ?issueType . }\n    FILTER (?issueType = cjf:Issue)\n    ?issue cjf:hasStateAssignment ?assignment .\n    ?assignment cjf:assignedState ?state .\n    OPTIONAL { ?state rdf:type ?stateType . }\n    FILTER (?stateType = cjf:Open || ?stateType = cjf:Addressed ||\n            ?stateType = cjf:Resolved)\n    OPTIONAL { ?assignment cjf:hasTriggeringRelationship ?trigger .\n        OPTIONAL { ?sourceMove cjf:makesAddresses ?trigger .\n            OPTIONAL { ?sourceMove sio:SIO_000206 ?textSpan .\n                ?textSpan cjf:hasConversationText ?evidence .\n            } } }\n}"
        }
      ],
      "examples": [
        {
          "label": "Turn 18 · Resolved",
          "rowIndex": 3,
          "terms": {
            "issue": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "issueType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "challenge": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_5f1d562576fc1fab7869",
              "origin": "recorded",
              "display": "Relationship_5f1d5625…"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "assignment": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Assignment_3cfe4fcd6c82b91ca5d0",
              "origin": "recorded",
              "display": "Assignment_3cfe4fcd…"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_3cfe4fcd6c82b91ca5d0",
              "origin": "recorded",
              "display": "State_3cfe4fcd…"
            },
            "stateType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Resolved",
              "origin": "inferred",
              "display": "Resolved"
            },
            "trigger": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_befcc7cd96d3963088da",
              "origin": "recorded",
              "display": "Relationship_befcc7cd…"
            },
            "sourceMove": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0048",
              "origin": "recorded",
              "display": "M0048"
            },
            "textSpan": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_827beea34ebeb6a589d1",
              "origin": "recorded",
              "display": "Span_827beea3…"
            },
            "evidence": {
              "value": "That settles the funding concern.",
              "origin": "recorded"
            }
          },
          "edges": {
            "makesChallenge": "recorded",
            "target": "recorded",
            "issueType": "recorded",
            "history": "recorded",
            "assigned": "recorded",
            "type": "inferred",
            "trigger": "recorded",
            "sourceAddress": "recorded",
            "span": "recorded",
            "words": "recorded"
          },
          "note": "The assignment is at turn 18. This evidence span on its source move comes from turn 19.",
          "answer": {
            "issue": "sample:Move_OCT21_A-M0010",
            "assignment": "sample:Assignment_3cfe4fcd6c82b91ca5d0",
            "stateType": "cjf:Resolved",
            "sourceMove": "sample:Move_OCT21_A-M0048",
            "evidence": "That settles the funding concern."
          }
        },
        {
          "label": "Turn 5 · Open",
          "rowIndex": 6,
          "terms": {
            "issue": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "issueType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "challenge": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_5f1d562576fc1fab7869",
              "origin": "recorded",
              "display": "Relationship_5f1d5625…"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "assignment": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Assignment_8b66f2862fe0f2165de0",
              "origin": "recorded",
              "display": "Assignment_8b66f286…"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_8b66f2862fe0f2165de0",
              "origin": "recorded",
              "display": "State_8b66f286…"
            },
            "stateType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Open",
              "origin": "recorded",
              "display": "Open"
            }
          },
          "edges": {
            "makesChallenge": "recorded",
            "target": "recorded",
            "issueType": "recorded",
            "history": "recorded",
            "assigned": "recorded",
            "type": "recorded"
          },
          "note": "This initial Open assignment survives with the optional trigger, source move and evidence unbound.",
          "answer": {
            "issue": "sample:Move_OCT21_A-M0010",
            "assignment": "sample:Assignment_8b66f2862fe0f2165de0",
            "stateType": "cjf:Open",
            "sourceMove": "",
            "evidence": ""
          }
        },
        {
          "label": "Turn 15 · Addressed",
          "rowIndex": 5,
          "terms": {
            "issue": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "issueType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "challenge": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_5f1d562576fc1fab7869",
              "origin": "recorded",
              "display": "Relationship_5f1d5625…"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "assignment": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Assignment_784175fca71db18ddd24",
              "origin": "recorded",
              "display": "Assignment_784175fc…"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_784175fca71db18ddd24",
              "origin": "recorded",
              "display": "State_784175fc…"
            },
            "stateType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Addressed",
              "origin": "inferred",
              "display": "Addressed"
            },
            "trigger": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_6cb6cf83824e9dcb8eac",
              "origin": "recorded",
              "display": "Relationship_6cb6cf83…"
            },
            "sourceMove": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0039",
              "origin": "recorded",
              "display": "M0039"
            },
            "textSpan": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_6b3e81266a0c796e4b88",
              "origin": "recorded",
              "display": "Span_6b3e8126…"
            },
            "evidence": {
              "value": "Then we could cover Platform A’s $6,000 gap by moving the funds reserved for the reporting add-on.",
              "origin": "recorded"
            }
          },
          "edges": {
            "makesChallenge": "recorded",
            "target": "recorded",
            "issueType": "recorded",
            "history": "recorded",
            "assigned": "recorded",
            "type": "inferred",
            "trigger": "recorded",
            "sourceAddress": "recorded",
            "span": "recorded",
            "words": "recorded"
          },
          "answer": {
            "issue": "sample:Move_OCT21_A-M0010",
            "assignment": "sample:Assignment_784175fca71db18ddd24",
            "stateType": "cjf:Addressed",
            "sourceMove": "sample:Move_OCT21_A-M0039",
            "evidence": "Then we could cover Platform A’s $6,000 gap by moving the funds reserved for the reporting add-on."
          }
        },
        {
          "label": "Turn 18 · Addressed",
          "rowIndex": 1,
          "terms": {
            "issue": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0010",
              "origin": "recorded",
              "display": "M0010"
            },
            "issueType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Issue",
              "origin": "recorded",
              "display": "Issue"
            },
            "challenge": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_5f1d562576fc1fab7869",
              "origin": "recorded",
              "display": "Relationship_5f1d5625…"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "recorded",
              "display": "M0003"
            },
            "assignment": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Assignment_3cfe4fcd6c82b91ca5d0",
              "origin": "recorded",
              "display": "Assignment_3cfe4fcd…"
            },
            "state": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/State_3cfe4fcd6c82b91ca5d0",
              "origin": "recorded",
              "display": "State_3cfe4fcd…"
            },
            "stateType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Addressed",
              "origin": "inferred",
              "display": "Addressed"
            },
            "trigger": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Relationship_befcc7cd96d3963088da",
              "origin": "recorded",
              "display": "Relationship_befcc7cd…"
            },
            "sourceMove": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0048",
              "origin": "recorded",
              "display": "M0048"
            },
            "textSpan": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_827beea34ebeb6a589d1",
              "origin": "recorded",
              "display": "Span_827beea3…"
            },
            "evidence": {
              "value": "That settles the funding concern.",
              "origin": "recorded"
            }
          },
          "edges": {
            "makesChallenge": "recorded",
            "target": "recorded",
            "issueType": "recorded",
            "history": "recorded",
            "assigned": "recorded",
            "type": "inferred",
            "trigger": "recorded",
            "sourceAddress": "recorded",
            "span": "recorded",
            "words": "recorded"
          },
          "note": "The turn-18 State also has the class Resolved.",
          "answer": {
            "issue": "sample:Move_OCT21_A-M0010",
            "assignment": "sample:Assignment_3cfe4fcd6c82b91ca5d0",
            "stateType": "cjf:Addressed",
            "sourceMove": "sample:Move_OCT21_A-M0048",
            "evidence": "That settles the funding concern."
          }
        }
      ]
    },
    {
      "id": 5,
      "question": "For the final platform-selection Outcome, which speakers explicitly agreed with its selected Option, and which ExpressedPosition moves and source turns provide the evidence?",
      "query": "CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.span.rq",
      "csv": "CQAnswers/CQ5/CQ5.speakers-that-agreed-with-group-outcome.answer.csv",
      "size": [
        770,
        560
      ],
      "nodes": [
        {
          "id": "outcome",
          "x": 22,
          "y": 20,
          "w": 158,
          "h": 84,
          "title": "The decision"
        },
        {
          "id": "option",
          "x": 326,
          "y": 20,
          "w": 146,
          "h": 84,
          "title": "Chosen option"
        },
        {
          "id": "pos",
          "x": 22,
          "y": 248,
          "w": 158,
          "h": 106,
          "title": "A position"
        },
        {
          "id": "speaker",
          "x": 326,
          "y": 159,
          "w": 146,
          "h": 90,
          "title": "The person"
        },
        {
          "id": "speaker_name",
          "x": 610,
          "y": 159,
          "w": 142,
          "h": 90,
          "title": "Their name"
        },
        {
          "id": "support",
          "x": 326,
          "y": 313,
          "w": 146,
          "h": 92,
          "title": "Evidence span"
        },
        {
          "id": "support_text",
          "x": 610,
          "y": 293,
          "w": 142,
          "h": 142,
          "title": "Exact words"
        },
        {
          "id": "utterance",
          "x": 326,
          "y": 458,
          "w": 146,
          "h": 84,
          "title": "Source utterance"
        },
        {
          "id": "turn",
          "x": 610,
          "y": 458,
          "w": 142,
          "h": 84,
          "title": "Turn number"
        }
      ],
      "edges": [
        {
          "id": "selection",
          "predicate": "selects",
          "d": "M180 62 H326",
          "x": 253,
          "y": 45,
          "ends": [
            "outcome",
            "option"
          ]
        },
        {
          "id": "target",
          "predicate": "hasPositionTowards",
          "d": "M101 248 V148 Q101 132 117 132 H383 Q399 132 399 116 V104",
          "x": 244,
          "y": 122,
          "ends": [
            "pos",
            "option"
          ]
        },
        {
          "id": "speaker",
          "predicate": "hasSpeaker",
          "d": "M180 270 H214 Q230 270 230 254 V220 Q230 204 246 204 H326",
          "x": 259,
          "y": 188,
          "ends": [
            "pos",
            "speaker"
          ]
        },
        {
          "id": "name",
          "predicate": "hasSpeakerName",
          "d": "M472 204 H610",
          "x": 541,
          "y": 187,
          "ends": [
            "speaker",
            "speaker_name"
          ]
        },
        {
          "id": "positive",
          "predicate": "isPositiveSupportedBy",
          "d": "M180 326 H230 Q246 326 246 342 V343 Q246 359 262 359 H326",
          "x": 253,
          "y": 309,
          "ends": [
            "pos",
            "support"
          ]
        },
        {
          "id": "words",
          "predicate": "hasConversationText",
          "d": "M472 359 H610",
          "x": 541,
          "y": 342,
          "ends": [
            "support",
            "support_text"
          ]
        },
        {
          "id": "utterance",
          "predicate": "hasUtterance",
          "d": "M180 342 H202 Q218 342 218 358 V484 Q218 500 234 500 H326",
          "x": 267,
          "y": 483,
          "ends": [
            "pos",
            "utterance"
          ]
        },
        {
          "id": "turn",
          "predicate": "hasTurnNumber",
          "d": "M472 500 H610",
          "x": 541,
          "y": 483,
          "ends": [
            "utterance",
            "turn"
          ]
        },
        {
          "id": "agreement",
          "predicate": "rdf:type",
          "d": "M101 354 V397",
          "x": 101,
          "y": 380,
          "ends": [
            "pos",
            "agreement"
          ]
        }
      ],
      "steps": [
        {
          "title": "Find the selected Option.",
          "nodes": [
            "outcome",
            "option"
          ],
          "edges": [
            "selection"
          ],
          "code": "SELECT * WHERE {\n    sample:Move_OCT21_A-M0067 cjf:selects ?option .\n}"
        },
        {
          "title": "Find agreeing positions about the Option.",
          "nodes": [
            "pos",
            "agreement",
            "option"
          ],
          "edges": [
            "target",
            "agreement"
          ],
          "code": "SELECT * WHERE {\n    sample:Move_OCT21_A-M0067 cjf:selects ?option .\n    ?pos cjf:hasPositionTowards ?option .\n    ?pos a cjf:Agreement .\n}"
        },
        {
          "title": "Get the speaker and their name.",
          "nodes": [
            "pos",
            "speaker",
            "speaker_name"
          ],
          "edges": [
            "speaker",
            "name"
          ],
          "code": "SELECT * WHERE {\n    sample:Move_OCT21_A-M0067 cjf:selects ?option .\n    ?pos cjf:hasPositionTowards ?option .\n    ?pos a cjf:Agreement .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName ?speaker_name .\n}"
        },
        {
          "title": "Get the evidence span and supporting text.",
          "nodes": [
            "pos",
            "support",
            "support_text"
          ],
          "edges": [
            "positive",
            "words"
          ],
          "code": "SELECT * WHERE {\n    sample:Move_OCT21_A-M0067 cjf:selects ?option .\n    ?pos cjf:hasPositionTowards ?option .\n    ?pos a cjf:Agreement .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName ?speaker_name .\n    ?pos cjf:isPositiveSupportedBy ?support .\n    ?support cjf:hasConversationText ?support_text .\n}"
        },
        {
          "title": "Get the source utterance and turn.",
          "nodes": [
            "pos",
            "utterance",
            "turn"
          ],
          "edges": [
            "utterance",
            "turn"
          ],
          "code": "SELECT * WHERE {\n    sample:Move_OCT21_A-M0067 cjf:selects ?option .\n    ?pos cjf:hasPositionTowards ?option .\n    ?pos a cjf:Agreement .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName ?speaker_name .\n    ?pos cjf:isPositiveSupportedBy ?support .\n    ?support cjf:hasConversationText ?support_text .\n    ?pos cjf:hasUtterance ?utterance .\n    ?utterance cjf:hasTurnNumber ?turn .\n}"
        }
      ],
      "examples": [
        {
          "label": "Speaker D · turn 25",
          "rowIndex": 0,
          "terms": {
            "outcome": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0067",
              "origin": "recorded",
              "display": "M0067"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "inferred",
              "display": "M0003"
            },
            "pos": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0061",
              "origin": "inferred",
              "display": "M0061"
            },
            "agreement": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Agreement",
              "origin": "recorded",
              "display": "Agreement"
            },
            "speaker": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Speaker_b5efae1edfaf7c011c3d",
              "origin": "inferred",
              "display": "Speaker_b5efae1e…"
            },
            "speaker_name": {
              "value": "Speaker D",
              "origin": "recorded"
            },
            "support": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_1a619ea3434f1bca467c",
              "origin": "recorded",
              "display": "Span_1a619ea3…"
            },
            "support_text": {
              "value": "I support choosing Platform A.",
              "origin": "recorded"
            },
            "utterance": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Turn_25",
              "origin": "recorded",
              "display": "Turn_25"
            },
            "turn": {
              "value": "25",
              "origin": "recorded"
            }
          },
          "edges": {
            "selection": "inferred",
            "target": "inferred",
            "agreement": "inferred",
            "speaker": "inferred",
            "name": "recorded",
            "positive": "recorded",
            "words": "recorded",
            "utterance": "recorded",
            "turn": "recorded"
          },
          "answer": {
            "pos": "sample:Move_OCT21_A-M0061",
            "speaker_name": "Speaker D",
            "support_text": "I support choosing Platform A.",
            "turn": "25"
          }
        },
        {
          "label": "Speaker B · turn 26",
          "rowIndex": 1,
          "terms": {
            "outcome": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0067",
              "origin": "recorded",
              "display": "M0067"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "inferred",
              "display": "M0003"
            },
            "pos": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0062",
              "origin": "inferred",
              "display": "M0062"
            },
            "agreement": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Agreement",
              "origin": "recorded",
              "display": "Agreement"
            },
            "speaker": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Speaker_2948d155af88e5ec9810",
              "origin": "inferred",
              "display": "Speaker_2948d155…"
            },
            "speaker_name": {
              "value": "Speaker B",
              "origin": "recorded"
            },
            "support": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_b44b06c5d0fa09590314",
              "origin": "recorded",
              "display": "Span_b44b06c5…"
            },
            "support_text": {
              "value": "I agree with choosing Platform A.",
              "origin": "recorded"
            },
            "utterance": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Turn_26",
              "origin": "recorded",
              "display": "Turn_26"
            },
            "turn": {
              "value": "26",
              "origin": "recorded"
            }
          },
          "edges": {
            "selection": "inferred",
            "target": "inferred",
            "agreement": "inferred",
            "speaker": "inferred",
            "name": "recorded",
            "positive": "recorded",
            "words": "recorded",
            "utterance": "recorded",
            "turn": "recorded"
          },
          "answer": {
            "pos": "sample:Move_OCT21_A-M0062",
            "speaker_name": "Speaker B",
            "support_text": "I agree with choosing Platform A.",
            "turn": "26"
          }
        },
        {
          "label": "Speaker C · turn 27",
          "rowIndex": 2,
          "terms": {
            "outcome": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0067",
              "origin": "recorded",
              "display": "M0067"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "inferred",
              "display": "M0003"
            },
            "pos": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0063",
              "origin": "inferred",
              "display": "M0063"
            },
            "agreement": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Agreement",
              "origin": "recorded",
              "display": "Agreement"
            },
            "speaker": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Speaker_1ce82228187659212b16",
              "origin": "inferred",
              "display": "Speaker_1ce82228…"
            },
            "speaker_name": {
              "value": "Speaker C",
              "origin": "recorded"
            },
            "support": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_20698aac390dc7ca1e27",
              "origin": "recorded",
              "display": "Span_20698aac…"
            },
            "support_text": {
              "value": "I’m voting for Platform A as well.",
              "origin": "recorded"
            },
            "utterance": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Turn_27",
              "origin": "recorded",
              "display": "Turn_27"
            },
            "turn": {
              "value": "27",
              "origin": "recorded"
            }
          },
          "edges": {
            "selection": "inferred",
            "target": "inferred",
            "agreement": "inferred",
            "speaker": "inferred",
            "name": "recorded",
            "positive": "recorded",
            "words": "recorded",
            "utterance": "recorded",
            "turn": "recorded"
          },
          "answer": {
            "pos": "sample:Move_OCT21_A-M0063",
            "speaker_name": "Speaker C",
            "support_text": "I’m voting for Platform A as well.",
            "turn": "27"
          }
        },
        {
          "label": "Speaker A · turn 28",
          "rowIndex": 3,
          "terms": {
            "outcome": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0067",
              "origin": "recorded",
              "display": "M0067"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "inferred",
              "display": "M0003"
            },
            "pos": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0066",
              "origin": "inferred",
              "display": "M0066"
            },
            "agreement": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/Agreement",
              "origin": "recorded",
              "display": "Agreement"
            },
            "speaker": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Speaker_8a4bce894543c95c6fef",
              "origin": "inferred",
              "display": "Speaker_8a4bce89…"
            },
            "speaker_name": {
              "value": "Speaker A",
              "origin": "recorded"
            },
            "support": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_6b3cb4c291f3c87cd991",
              "origin": "recorded",
              "display": "Span_6b3cb4c2…"
            },
            "support_text": {
              "value": "I’m comfortable selecting platform A today.",
              "origin": "recorded"
            },
            "utterance": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Turn_28",
              "origin": "recorded",
              "display": "Turn_28"
            },
            "turn": {
              "value": "28",
              "origin": "recorded"
            }
          },
          "edges": {
            "selection": "inferred",
            "target": "inferred",
            "agreement": "inferred",
            "speaker": "inferred",
            "name": "recorded",
            "positive": "recorded",
            "words": "recorded",
            "utterance": "recorded",
            "turn": "recorded"
          },
          "answer": {
            "pos": "sample:Move_OCT21_A-M0066",
            "speaker_name": "Speaker A",
            "support_text": "I’m comfortable selecting platform A today.",
            "turn": "28"
          }
        }
      ]
    },
    {
      "id": 6,
      "question": "What positions did Speaker C express toward Platform A and Platform B throughout the conversation, and what are the identifiers, target Options, summaries, supporting utterances, and turn numbers of these Expressed Positions?",
      "query": "CQAnswers/CQ6/CQ6.speaker-c-platform-positions.snap.rq",
      "csv": "CQAnswers/CQ6/CQ6.speaker-c-platform-positions.answers.csv",
      "size": [
        866,
        640
      ],
      "nodes": [
        {
          "id": "posType",
          "x": 15,
          "y": 19,
          "w": 164,
          "h": 91,
          "title": "Position type"
        },
        {
          "id": "speaker",
          "x": 342,
          "y": 18,
          "w": 175,
          "h": 89,
          "title": "The person"
        },
        {
          "id": "speakerName",
          "x": 668,
          "y": 18,
          "w": 179,
          "h": 86,
          "title": "Speaker name"
        },
        {
          "id": "pos",
          "x": 15,
          "y": 172,
          "w": 168,
          "h": 99,
          "title": "C’s position"
        },
        {
          "id": "option",
          "x": 342,
          "y": 171,
          "w": 175,
          "h": 94,
          "title": "Target Option"
        },
        {
          "id": "summary",
          "x": 662,
          "y": 152,
          "w": 186,
          "h": 140,
          "title": "Recorded summary"
        },
        {
          "id": "support",
          "x": 15,
          "y": 360,
          "w": 168,
          "h": 93,
          "title": "Evidence span"
        },
        {
          "id": "utterance",
          "x": 342,
          "y": 356,
          "w": 175,
          "h": 92,
          "title": "Source utterance"
        },
        {
          "id": "turn",
          "x": 668,
          "y": 358,
          "w": 179,
          "h": 90,
          "title": "Turn number"
        },
        {
          "id": "support_text",
          "x": 15,
          "y": 496,
          "w": 207,
          "h": 130,
          "title": "C’s words"
        },
        {
          "id": "conversation",
          "x": 343,
          "y": 518,
          "w": 211,
          "h": 88,
          "title": "Sample conversation"
        }
      ],
      "edges": [
        {
          "id": "posType",
          "predicate": "rdf:type",
          "d": "M83 172 V110",
          "x": 83,
          "y": 143,
          "ends": [
            "pos",
            "posType"
          ]
        },
        {
          "id": "speaker",
          "predicate": "hasSpeaker",
          "d": "M183 191 H218 Q234 191 234 175 V93 Q234 77 250 77 H342",
          "x": 266,
          "y": 64,
          "ends": [
            "pos",
            "speaker"
          ]
        },
        {
          "id": "name",
          "predicate": "hasSpeakerName",
          "d": "M517 62 H668",
          "x": 594,
          "y": 48,
          "ends": [
            "speaker",
            "speakerName"
          ]
        },
        {
          "id": "target",
          "predicate": "hasPositionTowards",
          "d": "M183 221 H342",
          "x": 263,
          "y": 207,
          "ends": [
            "pos",
            "option"
          ]
        },
        {
          "id": "summary",
          "predicate": "hasSummary",
          "d": "M183 249 H196 Q207 249 207 261 V299 Q207 310 219 310 H634 Q647 310 647 297 V259 Q647 246 659 246 H662",
          "x": 426,
          "y": 300,
          "ends": [
            "pos",
            "summary"
          ]
        },
        {
          "id": "span",
          "predicate": "SIO_000206",
          "d": "M95 271 V360",
          "x": 97,
          "y": 324,
          "ends": [
            "pos",
            "support"
          ]
        },
        {
          "id": "words",
          "predicate": "hasConversationText",
          "d": "M95 453 V496",
          "x": 93,
          "y": 482,
          "ends": [
            "support",
            "support_text"
          ]
        },
        {
          "id": "utterance",
          "predicate": "isPartOfUtterance",
          "d": "M183 406 H342",
          "x": 265,
          "y": 392,
          "ends": [
            "support",
            "utterance"
          ]
        },
        {
          "id": "attribution",
          "predicate": "prov:wasAttributedTo",
          "d": "M517 383 H557 Q574 383 574 367 V111 Q574 95 558 95 H517",
          "x": 573,
          "y": 138,
          "ends": [
            "utterance",
            "speaker"
          ]
        },
        {
          "id": "conversation",
          "predicate": "prov:wasGeneratedBy",
          "d": "M425 448 V518",
          "x": 432,
          "y": 488,
          "ends": [
            "utterance",
            "conversation"
          ]
        },
        {
          "id": "turn",
          "predicate": "hasTurnNumber",
          "d": "M517 416 H668",
          "x": 591,
          "y": 401,
          "ends": [
            "utterance",
            "turn"
          ]
        }
      ],
      "steps": [
        {
          "title": "Find the positions expressed by Speaker C.",
          "nodes": [
            "pos",
            "posType",
            "speaker",
            "speakerName"
          ],
          "edges": [
            "posType",
            "speaker",
            "name"
          ],
          "code": "SELECT * WHERE {\n    ?pos a cjf:ExpressedPosition .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName \"Speaker C\" .\n}"
        },
        {
          "title": "Keep positions about Platform A or Platform B.",
          "nodes": [
            "pos",
            "option"
          ],
          "edges": [
            "target"
          ],
          "code": "SELECT * WHERE {\n    ?pos a cjf:ExpressedPosition .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName \"Speaker C\" .\n    ?pos cjf:hasPositionTowards ?option .\n    FILTER (?option = sample:Move_OCT21_A-M0003\n            || ?option = sample:Move_OCT21_A-M0021)\n}"
        },
        {
          "title": "Get the summary, if one is recorded.",
          "nodes": [
            "pos",
            "summary"
          ],
          "edges": [
            "summary"
          ],
          "code": "SELECT * WHERE {\n    ?pos a cjf:ExpressedPosition .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName \"Speaker C\" .\n    ?pos cjf:hasPositionTowards ?option .\n    FILTER (?option = sample:Move_OCT21_A-M0003\n            || ?option = sample:Move_OCT21_A-M0021)\n    OPTIONAL { ?pos cjf:hasSummary ?summary . }\n}"
        },
        {
          "title": "Read the evidence for this position.",
          "nodes": [
            "pos",
            "support",
            "support_text"
          ],
          "edges": [
            "span",
            "words"
          ],
          "code": "SELECT * WHERE {\n    ?pos a cjf:ExpressedPosition .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName \"Speaker C\" .\n    ?pos cjf:hasPositionTowards ?option .\n    FILTER (?option = sample:Move_OCT21_A-M0003\n            || ?option = sample:Move_OCT21_A-M0021)\n    OPTIONAL { ?pos cjf:hasSummary ?summary . }\n    ?pos sio:SIO_000206 ?support .\n    ?support cjf:hasConversationText ?support_text .\n}"
        },
        {
          "title": "Check the utterance, its speaker, and its turn.",
          "nodes": [
            "support",
            "utterance",
            "speaker",
            "conversation",
            "turn"
          ],
          "edges": [
            "utterance",
            "attribution",
            "conversation",
            "turn"
          ],
          "code": "SELECT * WHERE {\n    ?pos a cjf:ExpressedPosition .\n    ?pos cjf:hasSpeaker ?speaker .\n    ?speaker cjf:hasSpeakerName \"Speaker C\" .\n    ?pos cjf:hasPositionTowards ?option .\n    FILTER (?option = sample:Move_OCT21_A-M0003\n            || ?option = sample:Move_OCT21_A-M0021)\n    OPTIONAL { ?pos cjf:hasSummary ?summary . }\n    ?pos sio:SIO_000206 ?support .\n    ?support cjf:hasConversationText ?support_text .\n    ?support cjf:isPartOfUtterance ?utterance .\n    ?utterance prov:wasAttributedTo ?speaker .\n    ?utterance prov:wasGeneratedBy sample:Conversation .\n    ?utterance cjf:hasTurnNumber ?turn .\n}"
        }
      ],
      "examples": [
        {
          "label": "Turn 9 · Platform B",
          "rowIndex": 0,
          "terms": {
            "pos": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0020",
              "origin": "recorded",
              "display": "M0020"
            },
            "posType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/ExpressedPosition",
              "origin": "recorded",
              "display": "ExpressedPosition"
            },
            "speaker": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Speaker_1ce82228187659212b16",
              "origin": "inferred",
              "display": "Speaker_1ce82228…"
            },
            "speakerName": {
              "value": "Speaker C",
              "origin": "recorded"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0021",
              "origin": "inferred",
              "display": "M0021"
            },
            "summary": {
              "value": "C currently prefers Platform B.",
              "origin": "recorded"
            },
            "support": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_dfdf74ccf0c59078466f",
              "origin": "recorded",
              "display": "Span_dfdf74cc…"
            },
            "support_text": {
              "value": "I’d still prefer Platform B at this point.",
              "origin": "recorded"
            },
            "utterance": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Turn_9",
              "origin": "recorded",
              "display": "Turn_9"
            },
            "conversation": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Conversation",
              "origin": "recorded",
              "display": "Conversation"
            },
            "turn": {
              "value": "9",
              "origin": "recorded"
            }
          },
          "edges": {
            "posType": "recorded",
            "speaker": "inferred",
            "name": "recorded",
            "target": "inferred",
            "summary": "recorded",
            "span": "recorded",
            "words": "recorded",
            "utterance": "recorded",
            "attribution": "recorded",
            "conversation": "recorded",
            "turn": "recorded"
          },
          "note": "The position records its supporting span directly.",
          "answer": {
            "pos": "sample:Move_OCT21_A-M0020",
            "option": "sample:Move_OCT21_A-M0021",
            "summary": "C currently prefers Platform B.",
            "support_text": "I’d still prefer Platform B at this point.",
            "turn": "9"
          }
        },
        {
          "label": "Turn 27 · Platform A",
          "rowIndex": 1,
          "terms": {
            "pos": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0063",
              "origin": "recorded",
              "display": "M0063"
            },
            "posType": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/ExpressedPosition",
              "origin": "recorded",
              "display": "ExpressedPosition"
            },
            "speaker": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Speaker_1ce82228187659212b16",
              "origin": "inferred",
              "display": "Speaker_1ce82228…"
            },
            "speakerName": {
              "value": "Speaker C",
              "origin": "recorded"
            },
            "option": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Move_OCT21_A-M0003",
              "origin": "inferred",
              "display": "M0003"
            },
            "summary": {
              "value": "C agrees with choosing Platform A.",
              "origin": "recorded"
            },
            "support": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Span_20698aac390dc7ca1e27",
              "origin": "inferred",
              "display": "Span_20698aac…"
            },
            "support_text": {
              "value": "I’m voting for Platform A as well.",
              "origin": "recorded"
            },
            "utterance": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Turn_27",
              "origin": "recorded",
              "display": "Turn_27"
            },
            "conversation": {
              "value": "https://tw.rpi.edu/ontology-engineering/oe2026/tracking-cjf/CQSample/Conversation",
              "origin": "recorded",
              "display": "Conversation"
            },
            "turn": {
              "value": "27",
              "origin": "recorded"
            }
          },
          "edges": {
            "posType": "recorded",
            "speaker": "inferred",
            "name": "recorded",
            "target": "inferred",
            "summary": "recorded",
            "span": "inferred",
            "words": "recorded",
            "utterance": "recorded",
            "attribution": "recorded",
            "conversation": "recorded",
            "turn": "recorded"
          },
          "note": "Positive support on this position entails the general SIO evidence relationship.",
          "answer": {
            "pos": "sample:Move_OCT21_A-M0063",
            "option": "sample:Move_OCT21_A-M0003",
            "summary": "C agrees with choosing Platform A.",
            "support_text": "I’m voting for Platform A as well.",
            "turn": "27"
          }
        }
      ]
    }
  ]
};
