import requests
import openai

# GitLab and OpenAI Configuration
GITLAB_URL = "https://gitlab.com"
PROJECT_ID = "your_project_id"
ACCESS_TOKEN = "your_gitlab_access_token"
OPENAI_API_KEY = "your_openai_api_key"

openai.api_key = OPENAI_API_KEY


def get_open_merge_requests():
    """Fetch open merge requests from GitLab."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/merge_requests"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"state": "opened", "per_page": 100}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch MRs: {response.status_code} {response.text}")
        return []


def get_merge_request_changes(mr_id):
    """Fetch changes (diffs) for a specific MR."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/merge_requests/{mr_id}/changes"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("changes", [])
    else:
        print(f"Failed to fetch changes for MR {mr_id}: {response.status_code} {response.text}")
        return []


def review_merge_request(mr):
    """Use ChatGPT to review an MR."""
    title = mr['title']
    description = mr['description']
    changes = get_merge_request_changes(mr['id'])

    if not changes:
        return "No changes to review."

    # Prepare the code diff summary for ChatGPT
    changes_summary = "\n".join(
        [f"File: {change['new_path']}\n{change['diff']}" for change in changes[:3]]  # Limit to 3 files
    )

    prompt = f"""
You are a code reviewer. Review the following merge request and provide feedback:
    
Title: {title}
Description: {description}

Changes:
{changes_summary}

Provide actionable feedback on code quality, style, and potential issues.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
    )

    return response["choices"][0]["message"]["content"]


def main():
    """Main function to fetch and review MRs."""
    merge_requests = get_open_merge_requests()

    if not merge_requests:
        print("No open merge requests found.")
        return

    print(f"Found {len(merge_requests)} open merge requests.")
    for mr in merge_requests:
        print(f"\nReviewing MR: {mr['title']} (ID: {mr['id']})")
        feedback = review_merge_request(mr)
        print(f"Feedback:\n{feedback}")

        # Optionally, post feedback as a comment on the MR
        # post_comment_on_merge_request(mr['id'], feedback)


def post_comment_on_merge_request(mr_id, comment):
    """Post ChatGPT feedback as a comment on the GitLab MR."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/merge_requests/{mr_id}/notes"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {"body": comment}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Comment posted successfully on MR {mr_id}.")
    else:
        print(f"Failed to post comment on MR {mr_id}: {response.status_code} {response.text}")


if __name__ == "__main__":
    main()

