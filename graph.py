#!/usr/bin/env python
# coding: utf-8

from graphviz import Digraph
import networkx as nx
from itertools import combinations


"""
---------------------
Define causal effects
---------------------
"""

edges = (
    (
        [
            ("family", v)
            for v in [
                "genetics",
                "early stimulation",
                "exposure",
                "motivation",
            ]
        ]
        + [
            ("genetics", v)
            for v in [
                "early skills",
                "gender",
                "early interests",
                "advanced skills",
            ]
        ]
    )
    + [("gender", v) for v in ["early stimulation", "motivation", "exposure"]]
    + [("early skills", v) for v in ["exposure", "motivation", "advanced skills"]]
    + [("early interests", v) for v in ["early stimulation", "motivation"]]
    + [("early stimulation", v) for v in ["early skills", "motivation"]]
    + [
        ("motivation", "exposure"),
        ("exposure", "advanced skills"),
    ]
)


"""
---------------------
Isolate relevant path
---------------------
"""

path_nodes = {
    "gender",
    "early stimulation",
    "early skills",
    "exposure",
    "motivation",
    "advanced skills",
}

def subgraph_edges(all_edges, selected_nodes, exclude=set()):
    
    graph = nx.DiGraph()
    graph.add_edges_from(all_edges)
    subgraph = nx.subgraph(graph, selected_nodes)
    
    return set(subgraph.edges()) - exclude


path_edges = subgraph_edges(edges, path_nodes, exclude={("gender", "motivation"),
         ("gender", "exposure"),
         ("early stimulation", "motivation")})


"""
------------------------
Construct causal diagram
------------------------
"""

g = Digraph()
attr = {"color": "orange"}

for node in path_nodes:
    g.node(node, _attributes=attr)

for edge in path_edges:
    g.edge(*edge, _attributes=attr)

for edge in set(edges) - path_edges:
    g.edge(*edge)
    
    
"""
---------------------
Construct subgraph 1.
---------------------
"""
    
path_1 = {"family", "genetics", "early interests", "gender", "early stimulation", "early skills"}
g_1_edges = subgraph_edges(edges, path_1)
g_1 = Digraph()

for node in path_1 & path_nodes:
    g_1.node(node, _attributes=attr)
    
for edge in g_1_edges & path_edges:
    g_1.edge(*edge, _attributes=attr)
    
for edge in g_1_edges - path_edges:
    g_1.edge(*edge)
    

"""
---------------------
Construct subgraph 2.
---------------------
"""

path_2 = {"early skills", "motivation", "exposure", "advanced skills"}
g_2 = Digraph()
g_2.edges(subgraph_edges(edges, path_2))
