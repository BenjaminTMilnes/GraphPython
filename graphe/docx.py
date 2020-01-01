from graphe.core import *
from docx import Document


class WordExportContext(object):
    def __init__(self, dx):

        self.dx = dx

        self.currentParagraph = None

    def addParagraph(self):
        self.currentParagraph = self.dx.add_paragraph("")

    def addRun(self, text):
        self.currentParagraph.add_run(text)


class WordExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document, filePath):

        dx = Document()
        context = WordExportContext(dx)

        for section in document.sections:
            self.exportSection(section, context)

        dx.save(filePath)

    def exportSection(self, section, context):
        self.exportPageElements(section.subelements, context)

    def exportPageElements(self, pageElements, context):
        for pageElement in pageElements:
            self.exportPageElement(pageElement, context)

    def exportPageElement(self, pageElement, context):
        if isinstance(pageElement, GParagraph):
            context.addParagraph()
            self.exportPageElements(pageElement.subelements, context)
        if isinstance(pageElement, GTextElement):
            context.addRun(pageElement.text)
