<article class="mb-5" id="scenarioquery">
<content>
<h2>Queries</h2>
<ul>
    <h3> Study Match: Is there a study that matches this patient on a feature (s)? </h3>
    <strong> Query 1: SPARQL Query to fetch study titles that match a patient's race and gender </strong>
   <pre>
    PREFIX resource: <http://semanticscience.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sio: <http://semanticscience.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX chear: <http://hadatac.org/ont/chear#>
    PREFIX ncit: <http://purl.obolibrary.org/obo/NCIT_>
    PREFIX provcare: <http://www.case.edu/ProvCaRe/provcare#>

	SELECT DISTINCT ?studyTitle ?study WHERE 
	{
  		?study a ncit:C71104 .
  		?study dct:title ?studyTitle .
  		?study sio:hasParticipant ?studyArm .
  		?studyArm sio:hasProperty [a ?studyIntervention] .
  
  		{

  			?subPatient rdfs:subClassOf ?studyArm .
  			?subPatient rdfs:subClassOf ?restriction .
  			?restriction a owl:Restriction .
  			?restriction owl:someValuesFrom ncit:C16352 .
  
	}
  	{

  		?subPatient1 rdfs:subClassOf ?studyArm .
  		?subPatient1 rdfs:subClassOf ?restriction1 .
  		?restriction1 a owl:Restriction .
  		?restriction1 owl:someValuesFrom sio:Male .
	}
    }
  </pre>
  
  <strong> Result 1: Study titles retrieved from the study match query to find all studies in which African American Males are represented </strong>
  

 <table style="width:100%">
    <tr>
    <th>Study Title</th>
  </tr>
		
  <tr>
    <td>10-Year Follow-up of Intensive Glucose Control in Type 2 Diabetes</td>
  </tr>
  <tr>
    <td>New insulin glargine 300 U/ml compared with glargine 100 U/ml in insulin-nave people with type 2 diabetes on oral glucose-lowering drugs: a randomized controlled trial (EDITION 3)</td>
  </tr>
  <tr>
    <td>Efficacy and Safety of Degludec versus Glargine in Type 2 Diabetes</td>
  </tr>
  
  <tr>
    <td>Patientdirected titration for achieving glycaemic goals using a once daily basal insulin analogue: an assessment of two different fasting plasma glucose targets the TITRATETM study</td>
  </tr>
	 
<tr>
<td>Glycaemic control and hypoglycaemia with new insulin glargine 300 U/ml versus insulin glargine 100 U/ml in people with type 2 diabetes using basal insulin and oral antihyperglycaemic drugs: the EDITION 2 randomized 12-month trial including 6-month extension.
</td>
</tr>

<tr>
<td>Glycaemic control and hypoglycaemia with new insulin glargine 300 U/ml versus insulin glargine 100 U/ml in people with type 2 diabetes using basal insulin and oral antihyperglycaemic drugs: the EDITION 2 randomized 12-month trial including 6-month extension</td>
</tr>

<tr>
<td>Effects on blood pressure of reduced dietary sodium and the Dietary Approaches to Stop Hypertension (DASH) diet. DASH-Sodium Collaborative Research Group
</td>
</tr>

<tr>
<td>Telmisartan, ramipril, or both in patients at high risk for vascular events</td>
</tr>

<tr>
<td>Combined angiotensin inhibition for the treatment of diabetic nephropathy</td>
</tr>

<tr>
<td>Effect of Finerenone on Albuminuria in Patients With Diabetic Nephropathy: A Randomized Clinical Trial</td>
</tr>

<tr>
<td>A randomized trial of therapies for type 2 diabetes and coronary artery disease</td>
</tr>

<tr>
<td>Effects of combination lipid therapy in type 2 diabetes mellitus</td>
</tr>

<tr>
<td>Randomized controlled trial comparing impact on platelet reactivity of twice-daily with once-daily aspirin in people with Type 2 diabetes</td>
</tr>

<tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
</tr>

<tr>
<td>Effects of intensive blood-pressure control in type 2 diabetes mellitus</td>
</tr>
</table>


  
  
    
   <h3> Study Limitations: Are there absence or underrepresentation of population groups in this study? </h3>
   <strong> Query 2: SPARQL Query to fetch study titles and range of values reported for Age </strong>
   <pre>
PREFIX sco: <https://idea.tw.rpi.edu/projects/heals/studycohort/>
PREFIX resource: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX chear: <http://hadatac.org/ont/chear#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?studyTitle ?propType ?lowerBound ?propVal 
?upperBound
WHERE {

  ?study a ncit:C71104 .
  ?study dct:title ?studyTitle .
  ?study sio:hasParticipant ?studyArm .
  ?studyArm sio:hasAttribute | sio:hasProperty ?prop .
  
     { 
       ?prop a ?propType .
       ?prop sio:hasAttribute ?attr .
       ?attr a sio:Mean .
       ?attr sio:hasValue ?propVal .  
       ?prop sio:hasAttribute ?attr2 .
       ?attr2 a sio:StandardDeviation .
       ?attr2 sio:hasValue ?propVal2 .   
       BIND((?propVal2  + 2*?propVal) AS ?upperBound) .
       BIND((?propVal  - 2*?propVal2) AS ?lowerBound) . 
     } 
      UNION 
    { 
      ?prop a ?propType .
      ?prop sio:hasAttribute ?attr .
      ?attr a sio:Median .
      ?attr sio:hasValue ?propVal .  
      ?prop sio:hasAttribute ?attr2 .
      ?attr2 a stato:0000164 .
      ?prop sio:hasAttribute sio:MaximalValue .
      ?attr2 sio:hasValue ?upperBound .
      ?prop sio:hasAttribute sio:MinimalValue .
      ?attr2 sio:hasValue ?lowerBound .
    }
   FILTER (?upperBound <= 70) .  
   FILTER  (?propType IN (sio:Age)).

}
   
   </pre>
   
  <strong> Result 2: Study Titles and Age Ranges retrieved from the study limitation query to find studies where old adults above 70 are not represented </strong>
  
 <table style="width:100%">
    <tr>
    <th>Study Title </th>
    <th>Lower Bound</th> 
    <th>Median/Mean Age</th> 
    <th>Upper Bound</th> 
  </tr>

 <tr>
    <td>Effects on blood pressure of reduced dietary sodium and the Dietary Approaches to Stop Hypertension (DASH) diet., DASH-Sodium Collaborative Research Group</td>
    <td> 37</td> 
    <td>47</td>
    <td>57 </td> 
  </tr>
	
  <tr>
    <td>Effects on blood pressure of reduced dietary sodium and the Dietary Approaches to Stop Hypertension (DASH) diet., DASH-Sodium Collaborative Research Group</td>
    <td> 39</td> 
    <td>49</td>
    <td> 59</td> 
  </tr>
 
 <tr>
<td>Patientdirected titration for achieving glycaemic goals using a oncedaily basal insulin analogue: an assessment of two different fasting plasma glucose targets the TITRATETM study</td>
    <td> </td> 
    <td>56.6</td>
    <td> </td> 
  </tr>
	
<tr>
<td>Patientdirected titration for achieving glycaemic goals using a oncedaily basal insulin analogue: an assessment of two different fasting plasma glucose targets the TITRATETM study</td>
    <td> </td> 
    <td>57.2</td>
    <td> </td> 
  </tr>
  
<tr>
<td>Patientdirected titration for achieving glycaemic goals using a oncedaily basal insulin analogue: an assessment of two different fasting plasma glucose targets the TITRATETM study</td>
    <td> </td> 
    <td>56.9</td>
    <td> </td> 
  </tr>
  
  <tr>
<td>Randomized controlled trial comparing impact on platelet reactivity of twice-daily with once-daily aspirin in people with Type 2 diabetes</td>
    <td>44 </td> 
    <td>51</td>
    <td> 58</td> 
  </tr>
  
  <tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
    <td> </td> 
    <td>66</td>
    <td> </td> 
  </tr>
  
  <tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
    <td> </td> 
    <td>67</td>
    <td> </td> 
  </tr>
  
  <tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
    <td> </td> 
    <td>66</td>
    <td> </td> 
  </tr>
  
  <tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
    <td> </td> 
    <td>67</td>
    <td> </td> 
  </tr>
  
<tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
    <td> </td> 
    <td>67</td>
    <td> </td> 
  </tr>
  
  
 <tr>
<td>Cardiovascular outcomes using doxazosin vs. chlorthalidone for the treatment of hypertension in older adults with and without glucose disorders: a report from the ALLHAT study</td>
    <td> </td> 
    <td>67</td>
    <td> </td> 
  </tr>
</table>

   
   <h3> Study Quality Evaluation: Are there adequate population sizes and is there a heterogeneity of treatment effect among arms? </h3>
   <strong> Query 3: SPARQL query to find large scale studies with intervention arms size being at least 1/3rd the overall cohort size </strong>
   <pre>
PREFIX sco: <https://idea.tw.rpi.edu/projects/heals/studycohort/>
PREFIX resource: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX chear: <http://hadatac.org/ont/chear#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX provcare: <http://www.case.edu/ProvCaRe/provcare#>

SELECT DISTINCT ?studyTitle ?medicationLabel ?popSize ?totalCohortSize
WHERE {
  ?study a ncit:C71104 .
  ?study dct:title ?studyTitle .
  ?study sio:hasParticipant ?studyArm .
  ?studyArm sio:hasProperty ?intervention .
  ?intervention a ?interventionType .
  ?intervention prov:used ?medication .
  ?medication rdfs:label ?medicationLabel .
  ?studyArm sio:hasAttribute ?prop .
  ?prop a sco:PopulationSize .
  ?prop sio:hasValue ?popSize . 
  {
    SELECT DISTINCT ?study (SUM(?popSize) AS ?totalCohortSize) WHERE {  
        ?study sio:hasParticipant ?studyArm .    
	?studyArm sio:hasAttribute ?prop .
        ?prop a sco:PopulationSize .
        ?prop sio:hasValue ?popSize .  
   }  
   GROUP BY ?study 
   HAVING (?totalCohortSize > 1000)
   }
  FILTER (?popSize >= (?totalCohortSize/3)) .
  FILTER ((?interventionType rdfs:subClassOf* 
  provcare:Intervention ) && (?medication rdfs:subClassOf* 
  chebi:24436 )).
}
   
   </pre>
   <strong> Result 3:   Cohort sizes and individual study arm sizes of clinical trials retrieved from a query to find the studies having a cohort population <span>&#8805;</span> 1000 and individual study arm population sizes are at least <sup>1<sup>rd</sup> </sup>&frasl;<sub>3</sub> the cohort size
</strong>
 
 <table style="width:100%">
    <tr>
    <th>Study Title</th>
    <th>Cohort Size</th> 
    <th>Study Arm</th>
    <th>Arm Size</th> 
  </tr>
  <tr>
    <td>Long-term Metformin Use and Vitamin B12 Deficiency in the Diabetes Prevention Program Outcomes Study</td>
    <td> 1800 </td> 
    <td> Metformin</td> 
    <td> 753</td> 
  </tr>
  <tr>
    <td>Long-term Metformin Use and Vitamin B12 Deficiency in the Diabetes Prevention Program Outcomes Study</td>
    <td> 1800 </td> 
    <td>Metformin </td> 
    <td> 859</td> 
  </tr>
  <tr>
    <td>Effects of combination lipid therapy in type 2 diabetes mellitus </td>
    <td> 5518 </td> 
     <td> Metformin</td> 
     <td> 2765</td> 
  </tr>
    <tr>
    <td> Effects of combination lipid therapy in type 2 diabetes mellitus</td>
    <td> 5518  </td> 
    <td> Metformin</td>
    <td> 2753 </td> 
  </tr>
    <tr>
    <td> Efficacy and Safety of Degludec versus Glargine in Type 2 Diabetes </td>
    <td> 7637 </td> 
    <td> Metformin</td>
    <td>  3818</td> 
  </tr>
   <tr>
    <td> Efficacy and Safety of Degludec versus Glargine in Type 2 Diabetes </td>
    <td>7637  </td> 
    <td> Metformin</td>
    <td> 3819 </td> 
  </tr>
</table>

   
   
 </ul>
 </content>
 
 
 <article class="mb-5" id="visualization">
<content>
<h2> Value Retrieval Query for Visualization </h2>
<ul>
   <h3>  Star Plot Code </h3>
    <p>We present a query below that is used to retrieve the central value,  and upper and lower bounds for continuous characteristics of a study arm. The characteristics are those that overlap with the patient features that we gather for diabetic patients in NHANES, i.e. age, body mass index, systolic blood pressure, diastolic blood pressure, Hemoglobin A1C. This query is triggered in the faceted browser to generate the visualization.<br>
    This query can flexibly retrieve values for both mean +/- standard deviation, median and interquartile range representations with being agnostic of the expression of the characteristic. Also, if we were to constrain the query for values of other parameters, we would just included them in the filter clause. Hence, this query is a generalized faceted browser query.</p> 
	<pre>
	To run the code, please follow the steps as below:
	1. cd study-cohort-ontology 
	2. python3 -m venv env 
	3. source env/bin/activate
	4. pip install -r ../requirements.txt
	5. python3 starplot.py
	</pre>
    <p>The star plot code can be browsed at: <a href="https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Code/starplot.py"><small>https://raw.githubusercontent.com/tetherless-world/study-cohort-ontology/master/Code/starplot.py</small></a></p>
	
    <pre>
PREFIX sco: <small><https://idea.tw.rpi.edu/projects/heals/studycohort/></small>
PREFIX resource: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX chear: <http://hadatac.org/ont/chear#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX stato: <http://purl.obolibrary.org/obo/STATO_>
PREFIX ncit: <http://purl.obolibrary.org/obo/NCIT_>

SELECT DISTINCT ?studyTitle ?propType ?lowerBound ?propVal
?upperBound WHERE {

  ?study a ncit:C71104 .
  ?study dct:title ?studyTitle .
  ?study sio:hasParticipant ?studyArm .
  ?studyArm sio:hasAttribute | sio:hasProperty ?prop .
     { 
       ?prop a ?propType .
       ?prop sio:hasAttribute ?attr .
       ?attr a sio:Mean .
       ?attr sio:hasValue ?propVal .  
       ?prop sio:hasAttribute ?attr2 .
       ?attr2 a sio:StandardDeviation .
       ?attr2 sio:hasValue ?propVal2 .   
       BIND((?propVal2  + ?propVal) AS ?upperBound) .
       BIND((?propVal  - ?propVal2) AS ?lowerBound) . 
     } 
      UNION 
    { 
       ?prop a ?propType .
       ?prop sio:hasAttribute ?attr .
       ?attr a sio:Median .
       ?attr sio:hasValue ?propVal .  
       ?prop sio:hasAttribute ?attr2 .
      ?attr2 a stato:0000164 .
      ?prop sio:hasAttribute sio:MaximalValue .
      ?attr2 sio:hasValue ?upperBound .
      ?prop sio:hasAttribute sio:MinimalValue .
      ?attr2 sio:hasValue ?lowerBound .   
    }
   FILTER  (
    ?propType IN (
       sio:Age,
       ncit:C64796,
       sco:SystolicBloodPressure, 
       sco:DiastolicBloodPressure
   ) ).
   
}
    </pre>
 </ul>
 </content>
