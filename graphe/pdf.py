from datetime import datetime
import logging


class PDFName(object):
    def __init__(self, value):
        self.value = value


class PDFString(object):
    def __init__(self, value):
        self.value = value


class PDFDate(object):
    def __init__(self, value):
        self.value = value


class PDFNumber (object):
    def __init__(self, value):
        self.value = value



class PDFObjectReference(object):
    def __init__(self, _id, generation):
        self.id = _id
        self.generation = generation


class PDFIndirectObject(object):
    def __init__(self):
        self.document = None

        self.id = 0
        self.generation = 0
        self.byteOffset = 0

    def setIds(self):
        pass

    def getObjectReference(self):
        return PDFObjectReference(self.id, self.generation)

    def getDictionary(self):
        return {}


class PDFStreamObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.length = 0
        self.data = None

    def setIds(self):
        self.id = self.document.getNewId()

    def getDictionary(self):
        return {
            "Length": PDFNumber(self.length)
        }


class PDFTextStreamContext(object):
    def __init__(self, streamObject):
        self._streamObject = streamObject
        self._streamObject.data = ""
    
    def _setStreamObjectLength(self):
        self._streamObject.length = len(self._streamObject.data)
    
    def beginTextBlock(self):
        self._streamObject.data += "BT "
        self._setStreamObjectLength()

    def endTextBlock(self):
        self._streamObject.data += "ET "
        self._setStreamObjectLength()

    def setFont(self, fontName, fontSize):
        self._streamObject.data += "/{0} {1} Tf ".format(fontName, fontSize)
        self._setStreamObjectLength()

    def moveTo(self, x, y):
        self._streamObject.data += "{0} {1} Td ".format(x, y)
        self._setStreamObjectLength()

    def drawText(self, text):
        self._streamObject.data += "({0}) Tj ".format(text)
        self._setStreamObjectLength()

class PDFDocument (object):
    def __init__(self):
        self.header = PDFHeader()
        self.header.document = self

        self.crossReferenceTable = PDFCrossReferenceTable()
        self.crossReferenceTable.document = self

        self.trailer = PDFTrailer()
        self.trailer.document = self

        self._nextId = 1

    def getNewId(self):
        self._nextId += 1
        return self._nextId - 1


class PDFHeader(object):
    def __init__(self, version="1.1"):
        self.document = None

        self.version = version


class PDFCrossReferenceTable(object):
    def __init__(self):
        self.document = None

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


class PDFTrailer(object):
    def __init__(self):
        self.document = None

        self.root = PDFDocumentCatalogObject()
        self.info = PDFDocumentInformationObject()
        self.size = 0

    def setIds(self):
        self.info.document = self.document
        self.root.document = self.document

        self.info.setIds()
        self.root.setIds()

    def getDictionary(self):
        return {
            "Root": self.root.getObjectReference(),
            "Info": self.info.getObjectReference(),
            "Size": PDFNumber(self.size),
        }


class PDFDocumentInformationObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.title = ""
        self.subject = ""
        self.keywords = ""
        self.author = ""

    def setIds(self):
        self.id = self.document.getNewId()

    def getDictionary(self):
        return {
            "Title": PDFString(self.title),
            "Subject": PDFString(self.subject),
            "Keywords": PDFString(self.keywords),
            "Author": PDFString(self.author),
            "Creator": PDFString("Graphe"),
            "CreationDate":  PDFDate(datetime.now()),
            "ModDate": PDFDate(datetime.now()),
        }


class PDFDocumentCatalogObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.pages = None

    def setIds(self):
        self.id = self.document.getNewId()

        self.pages.document = self.document
        self.pages.setIds()

    def getDictionary(self):
        return {
            "Type": PDFName("Catalog"),
            "Pages": self.pages.getObjectReference()
        }

class PDFPagesObject(PDFIndirectObject):
    def __init__(self):
        super().__init__()

        self.parent = None
        self.children = []
        self.count = 0

    def setIds(self):
        self.id = self.document.getNewId()

        for child in self.children:
            child.document = self.document
            child.parent = self
            child.setIds()

            if isinstance(child, PDFPagesObject):
                self.count += child.count
            elif isinstance(child, PDFPageObject):
                self.count += 1

    def getDictionary(self):
        if self.parent != None:
            return {
                "Type": PDFName("Pages"),
                "Parent": self.parent.getObjectReference(),
                "Kids": [c.getObjectReference() for c in self.children],
                "Count": PDFNumber(self.count),
            }
        else:
            return {
                "Type": PDFName("Pages"),
                "Kids": [c.getObjectReference() for c in self.children],
                "Count": PDFNumber(self.count),
            }


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
                    "BaseFont": PDFName("Times-Italic"),
                    "Type": PDFName("Font"),
                    "Subtype": PDFName("Type1")
                }
            }
        }

    def setIds(self):
        self.id = self.document.getNewId()

        for c in self.contents:
            c.document = self.document
            c.setIds()

    def getDictionary(self):
        return {
            "Type": PDFName("Page"),
            "Parent": self.parent.getObjectReference(),
            "Rotate": PDFNumber(self.rotation),
            "MediaBox": [PDFNumber(self.mediaBoxLeft), PDFNumber(self.mediaBoxTop), PDFNumber(self.mediaBoxWidth), PDFNumber(self.mediaBoxHeight)],
            "Contents": [c.getObjectReference() for c in self.contents],
            "Resources":   self.resources,
        }




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

            self._writeHeader( pdfDocument.header)

            self._writePageObject( pdfDocument.trailer.root.pages)

            self._writeIndirectObject( pdfDocument.trailer.root)
            self._writeIndirectObject( pdfDocument.trailer.info)

            self._writeCrossReferenceTable( pdfDocument.crossReferenceTable)

            pdfDocument.trailer.size =  pdfDocument.crossReferenceTable.length

            self._writeTrailer( pdfDocument.trailer)

            self._write("startxref\n")
            self._write("{}\n".format(pdfDocument.crossReferenceTable.byteOffset))
            self._write("%%EOF")

            self._fileObject = None
            self._currentByteLength = 0

        self._document = None

    def _write(self, text):
        self._currentByteLength += len(str(text).encode("utf-8"))
        self._fileObject.write(str(text))

    def _writeHeader(self, pdfHeader):
        self._write("%PDF-{0}\n".format(pdfHeader.version))
        self._write("%áéíóú\n")

    def _writeCrossReferenceTable(self, pdfCrossReferenceTable):
        self._write("xref\n")
        self._write("{0} {1}\n".format(0, pdfCrossReferenceTable.length))

        for index, entry in enumerate( pdfCrossReferenceTable.entries):
            if index ==  pdfCrossReferenceTable.length - 1:
                pdfCrossReferenceTable.byteOffset = self._currentByteLength

            fn = "n" if entry.inUse == True else "f"

            self._write("{:010d} {:05d} {}\n".format(entry.byteOffset, entry.generationNumber, fn))


    def _writeTrailer(self, pdfTrailer):
        self._write("trailer")
        self._writeDictionary(pdfTrailer.getDictionary())

    def _writePageObject(self, pdfPage):

        self._writeIndirectObject( pdfPage)

        if isinstance(pdfPage, PDFPagesObject):
            for p in pdfPage.children:
                self._writePageObject( p)
        elif isinstance(pdfPage, PDFPageObject):
            for c in pdfPage.contents:
                self._writeIndirectObject( c)

    def _writeIndirectObject(self, pdfIndirectObject):
        pdfIndirectObject.byteOffset = self._currentByteLength

        entry = PDFCrossReferenceTableEntry()
        entry.byteOffset = pdfIndirectObject.byteOffset
        entry.orderIndex = pdfIndirectObject.id

        self._document.crossReferenceTable.entries.append(entry)

        self._write("{0} {1} obj".format(pdfIndirectObject.id, pdfIndirectObject.generation))

        self._writeDictionary( pdfIndirectObject.getDictionary())

        if isinstance(pdfIndirectObject, PDFStreamObject):
            self._write("stream\n")
            if pdfIndirectObject.data != None:
                self._write(pdfIndirectObject.data)
            self._write("\nendstream\n")

        self._write("endobj\n")

    def _writeDictionary(self, pdfDictionary, inline=False):
        if not inline:
            self._write("\n<<\n")
        else:
            self._write("<< ")

        for item in pdfDictionary:
            a = PDFName(item)
            b = pdfDictionary[item]

            if not inline:
                self._write("\t")

            self._writeName( a)

            self._write(" ")

            if isinstance(b, PDFObjectReference):
                self._writeObjectReference( b)
            if isinstance(b, PDFName):
                self._writeName( b)
            if isinstance(b, PDFString):
                self._writeString( b)
            if isinstance(b, PDFNumber):
                self._writeNumber( b)
            if isinstance(b, PDFDate):
                self._writeDate( b)
            if isinstance(b, list):
                self._writeList( b)
            if isinstance(b, dict):
                self._writeDictionary( b, True)

            if not inline:
                self._write("\n")
            else:
                self._write(" ")

        if not inline:
            self._write(">>\n")
        else:
            self._write(">>")

    def _writeList(self, pdfList):

        self._write("[")
        n = 0

        for item in pdfList:
            if n > 0:
                self._write(" ")
            n += 1

            if isinstance(item, PDFObjectReference):
                self._writeObjectReference( item)
            if isinstance(item, PDFName):
                self._writeName( item)
            if isinstance(item, PDFString):
                self._writeString( item)
            if isinstance(item, PDFNumber):
                self._writeNumber( item)
            if isinstance(item, PDFDate):
                self._writeDate( item)

        self._write("]")

    def _writeName(self, pdfName):
        self._write("/{0}".format(pdfName.value))

    def _writeString(self, pdfString):
        self._write("({0})".format(pdfString.value))

    def _writeNumber(self, pdfNumber):
        if isinstance(pdfNumber.value, int):
            self._write("{}".format(pdfNumber.value))
        elif isinstance(pdfNumber.value, float):
            self._write("{:01.6f}".format(pdfNumber.value))

    def _writeDate(self, pdfDate):
        self._write("(D:{0})".format(pdfDate.value.strftime("%Y%m%d%H%M%SZ")))

    def _writeObjectReference(self, pdfObjectReference):
        self._write("{0} {1} R".format(pdfObjectReference.id, pdfObjectReference.generation))


if __name__ == "__main__":

    pdfWriter = PDFWriter()

    pdfDocument = PDFDocument()

    pdfDocument.trailer.info.title = "asd"
    pdfDocument.trailer.info.subject = "asd"
    pdfDocument.trailer.info.keywords = "asd"
    pdfDocument.trailer.info.author = "asd"

    pdfPages = PDFPagesObject()
    pdfPage = PDFPageObject()
    pdfStream = PDFStreamObject()

    pdfDocument.trailer.root.pages = pdfPages
    pdfPages.children.append(pdfPage)
    pdfPage.contents.append(pdfStream)

    context = PDFTextStreamContext(pdfStream)

    context.beginTextBlock()
    context.setFont("F0", 12)
    context.moveTo(100, 100)
    context.drawText("Hello world!")
    context.endTextBlock()

    pdfWriter.writeDocument("test_pdf.txt", pdfDocument)
    pdfWriter.writeDocument("test_pdf.pdf", pdfDocument)
