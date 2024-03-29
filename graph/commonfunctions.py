from morph.core import *
from graph.core import *
from graph.docx import *
from graph.latex import *
from graph.md import *
from graph.txt import *
from graph.html import *
from graph.pdf import *
import logging

def compileGraphDocument(graphFilePath, morphFilePath, outputFilePath, outputFormat = "docx"):
    importer = GImporter()
    styleResolver = StyleResolver()

    logging.info("Importing Graph document.")
    graphDocument = importer.importDocument(graphFilePath)

    logging.info("Importing Morph document.")
    morphDocument = importMorphDocumentFromFile(morphFilePath)

    logging.info("Applying Morph style to Graph document.")
    styleResolver.applyMorphDocumentToGraphDocument(morphDocument, graphDocument)

    if outputFormat == "docx":
        exporter = WordExporter()
        logging.info("Exporting document as a Word (.docx) file to {}.".format(outputFilePath))
        exporter.exportDocument(graphDocument, outputFilePath)
    if outputFormat == "latex":
        exporter = LaTeXExporter()
        logging.info("Exporting document as a LaTeX (.tex) file to {}.".format(outputFilePath))
        exporter.exportDocument(graphDocument, outputFilePath)
    if outputFormat == "md":
        exporter = MarkdownExporter()
        logging.info("Exporting document as a Markdown (.md) file to {}.".format(outputFilePath))
        exporter.exportDocument(graphDocument, outputFilePath)
    if outputFormat == "txt":
        exporter = TextExporter()
        logging.info("Exporting document as a plain text (.txt) file to {}.".format(outputFilePath))
        exporter.exportDocument(graphDocument, outputFilePath)
    if outputFormat == "html":
        exporter = HTMLExporter()
        logging.info("Exporting document as a HTML (.html) file to {}.".format(outputFilePath))
        exporter.exportDocument(graphDocument, outputFilePath)