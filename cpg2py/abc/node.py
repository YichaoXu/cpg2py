from typing import Any, Dict, Optional
from .storage import Storage
import abc

class AbcNodeQuerier(abc.ABC):  
    
    def __init__(self, graph: Storage, nid: str) -> None:
        self.__nid: str = str(nid)
        self.__graph: Storage = graph
        if not graph.contains_node(self.__nid): 
            raise Exception(f'CANNOT FIND THE NODE ID {nid} IN GRAPH')
        return None
    
    @property
    def node_id(self) -> str:
        return self.__nid

    @property
    def properties(self) -> Optional[Dict[str, Any]]: 
        return self.__graph.get_node_props(self.__nid)
    
    def get_property(self, *prop_names: str) -> Optional[Any]: 
        prop_values = (self.__graph.get_node_prop(self.__nid, p_name) for p_name in prop_names)
        return next((value for value in prop_values if value is not None), None)
    
pass