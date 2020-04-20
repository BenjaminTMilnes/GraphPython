


class PDFDocument (object):
    def __init__(self):
        self.header = PDFHeader()
        self.crossReferenceTable = PDFCrossReferenceTable()

class PDFHeader(object):
    def __init__(self, version = "1.1"):
        self.version = version

class PDFCrossReferenceTable(object):
    def __init__(self):
        pass

class PDFIndirectObject(object):
    def __init__(self):
        self.id = 0
        self.generation = 0