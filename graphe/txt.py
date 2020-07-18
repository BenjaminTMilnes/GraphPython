from graphe.core import *


class TextExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document, filePath):

        with open(filePath, "w") as fileObject:

            for section in document.sections:
                self.exportSection(section, document, fileObject)

    def exportSection(self, section, document, fileObject):
        self.exportElements(section.subelements, document, fileObject)

    def exportElements(self, elements, document, fileObject, allowLineBreaks = True):
        for element in elements:
            self.exportElement(element, document, fileObject, allowLineBreaks)
    
    def exportElement(self, element, document, fileObject, allowLineBreaks = True):
        if isinstance(element, GTextElement):
            fileObject.write(element.text)
        if isinstance(element, GParagraph):
            fileObject.write("\n")
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks)
            fileObject.write("\n")
        if isinstance(element, GHeading):
            fileObject.write("\n")
            self.exportElements(element.subelements, document, fileObject, False)
            fileObject.write("\n")
        if isinstance(element, GBold):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks)
        if isinstance(element, GItalic):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks)
        if isinstance(element, GUnderline):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks)
        if isinstance(element, GStrikethrough):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks)
        if isinstance(element, GLineBreak):
            if allowLineBreaks:
                fileObject.write("\n")
            else:
                fileObject.write("")
        if isinstance(element, GVariable):
            fileObject.write(document.getValueOfVariable(element.name))
        if isinstance(element, GUnorderedList):
            fileObject.write("\n")
            for subelement in element.subelements:
                if isinstance(subelement, GListItem):
                    fileObject.write("- ")
                    self.exportElements(subelement.subelements, document, fileObject, allowLineBreaks)
                    fileObject.write("\n")
        if isinstance(element, GOrderedList):
            n = 1

            fileObject.write("\n")
            for subelement in element.subelements:
                if isinstance(subelement, GListItem):
                    fileObject.write("{}. ".format(n))
                    self.exportElements(subelement.subelements, document, fileObject, allowLineBreaks)
                    fileObject.write("\n")

                    n += 1
                
        if isinstance(element, GHyperlink):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks)