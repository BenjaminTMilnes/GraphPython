from datetime import datetime


class PDFName(object):
    def __init__(self, value):
        self.value = value


class PDFString(object):
    def __init__(self, value):
        self.value = value


class PDFNumber (object):
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
        self.entries = []

    @property
    def length(self):
        return len(self.entries)


class PDFCrossReferenceTableEntry(object):
    def __init__(self):
        self.byteOffset = 0
        self.generationNumber = 0
        self.inUse = True


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


class PDFStreamObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.length = 0
        self.data = None

    def getDictionary(self):
        return [
            (PDFName("Length"), PDFNumber(self.length))
        ]


class PDFTextStreamContext(object):
    def __init__(self, pdfStreamObject):

        self._streamObject = pdfStreamObject
        self._streamObject.data = ""

    def beginTextBlock(self):
        self._streamObject.data += "BT "
        self._streamObject.length = len(self._streamObject.data)

    def endTextBlock(self):
        self._streamObject.data += "ET "
        self._streamObject.length = len(self._streamObject.data)

    def setFont(self, fontName, fontSize):
        self._streamObject.data += "/{0} {1} Tf ".format(fontName, fontSize)
        self._streamObject.length = len(self._streamObject.data)

    def moveTo(self, x, y):
        self._streamObject.data += "{0} {1} Td ".format(x, y)
        self._streamObject.length = len(self._streamObject.data)

    def drawText(self, text):
        self._streamObject.data += "({0}) Tj ".format(text)
        self._streamObject.length = len(self._streamObject.data)


class PDFPagesObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.parent = None
        self.children = []
        self.count = 0

    def setIds(self):
        n = self.id

        for child in self.children:
            n += 1
            child.id = n
            child.parent = self
            child.setIds()

            if isinstance(child, PDFPagesObject):
                self.count += child.count
            elif isinstance(child, PDFPageObject):
                self.count += 1

    def getDictionary(self):
        return [
            (PDFName("Type"), PDFName("Pages")),
            (PDFName("Parent"), self.parent.getObjectReference()),
            (PDFName("Kids"), [c.getObjectReference() for c in self.children]),
            (PDFName("Count"), PDFNumber(self.count)),
        ]


class PDFPageObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.parent = None
        self.mediaBoxLeft = 0
        self.mediaBoxTop = 0
        self.mediaBoxWidth = 500
        self.mediaBoxHeight = 500
        self.rotation = 0
        self.contents = []
        self.resources = {}

    def setIds(self):
        n = self.id

        for c in self.contents:
            n += 1
            c.id = n
            c.setIds()

    def getDictionary(self):
        return [
            (PDFName("Type"), PDFName("Page")),
            (PDFName("Parent"), self.parent.getObjectReference()),
            (PDFName("Rotate"), PDFNumber(self.rotation)),
            (PDFName("MediaBox"), [PDFNumber(self.mediaBoxLeft), PDFNumber(self.mediaBoxTop), PDFNumber(self.mediaBoxWidth), PDFNumber(self.mediaBoxHeight)]),
            (PDFName("Contents"), [c.getObjectReference() for c in self.contents]),
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

            self._writePageObject(fileObject, pdfDocument.trailer.root.pages)

            self._writeIndirectObject(fileObject, pdfDocument.trailer.root)
            self._writeIndirectObject(fileObject, pdfDocument.trailer.info)

            self._writeCrossReferenceTable(fileObject)

            self._writeTrailer(fileObject, pdfDocument.trailer)

            fileObject.write("%%EOF")

    def _writeHeader(self, fileObject, pdfHeader):
        fileObject.write("%PDF-{0}\n".format(pdfHeader.version))

    def _writeCrossReferenceTable(self, fileObject, pdfCrossReferenceTable):
        fileObject.write("xref\n")
        fileObject.write("{0} {1}\n".format(0, pdfCrossReferenceTable.length))

        for entry in pdfCrossReferenceTable.entries:
            fn = "n" if entry.inUse == True else "f"

            fileObject.write("{0} {1} {2}".format(entry.byteOffset, entry.generationNumber, fn))

    def _writeTrailer(self, fileObject, pdfTrailer):
        fileObject.write("trailer")

        self._writeDictionary(fileObject, pdfTrailer.getDictionary())

    def _writePageObject(self, fileObject, pdfPage):

        self._writeIndirectObject(fileObject, pdfPage)

        if isinstance(pdfPage, PDFPagesObject):
            for p in pdfPage.children:
                self._writePageObject(fileObject, p)
        elif isinstance(pdfPage, PDFPageObject):
            for c in pdfPage.contents:
                self._writeIndirectObject(fileObject, c)

    def _writeIndirectObject(self, fileObject, pdfIndirectObject):
        fileObject.write("{0} {1} obj".format(pdfIndirectObject.id, pdfIndirectObject.generation))

        self._writeDictionary(fileObject, pdfIndirectObject.getDictionary())

        if isinstance(pdfIndirectObject, PDFStreamObject):
            fileObject.write("stream\n")
            if pdfIndirectObject.data != None:
                fileObject.write(pdfIndirectObject.data)
            fileObject.write("\nendstream\n")

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
            if isinstance(item[1], PDFNumber):
                self._writeNumber(fileObject, item[1])
            if isinstance(item[1], PDFDate):
                self._writeDate(fileObject, item[1])
            if isinstance(item[1], list):
                self._writeList(fileObject, item[1])

            fileObject.write("\n")

        fileObject.write(">>\n")

    def _writeList(self, fileObject, pdfList):

        fileObject.write("[")
        n = 0

        for item in pdfList:
            if n > 0:
                fileObject.write(" ")
            n += 1

            if isinstance(item, PDFObjectReference):
                self._writeObjectReference(fileObject, item)
            if isinstance(item, PDFName):
                self._writeName(fileObject, item)
            if isinstance(item, PDFString):
                self._writeString(fileObject, item)
            if isinstance(item, PDFNumber):
                self._writeNumber(fileObject, item)
            if isinstance(item, PDFDate):
                self._writeDate(fileObject, item)

        fileObject.write("]")

    def _writeName(self, fileObject, pdfName):
        fileObject.write("/{0}".format(pdfName.value))

    def _writeString(self, fileObject, pdfString):
        fileObject.write("({0})".format(pdfString.value))

    def _writeNumber(self, fileObject, pdfNumber):
        fileObject.write("{0}".format(pdfNumber.value))

    def _writeDate(self, fileObject, pdfDate):
        fileObject.write("(D:{0})".format(pdfDate.value.strftime("%Y%m%d%H%M%SZ")))

    def _writeObjectReference(self, fileObject, pdfObjectReference):
        fileObject.write("{0} {1} R".format(pdfObjectReference.id, pdfObjectReference.generation))


if __name__ == "__main__":

    pdfWriter = PDFWriter()

    pdfDocument = PDFDocument()
    pdfPages = PDFPagesObject()
    pdfPage = PDFPageObject()
    pdfStream = PDFStreamObject()

    pdfDocument.trailer.root.pages = pdfPages
    pdfPages.children.append(pdfPage)
    pdfPage.contents.append(pdfStream)

    context = PDFTextStreamContext(pdfStream)

    context.beginTextBlock()
    context.setFont("F1", 12)
    context.moveTo(100, 100)
    context.drawText("Hello world!")
    context.endTextBlock()

    pdfWriter.writeDocument("test_pdf.txt", pdfDocument)
