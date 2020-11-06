import rdflib
from rdflib.namespace import XSD, OWL
from crex.utils.namespaces import CRS_NS, RDF_NS, LCC_LR_NS
import ast
from unidecode import unidecode
import csv

# quick and dirty implementation to parse yacs data csv into rdf.

savename = 'yacs_course_data_v2.ttl'
# savename = 'yacs_course_data_v1.ttl'
combine_save_name = 'course-recommender-individuals.rdf'
# combine_save_name = 'course-recommender-individuals.rdf'
course_data_files = ['spring-2020.csv', 'fall-2020.csv', 'summer-2020.csv']
transcript_files = {
    'owen': 'ox_transcript.csv',
    'jacob': 'js_transcript.csv',
    'kelly': 'kf_transcript.csv'
}

LIMIT_COURSE_DEPT = True
COURSE_DEPT_CHOICES = ['CSCI']
SKIP_NONEXISTING_PREREQ = True
save_combined = True

department_data = 'rpi_departments.ttl'
q = rdflib.Graph()
q.parse(department_data, format='ttl')
code_to_uri = dict()
code_to_dept_uri = dict()
for s, p, o in q.triples((None, RDF_NS['type'], CRS_NS['DepartmentCode'])):
    code_to_uri[q.value(s, rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag')).value] = s
    code_to_dept_uri[q.value(s, rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag')).value] = q.value(s, CRS_NS['hasDepartment'])


data_rows = []
name_to_index = []
for file in course_data_files:
    skipfirst = True
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if not skipfirst:
                data_rows.append(row)
            else:
                if not name_to_index:
                    name_to_index = {item:row.index(unidecode(item)) for item in row}
                skipfirst = False


graph = rdflib.Graph()
graph.parse('course-recommender-individuals-seed.rdf')

# graph.bind('oe2020-crs-rec', CRS_NS)
# graph.bind('owl', OWL)
entity_ns = rdflib.Namespace('https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/')
# graph.bind('oe2020-crs-rec-ind', entity_ns)
# graph.bind('lcc-lr', rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/'))
entity_uri_dict = dict()

placeholder_topic_uri = entity_ns['topic00001']
graph.add((placeholder_topic_uri, RDF_NS['type'], CRS_NS['TopicArea']))
graph.add((placeholder_topic_uri, RDF_NS['type'], OWL['NamedIndividual']))
graph.add((placeholder_topic_uri, rdflib.namespace.RDFS['label'], rdflib.Literal('placeholder for topic', datatype=XSD.string)))

# manually add a few schedules
semesters = ['spring', 'summer', 'fall']
years = [2017, 2018, 2019, 2020, 2021]
for year in years:
    for sem in semesters:
        sem_yr = sem+" "+str(year)
        schedule_uri = entity_ns[f'sched{str(len(entity_uri_dict)).zfill(6)}']
        entity_uri_dict[sem_yr] = schedule_uri
        graph.add((schedule_uri, RDF_NS['type'], CRS_NS['SemesterSchedule']))
        graph.add((schedule_uri, RDF_NS['type'], OWL['NamedIndividual']))
        graph.add((schedule_uri, CRS_NS['hasSemester'], rdflib.Literal(sem, datatype=XSD.string)))
        graph.add((schedule_uri, CRS_NS['hasSemesterYear'], rdflib.Literal(year, datatype=XSD.integer)))


#make up new URIs.
def new_course_uri():
    return entity_ns[f'crs{str(len(entity_uri_dict)).zfill(6)}']

def new_course_sec_uri():
    return entity_ns[f'crsSec{str(len(entity_uri_dict)).zfill(6)}']


for row in data_rows[1:]:
    course_uri = entity_uri_dict.get(f"course-{row[name_to_index['short_name']]}", '')
    if LIMIT_COURSE_DEPT and not row[name_to_index['course_department']] in COURSE_DEPT_CHOICES:
        continue
    if not course_uri:
        course_uri = new_course_uri()
        entity_uri_dict[f"course-{row[name_to_index['short_name']]}"] = course_uri
        course_code_uri = new_course_uri()
        entity_uri_dict[row[name_to_index['short_name']]] = course_code_uri

        # TODO: right now department code is used to make department. change in future.
        dept_code_uri = code_to_uri[row[name_to_index['course_department']]]
        department_uri = code_to_dept_uri[row[name_to_index['course_department']]]

        graph.add((course_uri, RDF_NS['type'], CRS_NS['Course']))
        graph.add((course_uri, RDF_NS['type'], OWL['NamedIndividual']))
        graph.add((course_uri, CRS_NS['hasName'], rdflib.Literal(row[name_to_index['full_name']], datatype=XSD.string)))

        # TODO: not sure how to handle credit hours with ranges (e.g. "1-9") so just set to 1 for now
        if "-" in row[name_to_index['course_credit_hours']]:
            graph.add((course_uri, CRS_NS['hasCredits'],
                       rdflib.Literal(1, datatype=XSD.integer)))
        else:
            graph.add((course_uri, CRS_NS['hasCredits'], rdflib.Literal(row[name_to_index['course_credit_hours']], datatype=XSD.integer)))

        graph.add((course_uri, CRS_NS['hasDepartment'], department_uri))
        graph.add((course_uri, CRS_NS['hasCourseCode'], course_code_uri))
        graph.add((course_uri, CRS_NS['hasDescription'], rdflib.Literal(row[name_to_index['description']], datatype=XSD.string)))
        graph.add((course_uri, CRS_NS['hasTopic'], placeholder_topic_uri))

        graph.add((course_code_uri, RDF_NS['type'], CRS_NS['CourseCode']))
        graph.add((course_code_uri, RDF_NS['type'], OWL['NamedIndividual']))
        graph.add((course_code_uri, CRS_NS['hasLevel'], rdflib.Literal(row[name_to_index['course_level']], datatype=XSD.integer)))
        graph.add((course_code_uri, CRS_NS['hasDepartmentCode'], dept_code_uri))
        graph.add((course_code_uri, LCC_LR_NS['hasTag'], rdflib.Literal(row[name_to_index['short_name']], datatype=XSD.string)))

    schedule_uri = entity_uri_dict[row[name_to_index['semester']].lower()]
    course_sec_uri = new_course_sec_uri()
    entity_uri_dict[f'{str(course_sec_uri)}'] = course_sec_uri
    graph.add((course_sec_uri, RDF_NS['type'], CRS_NS['CourseSection']))
    graph.add((course_sec_uri, RDF_NS['type'], OWL['NamedIndividual']))
    graph.add((course_sec_uri, CRS_NS['isCourseSectionOf'], course_uri))
    graph.add((course_sec_uri, CRS_NS['hasSchedule'], schedule_uri))

for row in data_rows[1:]:
    # TODO: prerequisite information is not correctly parsed in the current data (10/20/2020). need to
    #  apply an extra check for "and" vs "or" vs "/" (slash usually for crosslisted courses)
    if LIMIT_COURSE_DEPT and not row[name_to_index['course_department']] in COURSE_DEPT_CHOICES:
        continue
    course_uri = entity_uri_dict[row[name_to_index['short_name']]]
    if row[name_to_index['prerequisites']]:
        for prereq in ast.literal_eval(row[name_to_index['prerequisites']]):

            prereq_uri = entity_uri_dict.get(prereq, '')
            if not prereq_uri:
                if SKIP_NONEXISTING_PREREQ:
                    continue
                prereq_uri = new_course_uri()
                entity_uri_dict[prereq] = prereq_uri

            graph.add((course_uri, CRS_NS['hasRequiredPrerequisite'], prereq_uri))
    if row[name_to_index['corequisites']]:
        for coreq in ast.literal_eval(row[name_to_index['corequisites']]):

            coreq_uri = entity_uri_dict.get(coreq, '')
            if not coreq_uri:
                if SKIP_NONEXISTING_PREREQ:
                    continue
                coreq_uri = new_course_uri()
                entity_uri_dict[coreq] = coreq_uri

            graph.add((course_uri, CRS_NS['hasCorequisite'], coreq_uri))

# user stuff

def new_pos_uri():
    return entity_ns[f'pos{str(len(entity_uri_dict)).zfill(6)}']

def new_usr_uri():
    return entity_ns[f'usr{str(len(entity_uri_dict)).zfill(6)}']

for user, file in transcript_files.items():
    print(user, file)
    user_uri = new_usr_uri()
    entity_uri_dict[user] = user_uri
    graph.add((user_uri, CRS_NS['hasName'], rdflib.Literal(user, datatype=XSD.string)))
    graph.add((user_uri, RDF_NS['type'], CRS_NS['Student']))
    graph.add((user_uri, RDF_NS['type'], OWL['NamedIndividual']))

    pos_uri = new_pos_uri()
    entity_uri_dict[str(pos_uri)] = pos_uri
    graph.add((pos_uri, RDF_NS['type'], CRS_NS['PlanOfStudy']))
    graph.add((pos_uri, RDF_NS['type'], OWL['NamedIndividual']))
    graph.add((user_uri, CRS_NS['hasStudyPlan'], pos_uri))


    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:

            course_code = row[0].replace(" ", "-")
            cc_uri = entity_uri_dict.get(course_code, '')
            if not cc_uri:
                print(f"course code missing: {course_code}")
                continue

            # graph.add((pos_uri, CRS_NS['hasCompletedCourse'], cc_uri))

            schedule_uri = entity_uri_dict[str(row[1] + " " + row[2]).lower()]

            course_sec_query = graph.query(f"""
            prefix crs-onto: <{CRS_NS}>
            SELECT ?csUri
            WHERE {{
            ?courseUri crs-onto:hasCourseCode {cc_uri.n3()} .
            ?csUri crs-onto:isCourseSectionOf ?courseUri ;
                crs-onto:hasSchedule {schedule_uri.n3()} .
            }}
            """)
            # expect only 1 result
            if not course_sec_query:
                course_sec_uri = new_course_sec_uri()
                entity_uri_dict[f'{str(course_sec_uri)}'] = course_sec_uri
                graph.add((course_sec_uri, RDF_NS['type'], CRS_NS['CourseSection']))
                graph.add((course_sec_uri, RDF_NS['type'], OWL['NamedIndividual']))
                graph.add((course_sec_uri, CRS_NS['isCourseSectionOf'], cc_uri))
                graph.add((course_sec_uri, CRS_NS['hasSchedule'], schedule_uri))
                # print(f'added missing course section {row[1]+" "+row[2]} of {course_code}')
            else:
                for res in course_sec_query:
                    graph.add((pos_uri, CRS_NS['hasCompletedCourse'], res.csUri))
                # print(f'found course section {row[1]+" "+row[2]} of {course_code}')

graph.serialize(savename, format='ttl')

if save_combined:
    graph.parse('rpi_departments.ttl', format='ttl')
    graph.parse('manualcurated_grad_requirements.ttl', format='ttl')
    graph.serialize(combine_save_name, format='xml')