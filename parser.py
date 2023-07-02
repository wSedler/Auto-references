from ctypes.wintypes import LCID
from nameparser import HumanName
import xml.etree.ElementTree as ET
import re

with open("C:\\Users\super\AppData\Roaming\Microsoft\Bibliography\Sources.xml", 'r', encoding="utf8") as f:
    data = f.read()

header_artical = """Synthesis of Quinol ines, 2-Quinolones, Phenanthridines, and 6(5
H)-Phenanthridinones via Palladium[0]-Mediated Ullmann
Cross-Coupling of 1-Bromo-2-nitroarenes with β-Halo-enals, -
enones, or -esters
By: Banwell, Martin G.; Lupton, David W.; Ma, Xinghua; Renner,
Jens; Sydnes, Magne O.
Organic Letters (2004), 6(16), 2741-2744.
"""


def parse(header_artical):
    pattern  = '([\S\n\t\v ]+)\nBy: ([\S\n\t\v ]+)\n(.+) (\(\d{4}\)), (.+), (\d+-?\d*)'
    groups = re.search(pattern, header_artical)
    title = groups.group(1)
    authors = groups.group(2)
    journal_name = groups.group(3)
    year = groups.group(4)
    issue = groups.group(5)
    pages = groups.group(6)

    title = re.sub('\n', ' ', re.sub('-\n', '-', title))
    authors = re.sub('\n', ' ', authors)
    authors = authors.split(';')

    return {'title': title, 'authors': authors, 'journal_name': journal_name, 'year': year, 'issue': issue, 'pages': pages}


def add_authors(authors, name_list):
    for author in authors:
        full_name = HumanName(author)
        person = ET.SubElement(name_list, "b:Person")
        last = ET.SubElement(person, "b:Last")
        last.text = full_name.last
        first = ET.SubElement(person, "b:First")
        first.text = full_name.first
        if full_name.middle != '':
            middle = ET.SubElement(person, "b:Middle")
            middle.text = full_name.middle

def get_teg(root):
    for node in root.iter():
        max_teg = 1
        if node == "b:Tag":
            gen_teg = re.search('tag(\d+)', node.text)
            if gen_teg:
                max_teg = max(max_teg, int(gen_teg.group(1)))
    
    return 'tag' + str(max_teg + 1)


def add_sourse(header_artical, data=data):
    elements = parse(header_artical)

    ET.register_namespace("b", "http://schemas.openxmlformats.org/officeDocument/2006/bibliography")
    root = ET.fromstring(data)
    source = ET.Element("b:Source")
    root.append(source)
    tag = ET.SubElement(source, "b:Tag")
    tag.text = get_teg(root)
    source_type = ET.SubElement(source, "b:SourceType")
    source_type.text = "JournalArticle"
    authors = ET.SubElement(source, "b:Author")
    spec = ET.SubElement(authors, "b:Author")
    name_list = ET.SubElement(spec, "b:NameList")
    # Insert authors into the list of names
    add_authors(elements['authors'], name_list)
    
    title = ET.SubElement(source, "b:Title")
    title.text = elements['title']
    journal_name = ET.SubElement(source, "b:JournalName")
    journal_name.text = elements['journal_name']
    year = ET.SubElement(source, "b:Year")
    year.text = elements['year']
    pages = ET.SubElement(source, "b:Pages")
    pages.text = elements['pages']
    #volume = ET.SubElement(source, "b:Volume")
    #volume.text = "6(16)"
    issue = ET.SubElement(source, "b:Issue")
    issue.text = elements['issue']
    lcid = ET.SubElement(source, "b:LCID")
    lcid.text = "1033"

    tree = ET.ElementTree(root)

    tree.write("C:\\Users\super\AppData\Roaming\Microsoft\Bibliography\Sources_test.xml", "utf-8", True)







