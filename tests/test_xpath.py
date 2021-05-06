import unittest
from parameterized import parameterized

from graph.xml import *

import logging 


class TestXPath(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    @parameterized.expand([
        ["///"],
        ["////"],
        ["/////"],
        ["/aaa///aaa"],
        ["/aaa//aaa/aaa//aaa///aaa"],
        ["//@@"],
        ["//@@@"],
        ["/aaa/aaa@bbb@bbb"],
        ["/aaa/aaa@bbb@bbb@bbb"],
        ["..."],
        ["...."],
        ["....."],
        ["/aaa//aaa/../aaa/.../aaa"],
        ["\\"],
        ["\\aaa"],
        ["\\aaa\\"],
        ["\\\\"],
        ["\\\\aaa"],
        ["\\\\aaa\\\\"],
        ["/aaa#bbb"],
        ["/aaa!bbb"],
        ["/aaa?bbb"],
        ["/aaa£bbb"],
        ["/aaa$bbb"],
        ["/aaa^bbb"],
        ["/aaa&bbb"],
        ["/aaa=bbb"],
        ["/aaa:bbb"],
        ["/aaa;bbb"],
        ["/aaa~bbb"],
    ])
    def test_invalid_xpath(self, xpath):
        with self.assertRaises(graph.xpath.XPathParsingError) as context:
            graph.xpath.parser.parseXPath(xpath)

    def test_parse_xpath_2(self):
        xpath = "/"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 1)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertEqual(str(expression), xpath)

    def test_parse_xpath_3(self):
        xpath = "/document"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 2)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertEqual(str(expression), xpath)
        
    def test_parse_xpath_4(self):
        xpath = "/document/*"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 3)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertEqual(str(expression), xpath)
              
    def test_parse_xpath_5(self):
        xpath = "/document/title"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 4)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "title")
        self.assertEqual(str(expression), xpath)
               
    def test_parse_xpath_6(self):
        xpath = "/document/sections"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 4)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "sections")
        self.assertEqual(str(expression), xpath)
              
    def test_parse_xpath_7(self):
        xpath = "/document/sections/*"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 5)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "sections")
        self.assertTrue(isinstance(expression.selectors[4], graph.xpath.SubelementsSelector))
        self.assertEqual(str(expression), xpath)
            
    def test_parse_xpath_8(self):
        xpath = "/document/sections/section"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 6)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "sections")
        self.assertTrue(isinstance(expression.selectors[4], graph.xpath.SubelementsSelector))
        self.assertTrue(isinstance(expression.selectors[5], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[5].elementName, "section")
        self.assertEqual(str(expression), xpath)
              
    def test_parse_xpath_9(self):
        xpath = "/document//p"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 4)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertEqual(expression.selectors[2].anyDepth, True)
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "p")
        self.assertEqual(str(expression), xpath)
              
    def test_parse_xpath_10(self):
        xpath = "/document//section//p"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 6)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertEqual(expression.selectors[2].anyDepth, True)
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "section")
        self.assertTrue(isinstance(expression.selectors[4], graph.xpath.SubelementsSelector))
        self.assertEqual(expression.selectors[4].anyDepth, True)
        self.assertTrue(isinstance(expression.selectors[5], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[5].elementName, "p")
        self.assertEqual(str(expression), xpath)
              
    def test_parse_xpath_11(self):
        xpath = "/document//section@*"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 5)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertEqual(expression.selectors[2].anyDepth, True)
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "section")
        self.assertTrue(isinstance(expression.selectors[4], graph.xpath.AttributesSelector))
        self.assertEqual(str(expression), xpath)
              
    def test_parse_xpath_12(self):
        xpath = "/document//section@ptr"
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), 6)
        self.assertTrue(isinstance(expression.selectors[0], graph.xpath.RootElementSelector))
        self.assertTrue(isinstance(expression.selectors[1], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[1].elementName, "document")
        self.assertTrue(isinstance(expression.selectors[2], graph.xpath.SubelementsSelector))
        self.assertEqual(expression.selectors[2].anyDepth, True)
        self.assertTrue(isinstance(expression.selectors[3], graph.xpath.ElementNameSelector))
        self.assertEqual(expression.selectors[3].elementName, "section")
        self.assertTrue(isinstance(expression.selectors[4], graph.xpath.AttributesSelector))
        self.assertTrue(isinstance(expression.selectors[5], graph.xpath.AttributeNameSelector))
        self.assertEqual(expression.selectors[5].attributeName, "ptr")
        self.assertEqual(str(expression), xpath)

    def test_xpath_1(self):
        d = XMLDocument.load("examples/example1.graph.xml")

        self.assertEqual(d.findByXPath("/")[0].name, "document")

    def test_xpath_2(self):
        d = XMLDocument.load("examples/example1.graph.xml")

        self.assertEqual(d.findByXPath("/document")[0].name, "document")

    def test_xpath_3(self):
        d = XMLDocument.load("examples/example1.graph.xml")

        self.assertEqual(len(d.findByXPath("/document/*")), 8)

    def test_xpath_4(self):
        d = XMLDocument.load("examples/example1.graph.xml")

        self.assertEqual(d.findByXPath("/document/title")[0].innerText, "The Tragedy of Darth Plagueis the Wise")
        
    def test_xpath_5(self):
        d = XMLDocument.load("examples/example1.graph.xml")

        self.assertEqual(d.findByXPath("/document@version")[0].value, "0.1")


if __name__ == "__main__":
    unittest.main()