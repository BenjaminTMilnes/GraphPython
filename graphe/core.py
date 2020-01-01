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


class GImporter(object):
    def importDocument(self, filePath):

        tree = et.parse(filePath)
        root = tree.getroot()

        document = GDocument()

        self._importMetadata(root, document)
        self._importSections(root, document)

        return document

    def _importMetadata(self, root, document):

        if "version" in root.attrib:
            version = root.attrib["version"]
            document.version = version

        if len(root.findall("./title")) > 0:
            title = "".join(root.findall("./title")[0].itertext()).strip()
            document.title = title
            
        if len(root.findall("./subtitle")) > 0:
            subtitle = "".join(root.findall("./subtitle")[0].itertext()).strip()
            document.subtitle = subtitle

        if len(root.findall("./abstract")) > 0:
            abstract = "".join(root.findall("./abstract")[0].itertext()).strip()
            document.abstract = abstract

        if len(root.findall("./keywords")) > 0:
            keywords = "".join(root.findall("./keywords")[0].itertext()).strip()
            document.keywords = [k.strip() for k in keywords.split(",")]

    def _importSections(self, root, document):

        sections = root.findall("./sections/section")

        for section in sections:
            s = GSection()

            s.document = document
            s.subelements = self._getPageElementsFromXML(section.findall("*"))

            document.sections.append(s)

    def _getPageElementsFromXML(self, xmlElements):
        e = []

        for xmlElement in xmlElements:
            e.append(self._getPageElementFromXML(xmlElement))

        return e

    def _getPageElementFromXML(self, xmlElement):

        if xmlElement.tag in ["page-break", "pb"]:
            return GPageBreak()

        e = None

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
            return

        xmlSubelements = xmlElement.findall("*")
        text = "".join(xmlElement.itertext())

        if len(xmlSubelements) > 0:
            e.subelements = self._getPageElementsFromXML()
        elif text != "":
            t = GTextElement(text)

            e.subelements.append(t)

        return e
