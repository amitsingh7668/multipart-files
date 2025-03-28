import ast
import os
import networkx as nx
from pyvis.network import Network

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

def generate_interactive_graph(G, output_file="dependency_graph.html"):
    """Generate an interactive dependency graph using pyvis."""
    net = Network(height="750px", width="100%", directed=True, notebook=False)
    
    for node in G.nodes:
        net.add_node(node, label=node, title=f"Module: {node}", color="lightblue")

    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    net.show_buttons(filter_=['physics'])
    net.show(output_file)
    print(f"Graph saved to {output_file}. Open it in a browser.")

# Set your project directory here
project_directory = "your_project_directory_here"
G = build_dependency_graph(project_directory)
generate_interactive_graph(G)
