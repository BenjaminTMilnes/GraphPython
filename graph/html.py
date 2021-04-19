from graph.core import *
from graph.xml import *


class HTMLExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document, filePath):
        with open(filePath, "w") as fileObject:
            html = XMLElement("html")

            html.setLineBreaks(False, False, True, False)

            head = XMLElement("head")
            head.setLineBreaks(True, False, True, False)

            body = XMLElement("body")
            body.setLineBreaks(True, False, True, False)

            title = XMLElement("title")
            title.setLineBreaks(True, False, False, False)
            title.subelements.append(XMLTextElement("{} by {}".format( document.title, document.authorName)))

            link1 = XMLElement("link")
            link1.setAttributeValue("href", "style.css")
            link1.setAttributeValue("type", "text/css")
            link1.setAttributeValue("rel", "stylesheet")
            link1.isSelfClosing = True

            meta1 = XMLElement("meta")
            meta1.setAttributeValue("charset", "utf-8")
            meta1.isSelfClosing = True

            meta2 = XMLElement("meta")
            meta2.setAttributeValue("name", "viewport")
            meta2.setAttributeValue("content", "width=device-width, user-scalable=no")
            meta2.isSelfClosing = True
            
            html.subelements.append(head)
            html.subelements.append(body)

            head.subelements.append(title)
            head.subelements.append(link1)
            head.subelements.append(meta1)
            head.subelements.append(meta2)

            htmlDocument = XMLDocument(HTML5Declaration(), html)

            for section in document.sections:
                self.exportSection(section, document, body, htmlDocument)

            xmlExporter = XMLExporter()

            t = xmlExporter.exportDocument(htmlDocument)

            fileObject.write(t)

    def exportSection(self, section, document, htmlElement, htmlDocument):
        s = XMLElement("section")
        s.setLineBreaks(True, False, False, False)
        self.exportElements(section.subelements, document, s, htmlDocument)
        htmlElement.subelements.append(s)

    def exportElements(self, elements, document, htmlElement, htmlDocument):
        for element in elements:
            self.exportElement(element, document, htmlElement, htmlDocument)
            
    def exportElement(self, element, document, htmlElement, htmlDocument):
        if isinstance(element, GParagraph):
            e = XMLElement("p")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GDivision):
            e = XMLElement("span")
            e.setLineBreaks(False, False, False, False)
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GHeading):
            l = element.level if element.level <= 6 else 6
            e = XMLElement("h{}".format(l))
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GItalic):
            e = XMLElement("em")
            e.setLineBreaks(False, False, False, False)
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GBold):
            e = XMLElement("b")
            e.setLineBreaks(False, False, False, False)
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GUnderline):
            e = XMLElement("span")
            e.setAttributeValue("style", "text-decoration: underline;")
            e.setLineBreaks(False, False, False, False)
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GStrikethrough):
            e = XMLElement("s")
            e.setLineBreaks(False, False, False, False)
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GHyperlink):
            e = XMLElement("a")
            e.setAttributeValue("href", element.url)
            e.setAttributeValue("title", element.title)
            e.setLineBreaks(False, False, False, False)
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GLineBreak):
            e = XMLElement("br")
            e.isSelfClosing = True
            htmlElement.subelements.append(e)

        if isinstance(element, GHorizontalRule):
            e = XMLElement("hr")
            e.isSelfClosing = True
            htmlElement.subelements.append(e)

        if isinstance(element, GUnorderedList):
            e = XMLElement("ul")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GOrderedList):
            e = XMLElement("ol")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GListItem):
            e = XMLElement("li")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GDefinitionList):
            e = XMLElement("dl")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GDefinitionListTerm):
            e = XMLElement("dt")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GDefinitionListDefinition):
            e = XMLElement("dd")
            self.exportElements(element.subelements, document, e, htmlDocument)
            htmlElement.subelements.append(e)

        if isinstance(element, GTextElement):
            t = XMLTextElement(element.text)
            htmlElement.subelements.append(t)
