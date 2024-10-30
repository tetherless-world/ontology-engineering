from bs4 import BeautifulSoup
import requests
import re


LINK = "https://www.cntraveler.com/gallery/the-best-hike-in-every-national-park"

response = requests.get(LINK)

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.title)

figures = soup.find_all("figure", class_=re.compile(r"^GallerySlideFigure"))

for figure in figures:
    park = figure.find("h2").get_text(strip=True)

    paragraph = figure.find("figcaption").find("p")
    children = list(paragraph.children)

    name = children[1].strip()
    hike_len = " ".join(children[3].split()[1:]).strip()
    hike_difficuty = children[5].split()[-1].strip()

    print(park)
    print(name)
    print(hike_len)
    print(hike_difficuty)
    print()