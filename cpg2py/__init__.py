from csv import DictReader
from pathlib import Path
from .cpg import _Graph
from .abc import *

def cpg_graph(node_csv: Path, edge_csv: Path) -> "_Graph":
    storage = Storage()
    with open(node_csv, 'r') as n_file: 
        reader = DictReader(n_file, delimiter='\t')
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
            f_nid = str(edge_props.get("start", None) )
            if f_nid is None: f_nid = str(edge_props.get("start:str"))
            t_nid = str(edge_props.get("end", None))
            if t_nid is None: t_nid = str(edge_props.get("end:str"))
            e_type = str(edge_props.get("type", None))
            if e_type is None: e_type = str(edge_props.get("type:str"))
            edge_id = (f_nid, t_nid, e_type)
            if not storage.contains_node(edge_id[0]): 
                storage.add_node(edge_id[0])
                print(f"WARN: node {edge_id[0]} does not exists")
            if not storage.contains_node(edge_id[1]): 
                storage.add_node(edge_id[1])
                print(f"WARN: node {edge_id[1]} does not exists")
            if not storage.add_edge(edge_id): 
                print(f"WARN: Edge {f_nid} -> {t_nid} already exists in the graph")
            if not storage.set_edge_props(edge_id, edge_props): 
                print(f"WARN: Failed to set properties for edge {edge_id}")
    return _Graph(storage)


__all__ = ['cpg_graph', 'AbcGraphQuerier', 'AbcNodeQuerier', 'AbcEdgeQuerier', 'Storage']