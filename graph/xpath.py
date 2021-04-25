

class XPathExpression(object):
    def __init__(self):
        self.selectors = []


class XPathSelector(object):
    pass


class ElementNameSelector(XPathSelector):
    def __init__(self, elementName):
        super(ElementNameSelector, self).__init__()

        self.elementName = elementName


class SubelementsSelector(XPathSelector):
    def __init__(self, anyDepth=False):
        super(SubelementsSelector, self).__init__()

        self.anyDepth = anyDepth


class RootElementSelector(XPathSelector):
    def __init__(self):
        super(RootElementSelector, self).__init__()


class SuperelementSelector(XPathSelector):
    def __init__(self):
        super(SuperelementSelector, self).__init__()


class AttributeNameSelector(XPathSelector):
    def __init__(self, attributeName):
        super(AttributeNameSelector, self).__init__()

        self.attributeName = attributeName


class AttributesSelector(XPathSelector):
    def __init__(self):
        super(AttributesSelector, self).__init__()


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


class XPathParsingError(Exception):
    def __init__(self, message):
        super(XPathParsingError, self).__init__(message)


class XPathParser(object):
    _elementNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    _attributeNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

    def _expect(self, text, inputText, marker):
        c = cut(inputText, marker.p, len(text))

        if c == text:
            marker.p += len(c)
            return True
        else:
            return False

    def parseXPath(self, xPath):
        marker = Marker()

        expression = XPathExpression()

        if cut(xPath, marker.p, 1) == "/":
            marker.p += 1
            expression.selectors.append(RootElementSelector())

        while marker.p < len(xPath):

            if cut(xPath, marker.p, 2) == "..":
                marker.p += 2
                expression.selectors.append(SuperelementSelector())
                continue

            if cut(xPath, marker.p, 2) == "//":
                marker.p += 2
                elementName = self._getElementName(xPath, marker)

                if elementName != None:
                    expression.selectors.append(SubelementsSelector(True))
                    expression.selectors.append(
                        ElementNameSelector(elementName))
                    continue
                elif cut(xPath, marker.p, 1) == "*":
                    expression.selectors.append(SubelementsSelector(True))
                    continue

            if cut(xPath, marker.p, 1) == "/":
                marker.p += 1
                elementName = self._getElementName(xPath, marker)

                if elementName != None:
                    expression.selectors.append(SubelementsSelector(False))
                    expression.selectors.append(
                        ElementNameSelector(elementName))
                    continue
                elif cut(xPath, marker.p, 1) == "*":
                    expression.selectors.append(SubelementsSelector(False))
                    continue

            if cut(xPath, marker.p, 1) == "@":
                marker.p += 1
                attributeName = self._getAttributeName(xPath, marker)

                if attributeName != None:
                    expression.selectors.append(AttributesSelector())
                    expression.selectors.append(
                        AttributeNameSelector(attributeName))
                    continue
                elif cut(xPath, marker.p, 1) == "*":
                    expression.selectors.append(AttributesSelector())
                    continue

        return expression

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
