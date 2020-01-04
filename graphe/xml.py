
class XMLDeclaration (object):
    def __init__(self):
        self.attributes = []


class XMLAttribute(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class XMLTextElement(object):
    def __init__(self, text=""):
        self.text = text


class XMLElement(object):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.subelements = []


class XMLDocument(object):
    def __init__(self, declaration, root):
        self.declaration = declaration
        self.root = root


class Marker(object):
    def __init__(self):
        self.position = 0

    @property
    def p(self):
        return self.position

    @p.setter
    def p(self, value):
        self.position = value

    def copy(self):
        m = Marker()

        m.position = self.position

        return m


def cut(text, start, length=1):
    a = start
    b = start + length

    return text[a:b]


class XMLParsingError(Exception):
    def __init__(self, message):
        super(XMLParsingError, self).__init__(message)


class XMLParser(object):

    def _expect(self, text, inputText, marker):
        c = cut(inputText, marker.p, len(text))

        if c == text:
            marker.p += len(c)
            return True
        else:
            return False

    def parseFromFile(self, filePath):
        with open(filePath, "r") as fo:
            data = fo.read()

            document = self.parseDocument(data)

            return document

    def parseDocument(self, inputText):
        marker = Marker()

        d = self._getDeclaration(inputText, marker)

        if d == None:
            raise XMLParsingError("Expected XML declaration.")

        root = self._getElement(inputText, marker)

        if root == None:
            raise XMLParsingError("Expected root element.")

        document = XMLDocument(d, root)

        return document

    def _getTextElement(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c not in "<>":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return XMLTextElement(t)

    def _getDeclaration(self, inputText, marker):
        m = marker.copy()

        if self._expect("<?xml", inputText, m) == False:
            return None

        attributes = []

        while True:
            attribute = self._getAttribute(inputText, m)

            if attribute == None:
                break
            else:
                attributes.append(attribute)

        self._getWhiteSpace(inputText, m)

        d = XMLDeclaration()

        d.attributes = attributes

        self._getWhiteSpace(inputText, m)

        if self._expect("?>", inputText, m) == False:
            raise XMLParsingError("Expected closing bracket ?>.")

        marker.p = m.p

        return d

    def _getElement(self, inputText, marker):
        m = marker.copy()

        if self._expect("<", inputText, m) == False:
            return None

        name = self._getElementName(inputText, m)

        if name == None:
            return None

        attributes = []

        while True:
            attribute = self._getAttribute(inputText, m)

            if attribute == None:
                break
            else:
                attributes.append(attribute)

        self._getWhiteSpace(inputText, m)

        e = XMLElement(name)

        e.attributes = attributes

        if self._expect("/>", inputText, m) == True:
            marker.p = m.p

            return e
        elif self._expect(">", inputText, m) == True:

            subelements = []

            while True:
                textElement = self._getTextElement(inputText, m)

                if textElement != None:
                    subelements.append(textElement)
                    continue

                element = self._getElement(inputText, m)

                if element != None:
                    subelements.append(element)
                    continue

                break

            if self._expect("</", inputText, m) == False:
                raise XMLParsingError("Expected closing XML tag </{0}>.".format(name))

            self._getWhiteSpace(inputText, m)

            if self._expect(name, inputText, m) == False:
                raise XMLParsingError("Expected closing XML tag </{0}>.".format(name))

            self._getWhiteSpace(inputText, m)

            if self._expect(">", inputText, m) == False:
                raise XMLParsingError("Expected closing XML tag </{0}>.".format(name))

            marker.p = m.p

            e.subelements = subelements

            return e

        else:
            raise XMLParsingError("Expected closing bracket >.")

    def _getElementName(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t

    def _getAttribute(self, inputText, marker):
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        name = self._getAttributeName(inputText, m)

        if name == None:
            return None

        self._getWhiteSpace(inputText, m)

        if self._expect("=", inputText, m) == False:
            return None

        self._getWhiteSpace(inputText, m)

        value = self._getAttributeValue(inputText, m)

        marker.p = m.p

        a = XMLAttribute(name, value)

        return a

    def _getAttributeName(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t

    def _getAttributeValue(self, inputText, marker):
        m = marker.copy()
        t = ""

        if self._expect("\"", inputText, m) == False:
            return None

        while True:
            c = cut(inputText, m.p, len("\""))
            m.p += 1
            if c == "\"":
                break
            else:
                t += c

        marker.p = m.p

        return t

    def _getWhiteSpace(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in " \t\n":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t
