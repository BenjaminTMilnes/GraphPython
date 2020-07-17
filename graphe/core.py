from datetime import datetime
import xml.etree.ElementTree as et
import re
from graphe.xml import *
from morphe.core import *


class GContributor(object):
    """
    Represents a Graphe contributor.
    """

    def __init__(self):

        self.name = ""
        self.type = ""
        self.emailAddress = ""
        self.address = ""
        self.website = ""


class GTextElement(object):
    """
    Represents a Graphe text element. Text elements can have style properties, but these 
    are always inherited from the containing element.
    """

    def __init__(self, text=""):

        self.text = text

        self.styleProperties = {
            "font-name": "inherit",
            "font-weight": "inherit",
            "font-height": "inherit",
            "font-variant": "inherit",
            "font-slant": "inherit",
        }


class GContentElement(object):
    """
    Represents a Graphe content element. Content elements can contain other elements, 
    whether they are other content elements or text elements. Content elements can also
    have style rules applied to them, which may then be inherited by subelements.
    """

    _elementNames = []

    def __init__(self):

        self.subelements = []

        self.id = ""

        self.styleClass = ""
        self.style = ""

        self.styleProperties = {}

        self.language = ""

    @property
    def styleClassNames(self):
        cn = self.styleClass.split(" ")
        cn = [s for s in cn if re.match("[A-Za-z0-9_\-]+", s)]

        return cn


class GParagraph(GContentElement):
    """
    Represents a Graphe paragraph.
    """

    _elementNames = ["paragraph", "p"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


class GHeading(GContentElement):
    _elementNames = ["heading1", "heading2", "heading3", "heading4", "heading5", "heading6", "heading7", "heading8", "heading9", "heading10", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10"]
    _levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self, level=1):
        super(GHeading, self).__init__()

        self.level = level

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


class GDivision (GContentElement):
    _elementNames = ["division", "d"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


class GBold(GContentElement):
    _elementNames = ["bold", "b"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "bold",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


class GItalic(GContentElement):
    _elementNames = ["italic", "i"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "italic",
            "text-alignment": "inherit",
        }


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


class GDefinitionList(GContentElement):
    _elementNames = ["definition-list", "dl"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


class GDefinitionListTerm(GContentElement):
    _elementNames = ["definition-list-term", "dlt"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


class GDefinitionListDefinition(GContentElement):
    _elementNames = ["definition-list-definition", "dld"]

    def __init__(self):

        self.styleProperties = {
            "font-name": "inherit",
            "font-variant": "inherit",
            "font-height": "inherit",
            "font-weight": "inherit",
            "font-slant": "inherit",
            "text-alignment": "inherit",
        }


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

        self.header = None
        self.footer = None


class GHeader(GContentElement):
    def __init__(self):
        super(GContentElement, self).__init__()


class GFooter(GContentElement):
    def __init__(self):
        super(GContentElement, self).__init__()


class GSection(GContentElement):
    _elementNames = ["section"]

    def __init__(self):
        super(GSection, self).__init__()

        self.document = None

        self.pageTemplateReference = ""

    @property
    def pageTemplate(self):
        if self.document != None:
            pageTemplates = [pt for pt in self.document.templates if pt.reference == self.pageTemplateReference]

            if len(pageTemplates) > 0:
                return pageTemplates[0]
            else:
                return None
        else:
            return None


class GDocument(object):
    def __init__(self):
        self.version = ""
        self.title = ""
        self.subtitle = ""
        self.abstract = ""
        self.keywords = []
        self.draft = ""
        self.edition = ""
        self.isbn = ""
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


class GLength(object):
    def __init__(self, number, unit):
        if unit not in ["mm", "cm", "dm", "m", "in", "pt"]:
            raise ValueError("'{0}' is not a valid length unit.".format(unit))

        self.number = number
        self.unit = unit

    def __str__(self):
        return "{0}{1}".format(self.number, self.unit)

    def toMM(self):
        if self.unit == "mm":
            return self
        elif self.unit == "cm":
            return GLength(self.number * 10, "mm")
        elif self.unit == "dm":
            return GLength(self.number * 100, "mm")
        elif self.unit == "m":
            return GLength(self.number * 1000, "mm")
        elif self.unit == "in":
            return GLength(self.number * 25.4, "mm")
        elif self.unit == "pt":
            return GLength(self.number * 25.4 / 72, "mm")

    def toCM(self):
        n = self.toMM().number

        return GLength(n / 10, "cm")

    def toDM(self):
        n = self.toMM().number

        return GLength(n / 100, "dm")

    def toM(self):
        n = self.toMM().number

        return GLength(n / 1000, "m")

    def toInches(self):
        n = self.toMM().number

        return GLength(n / 25.4, "in")

    def toPoints(self):
        n = self.toMM().number

        return GLength(n * 72 / 25.4, "pt")


def makeGLength(mlength):
    return GLength(float(mlength.number.value), mlength.unit.value)


class GrapheValidationError (Exception):
    def __init__(self, message):
        super(GrapheValidationError, self).__init__(message)


class GImporter(object):
    def __init__(self):

        self.allowedDocumentVersions = ["0.1"]

    def _getAttributeValueOfSynonymousAttributes(self, element, attributeNames):

        value = ""

        for an in attributeNames:
            av = element.getAttributeValue(an)

            if av != "":
                value = av

        return value

    def importDocument(self, filePath):
        xmlParser = XMLParser()

        root = xmlParser.parseFromFile(filePath).root

        document = GDocument()

        self._importMetadata(root, document)
        self._importTemplates(root, document)
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
        draft = root.getFirstElementWithName("draft")
        edition = root.getFirstElementWithName("edition")
        isbn = root.getFirstElementWithName("isbn")

        if title == None:
            raise GrapheValidationError("A Graphe document must have a title.")

        document.title = title.innerText.strip()

        if subtitle != None:
            document.subtitle = subtitle.innerText.strip()

        if abstract != None:
            document.abstract = abstract.innerText.strip()

        if keywords != None:
            document.keywords = [k.strip() for k in keywords.innerText.split(",")]

        if draft != None:
            document.draft = draft.innerText.strip()

        if edition != None:
            document.edition = edition.innerText.strip()

        if isbn != None:
            document.isbn = isbn.innerText.strip()

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

    def _importTemplates(self, root, document):

        templates = root.getFirstElementWithName("templates", False)
        pageTemplates = root.getElementsByName("page-template", False)

        for pageTemplate in pageTemplates:
            pt = GPageTemplate()

            pt.reference = self._getAttributeValueOfSynonymousAttributes(pageTemplate, ["r", "reference"])

            header = pageTemplate.getFirstElementWithName("header", False)
            footer = pageTemplate.getFirstElementWithName("footer", False)

            if header != None:
                h = GHeader()

                h.subelements = self._getPageElementsFromXML(pageTemplate.subelements)

                pt.header = h

            if footer != None:
                f = GFooter()

                f.subelements = self._getPageElementsFromXML(pageTemplate.subelements)

                pt.footer = f

            document.templates.append(pt)

    def _importSections(self, root, document):

        sections = root.getFirstElementWithName("sections", False).getElementsByName("section", False)

        for section in sections:
            s = GSection()

            s.document = document

            s.id = section.getAttributeValue("id")
            s.style = section.getAttributeValue("style")
            s.styleClass = section.getAttributeValue("style-class")
            s.language = self._getAttributeValueOfSynonymousAttributes(section, ["l", "language"])
            s.pageTemplateReference = self._getAttributeValueOfSynonymousAttributes(section, ["ptr", "page-template-reference"])

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
        if xmlElement.name in GDefinitionList._elementNames:
            e = GDefinitionList()
        if xmlElement.name in GDefinitionListTerm._elementNames:
            e = GDefinitionListTerm()
        if xmlElement.name in GDefinitionListDefinition._elementNames:
            e = GDefinitionListDefinition()
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
            e.reference = self._getAttributeValueOfSynonymousAttributes(xmlElement, ["r", "reference"])

        if e == None:
            raise GrapheValidationError("<{0}> is not a valid element type.".format(xmlElement.name))

        e.id = xmlElement.getAttributeValue("id")
        e.style = xmlElement.getAttributeValue("style")
        e.styleClass = xmlElement.getAttributeValue("style-class")
        e.language = self._getAttributeValueOfSynonymousAttributes(xmlElement, ["l", "language"])

        e.subelements = self._getPageElementsFromXML(xmlElement.subelements)

        if (isinstance(e, GParagraph) or isinstance(e, GHeading) or isinstance(e, GDivision)) and len(e.subelements) > 0:
            fse = e.subelements[0]
            lse = e.subelements[-1]

            if isinstance(fse, GTextElement):
                fse.text = fse.text.lstrip()

            if isinstance(lse, GTextElement):
                lse.text = lse.text.rstrip()

        return e


class StyleResolver(object):
    def linearise(self, elements):
        e = elements.copy()

        for element in elements:
            if isinstance(element, GContentElement):
                e = e + self.linearise(element.subelements)

        return e

    def selectElementsByName(self, elements, name):
        return [e for e in elements if isinstance(e, GContentElement) and name in e._elementNames]

    def selectElementsById(self, elements, i):
        return [e for e in elements if isinstance(e, GContentElement) and e.id == i]

    def selectElementsByClassName(self, elements, className):
        return [e for e in elements if isinstance(e, GContentElement) and className in e.styleClassNames]

    def selectFirstOrderSubelements(self, elements):
        return [subelement for element in elements if isinstance(element, GContentElement) for subelement in element.subelements]

    def selectNthOrderSubelements(self, elements):
        return self.linearise(self.selectFirstOrderSubelements(elements))

    def applyStylePropertyToElement(self, styleProperty, precedence, element):
        p = styleProperty
        e = element

        if p.name == "page-size":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 2:
                e.styleProperties["page-width"] = makeGLength(p.value.lengths[0])
                e.styleProperties["page-height"] = makeGLength(p.value.lengths[1])
        elif p.name == "page-width":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["page-width"] = makeGLength(p.value.lengths[0])
        elif p.name == "page-height":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["page-height"] = makeGLength(p.value.lengths[0])

        elif p.name == "margin":
            if isinstance(p.value, MLengthSet):
                if len(p.value.lengths) == 4:
                    e.styleProperties["margin-top"] = makeGLength(p.value.lengths[0])
                    e.styleProperties["margin-right"] = makeGLength(p.value.lengths[1])
                    e.styleProperties["margin-bottom"] = makeGLength(p.value.lengths[2])
                    e.styleProperties["margin-left"] = makeGLength(p.value.lengths[3])
                if len(p.value.lengths) == 2:
                    e.styleProperties["margin-top"] = makeGLength(p.value.lengths[0])
                    e.styleProperties["margin-right"] = makeGLength(p.value.lengths[1])
                    e.styleProperties["margin-bottom"] = makeGLength(p.value.lengths[0])
                    e.styleProperties["margin-left"] = makeGLength(p.value.lengths[1])
                if len(p.value.lengths) == 1:
                    e.styleProperties["margin-top"] = makeGLength(p.value.lengths[0])
                    e.styleProperties["margin-right"] = makeGLength(p.value.lengths[0])
                    e.styleProperties["margin-bottom"] = makeGLength(p.value.lengths[0])
                    e.styleProperties["margin-left"] = makeGLength(p.value.lengths[0])
        elif p.name == "margin-top":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["margin-top"] = makeGLength(p.value.lengths[0])
        elif p.name == "margin-right":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["margin-right"] = makeGLength(p.value.lengths[0])
        elif p.name == "margin-bottom":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["margin-bottom"] = makeGLength(p.value.lengths[0])
        elif p.name == "margin-left":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["margin-left"] = makeGLength(p.value.lengths[0])

        elif p.name == "font-height":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["font-height"] = makeGLength(p.value.lengths[0])

        elif p.name == "line-height":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["line-height"] = makeGLength(p.value.lengths[0])

        elif p.name == "text-indentation":
            if isinstance(p.value, MLengthSet) and len(p.value.lengths) == 1:
                e.styleProperties["text-indentation"] = makeGLength(p.value.lengths[0])

        else:
            e.styleProperties[p.name] = p.value

    def applyStyleRuleToDocument(self, styleRule, document):

        sections = document.sections

        allElements = self.linearise(sections)

        while len(styleRule.selectors) > 0:
            selector = styleRule.selectors.pop(0)

            if isinstance(selector, MElementNameSelector):
                allElements = self.selectElementsByName(allElements, selector.elementName)
                continue

            if isinstance(selector, MClassSelector):
                allElements = self.selectElementsByClassName(allElements, selector.className)
                continue

            if isinstance(selector, MIdSelector):
                allElements = self.selectElementsById(allElements, selector.id)
                if len(allElements) > 0:
                    allElements = [allElements[0]]
                continue

            if isinstance(selector, MSubelementSelector):
                allElements = self.selectNthOrderSubelements(allElements)
                continue

        for e in allElements:
            for p in styleRule.properties:
                self.applyStylePropertyToElement(p, 1, e)

    def applyMorpheDocumentToGrapheDocument(self, morpheDocument, grapheDocument):
        for styleRule in morpheDocument.styleRules:
            self.applyStyleRuleToDocument(styleRule, grapheDocument)

        allElements = self.linearise(grapheDocument.sections)

        for element in allElements:
            if isinstance(element, GContentElement):
                styleProperties = importMorpheProperties(element.style)

                for styleProperty in styleProperties:
                    self.applyStylePropertyToElement(styleProperty, 1, element)

        for section in grapheDocument.sections:
            self.cascadeToSubelements(section)

    def cascadeToSubelements(self, element):
        for subelement in element.subelements:
            for spn in element.styleProperties:
                if spn in subelement.styleProperties and subelement.styleProperties[spn] == "inherit":
                    subelement.styleProperties[spn] = element.styleProperties[spn]

            if isinstance(subelement, GContentElement):
                self.cascadeToSubelements(subelement)
