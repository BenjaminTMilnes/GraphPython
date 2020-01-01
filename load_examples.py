from graphe.core import *
import json

importer = GImporter()

document = importer.importDocument("examples/example1.graphe.xml")

print(document.title)
print(document.subtitle)
