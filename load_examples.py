from graphe.core import *
from graphe.docx import *
from morphe.core import *
import json
import logging

logging.basicConfig(level=logging.INFO)

importer = GImporter()
resolver = StyleResolver()

document = importer.importDocument("examples/example1.graphe.xml")
morpheDocument = importMorpheDocumentFromFile("examples/example1.morphe")

print(document.title)
print(document.subtitle)

print(len(morpheDocument.styleRules))

resolver.applyMorpheDocumentToGrapheDocument(morpheDocument, document)

exporter = WordExporter()

exporter.exportDocument(document, "examples/example1.docx")
