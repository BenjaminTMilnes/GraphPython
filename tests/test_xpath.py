import unittest
from parameterized import parameterized

from graph.xml import *


class TestXPath(unittest.TestCase):

    @parameterized.expand([
        ["/document/title", 4],
        ["/document/sections/section", 6],
        ["/document/sections/*", 5],
        ["/document//p", 4],
        ["/document//section//p", 6],
        ["/document//section@ptr", 6],
        ["/document//section@*", 5],
    ])
    def test_parse_xpath(self, xpath, numberOfSelectors):
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), numberOfSelectors)
        self.assertEqual(str(expression), xpath)


    @parameterized.expand([
        ["/document/title", "The Tragedy of Darth Plagueis the Wise"],
    ])
    def test_xpath(self, xpath, value):
        d = XMLDocument.load("examples/example1.graph.xml")

        #self.assertEqual(d.findByXPath(xpath)[0].innerText, value)


if __name__ == "__main__":
    unittest.main()