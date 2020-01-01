from datetime import datetime
import xml.etree.ElementTree as et


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
    def __init__(self):

        self._elementNames = []
        self.subelements = []

        self.styleClass = ""
        self.style = ""


class GParagraph(GContentElement):
    def __init__(self):
        super(GParagraph, self).__init__()

        self._elementNames = ["paragraph", "p"]


class GHeading(GContentElement):
    def __init__(self, level=1):
        super(GHeading, self).__init__()

        self.level = level
        self._elementNames = ["heading{0}".format(self.level), "h{0}".format(self.level)]


class GBold(GContentElement):
    def __init__(self):

        self._elementNames = ["bold", "b"]


class GItalic(GContentElement):
    def __init__(self):

        self._elementNames = ["italic", "i"]


class GUnderline(GContentElement):
    def __init__(self):

        self._elementNames = ["underline", "u"]


class GStrikethrough(GContentElement):
    def __init__(self):

        self._elementNames = ["strikethrough", "s"]


class GPageBreak(GContentElement):
    def __init__(self):

        self._elementNames = ["page-break", "pb"]


class GUnorderedList(GContentElement):
    def __init__(self):

        self._elementNames = ["unordered-list", "ul"]


class GOrderedList(GContentElement):
    def __init__(self):

        self._elementNames = ["ordered-list", "ol"]


class GListItem(GContentElement):
    def __init__(self):

        self._elementNames = ["list-item", "li"]


class GTemplate(GContentElement):
    def __init__(self):
        super(GContentElement, self).__init__()

        self.reference = ""


class GPageTemplate(GTemplate):
    def __init__(self):
        super(GPageTemplate, self).__init__()


class GSection(GContentElement):
    def __init__(self):
        super(GSection, self).__init__()

        self._elementNames = ["section"]

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
        self.headingTags = ["heading1", "heading2", "heading3", "heading4", "heading5", "heading6", "heading7", "heading8", "heading9", "heading10", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10"]
        self.headingTagLevels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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

    def _getPageElementsFromXML(self, xmlElements):
        return [self._getPageElementFromXML(e) for e in xmlElements]

    def _getPageElementFromXML(self, xmlElement):

        if xmlElement.tag in ["page-break", "pb"]:
            return GPageBreak()

        e = None

        if xmlElement.tag in self.headingTags:
            e = GHeading()
            i = self.headingTags.index(xmlElement.tag)
            e.level = self.headingTagLevels[i]
        if xmlElement.tag in ["paragraph", "p"]:
            e = GParagraph()
        if xmlElement.tag in ["bold", "b"]:
            e = GBold()
        if xmlElement.tag in ["italic", "i"]:
            e = GItalic()
        if xmlElement.tag in ["underline", "u"]:
            e = GUnderline()
        if xmlElement.tag in ["strikethrough", "s"]:
            e = GStrikethrough()
        if xmlElement.tag in ["ordered-list", "ol"]:
            e = GOrderedList()
        if xmlElement.tag in ["unordered-list", "ul"]:
            e = GUnorderedList()
        if xmlElement.tag in ["list-item", "li"]:
            e = GListItem()

        if e == None:
            raise GrapheValidationError("<{0}> is not a valid element type.".format(xmlElement.tag))

        xmlSubelements = xmlElement.findall("*")
        text = "".join(xmlElement.itertext())

        if len(xmlSubelements) > 0:
            e.subelements = self._getPageElementsFromXML()
        elif text != "":
            t = GTextElement(text)

            e.subelements.append(t)

        return e
