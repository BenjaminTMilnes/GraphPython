from graph.core import *


class TextExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document, filePath):
        with open(filePath, "w") as fileObject:
            for section in document.sections:
                self.exportSection(section, document, fileObject)

    def exportSection(self, section, document, fileObject):
        self.exportElements(section.subelements, document, fileObject)

    def exportElements(self, elements, document, fileObject, allowLineBreaks = True, indentation = 0):
        for element in elements:
            self.exportElement(element, document, fileObject, allowLineBreaks, indentation)
    
    def exportElement(self, element, document, fileObject, allowLineBreaks = True, indentation = 0):
        if isinstance(element, GTextElement):
            fileObject.write(element.text)
        if isinstance(element, GParagraph):
            fileObject.write("\n")
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks, indentation)
            fileObject.write("\n")
        if isinstance(element, GHeading):
            fileObject.write("\n")
            self.exportElements(element.subelements, document, fileObject, False, indentation)
            fileObject.write("\n")
        if isinstance(element, GBold):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks, indentation)
        if isinstance(element, GItalic):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks, indentation)
        if isinstance(element, GUnderline):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks, indentation)
        if isinstance(element, GStrikethrough):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks, indentation)
        if isinstance(element, GLineBreak):
            if allowLineBreaks:
                fileObject.write("\n")
            else:
                fileObject.write("")
        if isinstance(element, GVariable):
            fileObject.write(document.getValueOfVariable(element.name))
        if isinstance(element, GUnorderedList):
            n = 1

            fileObject.write("\n")
            for subelement in element.subelements:
                if isinstance(subelement, GListItem):
                    if n > 1:
                        fileObject.write("\n")

                    fileObject.write("{}- ".format("    " * indentation))
                    self.exportElements(subelement.subelements, document, fileObject, allowLineBreaks, indentation + 1)
            
                    n += 1

            if indentation == 0:
                fileObject.write("\n")

        if isinstance(element, GOrderedList):
            n = 1

            fileObject.write("\n")
            for subelement in element.subelements:
                if isinstance(subelement, GListItem):
                    if n > 1:
                        fileObject.write("\n")

                    fileObject.write("{}{}. ".format("    " * indentation, n))
                    self.exportElements(subelement.subelements, document, fileObject, allowLineBreaks, indentation + 1)
                    
                    n += 1

            if indentation == 0:
                fileObject.write("\n")
                
        if isinstance(element, GHyperlink):
            self.exportElements(element.subelements, document, fileObject, allowLineBreaks, indentation)
        if isinstance(element, GHorizontalRule):
            fileObject.write("\n")
            fileObject.write("-" * 40)
            fileObject.write("\n")