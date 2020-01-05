from datetime import datetime
import xml.etree.ElementTree as et
import re
from graphe.xml import *


class GContributor(object):
    def __init__(self):

        self.name = ""
        self.type = ""
        self.emailAddress = ""
        self.address = ""
        self.website = ""


class GTextElement(object):
    def __init__(self, text=""):

        self.text = text


class GContentElement(object):
    _elementNames = []

    def __init__(self):

        self.subelements = []

        self.id = ""
        self.styleClass = ""
        self.style = ""
        self.language = ""


class GParagraph(GContentElement):
    _elementNames = ["paragraph", "p"]


class GHeading(GContentElement):
    _elementNames = ["heading1", "heading2", "heading3", "heading4", "heading5", "heading6", "heading7", "heading8", "heading9", "heading10", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10"]
    _levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self, level=1):
        super(GHeading, self).__init__()

        self.level = level


class GDivision (GContentElement):
    _elementNames = ["division", "d"]


class GBold(GContentElement):
    _elementNames = ["bold", "b"]


class GItalic(GContentElement):
    _elementNames = ["italic", "i"]


class GUnderline(GContentElement):
    _elementNames = ["underline", "u"]


class GStrikethrough(GContentElement):
    _elementNames = ["strikethrough", "s"]


class GHyperlink(GContentElement):

    _elementNames = ["hyperlink", "hl"]

    def __init__(self):
        super(GHyperlink, self).__init__()

        self.url = ""
        self.title = ""


class GLineBreak(GContentElement):
    _elementNames = ["line-break", "lb"]


class GPageBreak(GContentElement):
    _elementNames = ["page-break", "pb"]


class GUnorderedList(GContentElement):
    _elementNames = ["unordered-list", "ul"]


class GOrderedList(GContentElement):
    _elementNames = ["ordered-list", "ol"]


class GListItem(GContentElement):
    _elementNames = ["list-item", "li"]


class GVariable(GContentElement):
    _elementNames = ["variable", "v"]

    def __init__(self):
        self.name = ""


class GTableOfContents(GContentElement):
    _elementNames = ["table-of-contents", "toc"]


class GCitation(GContentElement):
    _elementNames = ["citation", "c"]

    def __init__(self):
        super(GCitation, self).__init__()

        self.reference = ""


class GTemplate(GContentElement):
    def __init__(self):
        super(GContentElement, self).__init__()

        self.reference = ""


class GPageTemplate(GTemplate):
    def __init__(self):
        super(GPageTemplate, self).__init__()


class GSection(GContentElement):
    _elementNames = ["section"]

    def __init__(self):
        super(GSection, self).__init__()

        self.document = None

        self.pageTemplateReference = ""

    @property
    def pageTemplate(self):
        if self.document != None:
            return [pt for pt in self.document.templates if pt.reference == self.pageTemplateReference][0]
        else:
            return None


class GDocument(object):
    def __init__(self):
        self.version = ""
        self.title = ""
        self.subtitle = ""
        self.abstract = ""
        self.keywords = []
        self.contributors = []
        self.publicationDate = datetime.now()
        self.templates = []
        self.sections = []

    @property
    def authorName(self):
        a = [c for c in self.contributors if c.type == "author"]

        if len(a) > 0:
            return a[0].name
        else:
            return ""


class GrapheValidationError (Exception):
    def __init__(self, message):
        super(GrapheValidationError, self).__init__(message)


class GImporter(object):
    def __init__(self):

        self.allowedDocumentVersions = ["0.1"]

    def importDocument(self, filePath):
        xmlParser = XMLParser()

        root = xmlParser.parseFromFile(filePath).root

        document = GDocument()

        self._importMetadata(root, document)
        self._importSections(root, document)

        return document

    def _importMetadata(self, root, document):

        if root.name != "document":
            raise GrapheValidationError("The root element in a Graphe document file must be a <document> element.")

        if not root.hasAttribute("version"):
            raise GrapheValidationError("The <document> element must have a 'version' attribute.")

        version = root.getAttributeValue("version")

        if version not in self.allowedDocumentVersions:
            raise GrapheValidationError("'{0}' is not a valid Graphe version.".format(version))

        document.version = version

        title = root.getFirstElementWithName("title")
        subtitle = root.getFirstElementWithName("subtitle")
        abstract = root.getFirstElementWithName("abstract")
        keywords = root.getFirstElementWithName("keywords")

        if title == None:
            raise GrapheValidationError("A Graphe document must have a title.")

        document.title = title.innerText.strip()

        if subtitle != None:
            document.subtitle = subtitle.innerText.strip()

        if abstract != None:
            document.abstract = abstract.innerText.strip()

        if keywords != None:
            document.keywords = [k.strip() for k in keywords.innerText.split(",")]

        contributors = root.getFirstElementWithName("contributors").getElementsByName("contributor")

        for contributor in contributors:
            c = GContributor()

            if contributor.hasAttribute("type"):
                t = contributor.getAttributeValue("type")

                if t.lower() in ["author", "editor"]:
                    c.type = t.lower()
                else:
                    raise GrapheValidationError("'{0}' is not a valid Graphe contributor type.".format(t))

            name = contributor.getFirstElementWithName("name")
            emailAddress = contributor.getFirstElementWithName("email-address")
            address = contributor.getFirstElementWithName("address")
            website = contributor.getFirstElementWithName("website")

            if name != None:
                c.name = name.innerText.strip()

            if emailAddress != None:
                c.emailAddress = emailAddress.innerText.strip()

            if address != None:
                c.address = address.innerText.strip()

            if website != None:
                c.website = website.innerText.strip()

            document.contributors.append(c)

    def _importSections(self, root, document):

        sections = root.getFirstElementWithName("sections", False).getElementsByName("section", False)

        for section in sections:
            s = GSection()

            s.document = document
            s.subelements = self._getPageElementsFromXML(section.subelements)

            document.sections.append(s)

    def _getPageElementsFromXML(self, xmlElements):
        return [self._getPageElementFromXML(e) for e in xmlElements]

    def _getPageElementFromXML(self, xmlElement):

        if isinstance(xmlElement, XMLTextElement):
            return GTextElement(xmlElement.text)

        if xmlElement.name in GPageBreak._elementNames:
            return GPageBreak()
        if xmlElement.name in GLineBreak._elementNames:
            return GLineBreak()

        e = None

        if xmlElement.name in GHeading._elementNames:
            e = GHeading()
            i = GHeading._elementNames.index(xmlElement.name)
            e.level = GHeading._levels[i]
        if xmlElement.name in GParagraph._elementNames:
            e = GParagraph()
        if xmlElement.name in GDivision._elementNames:
            e = GDivision()
        if xmlElement.name in GBold._elementNames:
            e = GBold()
        if xmlElement.name in GItalic._elementNames:
            e = GItalic()
        if xmlElement.name in GUnderline._elementNames:
            e = GUnderline()
        if xmlElement.name in GStrikethrough._elementNames:
            e = GStrikethrough()
        if xmlElement.name in GOrderedList._elementNames:
            e = GOrderedList()
        if xmlElement.name in GUnorderedList._elementNames:
            e = GUnorderedList()
        if xmlElement.name in GListItem._elementNames:
            e = GListItem()
        if xmlElement.name in GHyperlink._elementNames:
            e = GHyperlink()
            e.url = xmlElement.getAttributeValue("url")
            e.title = xmlElement.getAttributeValue("title")
        if xmlElement.name in GVariable._elementNames:
            e = GVariable()
            e.name = xmlElement.getAttributeValue("name")
        if xmlElement.name in GTableOfContents._elementNames:
            e = GTableOfContents()
        if xmlElement.name in GCitation._elementNames:
            e = GCitation()
            e.reference = xmlElement.getAttributeValue("r")
            e.reference = xmlElement.getAttributeValue("reference")

        if e == None:
            raise GrapheValidationError("<{0}> is not a valid element type.".format(xmlElement.name))

        e.id = xmlElement.getAttributeValue("id")
        e.style = xmlElement.getAttributeValue("style")
        e.styleClass = xmlElement.getAttributeValue("style-class")
        e.language = xmlElement.getAttributeValue("l")
        e.language = xmlElement.getAttributeValue("language")

        e.subelements = self._getPageElementsFromXML(xmlElement.subelements)

        if (isinstance(e, GParagraph) or isinstance(e, GHeading) or isinstance(e, GDivision)) and len(e.subelements) > 0:
            fse = e.subelements[0]
            lse = e.subelements[-1]

            if isinstance(fse, GTextElement):
                fse.text = fse.text.lstrip()

            if isinstance(lse, GTextElement):
                lse.text = lse.text.rstrip()

        return e
