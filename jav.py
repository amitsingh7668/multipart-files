import requests
import openai  # Install using: pip install openai

# GitLab Configuration
OPENAI_API_KEY = "your_openai_api_key"
GITLAB_TOKEN = "your_gitlab_token"  # Replace with your token
GITLAB_PROJECT_ID = "your_project_id"  # Replace with your GitLab project ID
API_URL = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/tree"
RAW_BASE_URL = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/files"
BRANCH = "main"  # Change if using a different branch

# Storage for summary
class_usage = {}
total_classes = 0

def get_repo_files(path=""):
    """Fetch all Java files in the repository recursively from GitLab."""
    url = API_URL
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    params = {"recursive": True, "ref": BRANCH}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        files = []
        for item in response.json():
            if item["type"] == "blob" and item["path"].endswith(".java"):
                files.append(item["path"])
        return files
    else:
        print("Error:", response.json())
        return []

def get_file_content(file_path):
    """Fetch the raw content of a Java file from GitLab."""
    url = f"{RAW_BASE_URL}/{file_path}?ref={BRANCH}"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("content", "").encode('utf-8').decode('utf-8')
    else:
        print(f"Error fetching {file_path}: {response.status_code}")
        return None

def get_contributors():
    """Fetch contributor details from GitLab API."""
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/repository/contributors"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    response = requests.get(url, headers=headers)

    contributors = []
    if response.status_code == 200:
        for user in response.json():
            contributors.append(f"- [{user['name']}]({user['email']})")
    else:
        print("Error fetching contributors:", response.json())

    return contributors

def get_repo_language():
    """Fetch the primary language used in the GitLab repository."""
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get("language", "Not specified")
    else:
        print(f"Error fetching repository language: {response.status_code}")
        return "Not specified"

def main():
    print("Fetching repository files...")
    files = get_repo_files()
    files_info = {}

    for file in files:
        print(f"Processing {file}...")
        content = get_file_content(file)
        if content:
            files_info[file] = {"content": content}
    print("Java project files processed successfully!")

if __name__ == "__main__":
    main()
