# GraphePython

Graphe, from *Graphe*, a Greek word meaning 'writing', 'the art of writing'.

---

Graphe is a mark-up language used for describing the content of printable documents. Graphe is an XML-based language with a lot of similarities to HTML - many of the XML elements have the same name - but with many extra features which are very useful for printed documents.

This repository contains a Python implementation of Graphe.

## An example Graphe document

```xml

<?xml version="1.0" encoding="utf-8"?>
<document>
    <title>Example Document</title>
    <subtitle>written in Graphe</subtitle>
    <keywords>graphe, example, document</keywords>
    <contributors>
        <contributor type="author">
            <name>B. T. Milnes</name>
            <website>https://github.com/BenjaminTMilnes/</website>
            <email-address>example@example.com</email-address>
        </contributor>
    </contributors>
    <sections>
        <section>
            <h1>This is a heading</h1>
            <p>This is a paragraph</p>
        </section>
    </sections>
</document>

```