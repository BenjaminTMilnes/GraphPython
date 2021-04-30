import re
import graph.xpath 


class XMLDocument(object):
    """
    Represents an XML document.

    Parameters
    ----------
    declaration : XMLDeclaration
        An XML declaration object
    root : XMLElement
        An XML element that is the root element of this document

    Attributes
    ----------
    declaration : XMLDeclaration
        This document's XML declaration
    root : XMLElement
        This document's root element
    """
    def __init__(self, declaration, root):
        self.declaration = declaration
        self.root = root

        self.root.document = self

        # Calling the setDepth function here results in iterating over 
        # all of the elements in the document and sets their relational 
        # properties.
        self.root._setDepth()

    @staticmethod 
    def fromString(s):
        parser = XMLParser()

        document = parser.parseDocument(s)

        return document 

    @staticmethod 
    def load(filePath):
        parser = XMLParser()

        document = parser.parseFromFile(filePath)
        document.root._setDepth()
        document.root.root = document.root 

        return document 

    def save(self, filePath):
        exporter = XMLExporter()

        s = exporter.exportDocument(self)

        with open(filePath, "w", encoding="utf-8") as fo:
            fo.write(s)
            
    def findByXPath(self, xpath):
        return graph.xpath.resolver.applyXPathToElement(self.root, xpath)


class XMLAttribute(object):
    """
    Represents an XML attribute.

    Parameters
    ----------
    name : str
        The name of this attribute
    value : str
        The value of this attribute

    Attributes
    ----------
    name : str
        The name of this attribute
    value : str
        The value of this attribute
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value


class XMLDeclaration(object):
    """
    Represents an XML declaration.

    Attributes
    ----------
    attributes : list<XMLAttribute>
        The attributes of this declaration
    """
    def __init__(self):
        self.attributes = []

    def _getAttributeValue(self, attributeName):
        """
        Gets the value of the attribute with the given name. 
        Returns an empty string if there is no such attribute.
        """
        a = [attribute for attribute in self.attributes if attribute.name == attributeName]

        if len(a) > 0:
            return a[0].value
        else:
            return ""

    def _setAttributeValue(self, attributeName, attributeValue):
        """
        Sets the value of the attribute with the given name. 
        This function will add a new attribute with the given 
        name if there isn't one already.
        """
        a = [attribute for attribute in self.attributes if attribute.name == attributeName]

        if len(a) > 0:
            a[0].value = attributeValue
        else:
            self.attributes.append(XMLAttribute(attributeName, attributeValue))

    @property
    def version(self):
        return self._getAttributeValue("version")

    @version.setter
    def version(self, value):
        self._setAttributeValue("version", value)

    @property
    def encoding(self):
        return self._getAttributeValue("encoding")

    @encoding.setter
    def encoding(self, value):
        self._setAttributeValue("encoding", value)

    @property
    def standalone(self):
        return self._getAttributeValue("standalone")

    @standalone.setter
    def standalone(self, value):
        self._setAttributeValue("standalone", value)


class HTML5Declaration(object):
    pass


class XMLElement(object):
    def __init__(self, name):
        self.document = None
        self.root = None
        self.superelement = None

        self.depth = 0

        self.name = name
        self.attributes = []
        self.subelements = []

        self.isSelfClosing = False

        self.lineBreakBeforeOpeningTag = True
        self.lineBreakAfterOpeningTag = True
        self.lineBreakBeforeClosingTag = True
        self.lineBreakAfterClosingTag = False

    def _setDepth(self, depth=0):
        self.depth = depth

        for e in self.subelements:
            e._setDepth(depth + 1)

            e.document = self.document

            if self.root == None:
                e.root = self
            else:
                e.root = self.root

            e.superelement = self

    def setLineBreaks(self, lb1, lb2, lb3, lb4):
        self.lineBreakBeforeOpeningTag = lb1
        self.lineBreakAfterOpeningTag = lb2
        self.lineBreakBeforeClosingTag = lb3
        self.lineBreakAfterClosingTag = lb4

    @property
    def hasAttributes(self):
        return len(self.attributes) > 0

    def hasAttribute(self, attributeName):
        return len([a for a in self.attributes if a.name == attributeName]) > 0

    def getAttributeValue(self, attributeName):
        a = [attribute for attribute in self.attributes if attribute.name == attributeName]

        if len(a) > 0:
            return a[0].value
        else:
            return ""

    def setAttributeValue(self, attributeName, attributeValue):
        a = [attribute for attribute in self.attributes if attribute.name == attributeName]

        if len(a) > 0:
            a[0].value = attributeValue
        else:
            self.attributes.append(XMLAttribute(attributeName, attributeValue))

    @property
    def hasSubelements(self):
        return len(self.subelements) > 0

    @property
    def firstSubelement(self):
        if len(self.subelements) > 0:
            return self.subelements[0]
        else:
            return None

    @property
    def lastSubelement(self):
        if len(self.subelements) > 0:
            return self.subelements[-1]
        else:
            return None

    def getSubelementsByName(self, name, anyDepth=True):
        e = [element for element in self.subelements if isinstance(element, XMLElement) and element.name == name]

        if anyDepth:
            for element in self.subelements:
                if isinstance(element, XMLElement):
                    e += element.getSubelementsByName(name, anyDepth)

        return e

    def getFirstSubelementWithName(self, name, anyDepth=True):
        e = self.getSubelementsByName(name, anyDepth)

        if len(e) > 0:
            return e[0]
        else:
            return None

    @property
    def innerText(self):
        t = ""

        for e in self.subelements:
            if isinstance(e, XMLTextElement):
                t += e.text
            elif isinstance(e, XMLElement):
                t += e.innerText

        return t

    def findByXPath(self, xpath):
        return graph.xpath.resolver.applyXPathToElement(self, xpath)


class XMLTextElement(object):
    def __init__(self, text=""):
        self.document = None
        self.root = None
        self.superelement = None

        self.depth = 0

        self.text = text

    def _setDepth(self, depth=0):
        self.depth = depth 


class XMLComment(object):
    """
    Represents an XML comment.

    Attributes
    ----------
    text : str
        The text of this comment.
    """
    def __init__(self, text = ""):
        self.document = None
        self.root = None
        self.superelement = None

        self.depth = 0

        self.text = text

    def _setDepth(self, depth=0):
        self.depth = depth 


class XMLExporter(object):
    def __init__(self):
        pass

    def exportDocument(self, document):
        document.root._setDepth()

        return "{}\n{}".format(self.exportDeclaration(document.declaration), self.exportElement(document.root))

    def exportDeclaration(self, declaration):
        if isinstance(declaration, XMLDeclaration):
            return "<?xml {} ?>".format(self.exportAttributes(declaration.attributes))
        if isinstance(declaration, HTML5Declaration):
            return "<!DOCTYPE html>"

    def exportElements(self, elements):
        return "".join([self.exportElement(e) for e in elements])

    def exportElement(self, element):
        if isinstance(element, XMLTextElement):
            return self.exportTextElement(element)
        elif isinstance(element, XMLComment):
            return self.exportComment(element)
        elif isinstance(element, XMLElement):
            t1 = self.exportAttributes(element.attributes)

            if element.isSelfClosing and len(element.subelements) == 0:    
                if t1 == "":
                    t2 = "<{} />".format(element.name)
                else:
                    t2 = "<{} {} />".format(element.name, t1)

                indentation = 4 * element.depth * " "
                lb1 = "\n" + indentation if element.lineBreakBeforeOpeningTag else ""
                lb4 = "\n" + indentation if element.lineBreakAfterClosingTag else ""
                
                return "{}{}{}".format(lb1, t2, lb4)
            else:
                if t1 == "":
                    t2 = "<{}>".format(element.name)
                else:
                    t2 = "<{} {}>".format(element.name, t1)

                t3 = self.exportElements(element.subelements)
                t4 = "</{}>".format(element.name)

                indentation = 4 * element.depth * " "
                lb1 = "\n" + indentation if element.lineBreakBeforeOpeningTag else ""
                lb2 = "\n" + indentation if element.lineBreakAfterOpeningTag else ""
                lb3 = "\n" + indentation if element.lineBreakBeforeClosingTag else ""
                lb4 = "\n" + indentation if element.lineBreakAfterClosingTag else ""

                return "{}{}{}{}{}{}{}".format(lb1, t2, lb2, t3, lb3, t4, lb4)

    def exportAttributes(self, attributes):
        return " ".join([self.exportAttribute(a) for a in attributes if a.value != ""])

    def exportAttribute(self, attribute):
        return "{}=\"{}\"".format(attribute.name, attribute.value)

    def exportTextElement(self, textElement):
        return textElement.text

    def exportComment(self, comment):
        if comment.text.find("--") < 0:
            raise ValueError("XML comments cannot have '--' in them.")

        return "<!-- {} -->".format(comment.text)


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
    _elementNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    _attributeNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

    def _expect(self, text, inputText, marker):
        c = cut(inputText, marker.p, len(text))

        if c == text:
            marker.p += len(c)
            return True
        else:
            return False

    def _compressWhiteSpace(self, text):
        return re.sub(r"\s+", " ", text)

    def parseFromFile(self, filePath):
        with open(filePath, "r", encoding="utf-8") as fo:
            data = fo.read()

            document = self.parseDocument(data)

            return document

    def parseDocument(self, inputText):
        marker = Marker()

        d = self._getDeclaration(inputText, marker)

        if d == None:
            raise XMLParsingError("Expected XML declaration.")

        self._getWhiteSpace(inputText, marker)

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

        t = self._compressWhiteSpace(t)

        return XMLTextElement(t)

    def _getComment(self, inputText, marker):
        m = marker.copy()

        if self._expect("<!--", inputText, m) == False:
            return None 

        commentStart = m.p

        while m.p < len(inputText) - 2:
            if cut(inputText, m.p, 3) == "-->":
                break 

            m.p += 1

        commentEnd = m.p 

        c = XMLComment()
        c.text = inputText[commentStart, commentEnd].strip()

        m.p += 3
        marker.p = m.p 

        return c 

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

        if self._expect("?>", inputText, m) == False:
            raise XMLParsingError("Expected closing bracket ?>.")

        marker.p = m.p

        d = XMLDeclaration()

        d.attributes = attributes

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

                comment = self._getComment(inputText, m)

                if comment != None:
                    subelements.append(comment)
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

            if len(subelements) > 0 and isinstance(subelements[0], XMLTextElement) and subelements[0].text == " ":
                subelements = subelements[1:]

            if len(subelements) > 0 and isinstance(subelements[-1], XMLTextElement) and subelements[-1].text == " ":
                subelements = subelements[:-1]

            e.subelements = subelements

            return e

        else:
            raise XMLParsingError("Expected closing bracket >.")

    def _getElementName(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in XMLParser._elementNameCharacters:
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

            if c in XMLParser._attributeNameCharacters:
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
        quoteMarkType = "none"
        q = ""

        if self._expect("\"", inputText, m) == True:
            quoteMarkType = "double"
            q = "\""
        elif self._expect("'", inputText, m) == True:
            quoteMarkType = "single"
            q = "'"
        else:
            return None

        while True:
            c = cut(inputText, m.p, len(q))
            m.p += 1
            if c == q:
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
