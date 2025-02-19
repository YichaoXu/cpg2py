import os
from .cpg2py import cpg_graph


example_path = os.path.join(os.path.dirname(__file__), "_example")
node_csv_path = os.path.join(example_path, "nodes.csv")
rels_csv_path = os.path.join(example_path, "rels.csv")

graph = cpg_graph(node_csv_path, rels_csv_path)

for e in graph.edges(): 
    print(e.edge_id)

