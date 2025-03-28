import ast
import networkx as nx
import matplotlib.pyplot as plt
import os

def extract_imports(filename):
    """Parse a Python file and extract imported modules."""
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filename)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    
    return imports

def build_dependency_graph(directory):
    """Traverse a directory, analyze Python files, and build a dependency graph."""
    G = nx.DiGraph()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                imports = extract_imports(filepath)
                
                G.add_node(module_name)
                for imp in imports:
                    G.add_edge(module_name, imp)

    return G

def draw_graph(G):
    """Visualize the dependency graph."""
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10)
    plt.title("Python Module Dependency Graph")
    plt.show()

# Set the directory to analyze (change this to your project's root)
project_directory = "your_project_directory_here"
G = build_dependency_graph(project_directory)
draw_graph(G)
