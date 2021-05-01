import unittest
from parameterized import parameterized

from graph.xml import *

import logging 


class TestXPath(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    @parameterized.expand([
        ["/", 1],
        ["/document", 2],
        ["/document/*", 3],
        ["/document/title", 4],
        ["/document/sections/section", 6],])
    #    ["/document/sections/*", 5],
    #    ["/document//p", 4],
    #    ["/document//section//p", 6],
    #    ["/document//section@ptr", 6],
    #    ["/document//section@*", 5],
    #])
    def test_parse_xpath(self, xpath, numberOfSelectors):
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), numberOfSelectors)
        self.assertEqual(str(expression), xpath)

"""
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
"""


if __name__ == "__main__":
    unittest.main()