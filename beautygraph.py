import ast
import os
import sys
import networkx as nx
from pyvis.network import Network
import pkg_resources

# Get installed third-party packages
installed_packages = {pkg.key for pkg in pkg_resources.working_set}

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
                
                G.add_node(module_name, type="internal")  # Mark as internal project file
                for imp in imports:
                    if imp in sys.builtin_module_names:
                        G.add_node(imp, type="builtin")  # Standard Python module
                    elif imp in installed_packages:
                        G.add_node(imp, type="third-party")  # External package
                    else:
                        G.add_node(imp, type="internal")  # Another project file
                    
                    G.add_edge(module_name, imp)

    return G

def generate_interactive_graph(G, output_file="dependency_graph.html"):
    """Generate an interactive dependency graph with colored nodes using pyvis."""
    net = Network(height="750px", width="100%", directed=True, notebook=False)

    color_map = {
        "internal": "lightblue",
        "builtin": "lightgray",
        "third-party": "orange"
    }

    if len(G.nodes) == 0:
        print("Graph is empty! No dependencies found.")
        return
    
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "internal")  # Default to internal
        net.add_node(node, label=node, title=f"Module: {node}", color=color_map[node_type])

    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    net.show_buttons(filter_=['physics'])
    net.write_html(output_file)
    print(f"Graph saved to {output_file}. Open it in a browser.")

# Set your project directory here
project_directory = "your_project_directory_here"
G = build_dependency_graph(project_directory)
generate_interactive_graph(G)
