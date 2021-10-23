from owlready2 import *
from rdflib import Graph

eupont = Graph()

eupont.parse("http://elite.polito.it/ontologies/eupont-ifttt.owl", format='xml')

# number of triples
print(len(eupont))