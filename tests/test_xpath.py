import unittest
from parameterized import parameterized

from graph.xml import *

import logging 


class TestXPath(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    @parameterized.expand([
        ["/document/title", 5],
        ["/document/sections/section", 7],
        ["/document/sections/*", 6],
        ["/document//p", 5],
        ["/document//section//p", 7],
        ["/document//section@ptr", 7],
        ["/document//section@*", 6],
    ])
    def test_parse_xpath(self, xpath, numberOfSelectors):
        expression = graph.xpath.parser.parseXPath(xpath)

        self.assertEqual(len(expression.selectors), numberOfSelectors)
        self.assertEqual(str(expression), xpath)


    def test_xpath(self):
        d = XMLDocument.load("examples/example1.graph.xml")

        self.assertEqual(d.findByXPath("/document/title")[0].innerText, "The Tragedy of Darth Plagueis the Wise")


if __name__ == "__main__":
    unittest.main()