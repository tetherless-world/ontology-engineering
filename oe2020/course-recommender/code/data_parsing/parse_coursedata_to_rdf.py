import rdflib
from rdflib.namespace import XSD, OWL
from crex.utils.namespaces import CRS_NS, RDF_NS, LCC_LR_NS
import ast
import csv

# quick and dirty implementation to parse yacs data csv into rdf.

savename = 'yacs_CSCI_course_data.ttl'
combine_save_name = 'course-recommender-individuals.rdf'
course_data_files = ['spring-2020.csv', 'fall-2020.csv', 'summer-2020.csv']

LIMIT_COURSE_DEPT = True
COURSE_DEPT_CHOICES = ['CSCI']
SKIP_NONEXISTING_PREREQ = True

department_data = '../../archived/rpi_departments.ttl'
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
                    name_to_index = {item:row.index(item) for item in row}
                skipfirst = False


graph = rdflib.Graph()
graph.parse('../../archived/course-recommender-individuals-seed.rdf')

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


#make up new URIs.
def new_uri():
    return entity_ns[f'crs{str(len(entity_uri_dict)).zfill(6)}']


for row in data_rows[1:]:
    course_uri = entity_uri_dict.get(f"course-{row[name_to_index['short_name']]}", '')
    if LIMIT_COURSE_DEPT and not row[name_to_index['course_department']] in COURSE_DEPT_CHOICES:
        continue
    if not course_uri:
        course_uri = new_uri()
        entity_uri_dict[f"course-{row[name_to_index['short_name']]}"] = course_uri
        course_code_uri = new_uri()
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
                prereq_uri = new_uri()
                entity_uri_dict[prereq] = prereq_uri

            graph.add((course_uri, CRS_NS['hasRequiredPrerequisite'], prereq_uri))
    if row[name_to_index['corequisites']]:
        for coreq in ast.literal_eval(row[name_to_index['corequisites']]):

            coreq_uri = entity_uri_dict.get(coreq, '')
            if not coreq_uri:
                if SKIP_NONEXISTING_PREREQ:
                    continue
                coreq_uri = new_uri()
                entity_uri_dict[coreq] = coreq_uri

            graph.add((course_uri, CRS_NS['hasCorequisite'], coreq_uri))
graph.serialize(savename, format='ttl')

graph.parse('../../archived/rpi_departments.ttl', format='ttl')
graph.parse('../../archived/manualcurated_grad_requirements.ttl', format='ttl')
graph.serialize(combine_save_name, format='xml')