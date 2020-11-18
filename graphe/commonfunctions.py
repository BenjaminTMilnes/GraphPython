from morphe.core import *
from graphe.core import *
from graphe.docx import *
from graphe.latex import *
from graphe.md import *
from graphe.txt import *
from graphe.html import *
import logging

def compileGrapheDocument(grapheFilePath, morpheFilePath, outputFilePath, outputFormat = "docx"):
    importer = GImporter()
    styleResolver = StyleResolver()

    logging.info("Importing Graphe document.")
    grapheDocument = importer.importDocument(grapheFilePath)

    logging.info("Importing Morphe document.")
    morpheDocument = importMorpheDocumentFromFile(morpheFilePath)

    logging.info("Applying Morphe style to Graphe document.")
    styleResolver.applyMorpheDocumentToGrapheDocument(morpheDocument, grapheDocument)

    if outputFormat == "docx":
        exporter = WordExporter()
        logging.info("Exporting document as a Word (.docx) file to {}.".format(outputFilePath))
        exporter.exportDocument(grapheDocument, outputFilePath)
    if outputFormat == "latex":
        exporter = LaTeXExporter()
        logging.info("Exporting document as a LaTeX (.tex) file to {}.".format(outputFilePath))
        exporter.exportDocument(grapheDocument, outputFilePath)
    if outputFormat == "md":
        exporter = MarkdownExporter()
        logging.info("Exporting document as a Markdown (.md) file to {}.".format(outputFilePath))
        exporter.exportDocument(grapheDocument, outputFilePath)
    if outputFormat == "txt":
        exporter = TextExporter()
        logging.info("Exporting document as a plain text (.txt) file to {}.".format(outputFilePath))
        exporter.exportDocument(grapheDocument, outputFilePath)
    if outputFormat == "html":
        exporter = HTMLExporter()
        logging.info("Exporting document as a HTML (.html) file to {}.".format(outputFilePath))
        exporter.exportDocument(grapheDocument, outputFilePath)

