---
layout: default
title: related_work
---

## Related Work and References

CareAir sits at the intersection of four bodies of work: the healthcare ventilation standards that define *what* must be checked, the semantic building models that describe *where* and *by what equipment* air is delivered, the assessment and policy vocabularies that describe *how a verdict is structured*, and the provenance and measurement vocabularies that let the verdict *carry its evidence*. The lists below give the sources we built on, grouped that way, followed by the prior course project we reviewed and the methodology we followed. Citations use the Chicago format where a publication exists; standards and online specifications are cited as such.

### Ventilation requirements for healthcare facilities

These are the documents whose numeric thresholds and space lists the ontology encodes. The CDC guideline is the open source of the values actually used in the test data; ASHRAE 170 is the engineering standard the guideline refers to.

- Sehulster, Lynne, and Raymond Y. W. Chinn. "Guidelines for Environmental Infection Control in Health-Care Facilities: Recommendations of CDC and the Healthcare Infection Control Practices Advisory Committee (HICPAC)." *MMWR Recommendations and Reports* 52, no. RR-10 (2003): 1–42. Current online edition: Centers for Disease Control and Prevention, *Guidelines for Environmental Infection Control in Health-Care Facilities*, Appendix B "Air", [https://www.cdc.gov/infection-control/hcp/environmental-control/appendix-b-air.html](https://www.cdc.gov/infection-control/hcp/environmental-control/appendix-b-air.html). Source of the room taxonomy and of the six policy kinds (design temperature, relative humidity, minimum outdoor air changes per hour, all air exhausted directly to outdoors, air movement relationship to adjacent area, recirculation by room units).
- ASHRAE. *ANSI/ASHRAE/ASHE Standard 170-2021, Ventilation of Health Care Facilities.* Atlanta, GA: ASHRAE, 2021. Table 7.1 "Design Parameters" was used for the pressure-relationship and air-change requirements per space type and for term definitions.
- Facility Guidelines Institute. *Guidelines for Design and Construction of Hospitals.* St. Louis, MO: FGI. [https://fgiguidelines.org/](https://fgiguidelines.org/). Adopts ASHRAE 170 and defines the clinical space program the room taxonomy mirrors.
- ASHRAE. *ASHRAE Terminology: A Comprehensive Glossary of Terms for the Built Environment.* [https://terminology.ashrae.org/](https://terminology.ashrae.org/). Primary source of HVAC component, airflow and measurement definitions in the terminology list.
- ASHRAE. *Addendum s to ASHRAE Guideline 36-2018, High-Performance Sequences of Operation for HVAC Systems.* Atlanta, GA: ASHRAE, 2021. Source for damper and air-handling-unit sequence terminology.
- American Society for Health Care Engineering. "Evaluate and Implement Operating Room Airflow Setback." *Energy to Care*. Chicago, IL: ASHE. [https://www.ashe.org/](https://www.ashe.org/).
- Tejero-González, Ana, Héctor López-Pérez, and Francisco Espí-García. "Safety and Energy Implications of Setback Control in Operating Rooms during Unoccupied Periods." *Applied Sciences* 12, no. 9 (2022): 4098. [https://doi.org/10.3390/app12094098](https://doi.org/10.3390/app12094098). Motivates the energy argument in the use case: a facility that can *demonstrate* compliance continuously, with provenance, can take the unoccupied setback that one that can only *assert* compliance cannot.

### Semantic models of buildings, equipment and sensors

The building side of CareAir reuses or aligns with the following. RealEstateCore, SAREF4BLDG and FSO are imported or referenced directly; ASHRAE 223P and Brick were reviewed as the likely sources of real building data.

- Hammar, Karl, Erik Oskar Wallin, Per Karlberg, and David Hälleberg. "The RealEstateCore Ontology." In *The Semantic Web – ISWC 2019*, Lecture Notes in Computer Science 11779, 130–145. Cham: Springer, 2019. RealEstateCore Consortium, *RealEstateCore Core Module* 3.3, [https://doc.realestatecore.io/3.3/core.html](https://doc.realestatecore.io/3.3/core.html). Provides `Building`, `Room` and `serves`.
- Daniele, Laura, Frank den Hartog, and Jasper Roes. "Created in Close Interaction with the Industry: The Smart Appliances REFerence (SAREF) Ontology." In *Formal Ontologies Meet Industry (FOMI 2015)*, Lecture Notes in Business Information Processing 225, 100–112. Cham: Springer, 2015.
- Poveda-Villalón, María, and Raúl García-Castro. "Extending the SAREF Ontology for Building Devices and Topology." In *Proceedings of the 6th Linked Data in Architecture and Construction Workshop (LDAC 2018)*, CEUR Workshop Proceedings 2159, 16–23, 2018. ETSI, *SAREF4BLDG: An Extension of SAREF for the Building Domain*, v2.1.1, 2025, [https://saref.etsi.org/saref4bldg/v2.1.1/](https://saref.etsi.org/saref4bldg/v2.1.1/). Provides the sensor and equipment classes.
- ETSI. *SAREF4SYST: An Extension of SAREF for Typology of Systems and Their Inter-connections*, v1.1.2, 2020. [https://saref.etsi.org/saref4syst/v1.1.2/](https://saref.etsi.org/saref4syst/v1.1.2/). Reviewed for the system/sub-system and connection pattern.
- Kukkonen, Ville, Ali Kücükavci, Mikki Seidenschnur, Mads Holten Rasmussen, Kevin Michael Smith, and Christian Anker Hviid. "An Ontology to Support Flow System Descriptions from Design to Operation of Buildings." *Automation in Construction* 134 (2022): 104067. Flow Systems Ontology (FSO), [https://alikucukavci.github.io/FSO/](https://alikucukavci.github.io/FSO/). Provides `fso:System`, `fso:Component` and `fso:hasComponent`, the super-classes of our building service system and component.
- ASHRAE SPC 223. *ASHRAE Standard 223P, Semantic Data Model for Analytics and Automation Applications in Buildings* (public review draft) and user documentation "Sensors and Properties". [https://open223.info/](https://open223.info/), [https://docs.open223.info/sensors-and-properties](https://docs.open223.info/sensors-and-properties). The connection-point and observable-property model that the DOE prototype hospital topology would be expressed in; the use case assumes a validated 223P model as pre-condition P1.
- Fierro, Gabe, Anand Prakash, Cory Mosiman, Marco Pritoni, Paul Raftery, Michael Wetter, and David E. Culler. "Shepherding Metadata Through the Building Lifecycle." In *Proceedings of the 7th ACM International Conference on Systems for Energy-Efficient Buildings, Cities, and Transportation (BuildSys '20)*, 70–79. New York: ACM, 2020. [https://doi.org/10.1145/3408308.3427627](https://doi.org/10.1145/3408308.3427627). Background on 223P and Brick interoperability.
- Balaji, Bharathan, Arka Bhattacharya, Gabriel Fierro, Jingkun Gao, Joshua Gluck, Dezhi Hong, Aslak Johansen, Jason Koh, Joern Ploennigs, Yuvraj Agarwal, Mario Bergés, David Culler, Rajesh K. Gupta, Mikkel Baun Kjærgaard, Mani Srivastava, and Kamin Whitehouse. "Brick: Metadata Schema for Portable Smart Building Applications." *Applied Energy* 226 (2018): 1273–1292. [https://doi.org/10.1016/j.apenergy.2018.02.091](https://doi.org/10.1016/j.apenergy.2018.02.091). Brick Consortium, *Brick Schema* v1.4, [https://ontology.brickschema.org/1.4/](https://ontology.brickschema.org/1.4/). Reviewed for sensor-point and equipment typing where 223P is coarser.
- Fierro, Gabe, Marco Pritoni, Moustafa AbdelBaky, Daniel Lengyel, John Leyden, Anand Prakash, Pranav Gupta, Paul Raftery, Therese Peffer, Greg Thomson, and David E. Culler. "Mortar: An Open Testbed for Portable Building Analytics." *ACM Transactions on Sensor Networks* 16, no. 1 (2019): 1–31. [https://doi.org/10.1145/3366375](https://doi.org/10.1145/3366375). Example of portable, model-driven analytics over Brick graphs.
- Miller, Clayton, Anjukan Kathirgamanathan, Bianca Picchetti, Pandarasamy Arjunan, June Young Park, Zoltan Nagy, Paul Raftery, Brodie W. Hobson, Zixiao Shi, and Forrest Meggers. "The Building Data Genome Project 2, Energy Meter Data from the ASHRAE Great Energy Predictor III Competition." *Scientific Data* 7, no. 1 (2020): 368. [https://doi.org/10.1038/s41597-020-00712-x](https://doi.org/10.1038/s41597-020-00712-x). Reviewed as a source of open building time-series data.
- Haller, Armin, Krzysztof Janowicz, Simon J. D. Cox, Maxime Lefrançois, Kerry Taylor, Danh Le Phuoc, Joshua Lieberman, Raúl García-Castro, Rob Atkinson, and Claus Stadler. "The Modular SSN Ontology: A Joint W3C and OGC Standard Specifying the Semantics of Sensors, Observations, Sampling, and Actuation." *Semantic Web* 10, no. 1 (2019): 9–32. W3C Recommendation *Semantic Sensor Network Ontology*, 2017, [https://www.w3.org/TR/vocab-ssn/](https://www.w3.org/TR/vocab-ssn/). The observation and feature-of-interest pattern behind `measures`, `measuredIn` and `recordedIn`.
- U.S. Department of Energy, Building Energy Codes Program / Pacific Northwest National Laboratory. *Prototype Building Models – Hospital* (EnergyPlus). [https://www.energycodes.gov/prototype-building-models](https://www.energycodes.gov/prototype-building-models). The building model from which the zone volumes and AHU-to-terminal-unit topology of the test scenario were taken.

### Compliance, policy and assessment vocabularies

The assessment module (assessment context, policy assessment, compliance assessment and their satisfied / unsatisfied / unknown states) borrows its structure from these.

- National Institute of Standards and Technology. *OSCAL Assessment Layer: Assessment Plan and Assessment Results Models.* Open Security Controls Assessment Language. [https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/). Source of the decomposition of an assessment into scope and context, reviewed controls (our policies), observations (our measurements) and findings (our policy assessments).
- W3C ODRL Community Group. "ODRL Formal Semantics", sections "Evaluation Report" and "General Semantics of Rules". Evolving community document. [https://w3c.github.io/odrl/formal-semantics/](https://w3c.github.io/odrl/formal-semantics/). Source of the policy-grouping semantics and of the satisfied / unsatisfied evaluation vocabulary for policies.
- Abou-Zahra, Shadi, ed. *Evaluation and Report Language (EARL) 1.0 Schema.* W3C Working Group Note, 2 February 2017. [https://www.w3.org/TR/2017/NOTE-EARL10-Schema-20170202/](https://www.w3.org/TR/2017/NOTE-EARL10-Schema-20170202/). Pattern for recording a test subject, a criterion, an outcome and evidence together.
- International Organization for Standardization. *ISO/IEC 17000:2020, Conformity Assessment – Vocabulary and General Principles.* Geneva: ISO, 2020. Source of the compliance-assessment definitions.
- International Organization for Standardization. *ISO 704:2022, Terminology Work – Principles and Methods*, 4th ed. Geneva: ISO, 2022. Every definition in the ontology was written following its genus-and-differentia rules.

### Measurement, units and provenance

- Lebo, Timothy, Satya Sahoo, Deborah McGuinness, Khalid Belhajjame, James Cheney, David Corsar, Daniel Garijo, Stian Soiland-Reyes, Stephan Zednik, and Jun Zhao, eds. *PROV-O: The PROV Ontology.* W3C Recommendation, 30 April 2013. [https://www.w3.org/TR/prov-o/](https://www.w3.org/TR/prov-o/). Imported; supplies measurement time, derivation of computed measurements and the association of an assessment with equipment.
- Object Management Group. *Commons Ontology Library: Quantities and Units* (20240801), *Collections* (20221101), *Parties and Situations* (20250801), *Contextual Designators* (20250801). [https://www.omg.org/spec/Commons/](https://www.omg.org/spec/Commons/). Quantities and Units is imported for values with units on measurements and policy bounds; the other three supply transitive part-of, `actsOn` / `isAffectedBy`, and `uses`.
- Joint Committee for Guides in Metrology. *International Vocabulary of Metrology – Basic and General Concepts and Associated Terms (VIM)*, 3rd ed., JCGM 200:2012. [https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf](https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf). Source of the definitions of measurement and derived measurement.
- QUDT.org. *QUDT Quantity Kinds Vocabulary.* [http://qudt.org/vocab/quantitykind/](http://qudt.org/vocab/quantitykind/). Reviewed for units; OMG Commons was adopted instead.
- Kuhn, Tobias, Christine Chichester, Michael Krauthammer, Núria Queralt-Rosinach, Ruben Verborgh, George Giannakopoulos, Axel-Cyrille Ngonga Ngomo, Raffaele Viglianti, and Michel Dumontier. "Decentralized Provenance-Aware Publishing with Nanopublications." *PeerJ Computer Science* 2 (2016): e78. [https://doi.org/10.7717/peerj-cs.78](https://doi.org/10.7717/peerj-cs.78). The assertion / provenance / publication-info packaging that the proposed architecture uses for each sensor reading and each assessment.

### Reasoning with OWL and rules

- Horrocks, Ian, Peter F. Patel-Schneider, Harold Boley, Said Tabet, Benjamin Grosof, and Mike Dean. *SWRL: A Semantic Web Rule Language Combining OWL and RuleML.* W3C Member Submission, 21 May 2004. [https://www.w3.org/submissions/SWRL/](https://www.w3.org/submissions/SWRL/). The rules S1 to S11 that compare measurements with policy bounds and attach equipment to failed assessments are written in SWRL with the `swrlb` comparison built-ins.
- Sirin, Evren, Bijan Parsia, Bernardo Cuenca Grau, Aditya Kalyanpur, and Yarden Katz. "Pellet: A Practical OWL-DL Reasoner." *Journal of Web Semantics* 5, no. 2 (2007): 51–53. [https://doi.org/10.1016/j.websem.2007.03.004](https://doi.org/10.1016/j.websem.2007.03.004). The reasoner used to evaluate the ontology and its rules in Protégé; HermiT rejects the numeric built-ins.
- Knublauch, Holger, and Dimitris Kontokostas, eds. *Shapes Constraint Language (SHACL).* W3C Recommendation, 20 July 2017. [https://www.w3.org/TR/shacl/](https://www.w3.org/TR/shacl/). Planned for the closed-world step that marks a policy assessment *unknown* when no measurement was logged.

### Prior course project reviewed for reuse

- Chung, J., K. Rook, and G. Jacoby-Cooper. "Indoor Environment Manager." Ontology Engineering 2022 class project, Rensselaer Polytechnic Institute, Troy, NY. [https://github.com/tetherless-world/ontology-engineering](https://github.com/tetherless-world/ontology-engineering). Reviewed in Section X of the use case; it also reuses SAREF4BLDG, and its treatment of indoor environmental conditions informed the sensor-measurement module, but it does not model compliance frameworks, derived measurements or the serves relation.

### Ontology engineering methodology

- Noy, Natalya F., and Deborah L. McGuinness. *Ontology Development 101: A Guide to Creating Your First Ontology.* Stanford Knowledge Systems Laboratory Technical Report KSL-01-05, 2001.
- Kendall, Elisa F., and Deborah L. McGuinness. *Ontology Engineering.* Synthesis Lectures on Data, Semantics, and Knowledge. Cham: Springer, 2019.
- Allemang, Dean, James Hendler, and Fabien Gandon. *Semantic Web for the Working Ontologist: Effective Modeling for Linked Data, RDFS, and OWL*, 3rd ed. New York: ACM Books, 2020.

### Project resources

- Ontology: [ventilation-compliance.rdf](ventilation-compliance.rdf); test individuals: [individuals.rdf](individuals.rdf)
- Curated terminology list with the full numbered reference sheet: [Terminology List](termlist)
- Use case document (version 10): [Use Case](usecase)
- Competency questions and SPARQL: [Demonstration and Queries](demo)
- Conceptual model slides: [Conceptual model presentation](https://docs.google.com/presentation/d/1Jslrjg4Fa2leQd6L-PwvgwmYcpPFwSQnfC6ZbXWKu54/edit?usp=sharing)
