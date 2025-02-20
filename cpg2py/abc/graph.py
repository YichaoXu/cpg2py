
from __future__ import annotations

from .edge import AbcEdgeQuerier
from .node import AbcNodeQuerier

from typing import Callable, Deque, List, Optional, Iterable
from collections import deque
from .storage import Storage
import abc

class AbcGraphQuerier(abc.ABC): 

    __NodeCondition = Callable[[AbcNodeQuerier], bool]
    __EdgeCondition = Callable[[AbcEdgeQuerier], bool]
    __always_true = lambda _: True

    __NodesResult = Iterable[AbcNodeQuerier]
    __EdgesResult = Iterable[AbcEdgeQuerier]

    def __init__(self, target: Storage, maxdepth: int=-1) -> None:
        self.__graph: Storage = target
        self.__maxdepth: int = maxdepth

    @property
    def storage(self) -> Storage: 
        return self.__graph

    @abc.abstractmethod
    def node(self, whose_id_is: str) -> Optional[AbcNodeQuerier]: 
        raise NotImplementedError

    @abc.abstractmethod
    def edge(self, fid, tid, eid) -> Optional[AbcEdgeQuerier]: 
        raise NotImplementedError

    def nodes(self, who_satisifies: __NodeCondition=__always_true)-> __NodesResult: 
        for nid in self.__graph.get_nodes(): 
            cur_node = self.node(whose_id_is=nid)
            if cur_node and who_satisifies(cur_node): yield cur_node 
        pass
    
    def first_node(self, who_satisifies: __NodeCondition=__always_true)-> Optional[AbcNodeQuerier]:
        return next(self.nodes(who_satisifies), None) 

    def edges(self, who_satisifies: __EdgeCondition = __always_true) -> __EdgesResult: 
        for from_id, to_id, edge_id in self.__graph.get_edges(): 
            cur_edge = self.edge(from_id, to_id, edge_id)
            if cur_edge and who_satisifies(cur_edge): yield cur_edge
        pass 

    def succ(self, of: AbcNodeQuerier, who_satisifies: __EdgeCondition = __always_true) -> __NodesResult: 
        for src, dst, type in self.__graph.out_edges(of.id):
            if not who_satisifies(self.edge(src, dst, type)): continue
            yield self.node(whose_id_is=dst)
        pass

    def prev(self, of: AbcNodeQuerier, who_satisifies: __EdgeCondition = __always_true) -> __NodesResult: 
        for src, dst, type in self.__graph.in_edges(of.id):
            if not who_satisifies(self.edge(src, dst, type)): continue
            yield self.node(whose_id_is=src)
        pass

    def __bfs_search(self, root: AbcNodeQuerier, condition: __EdgeCondition, reverse: bool) -> __NodesResult: 
        '''
        return the nodes from (any edge relation) src node by the bfs order (src node will not included)
        '''
        if root is None: return 
        visited_nids: List[str] = list()
        nodes_queue: Deque[AbcNodeQuerier] = deque([root, None])
        depth = self.__maxdepth
        while depth != 0 and len(nodes_queue) > 1: 
            cur_node = nodes_queue.popleft()
            if cur_node == None: 
                nodes_queue.append(None)
                depth -= 1
            elif cur_node.id not in visited_nids:
                visited_nids.append(cur_node.id)
                if not reverse: n_nodes = self.succ(cur_node, condition)
                else: n_nodes = self.prev(cur_node, condition)
                nodes_queue.extend(n_nodes)
                if root.id != cur_node.id: yield cur_node
        pass

    def descendants(self, src: AbcNodeQuerier, condition: __EdgeCondition = __always_true) -> __NodesResult: 
        '''
        return the result of descendants from (any edge relation) src node by the bfs order (src node will not included)
        '''
        return self.__bfs_search(src, condition, reverse=False)

    def ancestors(self, src: AbcNodeQuerier, condition: __EdgeCondition = __always_true) -> __NodesResult:
        '''
        return the result of ancestors from (any edge relation) src node by the bfs order (src node will not included)
        '''
        return self.__bfs_search(src, condition, reverse=True)

pass
    
