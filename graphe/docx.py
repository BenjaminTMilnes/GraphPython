from graphe.core import *
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.section import WD_SECTION
from datetime import datetime


class WordExportContext(object):
    def __init__(self, dx):

        self.dx = dx

        self.n = 0
        self.currentSection = self.dx.sections[0]
        self.currentParagraph = None
        self.currentRun = None

    def addSection(self, pageWidth, pageHeight, topMargin=25, rightMargin=25, bottomMargin=25, leftMargin=25):
        if self.n > 0:
            self.currentSection = self.dx.add_section(WD_SECTION.NEW_PAGE)

        self.n = 1

        self.currentSection.page_width = pageWidth
        self.currentSection.page_height = pageHeight
        self.currentSection.top_margin = Mm(topMargin)
        self.currentSection.right_margin = Mm(rightMargin)
        self.currentSection.bottom_margin = Mm(bottomMargin)
        self.currentSection.left_margin = Mm(leftMargin)

    def addHeading(self, level):
        self.currentParagraph = self.dx.add_paragraph("")

        return

        if level > 9:
            level = 9
        if level < 1:
            level = 1
        self.currentParagraph = self.dx.add_heading("", level)

    def addParagraph(self):
        self.currentParagraph = self.dx.add_paragraph("")

    def addRun(self, text, fontName="Times New Roman", fontHeight=12, bold=False, italic=False, underline=False, strikethrough=False):
        self.currentRun = self.currentParagraph.add_run(text)
        self.currentRun.font.name = fontName
        self.currentRun.font.size = Pt(fontHeight)
        self.currentRun.font.bold = bold
        self.currentRun.font.italic = italic
        self.currentRun.font.underline = underline
        self.currentRun.font.strike = strikethrough
        self.currentRun.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    def addLineBreak(self):
        self.currentRun.add_break()


class WordExporter(object):
    def __init__(self):
        pass

    def _getLength(self, length):
        if length.unit.value == "mm":
            return Mm(float( length.number.value))

    def exportDocument(self, document, filePath):

        dx = Document()
        context = WordExportContext(dx)

        for section in document.sections:
            self.exportSection(section, document, context)

        dx.save(filePath)

    def exportSection(self, section, document, context):
        pageWidth = self._getLength(section.styleProperties.get("page-size").lengths[0])
        pageHeight = self._getLength(section.styleProperties.get("page-size").lengths[1])
        context.addSection( pageWidth, pageHeight)
        self.exportPageElements(section.subelements, document, context)

    def exportPageElements(self, pageElements, document, context):
        for pageElement in pageElements:
            self.exportPageElement(pageElement, document, context)

    def exportPageElement(self, pageElement, document, context):
        if isinstance(pageElement, GParagraph):
            context.addParagraph()
            self.exportPageElements(pageElement.subelements, document, context)
        if isinstance(pageElement, GHeading):
            context.addHeading(pageElement.level)
            self.exportPageElements(pageElement.subelements, document, context)
        if isinstance(pageElement, GDivision):
            context.addParagraph()
            self.exportPageElements(pageElement.subelements, document, context)
        if isinstance(pageElement, GVariable):
            if pageElement.name == "title":
                context.addRun(document.title)
            if pageElement.name == "subtitle":
                context.addRun(document.subtitle)
            if pageElement.name == "authorName":
                context.addRun(document.authorName)
            if pageElement.name == "currentYear":
                context.addRun(str(datetime.now().year))
        if isinstance(pageElement, GHyperlink):
            self.exportPageElements(pageElement.subelements, document, context)
        if isinstance(pageElement, GTextElement):
            context.addRun(pageElement.text)
        if isinstance(pageElement, GLineBreak):
            context.addLineBreak()
