from graphe.core import *
from graphe.docx import *
from morphe.core import *
import json

importer = GImporter()
resolver = StyleResolver()

document = importer.importDocument("examples/example1.graphe.xml")
morpheDocument = importMorpheDocumentFromFile("examples/example1.morphe")

print(document.title)
print(document.subtitle)

print(len(morpheDocument.styleRules))

resolver.applyMorpheDocumentToGrapheDocument(morpheDocument, document)

print(document.sections[0].styleProperties)
print(document.sections[0].subelements[0].styleProperties)

exporter = WordExporter()

exporter.exportDocument(document, "examples/example1.docx")
