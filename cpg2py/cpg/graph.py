
from __future__ import annotations

from .edge import _Edge
from .node import _Node
from ..abc import AbcGraphQuerier, Storage 

from typing import Callable, Iterable, Optional
import json, functools

class _Graph(AbcGraphQuerier): 
    '''
    OPG is Object Property Diagram used by ODgen and FAST
    '''
    __EdgeCondition = Callable[[_Edge], bool]
    __always_true = lambda _: True

    def __init__(self, target: Storage) -> None:
        super().__init__(target)
        return None

    def node(self, whose_id_is: str) -> Optional[_Node]:
        try: 
            return _Node(self.storage, whose_id_is)
        except Exception as e: print(
            f'✘ {_Graph} ERROR:'
            f'Cannot find node with id {whose_id_is}.'
            f'(exception is {e})'
        )
        return None
    
    def edge(self, fid: str, tid: str, eid:str) -> Optional[_Edge]: 
        try: 
            return _Edge(self.storage, fid, tid, eid)
        except Exception as e: print(
            f'✘ {_Graph} ERROR:'
            f'Cannot find edge from {fid} to {tid}, and eid is {str(eid)}.'
            f'(exception is {e})'
        )
        return None
    
    @functools.lru_cache()
    def topfile_node(self, of_nid: str) -> _Node: 
        '''
        find the top file node from the input node.
        '''
        of_node = self.node(of_nid)
        if of_node.type == "File": return of_node
        if 'TOPLEVEL_FILE' in of_node.flags: return of_node
        parents = self.prev(of_node, lambda e: e.type in ["PARENT_OF", "ENTRY", "EXIT"])
        for pre in parents: 
            top_file = self.topfile_node(pre.id)
            if top_file is not None: return top_file
        raise Exception(f'❌ INNER ERROR(500): CANNOT FIND THE TOPFILE.')
    
    def succ(self, of: _Node, who_satisifies: __EdgeCondition = __always_true) -> Iterable[_Node]: 
        '''
        return the next nodes connected with the input one.
        '''
        return super().succ(of.id, who_satisifies)
    
    def prev(self, of, who_satisifies = __always_true) -> Iterable[_Node]:
        '''
        return the previous nodes connected with the input one.
        '''
        return super().prev(of, who_satisifies)


    def children(self, of: _Node, extra: __EdgeCondition = __always_true) -> Iterable[_Node]: 
        '''
        return the next nodes connected with the input one.
        The edge type between them is PARENT_OF 
        '''
        return self.succ(of, lambda e: extra(e) and (e.type == "PARENT_OF"))

    def parent(self, of: _Node, extra:__EdgeCondition = __always_true) -> Iterable[_Node]: 
        '''
        return the prev nodes connected with the input one.
        The edge type between them is PARENT_OF 
        '''
        return self.prev(of, lambda e: extra(e) and (e.type == "PARENT_OF"))

    def flow_to(self, of: _Node, extra: __EdgeCondition = __always_true) -> Iterable[_Node]: 
        '''
        return the next nodes connected with the input one.
        The edge type between them is FLOW_TO 
        '''
        return self.succ(of, lambda e: extra(e) and (e.type == "FLOWS_TO"))

    def flow_from(self, of: _Node, extra: __EdgeCondition = __always_true) -> Iterable[_Node]:
        '''
        return the previous nodes connected with the input one.
        The edge type between them is FLOW_TO 
        '''
        return self.prev(of, lambda e: extra(e) and (e.type == "FLOWS_TO"))
    
pass
