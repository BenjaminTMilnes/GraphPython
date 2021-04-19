# GraphPython

Graph, from *Graphe*, a Greek word meaning 'writing', 'the art of writing'.

---

Graph is a mark-up language used for describing the content of printable documents. Graph is an XML-based language with a lot of similarities to HTML - many of the XML elements have the same name - but with many extra features which are very useful for printed documents.

This repository contains a Python implementation of Graph.

## An example Graph document

```xml

<?xml version="1.0" encoding="utf-8"?>
<document>
    <title>Example Document</title>
    <subtitle>written in Graph</subtitle>
    <keywords>graph, example, document</keywords>
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