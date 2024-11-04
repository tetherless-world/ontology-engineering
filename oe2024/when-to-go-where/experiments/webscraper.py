from bs4 import BeautifulSoup
import requests
import re


LINK = "https://www.cntraveler.com/gallery/the-best-hike-in-every-national-park"

response = requests.get(LINK)

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.title)

figures = soup.find_all("figure", class_=re.compile(r"^GallerySlideFigure"))

parks = []

for figure in figures:
    park = figure.find("h2").get_text(strip=True)

    paragraph = figure.find("figcaption").find("p")
    children = list(paragraph.children)

    name = children[1].strip()
    hike_len = " ".join(children[3].split()[1:]).strip()
    hike_difficuty = children[5].split()[-1].strip()

    parks.append(park)
    print(park)
    print(name)
    print(hike_len)
    print(hike_difficuty)
    print()

print(parks)
# List of park names
parks = ["BigBend", "Yellowstone", "Yosemite", "GrandCanyon"]

def convert_to_camel_case(name):
    # Remove non-alphanumeric characters
    name = re.sub(r'[^A-Za-z0-9 ]+', '', name)
    # Split by spaces, capitalize each word, and join without spaces
    return ''.join(word.capitalize() for word in name.split())

camel_case_parks = [convert_to_camel_case(park) for park in parks]

# Add each park as an individual
for original_name, camel_case_name in zip(parks, camel_case_parks):
    xml_element = f"""
    <owl:NamedIndividual rdf:about="https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere-individuals/{camel_case_name}">
        <rdf:type rdf:resource="https://tw.rpi.edu/ontology-engineering/oe2024/when-to-go-where/WhenToGoWhere/NationalPark"/>
        <rdfs:label>{camel_case_name}</rdfs:label>
    </owl:NamedIndividual>
    """
    print(xml_element)