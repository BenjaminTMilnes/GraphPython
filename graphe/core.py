from datetime import datetime
import xml.etree.ElementTree as et
import re


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
    _levels = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]

    def __init__(self, level=1):
        super(GHeading, self).__init__()

        self.level = level


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
        self.url = ""
        self.title = ""

class GPageBreak(GContentElement):
    _elementNames = ["page-break", "pb"]


class GUnorderedList(GContentElement):
    _elementNames = ["unordered-list", "ul"]


class GOrderedList(GContentElement):
    _elementNames = ["ordered-list", "ol"]


class GListItem(GContentElement):
    _elementNames = ["list-item", "li"]


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


class GrapheValidationError (Exception):
    def __init__(self, message):
        super(GrapheValidationError, self).__init__(message)


class GImporter(object):
    def __init__(self):

        self.allowedDocumentVersions = ["0.1"]

    def importDocument(self, filePath):

        tree = et.parse(filePath)
        root = tree.getroot()

        document = GDocument()

        self._importMetadata(root, document)
        self._importSections(root, document)

        return document

    def _importMetadata(self, root, document):

        if root.tag != "document":
            raise GrapheValidationError("The root element in a Graphe document file must be a <document> element.")

        if "version" not in root.attrib:
            raise GrapheValidationError("The <document> element must have a 'version' attribute.")

        version = root.attrib["version"]

        if version not in self.allowedDocumentVersions:
            raise GrapheValidationError("'{0}' is not a valid Graphe version.".format(version))

        document.version = version

        title = root.find("./title")
        subtitle = root.find("./subtitle")
        abstract = root.find("./abstract")
        keywords = root.find("./keywords")

        if title == None:
            raise GrapheValidationError("A Graphe document must have a title.")

        title_text = "".join(title.itertext()).strip()
        document.title = title_text

        if subtitle != None:
            subtitle_text = "".join(subtitle.itertext()).strip()
            document.subtitle = subtitle_text

        if abstract != None:
            abstract_text = "".join(abstract.itertext()).strip()
            document.abstract = abstract_text

        if keywords != None:
            keywords_text = "".join(keywords.itertext()).strip()
            document.keywords = [k.strip() for k in keywords_text.split(",")]

    def _importSections(self, root, document):

        sections = root.findall("./sections/section")

        for section in sections:
            s = GSection()

            s.document = document
            s.subelements = self._getPageElementsFromXML(section.findall("*"))

            document.sections.append(s)

    def _compressWhiteSpace(self, text):
        return re.sub(r"\s+", " ", text)

    def _getPageElementsFromXML(self, xmlElements):
        return [self._getPageElementFromXML(e) for e in xmlElements]

    def _getPageElementFromXML(self, xmlElement):

        if xmlElement.tag in GPageBreak._elementNames:
            return GPageBreak()

        e = None

        if xmlElement.tag in GHeading._elementNames:
            e = GHeading()
            i = GHeading._elementNames.index(xmlElement.tag)
            e.level = GHeading._levels[i]
        if xmlElement.tag in GParagraph._elementNames:
            e = GParagraph()
        if xmlElement.tag in GBold._elementNames:
            e = GBold()
        if xmlElement.tag in GItalic._elementNames:
            e = GItalic()
        if xmlElement.tag in GUnderline._elementNames:
            e = GUnderline()
        if xmlElement.tag in GStrikethrough._elementNames:
            e = GStrikethrough()
        if xmlElement.tag in GOrderedList._elementNames:
            e = GOrderedList()
        if xmlElement.tag in GUnorderedList._elementNames:
            e = GUnorderedList()
        if xmlElement.tag in GListItem._elementNames:
            e = GListItem()
        if xmlElement.tag in GHyperlink._elementNames:
            e = GHyperlink()
                
            if "url" in xmlElement.attrib:
                e.url = xmlElement.attrib["url"]
                
            if "title" in xmlElement.attrib:
                e.title = xmlElement.attrib["title"]

        if e == None:
            raise GrapheValidationError("<{0}> is not a valid element type.".format(xmlElement.tag))

        if "id" in xmlElement.attrib:
            e.id = xmlElement.attrib["id"]

        if "style" in xmlElement.attrib:
            e.style = xmlElement.attrib["style"]

        if "style-class" in xmlElement.attrib:
            e.styleClass = xmlElement.attrib["style-class"]

        if "l" in xmlElement.attrib:
            e.language = xmlElement.attrib["l"]

        if "language" in xmlElement.attrib:
            e.language = xmlElement.attrib["language"]

        xmlSubelements = xmlElement.findall("*")
        text = "".join(xmlElement.itertext())

        if len(xmlSubelements) > 0:
            e.subelements = self._getPageElementsFromXML()
        elif text != "":
            text = self._compressWhiteSpace(text)

            t = GTextElement(text)

            e.subelements.append(t)

        return e
