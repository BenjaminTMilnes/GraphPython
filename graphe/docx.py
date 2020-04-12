from graphe.core import *
from docx import Document
from docx.shared import Pt, Mm, Cm, Inches, RGBColor
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

alignments = {
    "justified": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "left-justified": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "right-justified": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "centre-justified": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "center-justified": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "centred": WD_ALIGN_PARAGRAPH.CENTER,
    "centered": WD_ALIGN_PARAGRAPH.CENTER,
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
}


class WordExportContext(object):
    def __init__(self, dx):

        self.dx = dx

        self.n = 0
        self.currentSection = self.dx.sections[0]
        self.currentParagraph = None
        self.currentRun = None

    def addSection(self, pageWidth, pageHeight, topMargin, rightMargin, bottomMargin, leftMargin):
        if self.n > 0:
            self.currentSection = self.dx.add_section(WD_SECTION.NEW_PAGE)

        self.n = 1

        self.currentSection.page_width = pageWidth
        self.currentSection.page_height = pageHeight
        self.currentSection.top_margin = topMargin
        self.currentSection.right_margin = rightMargin
        self.currentSection.bottom_margin = bottomMargin
        self.currentSection.left_margin = leftMargin

    def addHeading(self, level, textAlignment="left"):
        self.currentParagraph = self.dx.add_paragraph("")
        self.currentParagraph.alignment = alignments.get(textAlignment, WD_ALIGN_PARAGRAPH.LEFT)

        return

        if level > 9:
            level = 9
        if level < 1:
            level = 1
        self.currentParagraph = self.dx.add_heading("", level)

    def addParagraph(self, textAlignment="left"):
        self.currentParagraph = self.dx.add_paragraph("")
        self.currentParagraph.alignment = alignments.get(textAlignment, WD_ALIGN_PARAGRAPH.LEFT)

    def addRun(self, text, fontName="Times New Roman", fontHeight=12, bold=False, italic=False, underline=False, strikethrough=False, fontVariant="none"):
        self.currentRun = self.currentParagraph.add_run(text)
        self.currentRun.font.name = fontName
        self.currentRun.font.size = Pt(fontHeight)
        self.currentRun.font.bold = bold
        self.currentRun.font.italic = italic
        self.currentRun.font.underline = underline
        self.currentRun.font.strike = strikethrough
        self.currentRun.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        self.currentRun.font.small_caps = True if fontVariant in ["small-capitals", "small-caps"] else False

    def addLineBreak(self):
        self.currentRun.add_break()


class WordExporter(object):
    def __init__(self):
        pass

    def _getLength(self, length):
        if length.unit.value == "mm":
            return Mm(float(length.number.value))
        if length.unit.value == "cm":
            return Cm(float(length.number.value))
        if length.unit.value == "dm":
            return Cm(float(length.number.value) * 10)
        if length.unit.value == "m":
            return Cm(float(length.number.value) * 100)
        if length.unit.value == "pt":
            return Pt(float(length.number.value))
        if length.unit.value == "in":
            return Inches(float(length.number.value))

    def exportDocument(self, document, filePath):

        dx = Document()
        context = WordExportContext(dx)

        for section in document.sections:
            self.exportSection(section, document, context)

        dx.save(filePath)

    def exportSection(self, section, document, context):
        pageWidth = self._getLength(section.styleProperties.get("page-width"))
        pageHeight = self._getLength(section.styleProperties.get("page-height"))
        marginTop = self._getLength(section.styleProperties.get("margin-top"))
        marginRight = self._getLength(section.styleProperties.get("margin-right"))
        marginBottom = self._getLength(section.styleProperties.get("margin-bottom"))
        marginLeft = self._getLength(section.styleProperties.get("margin-left"))

        context.addSection(pageWidth, pageHeight, marginTop, marginRight, marginBottom, marginLeft)
        self.exportPageElements(section.subelements, document, context)

    def exportPageElements(self, pageElements, document, context):
        for pageElement in pageElements:
            self.exportPageElement(pageElement, document, context)

    def exportPageElement(self, pageElement, document, context):
        if isinstance(pageElement, GParagraph):
            textAlignment = pageElement.styleProperties.get("text-alignment", "left")

            context.addParagraph(textAlignment)
            self.exportPageElements(pageElement.subelements, document, context)
        if isinstance(pageElement, GHeading):
            textAlignment = pageElement.styleProperties.get("text-alignment", "left")

            context.addHeading(pageElement.level, textAlignment)
            self.exportPageElements(pageElement.subelements, document, context)
        if isinstance(pageElement, GDivision):
            textAlignment = pageElement.styleProperties.get("text-alignment", "left")

            context.addParagraph(textAlignment)
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
            fontName = pageElement.styleProperties.get("font-name", "Times New Roman")
            fontVariant = pageElement.styleProperties.get("font-variant", "none")
            #fontHeight = float(pageElement.styleProperties.get("font-height", 12).number.value)

            context.addRun(pageElement.text, fontName, 12, False, False, False, False, fontVariant)
        if isinstance(pageElement, GLineBreak):
            context.addLineBreak()
