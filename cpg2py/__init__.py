from pathlib import Path
from csv import DictReader
from .cpg import _Graph
from .abc import *

def cpg_graph(node_csv: Path, edge_csv: Path) -> _Graph: 
    storage = Storage()
    with open(node_csv, 'r') as n_file: 
        reader = DictReader(f, delimiter='\t')
        for node_props in reader: 
            nid = node_props.get("id:int", None) 
            if nid is None: node_props.get("id") 
            if not storage.add_node(nid): 
                print(f"Node {nid} already exists in the graph")
            if not storage.set_node_props(nid, node_props): 
                print(f"Failed to set properties for node {nid}")
    with open(edge_csv, 'r') as f:
        reader = DictReader(f, delimiter='\t')
        for edge_props in reader: 
            f_nid = edge_props.get("start", None) 
            if f_nid is None: f_nid = edge_props.get("start:str")
            t_nid = edge_props.get("end", None)
            if t_nid is None: t_nid = edge_props.get("end:str")
            e_type = edge_props.get("type", None)
            if e_type is None: e_type = edge_props.get("type:str")
            if not storage.add_edge(f_nid, t_nid, e_type): 
                print(f"Edge {f_nid} -> {t_nid} already exists in the graph")
            if not storage.set_edge_props(f_nid, t_nid, e_type, edge_props): 
                print(f"Failed to set properties for edge {f_nid} -> {t_nid}")
    return _Graph(storage)


__all__ = ['cpg_graph', 'AbcGraphQuerier', 'AbcNodeQuerier', 'AbcEdgeQuerier', 'Storage']