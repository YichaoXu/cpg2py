from typing import Optional, Iterable, Dict


class Storage:
    """ A directed multi-graph implementation supporting multiple edges between nodes. """

    __NodeID = str
    __EdgeID = tuple[str, str, str]
    __Property = dict[str, any]

    def __init__(self):
        """ Initializes an empty directed graph. """
        self.__nodes = dict()
        self.__edges = dict() 
        self.__struct = dict()

    ################################ GRAPH STRUCTURE APIs ################################

    def add_node(self, nid: __NodeID) -> bool:
        """ Adds a node to the graph. """
        if nid in self.__nodes: return False
        self.__nodes[nid] = {}
        self.__struct[nid] = []
        return True
    
    def contains_node(self, nid: __NodeID) -> bool:
        """ Checks if a node exists in the graph. """
        return nid in self.__nodes

    def add_edge(self, eid: __EdgeID) -> bool:
        """ Adds a directed edge from `start` to `end` with an optional edge type. """
        if eid in self.__edges: return False
        if eid[0] not in self.__nodes: return False
        if eid[1] not in self.__nodes: return False
        self.__edges[eid] = {}
        self.__struct[eid[0]].append(eid)
        self.__struct[eid[1]].append(eid)
        return True
    
    def contains_edge(self, eid: __EdgeID) -> bool:
        """ Checks if an edge exists in the graph. """
        return eid in self.__edges
    
    def out_edges(self, nid: __NodeID) -> Iterable[__EdgeID]:
        """ Returns a list of outgoing edges from a given node. """
        return (eid for eid in self.__struct.get(nid) if eid[0] == nid)

    def in_edges(self, nid: __NodeID) -> Iterable[__EdgeID]:
        """ Returns a list of incoming edges to a given node. """
        return (eid for eid in self.__struct.get(nid) if eid[1] == nid)

    def successors(self, nid: __NodeID) -> Iterable[__NodeID]:
        """ Returns all successor nodes of a given node. """
        return (eid[1] for eid in self.__struct.get(nid) if eid[0] == nid)

    def predecessors(self, nid: __NodeID) -> Iterable[__NodeID]:
        """ Returns all predecessor nodes of a given node. """
        return (eid[0] for eid in self.__struct.get(nid) if eid[1] == nid)
    
    ################################ GRAPH PROPERTIES APIs ################################

    def set_node_props(self, node: __NodeID, props: __Property) -> bool:
        """ Sets the properties of a node. """
        if node not in self.__nodes: return False
        prev_data: dict = self.__nodes[node]
        self.__nodes[node] = prev_data.update(props)
        return True
    
    def get_node_props(self, node: __NodeID) -> Optional[__Property]:
        """ Returns the properties of a node. """
        return self.__nodes.get(node, None)
    
    def set_node_prop(self, node: __NodeID, key: str, value: any) -> bool:
        """ Sets the properties of a node. """
        if node not in self.__nodes: return False
        self.__nodes[node][key] = value
        return True
    
    def get_node_prop(self, node: __NodeID, key: str) -> Optional[any]:
        """ Returns the properties of a node. """
        return self.__nodes.get(node, {}).get(key, None)
    
    def set_edge_props(self, eid: __EdgeID, props: __Property) -> bool:
        """ Sets the properties of an edge. """
        if eid not in self.__edges: return False
        prev_data: dict = self.__edges[eid]
        self.__edges[eid] = prev_data.update(props)
        return True
    
    def get_edge_props(self, start, end, edge_type="") -> Optional[__Property]:
        """ Returns the properties of an edge. """
        return self.__edges.get((start, end, edge_type), {})
      
    def set_edge_prop(self, eid: __EdgeID, key: str, value: any) -> bool:
        """ Sets the properties of an edge. """
        if eid not in self.__edges: return False
        self.__edges[eid][key] = value
        return
    
    def get_edge_prop(self, eid: __EdgeID, key: str) -> Optional[__Property]:
        """ Returns the properties of an edge. """
        return self.__edges.get(eid, {}).get(key, None)

    def __repr__(self):
        """ Returns a string representation of the graph. """
        return f"MultiDiGraph(nodes={len(self.nodes)}, edges={len(self.get_edges())})"
    
    ################################ GRAPH COMMON APIs ################################

    def get_nodes(self) -> Iterable[__NodeID]:
        """ Returns a list of all nodes in the graph. """
        return self.__nodes.keys()

    def get_edges(self) -> Iterable[__EdgeID]:
        """ Returns a list of all edges in the graph. """
        return self.__edges.keys()
    
    def remove_node(self, nid: __NodeID) -> bool:
        """ Removes a node from the graph. """
        if nid not in self.__nodes: return False
        self.__nodes.pop(nid)
        for eid in self.__struct[nid]:
            self.__edges.pop(eid)
        return True
    
    def remove_edge(self, eid: __EdgeID) -> bool:
        """ Removes an edge from the graph. """
        if eid not in self.__edges: return False
        self.__struct[eid[0]].remove(eid)
        self.__struct[eid[1]].remove(eid)
        self.__edges.pop(eid)
        return True