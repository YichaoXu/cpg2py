from __future__ import annotations
import abc
from .storage import Storage
from typing import Any, Dict, Optional, Tuple

class AbcEdgeQuerier(abc.ABC): 
    
    def __init__(self, graph: Storage, f_nid: str, t_nid: str, e_type: int = 0) -> None:
        self.__graph: Storage = graph
        self.__edge_id: Tuple[str, str, str] = (str(f_nid), str(t_nid), str(e_type))
        if not graph.contains_edge(self.__edge_id): 
            raise Exception('CANNOT FIND THE NODE ID {nid} IN GRAPH')
        return None

    @property
    def edge_id(self) -> Tuple[str, str, int]:
        return self.__edge_id
    
    @property
    def from_nid(self) -> str: 
        return self.__edge_id[0]

    @property
    def to_nid(self) -> str:
        return self.__edge_id[1]
    
    @property
    def edge_type(self) -> str: 
        return self.__edge_id[0]
    
    @property
    def properties(self) -> Optional[Dict[str, Any]]: 
        return self.__graph.get_edge_props(self.__edge_id)
    
    def get_property(self, *prop_names: str) -> Optional[Any]: 
        prop_values = (self.__graph.get_edge_prop(self.__edge_id, p_name) for p_name in prop_names)
        return next((value for value in prop_values if value is not None), None)

pass