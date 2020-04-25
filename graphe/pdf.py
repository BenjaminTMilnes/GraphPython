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


class PDFObjectReference(object):
    def __init__(self, id, generation):
        self.id = id
        self.generation = generation


class PDFDocument (object):
    def __init__(self):
        self.header = PDFHeader()
        self.trailer = PDFTrailer()
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

    def setIds(self):
        pass

    def getObjectReference(self):
        return PDFObjectReference(self.id, self.generation)

    def getDictionary(self):
        return []


class PDFPagesObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.parent = None
        self.children = []

    def setIds(self):
        n = self.id

        for child in self.children:
            n += 1
            child.id = n
            child.parent = self
            child.setIds()

    def getDictionary(self):
        return [
            (PDFName("Type"), PDFName("Pages")),
            (PDFName("Parent"), self.parent.getObjectReference()),
            (PDFName("Kids"), [c.getObjectReference() for c in self.children]),
        ]


class PDFPageObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

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
            (PDFName("Type"), PDFName("Page")),
            (PDFName("Parent"), self.parent.getObjectReference()),
        ]


class PDFDocumentInformationObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.title = ""
        self.subject = ""
        self.keywords = ""
        self.author = ""

    def getDictionary(self):
        return [
            (PDFName("Title"), PDFString(self.title)),
            (PDFName("Subject"), PDFString(self.subject)),
            (PDFName("Keywords"), PDFString(self.keywords)),
            (PDFName("Author"), PDFString(self.author)),
            (PDFName("Creator"), PDFString("Graphe")),
            (PDFName("CreationDate"),  PDFDate(datetime.now())),
            (PDFName("ModDate"), PDFDate(datetime.now())),
        ]


class PDFDocumentCatalogObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.pages = None

    def setIds(self):

        self.pages.id = self.id + 1
        self.pages.parent = self
        self.pages.setIds()

    def getDictionary(self):
        return [
            (PDFName("Type"), PDFName("Catalog")),
            (PDFName("Pages"), self.pages.getObjectReference())
        ]


class PDFTrailer(PDFIndirectObject):
    def __init__(self):
        self.root = PDFDocumentCatalogObject()
        self.info = PDFDocumentInformationObject()

    def setIds(self):
        self.info.id = 1

        self.root.id = 2
        self.root.setIds()

    def getDictionary(self):
        return [
            (PDFName("Root"), self.root.getObjectReference()),
            (PDFName("Info"), self.info.getObjectReference()),
        ]


class PDFWriter(object):
    def __init__(self):
        pass

    def writeDocument(self, filePath, pdfDocument):
        pdfDocument.trailer.setIds()

        with open(filePath, "w") as fileObject:
            self._writeHeader(fileObject, pdfDocument.header)

            self._writePageObject( fileObject, pdfDocument.trailer.root.pages)

            self._writeIndirectObject(fileObject, pdfDocument.trailer.root)
            self._writeIndirectObject(fileObject, pdfDocument.trailer.info)

            self._writeCrossReferenceTable(fileObject)

            self._writeTrailer(fileObject, pdfDocument.trailer)

            fileObject.write("%%EOF")

    def _writeHeader(self, fileObject, pdfHeader):
        fileObject.write("%PDF-{0}\n".format(pdfHeader.version))

    def _writeCrossReferenceTable(self, fileObject):
        fileObject.write("xref\n")

    def _writeTrailer(self, fileObject, pdfTrailer):
        fileObject.write("trailer")

        self._writeDictionary(fileObject, pdfTrailer.getDictionary())

    def _writePageObject(self, fileObject, pdfPage):

        self._writeIndirectObject(fileObject, pdfPage)

        if isinstance(pdfPage, PDFPagesObject):
            for p in pdfPage.children:
                self._writePageObject(fileObject, p)

    def _writeIndirectObject(self, fileObject, pdfIndirectObject):
        fileObject.write("{0} {1} obj".format(pdfIndirectObject.id, pdfIndirectObject.generation))

        self._writeDictionary(fileObject, pdfIndirectObject.getDictionary())

        fileObject.write("endobj\n")

    def _writeDictionary(self, fileObject, pdfDictionary):
        fileObject.write("\n<<\n")

        for item in pdfDictionary:
            fileObject.write("\t")
            self._writeName(fileObject, item[0])
            fileObject.write(" ")

            if isinstance(item[1], PDFObjectReference):
                self._writeObjectReference(fileObject, item[1])
            if isinstance(item[1], PDFName):
                self._writeName(fileObject, item[1])
            if isinstance(item[1], PDFString):
                self._writeString(fileObject, item[1])
            if isinstance(item[1], PDFDate):
                self._writeDate(fileObject, item[1])
            if isinstance(item[1], list):
                self._writeList(fileObject, item[1])

            fileObject.write("\n")

        fileObject.write(">>\n")

    def _writeList(self, fileObject, pdfList):
        
        fileObject.write("[")

        for item in pdfList:
            if isinstance(item, PDFObjectReference):
                self._writeObjectReference(fileObject, item)
            if isinstance(item, PDFName):
                self._writeName(fileObject, item)
            if isinstance(item, PDFString):
                self._writeString(fileObject, item)
            if isinstance(item, PDFDate):
                self._writeDate(fileObject, item)   
                
        fileObject.write("]")

    def _writeName(self, fileObject, pdfName):
        fileObject.write("/{0}".format(pdfName.value))

    def _writeString(self, fileObject, pdfString):
        fileObject.write("({0})".format(pdfString.value))

    def _writeDate(self, fileObject, pdfDate):
        fileObject.write("(D:{0})".format(pdfDate.value.strftime("%Y%m%d%H%M%SZ")))

    def _writeObjectReference(self, fileObject, pdfObjectReference):
        fileObject.write("{0} {1} R".format(pdfObjectReference.id, pdfObjectReference.generation))


if __name__ == "__main__":

    pdfWriter = PDFWriter()

    pdfDocument = PDFDocument()
    pdfPages = PDFPagesObject()
    pdfPage = PDFPageObject()

    pdfDocument.trailer.root.pages = pdfPages
    pdfPages.children.append(pdfPage)

    pdfWriter.writeDocument("test_pdf.txt", pdfDocument)
