from graphe.core import *


class LaTeXDocument(object):
    def __init__(self):
        self.subelements = []


class LaTeXTextElement(object):
    def __init__(self, text=""):
        self.text = text


class LaTeXParagraph(object):
    def __init__(self):
        self.subelements = []


class LaTeXNewLineCommand(object):
    def __init__(self):
        pass


class LaTeXCommand(object):
    def __init__(self, name, parameterAsSubelement=""):
        self.name = name
        self.orderedParameters = []
        self.namedParameters = {}
        self.parameterAsSubelement = parameterAsSubelement
        self.subelements = []
        self.newLineBefore = False
        self.newLineAfter = False

    def setText(self, text):
        self.subelements = [LaTeXTextElement(text)]


class LaTeXItalicCommand(LaTeXCommand):
    def __init__(self):
        super().__init__("textit")


class LaTeXBoldCommand(LaTeXCommand):
    def __init__(self):
        super().__init__("textbf")


class LaTeXDocumentClassCommand(LaTeXCommand):
    def __init__(self, documentClass="book"):
        super().__init__("documentclass", documentClass)

        self.newLineAfter = True


class LaTeXTitleCommand(LaTeXCommand):
    def __init__(self, text=""):
        super().__init__("title")

        self.newLineBefore = True
        self.newLineAfter = True

        self.setText(text)


class LaTeXAuthorCommand(LaTeXCommand):
    def __init__(self, text=""):
        super().__init__("author")

        self.newLineBefore = True
        self.newLineAfter = True

        self.setText(text)


class LaTeXSectionCommand(LaTeXCommand):
    def __init__(self, text=""):
        super().__init__("section")

        self.withoutNumbering = True

        self.newLineBefore = True
        self.newLineAfter = True

        self.setText(text)


class LaTeXChapterCommand(LaTeXCommand):
    def __init__(self, text=""):
        super().__init__("chapter")

        self.withoutNumbering = True

        self.newLineBefore = True
        self.newLineAfter = True

        self.setText(text)


class LaTeXEnvironment(object):
    def __init__(self, environmentName):
        self.environmentName = environmentName
        self.subelements = []

    def getBeginCommand(self):
        return LaTeXCommand("begin", self.environmentName)

    def getEndCommand(self):
        return LaTeXCommand("end", self.environmentName)


class LaTeXWriter(object):
    def __init__(self):
        pass

    def writeDocument(self, filePath, document):
        with open(filePath, "w") as fileObject:
            self._writeElements(fileObject, document.subelements)

    def _writeElements(self, fileObject, elements):
        for element in elements:
            self._writeElement(fileObject, element)

    def _writeElement(self, fileObject, element):
        if isinstance(element, LaTeXTextElement):
            fileObject.write("{0}".format(element.text))
        elif isinstance(element, LaTeXParagraph):
            fileObject.write("\n")
            self._writeElements(fileObject, element.subelements)
            fileObject.write("\n")
        elif isinstance(element, LaTeXNewLineCommand):
            fileObject.write(" \\\\ ")
        elif isinstance(element, LaTeXCommand):
            if element.newLineBefore:
                fileObject.write("\n")

            fileObject.write("\{0}".format(element.name))

            if element.name in ["chapter", "section", "subsection"] and element.withoutNumbering == True:
                fileObject.write("*")

            if len(element.orderedParameters) > 0 or len(element.namedParameters) > 0:
                fileObject.write("[")
                n = 0

                for p in element.orderedParameters:
                    if n > 0:
                        fileObject.write(",")

                    fileObject.write("{0}".format(p))
                    n += 1

                for p in element.namedParameters:
                    v = element.namedParameters[p]

                    if n > 0:
                        fileObject.write(",")

                    fileObject.write("{0}={1}".format(p, v))
                    n += 1

                fileObject.write("]")

            if element.parameterAsSubelement != "":
                fileObject.write("{")
                fileObject.write("{0}".format(element.parameterAsSubelement))
                fileObject.write("}")
            elif len(element.subelements) > 0:
                fileObject.write("{")
                self._writeElements(fileObject, element.subelements)
                fileObject.write("}")

            if element.newLineAfter:
                fileObject.write("\n")

        elif isinstance(element, LaTeXEnvironment):
            self._writeElement(fileObject,  element.getBeginCommand())
            fileObject.write("\n")
            self._writeElements(fileObject, element.subelements)
            fileObject.write("\n")
            self._writeElement(fileObject, element.getEndCommand())


class LaTeXExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document, filePath):

        latexDocument = LaTeXDocument()

        latexDocument.subelements.append(LaTeXDocumentClassCommand())

        encoding = LaTeXCommand("usepackage", "inputenc")
        encoding.orderedParameters.append("utf8")
        encoding.newLineAfter = True

        geometry = LaTeXCommand("usepackage", "geometry")
        geometry.namedParameters["paperwidth"] = str(document.sections[0].styleProperties.get("page-width"))
        geometry.namedParameters["paperheight"] = str(document.sections[0].styleProperties.get("page-height"))
        geometry.namedParameters["top"] = str(document.sections[0].styleProperties.get("margin-top"))
        geometry.namedParameters["bottom"] = str(document.sections[0].styleProperties.get("margin-bottom"))
        geometry.namedParameters["left"] = str(document.sections[0].styleProperties.get("margin-left"))
        geometry.namedParameters["right"] = str(document.sections[0].styleProperties.get("margin-right"))
        geometry.newLineAfter = True

        ebgaramond = LaTeXCommand("usepackage", "ebgaramond")
        ebgaramond.newLineAfter = True

        latexDocument.subelements.append(encoding)
        latexDocument.subelements.append(geometry)
        latexDocument.subelements.append(ebgaramond)

        title = LaTeXTitleCommand(document.title)
        author = LaTeXAuthorCommand(self.getAuthorsList(document))

        latexDocument.subelements.append(title)
        latexDocument.subelements.append(author)

        documentEnvironment = LaTeXEnvironment("document")

        latexDocument.subelements.append(documentEnvironment)

        n = 0

        for section in document.sections:
            if n > 0:
                newpage = LaTeXCommand("newpage")
                newpage.newLineBefore = True
                newpage.newLineAfter = True

                documentEnvironment.subelements.append(newpage)

            self.exportSection(section, document, documentEnvironment)

            n += 1

        latexWriter = LaTeXWriter()
        latexWriter.writeDocument(filePath, latexDocument)

    def exportSection(self, section, document, documentEnvironment):
        if False:
            if len(section.subelements) > 0 and isinstance(section.subelements[0], GHeading):
                sectionHeading = section.subelements[0]
                subelements = section.subelements[1:]
            else:
                sectionHeading = None
                subelements = section.subelements

            s = LaTeXChapterCommand()

            if sectionHeading != None:
                self.exportInlineElements(sectionHeading, s)

            documentEnvironment.subelements.append(s)
        else:
            subelements = section.subelements

        for element in subelements:
            if isinstance(element, GHeading):
                h = LaTeXParagraph()

                self.exportInlineElements(element, document, h)

                documentEnvironment.subelements.append(h)
            if isinstance(element, GParagraph):
                p = LaTeXParagraph()

                self.exportInlineElements(element, document, p)

                if element.styleProperties.get("text-alignment") == "centred":
                    documentEnvironment.subelements.append(LaTeXCommand("centering"))

                documentEnvironment.subelements.append(p)

    def exportInlineElements(self, gElement, gDocument, latexElement):

        for subelement in gElement.subelements:
            if isinstance(subelement, GTextElement):
                t = LaTeXTextElement(subelement.text)

                latexElement.subelements.append(t)
            if isinstance(subelement, GVariable):
                t = LaTeXTextElement(gDocument.getValueOfVariable(subelement.name))

                latexElement.subelements.append(t)
            if isinstance(subelement, GItalic):
                i = LaTeXItalicCommand()
                self.exportInlineElements(subelement, gDocument, i)

                latexElement.subelements.append(i)
            if isinstance(subelement, GBold):
                b = LaTeXBoldCommand()
                self.exportInlineElements(subelement, gDocument, b)

                latexElement.subelements.append(b)
            if isinstance(subelement, GLineBreak):
                latexElement.subelements.append(LaTeXNewLineCommand())

    def getAuthorsList(self, document):

        authors = [c.name for c in document.contributors if c.type == "author"]

        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return "{0} and {1}".format(authors[0], authors[1])
        elif len(authors) > 2:
            return "{0}, and {1}".format(", ".join(authors[:-1]), authors[-1])
        else:
            return ""
