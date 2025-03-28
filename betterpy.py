import ast
import os
import sys
import networkx as nx
from pyvis.network import Network
import pkg_resources

# Get installed third-party packages
installed_packages = {pkg.key for pkg in pkg_resources.working_set}

def extract_details(filename):
    """Parse a Python file to extract imported modules, classes, and functions."""
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filename)

    imports = set()
    classes = set()
    functions = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
        elif isinstance(node, ast.ClassDef):
            classes.add(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.add(node.name)

    return imports, classes, functions

def build_dependency_graph(directory):
    """Traverse a directory, analyze Python files, and build a dependency graph with class & function details."""
    G = nx.DiGraph()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                imports, classes, functions = extract_details(filepath)

                # Set node attributes
                details = f"📌 **Classes:** {', '.join(classes) if classes else 'None'}<br>🛠️ **Functions:** {', '.join(functions) if functions else 'None'}"
                G.add_node(module_name, type="internal", title=details)

                for imp in imports:
                    if imp in sys.builtin_module_names:
                        G.add_node(imp, type="builtin")
                    elif imp in installed_packages:
                        G.add_node(imp, type="third-party")
                    else:
                        G.add_node(imp, type="internal")
                    
                    G.add_edge(module_name, imp)

    return G

def generate_interactive_graph(G, output_file="dependency_graph.html"):
    """Generate an interactive dependency graph with collapsible nodes and detailed tooltips."""
    net = Network(height="750px", width="100%", directed=True, notebook=False, cdn_resources="remote")

    # Styling the nodes
    color_map = {
        "internal": "lightblue",
        "builtin": "lightgray",
        "third-party": "orange"
    }

    if len(G.nodes) == 0:
        print("Graph is empty! No dependencies found.")
        return
    
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "internal")
        title = data.get("title", "No details available")  # Show classes & functions inside a file
        net.add_node(node, label=node, title=title, color=color_map[node_type], shape="box")

    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    net.show_buttons(filter_=['physics'])
    net.write_html(output_file)
    print(f"Graph saved to {output_file}. Open it in a browser.")

# Set your project directory
project_directory = "your_project_directory_here"
G = build_dependency_graph(project_directory)
generate_interactive_graph(G)
