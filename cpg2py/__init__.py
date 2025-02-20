import os
from pathlib import Path
from csv import DictReader
from .cpg import _Graph
from .abc import *

def __remove_null_bytes(file_path: Path) -> Path:
    """Create a new clean file without NULL bytes and return its path."""
    clean_path = file_path.with_suffix(".clean.csv")  # Create a temp clean file
    if clean_path.exists(): os.remove(clean_path)
    with open(file_path, "rb") as f:
        content = f.read().replace(b"\x00", b"")  # Remove NULL bytes
    with open(clean_path, "wb") as f:
        f.write(content)
    return clean_path

def cpg_graph(node_csv: Path, edge_csv: Path) -> _Graph: 
    # Clean files before reading
    tmp_node_csv = __remove_null_bytes(node_csv)
    storage = Storage()
    with open(tmp_node_csv, 'r') as n_file: 
        reader = DictReader(n_file, delimiter='\t')
        for node_props in reader: 
            nid = node_props.get("id:int", None) 
            if nid is None: node_props.get("id") 
            if not storage.add_node(nid): 
                print(f"Node {nid} already exists in the graph")
            if not storage.set_node_props(nid, node_props): 
                print(f"Failed to set properties for node {nid}")
    if tmp_node_csv.exists(): os.remove(tmp_node_csv)
    tmp_edge_csv = __remove_null_bytes(edge_csv)
    with open(tmp_edge_csv, 'r') as f:
        reader = DictReader(f, delimiter='\t')
        for edge_props in reader: 
            f_nid = str(edge_props.get("start", None) )
            if f_nid is None: f_nid = str(edge_props.get("start:str"))
            t_nid = str(edge_props.get("end", None))
            if t_nid is None: t_nid = str(edge_props.get("end:str"))
            e_type = str(edge_props.get("type", None))
            if e_type is None: e_type = str(edge_props.get("type:str"))
            edge_id = (f_nid, t_nid, e_type)
            if not storage.add_edge(edge_id): 
                print(f"Edge {f_nid} -> {t_nid} already exists in the graph")
            if not storage.set_edge_props(edge_id, edge_props): 
                print(f"Failed to set properties for edge {edge_id}")
    if tmp_edge_csv.exists(): os.remove(tmp_edge_csv)
    return _Graph(storage)


__all__ = ['cpg_graph', 'AbcGraphQuerier', 'AbcNodeQuerier', 'AbcEdgeQuerier', 'Storage']