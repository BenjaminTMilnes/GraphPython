from graphe.commonfunctions import *
import logging

logging.basicConfig(level=logging.DEBUG)

#compileGrapheDocument("examples/example1.graphe.xml", "examples/example1.morphe",  "examples/example1.docx", "docx")
#compileGrapheDocument("examples/example1.graphe.xml", "examples/example1.morphe",  "examples/example1.tex", "latex")
#compileGrapheDocument("examples/example1.graphe.xml", "examples/example1.morphe",  "examples/example1.md", "md")
compileGrapheDocument("examples/example1.graphe.xml", "examples/example1.morphe",  "examples/example1.pdf", "pdf")
