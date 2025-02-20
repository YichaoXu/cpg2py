# **cpg2py: Graph-Based Query Engine for Joern CSV Files**

`cpg2py` is a Python library that provides a lightweight **graph-based query engine** for analyzing **Code Property Graphs (CPG)** extracted from Joern CSV files. The library offers an **abstract base class (ABC) architecture**, allowing users to extend and implement their own custom graph queries.

---

## **🚀 Features**

- **MultiDiGraph Representation**: A directed multi-graph with support for multiple edges between nodes.
- **CSV-Based Graph Construction**: Reads `nodes.csv` and `rels.csv` to construct a graph structure.
- **Extensible Abstract Base Classes (ABC)**:
  - `AbcGraphQuerier` for implementing **custom graph queries**.
  - `AbcNodeQuerier` for interacting with **nodes**.
  - `AbcEdgeQuerier` for interacting with **edges**.
- **Built-in Query Mechanisms**:
  - **Retrieve all edges**.
  - **Get incoming (**``**) and outgoing (**``**) edges of a node**.
  - **Find successors (**``**) and predecessors (**``**)**.
  - **Traverse AST, Control Flow, and Data Flow Graphs**.

---

## **📚 Installation**

To install the package, use:

```bash
pip install git+https://github.com/YichaoXu/cpg2py.git
```

Or clone the pip repository:

```bash
pip install cpg2py
```

---

## **📂 File Structure**

- **`nodes.csv`** (Example):
```csv
id:int	labels:label	type	flags:string_array	lineno:int	code	childnum:int	funcid:int	classname	namespace	endlineno:int	name	doccomment
0	Filesystem	Directory									"input"	
1	Filesystem	File									"example.php"	
2	AST	AST_TOPLEVEL	TOPLEVEL_FILE	1					""	25	"/input/example.php"	

````
- **`rels.csv`** (Example):
```csv
start	end	type
2	3	ENTRY
2	4	EXIT
6	7	ENTRY
6	9	PARENT_OF
````

---

## **📚 Usage**

### **1️⃣ Load Graph from Joern CSVs**

```python
from cpg2py import cpg_graph

# Load graph from CSV files
graph = cpg_graph("nodes.csv", "rels.csv")
```

---

### **2️⃣ Query Nodes & Edges**

```python
# Get a specific node
node = graph.node("2")
print(node.name, node.type)  # Example output: "/tmp/example.php" AST_TOPLEVEL

# Get a specific edge
edge = graph.edge("2", "3", "ENTRY")
print(edge.type)  # Output: ENTRY
```

---

### **3️⃣ Get Node Connections**

```python
# Get all outgoing edges from a node
outgoing_edges = graph.succ(node)
for out_node in outgoing_edges:
    print(out_node.id, out_node.name)

# Get all incoming edges to a node
incoming_edges = graph.prev(node)
for in_node in incoming_edges:
    print(in_node.id, in_node.name)
```

---

### **4️⃣ AST and Flow Queries**

```python
# Get top-level file node for a given node
top_file = graph.topfile_node("5")
print(top_file.name)  # Output: "example.php"

# Get child nodes in the AST hierarchy
children = graph.children(node)
print([child.id for child in children])

# Get data flow successors
flow_successors = graph.flow_to(node)
print([succ.id for succ in flow_successors])
```

---

## **🛠 Abstract Base Classes (ABC)**

The following abstract base classes (`ABC`) provide interfaces for extending **node**, **edge**, and **graph** querying behavior.

---

### **🔹 AbcNodeQuerier (Abstract Node Interface)**

This class defines how nodes interact with the graph storage.

```python
from cpg2py.abc import AbcNodeQuerier

class MyNodeQuerier(AbcNodeQuerier):
    def __init__(self, graph, nid):
        super().__init__(graph, nid)

    @property
    def name(self):
        return self.get_property("name")
```

---

### **🔹 AbcEdgeQuerier (Abstract Edge Interface)**

Defines the querying mechanisms for edges in the graph.

```python
from cpg2py.abc import AbcEdgeQuerier

class MyEdgeQuerier(AbcEdgeQuerier):
    def __init__(self, graph, f_nid, t_nid, e_type):
        super().__init__(graph, f_nid, t_nid, e_type)

    @property
    def type(self):
        return self.get_property("type")
```

---

### **🔹 AbcGraphQuerier (Abstract Graph Interface)**

This class provides an interface for implementing custom graph query mechanisms.

```python
from cpg2py.abc import AbcGraphQuerier

class MyGraphQuerier(AbcGraphQuerier):
    def node(self, nid: str):
        return MyNodeQuerier(self.storage, nid)

    def edge(self, fid, tid, eid):
        return MyEdgeQuerier(self.storage, fid, tid, eid)
```

---

## **🔍 Querying The Graph**

After implementing the abstract classes, you can perform advanced queries:

```python
graph = MyGraphQuerier(storage)

# Query node properties
node = graph.node("5")
print(node.name)  # Example Output: "main"

# Query edge properties
edge = graph.edge("5", "6", "FLOWS_TO")
print(edge.type)  # Output: "FLOWS_TO"
```

---

## **🐝 API Reference**

For a more detail APIs document please see our [APIs doc](docs/APIs.md) 

- **Graph Functions**:
  - `cpg_graph(node_csv, edge_csv)`: Loads graph from CSV files.
  - `graph.node(nid)`: Retrieves a node by ID.
  - `graph.edge(fid, tid, eid)`: Retrieves an edge.
  - `graph.succ(node)`: Gets successor nodes.
  - `graph.prev(node)`: Gets predecessor nodes.
- **Node Properties**:
  - `.name`: Node name.
  - `.type`: Node type.
  - `.line_num`: Source code line number.
- **Edge Properties**:
  - `.start`: Edge start node.
  - `.end`: Edge end node.
  - `.type`: Edge type.

---

## **🌟 License**

This project is licensed under the **MIT License**.

