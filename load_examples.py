from graphe.core import *
from graphe.docx import *
import json

importer = GImporter()

document = importer.importDocument("examples/example1.graphe.xml")

print(document.title)
print(document.subtitle)
print(document.sections[0].subelements[0].subelements[0].text)
print(document.sections[0].subelements[1].subelements[0].text)

exporter = WordExporter()

exporter.exportDocument(document, "examples/example1.docx")
