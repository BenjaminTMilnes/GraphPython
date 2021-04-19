from graph.commonfunctions import *
import logging

logging.basicConfig(level=logging.DEBUG)

compileGraphDocument("examples/example1.graph.xml", "examples/example1.morph",  "examples/example1.docx", "docx")
#compileGraphDocument("examples/example1.graph.xml", "examples/example1.morph",  "examples/example1.tex", "latex")
#compileGraphDocument("examples/example1.graph.xml", "examples/example1.morph",  "examples/example1.md", "md")
#compileGraphDocument("examples/example1.graph.xml", "examples/example1.morph",  "examples/example1.pdf", "pdf")
