from datetime import datetime


class GContributor (object):
    def __init__(self):

        self.name = ""
        self.type = ""
        self.emailAddress = ""
        self.address = ""
        self.website = ""


class GTextElement (object):
    def __init__(self, text=""):

        self.text = text


class GContentElement (object):
    def __init__(self):

        self._elementNames = []
        self.subelements = []

        self.styleClass = ""


class GParagraph (GContentElement):
    def __init__(self):
        super(GParagraph, self).__init__()

        self._elementNames = ["paragraph", "p"]


class GHeading (GContentElement):
    def __init__(self, level=1):
        super(GHeading, self).__init__()

        self.level = level
        self._elementNames = ["heading{0}".format(self.level), "h{0}".format(self.level)]


class GBold (GContentElement):
    def __init__(self):

        self._elementNames = ["bold", "b"]


class GItalic (GContentElement):
    def __init__(self):

        self._elementNames = ["italic", "i"]


class GUnderline (GContentElement):
    def __init__(self):

        self._elementNames = ["underline", "u"]


class GStrikethrough (GContentElement):
    def __init__(self):

        self._elementNames = ["strikethrough", "s"]


class GPageBreak (GContentElement):
    def __init__(self):

        self._elementNames = ["page-break", "pb"]


class GUnorderedList (GContentElement):
    def __init__(self):

        self._elementNames = ["unordered-list", "ul"]


class GOrderedList (GContentElement):
    def __init__(self):

        self._elementNames = ["ordered-list", "ol"]


class GListItem (GContentElement):
    def __init__(self):

        self._elementNames = ["list-item", "li"]


class GTemplate (GContentElement):
    def __init__(self):
        super(GContentElement, self).__init__()

        self.reference = ""


class GPageTemplate (GTemplate):
    def __init__(self):
        super(GPageTemplate, self).__init__()


class GSection (GContentElement):
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


class GDocument (object):
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
