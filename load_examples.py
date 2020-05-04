from graphe.core import *
from graphe.docx import *
from graphe.latex import *
from graphe.md import *
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

exporter = LaTeXExporter()
exporter.exportDocument(document, "examples/example1.tex")

markdownExporter = MarkdownExporter()
markdownExporter.exportDocument(document, "examples/example1.md")

#exporter = WordExporter()

#exporter.exportDocument(document, "examples/example1.docx")
