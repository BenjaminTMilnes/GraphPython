import unittest
from parameterized import parameterized

from graph.xml import *


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
        ["id='box1'", "id", "box1"],
        [" id = 'box1' ", "id", "box1"],
        ["   id   =   'box1'   ", "id", "box1"],
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
        ["<heading1 id='box1'></heading1>", "heading1", [["id", "box1"]], 0, ""],
        ["<heading1 id='box1' style='font-colour: red;'></heading1>", "heading1", [["id", "box1"], ["style", "font-colour: red;"]], 0, ""],
        ["<heading1>This is some text</heading1>", "heading1", [], 1, "This is some text"],
        ["<heading1 id=\"box1\" style=\"font-colour: red;\">This is some text</heading1>", "heading1", [["id", "box1"], ["style", "font-colour: red;"]], 1, "This is some text"],
        ["<heading1>This is some text <b>and some more text</b></heading1>", "heading1", [], 2, "This is some text and some more text"],
    ])
    def test_parse_element(self, text, name, attributes, numberOfSubelements, innerText):
        parser = XMLParser()

        e = parser._getElement(text, Marker())

        self.assertTrue(isinstance(e, XMLElement))
        self.assertEqual(e.name, name)
        self.assertEqual(len(e.attributes), len(attributes))
        self.assertEqual(len(e.subelements), numberOfSubelements)
        self.assertEqual(e.innerText, innerText)

    def test_parse_example_1(self):
        parser = XMLParser()

        d = parser.parseFromFile("examples/example1.graph.xml")

        self.assertEqual(d.root.name, "document")
        self.assertEqual(d.root.getAttributeValue("version"), "0.1")
        self.assertTrue(isinstance(d.root.subelements[0], XMLElement))
        self.assertEqual(d.root.subelements[0].name, "title")
        self.assertEqual(d.root.subelements[0].innerText, "The Tragedy of Darth Plagueis the Wise")
        self.assertEqual(d.root.subelements[2].name, "subtitle")
        self.assertEqual(d.root.subelements[2].innerText, "Did you ever hear it?")
        self.assertEqual(d.root.subelements[4].name, "abstract")
        self.assertEqual(d.root.subelements[4].innerText, "It's not a story the Jedi would teach you.")
        self.assertEqual(d.root.subelements[6].name, "keywords")
        self.assertEqual(d.root.subelements[6].innerText, "tragedy, Plagueis, Darth Plagueis, Sith")

        self.assertEqual(len(d.root.getSubelementsByName("contributor")), 1)
        self.assertEqual(d.root.getSubelementsByName("contributor")[0].getSubelementsByName("name")[0].innerText, "Sheev Palpatine")


if __name__ == "__main__":
    unittest.main()
