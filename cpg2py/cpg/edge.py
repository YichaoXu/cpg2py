from __future__ import annotations
from typing import Optional, Tuple
from ..abc import AbcGraphQuerier, AbcEdgeQuerier

class _Edge(AbcEdgeQuerier): 
    
    def __init__(self, graph: AbcGraphQuerier, f_nid: str, t_nid: str, e_type: str) -> None:
        super().__init__(graph, f_nid, t_nid, e_type)
        return None
    
    @property
    def id(self) -> Tuple[str, str, str]: 
        return self.edge_id

    @property
    def start(self) -> Optional[int]:
        start_str = str(self.get_property('start', 'start:START_ID'))
        return int(start_str) if start_str.isnumeric() else int(self.__from_id)

    @property
    def end(self) -> Optional[int]: 
        end_str = str(self.get_property('end', 'end:END_ID'))
        return int(end_str) if end_str.isnumeric() else int(self.__to_id) 

    @property
    def type(self) -> Optional[str]: 
        return self.get_property('type', 'type:TYPE')
    
    @property
    def var(self) -> Optional[str]: 
        return self.get_property('var')