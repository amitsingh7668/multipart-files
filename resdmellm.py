import requests

# GitLab API settings
GITLAB_TOKEN = "your_private_token"
PROJECT_ID = "your_project_id"  # You can get this from GitLab UI
BASE_URL = f"https://gitlab.com/api/v4/projects/{PROJECT_ID}"

HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}

# Get all files in the repository
def get_java_files():
    response = requests.get(f"{BASE_URL}/repository/tree?recursive=true", headers=HEADERS)
    files = response.json()
    
    # Filter only Java files
    java_files = [f["path"] for f in files if f["path"].endswith(".java")]
    return java_files

# Fetch the content of a given Java file
def get_file_content(file_path):
    url = f"{BASE_URL}/repository/files/{file_path.replace('/', '%2F')}/raw?ref=main"
    response = requests.get(url, headers=HEADERS)
    return response.text if response.status_code == 200 else None


import javalang

def analyze_java_code(code):
    tree = javalang.parse.parse(code)
    
    class_count = sum(1 for _ in tree.filter(javalang.tree.ClassDeclaration))
    method_count = sum(1 for _ in tree.filter(javalang.tree.MethodDeclaration))
    
    return class_count, method_count

def main():
    java_files = get_java_files()
    
    total_classes = 0
    total_methods = 0
    
    for file in java_files:
        print(f"Analyzing: {file}")
        code = get_file_content(file)
        
        if code:
            classes, methods = analyze_java_code(code)
            total_classes += classes
            total_methods += methods
            print(f"  → Classes: {classes}, Methods: {methods}")

    print("\nTotal Classes:", total_classes)
    print("Total Methods:", total_methods)

main()

