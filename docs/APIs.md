# **cpg2py: API Reference**

This document provides a full API reference for the `cpg2py` library.

---

## **🔹 Graph Structure APIs**
### **`cpg_graph(node_csv: Path, edge_csv: Path) -> _Graph`**
- Constructs a **multi-directed graph** from Joern CSV files (`nodes.csv`, `rels.csv`).

### **`class _Graph(AbcGraphQuerier)`**
- Represents the entire CPG graph.

#### **Graph-Level Queries**
- `node(whose_id_is: str) -> Optional[_Node]` → Get a node by ID.
- `edge(fid: str, tid: str, eid: str) -> Optional[_Edge]` → Get an edge by (source, target, type).
- `nodes(who_satisfies: Callable[[_Node], bool]) -> Iterable[_Node]` → Iterate over all nodes matching a condition.
- `edges(who_satisfies: Callable[[_Edge], bool]) -> Iterable[_Edge]` → Iterate over all edges matching a condition.

#### **Node Traversal**
- `succ(of: _Node, who_satisfies: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get successor nodes.
- `prev(of: _Node, who_satisfies: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get predecessor nodes.
- `children(of: _Node, extra: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get child nodes.
- `parent(of: _Node, extra: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get parent nodes.

#### **Data Flow & Control Flow**
- `flow_to(of: _Node, extra: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get data flow successors.
- `flow_from(of: _Node, extra: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get data flow predecessors.

#### **Hierarchy & Scope Queries**
- `topfile_node(of_nid: str) -> _Node` → Get the top-level file node for a given node.
- `descendants(src: _Node, condition: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get descendant nodes (BFS order).
- `ancestors(src: _Node, condition: Callable[[_Edge], bool]) -> Iterable[_Node]` → Get ancestor nodes (BFS order).

---

## **🔹 Node APIs**
### **`class _Node(AbcNodeQuerier)`**
- Represents a **single node** in the graph.

#### **Node Properties**
- `id: str` → Node ID.
- `code: Optional[str]` → Code content of the node.
- `label: Optional[str]` → Node label (e.g., "AST", "CFG").
- `flags: List[str]` → List of flags associated with the node.
- `line_num: Optional[int]` → Line number of the node.
- `children_num: Optional[int]` → Number of child nodes.
- `func_id: Optional[int]` → Function ID (if applicable).
- `class_name: Optional[str]` → Class name (if applicable).
- `namespace: Optional[str]` → Namespace of the node.
- `name: Optional[str]` → Name of the node.
- `end_num: Optional[int]` → Ending line number of the node.
- `comment: Optional[str]` → Docstring or comment associated with the node.
- `type: Optional[str]` → Node type (e.g., "AST_TOPLEVEL", "CFG_ENTRY").

---

## **🔹 Edge APIs**
### **`class _Edge(AbcEdgeQuerier)`**
- Represents a **single edge** in the graph.

#### **Edge Properties**
- `id: Tuple[str, str, str]` → Edge ID as (source, target, type).
- `start: Optional[int]` → Start node ID.
- `end: Optional[int]` → End node ID.
- `type: Optional[str]` → Edge type (e.g., "FLOWS_TO", "CALLS").
- `var: Optional[str]` → Variable associated with the edge.

---

## **🔹 Abstract Base Classes (ABC)**
### **`class AbcGraphQuerier`**
- `nodes(who_satisfies: Callable[[_Node], bool]) -> Iterable[_Node]`
- `edges(who_satisfies: Callable[[_Edge], bool]) -> Iterable[_Edge]`
- `succ(of: _Node, who_satisfies: Callable[[_Edge], bool]) -> Iterable[_Node]`
- `prev(of: _Node, who_satisfies: Callable[[_Edge], bool]) -> Iterable[_Node]`

### **`class AbcNodeQuerier`**
- `node_id: str`
- `properties: Optional[Dict[str, Any]]`
- `get_property(*prop_names: str) -> Optional[Any]`

### **`class AbcEdgeQuerier`**
- `edge_id: Tuple[str, str, str]`
- `from_nid: str`
- `to_nid: str`
- `edge_type: str`
- `properties: Optional[Dict[str, Any]]`
- `get_property(*prop_names: str) -> Optional[Any]`

---

## **📜 License**
This project is licensed under the **MIT License**.
