from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

graph = GraphvizOutput()
graph.output_file = "file4.png"

with PyCallGraph(output=graph):
  print("Hello world")