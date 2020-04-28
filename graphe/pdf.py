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
    def __init__(self, version="1.4"):
        self.version = version


class PDFCrossReferenceTable(object):
    def __init__(self):
        self.entries = []
        self.byteOffset = 0

        firstEntry = PDFCrossReferenceTableEntry()
        firstEntry.generationNumber = 65535
        firstEntry.inUse = False
        firstEntry.orderIndex = -1

        self.entries.append(firstEntry)

    @property
    def length(self):
        return len(self.entries)


class PDFCrossReferenceTableEntry(object):
    def __init__(self):
        self.byteOffset = 0
        self.generationNumber = 0
        self.inUse = True
        self.orderIndex = 0


class PDFIndirectObject(object):
    def __init__(self):
        self.id = 0
        self.generation = 0
        self.byteOffset = 0

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
        self.mediaBoxLeft = 0.0
        self.mediaBoxTop = 0.0
        self.mediaBoxWidth = 500.0
        self.mediaBoxHeight = 500.0
        self.rotation = 0
        self.contents = []
        self.resources = {
            "Font": {
                "F0": {
                    "BaseFont": PDFName("Times"),
                    "Type": PDFName("Font"),
                    "Subtype": PDFName("Type1")
                }
            }
        }

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
            (PDFName("Resources"),   self.resources),
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
        self.size = 0

    def setIds(self):
        self.info.id = 1

        self.root.id = 2
        self.root.setIds()

    def getDictionary(self):
        return [
            (PDFName("Root"), self.root.getObjectReference()),
            (PDFName("Info"), self.info.getObjectReference()),
            (PDFName("Size"), PDFNumber(self.size)),
        ]


class PDFWriter(object):
    def __init__(self):
        self._fileObject = None
        self._currentByteLength = 0

    def writeDocument(self, filePath, pdfDocument):
        pdfDocument.trailer.setIds()
        self._document = pdfDocument

        with open(filePath, "w", encoding="utf-8") as fileObject:
            self._fileObject = fileObject
            self._currentByteLength = 0

            self._writeHeader(fileObject, pdfDocument.header)

            self._writePageObject(fileObject, pdfDocument.trailer.root.pages)

            self._writeIndirectObject(fileObject, pdfDocument.trailer.root)
            self._writeIndirectObject(fileObject, pdfDocument.trailer.info)

            self._writeCrossReferenceTable(fileObject, pdfDocument.crossReferenceTable)

            pdfDocument.trailer.size =  len( pdfDocument.crossReferenceTable.entries) 

            self._writeTrailer(fileObject, pdfDocument.trailer)

            self._write("startxref\n")
            self._write("{}\n".format(pdfDocument.crossReferenceTable.byteOffset))
            self._write("%%EOF")

            self._fileObject = None
            self._currentByteLength = 0

        self._document = None

    def _write(self, text):
        self._currentByteLength += len(str(text).encode("utf-8"))
        self._fileObject.write(str(text))

    def _writeHeader(self, fileObject, pdfHeader):
        self._write("%PDF-{0}\n".format(pdfHeader.version))

    def _writeCrossReferenceTable(self, fileObject, pdfCrossReferenceTable):
        self._write("xref\n")
        self._write("{0} {1}\n".format(0, pdfCrossReferenceTable.length))

        #for entry in sorted(pdfCrossReferenceTable.entries, key=lambda x: x.orderIndex):
        for index, entry in enumerate( pdfCrossReferenceTable.entries):
            fn = "n" if entry.inUse == True else "f"

            self._write("{:010d} {:05d} {}\n".format(entry.byteOffset, entry.generationNumber, fn))

            if index == len( pdfCrossReferenceTable.entries) - 1:
                pdfCrossReferenceTable.byteOffset = self._currentByteLength

    def _writeTrailer(self, fileObject, pdfTrailer):
        self._write("trailer")

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
        pdfIndirectObject.byteOffset = self._currentByteLength

        entry = PDFCrossReferenceTableEntry()
        entry.byteOffset = pdfIndirectObject.byteOffset
        entry.orderIndex = pdfIndirectObject.id

        self._document.crossReferenceTable.entries.append(entry)

        self._write("{0} {1} obj".format(pdfIndirectObject.id, pdfIndirectObject.generation))

        self._writeDictionary(fileObject, pdfIndirectObject.getDictionary())

        if isinstance(pdfIndirectObject, PDFStreamObject):
            self._write("stream\n")
            if pdfIndirectObject.data != None:
                self._write(pdfIndirectObject.data)
            self._write("\nendstream\n")

        self._write("endobj\n")

    def _writeDictionary(self, fileObject, pdfDictionary, inline=False):
        if not inline:
            self._write("\n<<\n")
        else:
            self._write("<< ")

        for item in pdfDictionary:
            if isinstance(pdfDictionary, dict):
                a = PDFName(item)
                b = pdfDictionary[item]
            else:
                a = item[0]
                b = item[1]

            if not inline:
                self._write("\t")

            self._writeName(fileObject, a)

            self._write(" ")

            if isinstance(b, PDFObjectReference):
                self._writeObjectReference(fileObject, b)
            if isinstance(b, PDFName):
                self._writeName(fileObject, b)
            if isinstance(b, PDFString):
                self._writeString(fileObject, b)
            if isinstance(b, PDFNumber):
                self._writeNumber(fileObject, b)
            if isinstance(b, PDFDate):
                self._writeDate(fileObject, b)
            if isinstance(b, list):
                self._writeList(fileObject, b)
            if isinstance(b, dict):
                self._writeDictionary(fileObject, b, True)

            if not inline:
                self._write("\n")
            else:
                self._write(" ")

        if not inline:
            self._write(">>\n")
        else:
            self._write(">>")

    def _writeList(self, fileObject, pdfList):

        self._write("[")
        n = 0

        for item in pdfList:
            if n > 0:
                self._write(" ")
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

        self._write("]")

    def _writeName(self, fileObject, pdfName):
        self._write("/{0}".format(pdfName.value))

    def _writeString(self, fileObject, pdfString):
        self._write("({0})".format(pdfString.value))

    def _writeNumber(self, fileObject, pdfNumber):
        if isinstance(pdfNumber.value, int):
            self._write("{}".format(pdfNumber.value))
        elif isinstance(pdfNumber.value, float):
            self._write("{:01.6f}".format(pdfNumber.value))

    def _writeDate(self, fileObject, pdfDate):
        self._write("(D:{0})".format(pdfDate.value.strftime("%Y%m%d%H%M%SZ")))

    def _writeObjectReference(self, fileObject, pdfObjectReference):
        self._write("{0} {1} R".format(pdfObjectReference.id, pdfObjectReference.generation))


if __name__ == "__main__":

    pdfWriter = PDFWriter()

    pdfDocument = PDFDocument()
    pdfPages = PDFPagesObject()
    pdfPage = PDFPageObject()
    pdfStream = PDFStreamObject()

    pdfDocument.trailer.root.pages = pdfPages
    pdfPages.children.append(pdfPage)
    #pdfPage.contents.append(pdfStream)

    context = PDFTextStreamContext(pdfStream)

    context.beginTextBlock()
    context.setFont("F0", 12)
    context.moveTo(100, 100)
    context.drawText("Hello world!")
    context.endTextBlock()

    pdfWriter.writeDocument("test_pdf.txt", pdfDocument)
    pdfWriter.writeDocument("test_pdf.pdf", pdfDocument)
