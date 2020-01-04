import unittest
from parameterized import parameterized

from graphe.xml import *


class TestXML(unittest.TestCase):

    @parameterized.expand([
        ["id", "id"],
        ["url", "url"],
        ["id3", "id3"],
        ["id123", "id123"],
        ["id_id", "id_id"],
        ["id-id", "id-id"],
        ["id-id-123_123", "id-id-123_123"],
        ["id123::", "id123"],
        ["id123!!", "id123"],
    ])
    def test_parse_attribute_name(self, text, name):
        parser = XMLParser()

        n = parser._getAttributeName(text, Marker())

        self.assertEqual(n, name)

    @parameterized.expand([
        ["id=\"box1\"", "id", "box1"],
        [" id = \"box1\" ", "id", "box1"],
        ["   id   =   \"box1\"   ", "id", "box1"],
    ])
    def test_parse_attribute(self, text, name, value):
        parser = XMLParser()

        a = parser._getAttribute(text, Marker())

        self.assertTrue(isinstance(a, XMLAttribute))
        self.assertEqual(a.name, name)
        self.assertEqual(a.value, value)

    @parameterized.expand([
        ["<heading1></heading1>", "heading1", [], 0, ""],
        ["<heading1 id=\"box1\"></heading1>", "heading1", [["id", "box1"]], 0, ""],
        ["<heading1 id=\"box1\" style=\"font-colour: red;\"></heading1>", "heading1", [["id", "box1"], ["style", "font-colour: red;"]], 0, ""],
        ["<heading1>This is some text</heading1>", "heading1", [], 1, "This is some text"],
        ["<heading1 id=\"box1\" style=\"font-colour: red;\">This is some text</heading1>", "heading1", [["id", "box1"], ["style", "font-colour: red;"]], 1, "This is some text"],
        ["<heading1>This is some text <b>and some more text</b></heading1>", "heading1", [], 2, "This is some text "],
    ])
    def test_parse_element(self, text, name, attributes, n, t):
        parser = XMLParser()

        e = parser._getElement(text, Marker())

        self.assertTrue(isinstance(e, XMLElement))
        self.assertEqual(e.name, name)
        self.assertEqual(len(e.attributes), len(attributes))
        self.assertEqual(len(e.subelements), n)
        if n > 0:
            self.assertEqual(e.subelements[0].text, t)


if __name__ == "__main__":
    unittest.main()
