from graphe.core import *


class MarkdownExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document, filePath):

        with open(filePath, "w") as fileObject:

            for section in document.sections:
                self.exportSection(section, fileObject)

    def exportSection(self, section, fileObject):
        self.exportElements(section.subelements, fileObject)

    def exportElements(self, elements, fileObject):
        for element in elements:
            self.exportElement(element, fileObject)
    
    def exportElement(self, element, fileObject):
        if isinstance(element, GParagraph):
            for e in element.subelements:
                if isinstance(e, GTextElement):
                    fileObject.write(e.text)

            fileObject.write("\n\n")
        if isinstance(element, GHeading):
            l = 6 if element.level > 6 else element.level
            fileObject.write("{0} ".format( "#" * l) )

            for e in element.subelements:
                if isinstance(e, GTextElement):
                    fileObject.write(e.text)

            fileObject.write("\n\n")