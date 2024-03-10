import networkx as nx
from pyvis.network import Network
import json

def toNetwork(data: dict)->  nx.DiGraph:
    nt = nx.DiGraph()

    def checkKey(name):
        if name not in nt:
            nt.add_node(name, size=40)

    for node in data:
        checkKey(node)
        for child in data[node]:
            checkKey(child)
            nt.add_edge(node,child)
    return nt

def ntw_pyvis(ntx:nx.DiGraph):
    net = Network(width="1000px",height="1000px", directed=True)
    for node in ntx.nodes:
        net.add_node(node, **{"label":node},)

    for edge in ntx.edges:
        net.add_edge(edge[0], edge[1], width=1)
    net.show('graph.html')

with open("cg.json","r") as f:
    data = json.load(f)

ntw_pyvis(toNetwork(data))