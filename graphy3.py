import ast
import os
import sys
import networkx as nx
from pyvis.network import Network
import pkg_resources

# Get installed third-party packages (to exclude them)
installed_packages = {pkg.key for pkg in pkg_resources.working_set}

# Get list of built-in Python modules to exclude
builtin_modules = sys.builtin_module_names

# List of common standard library modules to exclude
standard_libraries = {
    "io", "json", "math", "os", "sys", "time", "re", "subprocess", "argparse", "unittest", "ctypes", "abc",
    "datetime", "random", "socket", "struct", "pickle", "sqlite3", "xml", "http", "logging", "pdb", "hashlib", "shutil",
    "base64", "csv", "email", "queue", "glob", "functools", "inspect", "threading", "asyncio", "concurrent", "traceback",
    "importlib", "webbrowser", "select", "http.client", "json.decoder", "json.encoder", "curses", "timeit", "platform"
}

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

                # Filter out built-in modules and third-party libraries
                imports = {imp for imp in imports if imp not in builtin_modules and imp not in installed_packages and imp not in standard_libraries}

                # Set node attributes: display classes and functions inside a module
                details = f"📌 **Classes:** {', '.join(classes) if classes else 'None'}<br>🛠️ **Functions:** {', '.join(functions) if functions else 'None'}"
                G.add_node(module_name, type="custom", title=details)

                for imp in imports:
                    G.add_node(imp, type="custom")  # Mark as custom import
                    G.add_edge(module_name, imp)

    return G

def generate_interactive_graph(G, output_file="dependency_graph.html"):
    """Generate an interactive dependency graph with collapsible nodes and detailed tooltips."""
    net = Network(height="750px", width="100%", directed=True, notebook=False, cdn_resources="remote")

    # Styling the nodes
    color_map = {
        "custom": "lightblue",  # Custom modules (project files)
    }

    if len(G.nodes) == 0:
        print("Graph is empty! No dependencies found.")
        return
    
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "custom")
        title = data.get("title", "No details available")  # Show classes & functions inside a file
        net.add_node(node, label=node, title=title, color=color_map[node_type], shape="box")

    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    net.show_buttons(filter_=['physics'])
    net.write_html(output_file)
    print(f"Graph saved to {output_file}. Open it in a browser.")

# Set your project directory here
project_directory = "your_project_directory_here"
G = build_dependency_graph(project_directory)
generate_interactive_graph(G)
