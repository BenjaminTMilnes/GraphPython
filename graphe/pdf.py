from datetime import datetime


class PDFName(object):
    def __init__(self, value):
        self.value = value


class PDFString(object):
    def __init__(self, value):
        self.value = value


class PDFDate(object):
    def __init__(self, value):
        self.value = value


class PDFDocument (object):
    def __init__(self):
        self.header = PDFHeader()
        self.crossReferenceTable = PDFCrossReferenceTable()


class PDFHeader(object):
    def __init__(self, version="1.1"):
        self.version = version


class PDFCrossReferenceTable(object):
    def __init__(self):
        pass


class PDFIndirectObject(object):
    def __init__(self):
        self.id = 0
        self.generation = 0

    def getDictionary(self):
        return {}


class PDFPageObject(PDFIndirectObject):
    def __init__(self):
        self.parent = None
        self.mediaBoxLeft = 0
        self.mediaBoxTop = 0
        self.mediaBoxWidth = 0
        self.mediaBoxHeight = 0
        self.rotation = 0
        self.contents = []
        self.resources = {}

    def getDictionary(self):
        return [
            [PDFName("Type"), PDFName("Page")]
        ]


class PDFDocumentInformationObject(PDFIndirectObject):
    def __init__(self):
        self.title = ""
        self.author = ""

    def getDictionary(self):
        return [
            [PDFName("Title"), PDFString(self.title)],
            [PDFName("Author"), PDFString(self.author)],
            [PDFName("Producer"), PDFString("Graphe")],
            [PDFName("ModDate"), PDFDate(datetime.now())],
            [PDFName("CreationDate"),  PDFDate(datetime.now())],
        ]


class PDFWriter(object):
    def __init__(self):
        pass

    def writeDocument(self, filePath, pdfDocument):
        with open(filePath, "w") as fileObject:
            self._writeHeader(fileObject, pdfDocument.header)

            fileObject.write("%%%%EOF")

    def _writeHeader(self, fileObject, pdfHeader):
        fileObject.write("%%PDF-{0}".format(pdfHeader.version))
