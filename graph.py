#!/usr/bin/env python
# coding: utf-8

from graphviz import Digraph
from itertools import combinations

g = Digraph()

attr = {"color": "orange"}

path_nodes = [
    "gender",
    "early stimulation",
    "early skills",
    "exposure",
    "motivation",
    "advanced skills",
]

for node in path_nodes:
    g.node(node, _attributes=attr)

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

path_edges = set(edges) & set(
    list(combinations(path_nodes, 2)) + list(combinations(reversed(path_nodes), 2))
) - set([("gender", "motivation"), ("gender", "exposure")])

for edge in path_edges:
    g.edge(*edge, _attributes=attr)

for edge in set(edges) - path_edges:
    g.edge(*edge)
