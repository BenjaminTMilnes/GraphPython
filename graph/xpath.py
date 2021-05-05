import logging 

logger = logging.getLogger(__name__)


class XPathExpression(object):
    def __init__(self):
        self.selectors = []

    def __str__(self):
        t = ""

        for index, selector in enumerate(self.selectors):
            notLast = index < len(self.selectors) - 1
            nextSelector = self.selectors[index + 1] if notLast else None 

            if isinstance(selector, ElementNameSelector):
                t += selector.elementName 
            if isinstance(selector, SubelementsSelector):
                if not isinstance(nextSelector, ElementNameSelector):
                    t += "//*" if selector.anyDepth else "/*" 
                else:
                    t += "//" if selector.anyDepth else "/" 
            if isinstance(selector, RootElementSelector):
                t += "/" 
            if isinstance(selector, SuperelementSelector):
                t += ".." 
            if isinstance(selector, CurrentElementSelector):
                t += "."  
            if isinstance(selector, AttributesSelector):
                if not isinstance(nextSelector, AttributeNameSelector):
                    t += "@*" 
                else:
                    t += "@"
            if isinstance(selector, AttributeNameSelector):
                t += selector.attributeName 

        return t 


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


class CurrentElementSelector(XPathSelector):
    def __init__(self):
        super(CurrentElementSelector, self).__init__()


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

        if cut(xPath, marker.p) == ".":
            marker.p += 1
            expression.selectors.append(CurrentElementSelector())

        while marker.p < len(xPath):
            """
            if cut(xPath, marker.p, 2) == "..":
                marker.p += 2
                expression.selectors.append(SuperelementSelector())
                continue
            """
            if cut(xPath, marker.p, 2) == "//":
                marker.p += 2

                elementName = self._getElementName(xPath, marker)

                if elementName != None:
                    if len(expression.selectors) == 0:
                        expression.selectors.append(RootElementSelector())
                    else:    
                        expression.selectors.append(SubelementsSelector(True))

                    expression.selectors.append(ElementNameSelector(elementName))
                    continue
                elif cut(xPath, marker.p) == "*":
                    marker.p += 1
                    
                    if len(expression.selectors) == 0:
                        expression.selectors.append(RootElementSelector())

                    expression.selectors.append(SubelementsSelector(True))
                    continue
            
            if cut(xPath, marker.p) == "/":
                marker.p += 1

                elementName = self._getElementName(xPath, marker)

                if elementName != None:
                    if len(expression.selectors) == 0:
                        expression.selectors.append(RootElementSelector())
                    else:    
                        expression.selectors.append(SubelementsSelector(False))

                    expression.selectors.append(ElementNameSelector(elementName))
                    continue
                elif cut(xPath, marker.p) == "*":
                    marker.p += 1

                    if len(expression.selectors) == 0:
                        expression.selectors.append(RootElementSelector())

                    expression.selectors.append(SubelementsSelector(False))
                    continue
                elif marker.p == len(xPath):
                    if len(expression.selectors) == 0:
                        expression.selectors.append(RootElementSelector())
                    continue 
            
            if cut(xPath, marker.p) == "@":
                marker.p += 1

                attributeName = self._getAttributeName(xPath, marker)

                if attributeName != None:
                    expression.selectors.append(AttributesSelector())
                    expression.selectors.append(AttributeNameSelector(attributeName))
                    continue
                elif cut(xPath, marker.p) == "*":
                    marker.p += 1

                    expression.selectors.append(AttributesSelector())
                    continue
            
            raise XPathParsingError("Could not parse XPath expression at position {}, '{}'.".format(marker.p, xPath[marker.p: marker.p + 20]))

        return expression

    def _getElementName(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in XPathParser._elementNameCharacters:
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

            if c in XPathParser._attributeNameCharacters:
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t

parser = XPathParser()

class XPathResolver(object):

    def applyXPathToElement(self, element, xpath):
        logger.debug("Applying XPath '{}' to {}.".format(xpath, element))

        expression = parser.parseXPath(xpath)

        logger.debug("Parsed XPath as '{}'.".format(expression))

        return self._applyExpressionToList([element], expression)

    def _applyExpressionToList(self, _list, expression):

        while len(expression.selectors) > 0:
            firstSelector = expression.selectors.pop(0)

            logger.debug("Applying selector {}.".format(firstSelector))

            _list = self._applySelectorToList(_list, firstSelector)

            logger.debug("List now has {} items.".format(len(_list)))
            logger.debug("List: {}.".format([(i.name if hasattr(i, "name") else i.text) for i in _list]))

        return _list 

    def _applySelectorToList(self, _list, selector):
        if isinstance(selector, ElementNameSelector):
            return [element for element in _list if hasattr(element, "name") and element.name == selector.elementName]

        if isinstance(selector, SubelementsSelector):
            subelements = []

            for element in _list:
                if hasattr(element, "subelements"):
                    subelements += element.subelements 

            subelements = [element for element in subelements if hasattr(element, "name")]

            return subelements 

        if isinstance(selector, AttributesSelector):
            attributes = []

            for element in _list:
                if hasattr(element, "attributes"):
                    attributes += element.attributes 

            return attributes 

        if isinstance(selector, AttributeNameSelector):
            return [attribute for attribute in _list if attribute.name == selector.attributeName]

        if isinstance(selector, RootElementSelector):
            return [_list[0].root]

resolver = XPathResolver()
