

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
    def __init__(self):
        super(SubelementsSelector, self).__init__()


class RootElementSelector(XPathSelector):
    def __init__(self):
        super(RootElementSelector, self).__init__()


class SuperelementSelector(XPathSelector):
    def __init__(self):
        super(SuperelementSelector, self).__init__()


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

        while marker.p < len(xPath):

            if cut(xPath, marker.p, 2) == "//":
                pass

            if cut(xPath, marker.p, 1) == "/":
                expression.selectors.append(SubelementsSelector())
                marker.p += 1
                continue

        return expression
