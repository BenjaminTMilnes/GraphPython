from graphe.core import *
from graphe.docx import *
import json

importer = GImporter()

document = importer.importDocument("examples/example1.graphe.xml")

print(document.title)
print(document.subtitle)

exporter = WordExporter()

exporter.exportDocument(document, "examples/example1.docx")
