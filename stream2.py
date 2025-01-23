import requests
import streamlit as st
import openai

# Streamlit App Title
st.title("GitLab Merge Request Reviewer with ChatGPT")

# Input fields for GitLab token, project ID, and OpenAI API key
st.sidebar.header("Configuration")
gitlab_url = st.sidebar.text_input("GitLab URL", value="https://gitlab.com")
private_token = st.sidebar.text_input("GitLab Private Token", type="password")
project_id = st.sidebar.text_input("GitLab Project ID")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# OpenAI API configuration
if openai_api_key:
    openai.api_key = openai_api_key


def get_open_merge_requests(gitlab_url, private_token, project_id):
    """Fetch open merge requests from GitLab."""
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests"
    headers = {"PRIVATE-TOKEN": private_token}
    params = {"state": "opened", "per_page": 100}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch merge requests: {response.status_code}")
        return []


def get_merge_request_changes(gitlab_url, private_token, project_id, mr_id):
    """Fetch changes (diffs) for a specific MR."""
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}/changes"
    headers = {"PRIVATE-TOKEN": private_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("changes", [])
    else:
        st.error(f"Failed to fetch changes for MR {mr_id}: {response.status_code}")
        return []


def review_merge_request(mr_title, mr_description, changes):
    """Use ChatGPT to review an MR."""
    changes_summary = "\n".join(
        [f"File: {change['new_path']}\n{change['diff']}" for change in changes[:3]]
    )

    prompt = f"""
You are a code reviewer. Review the following merge request and provide actionable feedback:

Title: {mr_title}
Description: {mr_description}

Changes:
{changes_summary}

Provide constructive feedback on code quality, style, and potential issues.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


def post_comment_on_merge_request(gitlab_url, private_token, project_id, mr_id, comment):
    """Post ChatGPT feedback as a comment on the GitLab MR."""
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}/notes"
    headers = {"PRIVATE-TOKEN": private_token}
    data = {"body": comment}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        st.success(f"Comment posted successfully on MR {mr_id}.")
    else:
        st.error(f"Failed to post comment on MR {mr_id}: {response.status_code}")


# Main App Logic
if private_token and project_id:
    st.sidebar.header("Merge Requests")
    merge_requests = get_open_merge_requests(gitlab_url, private_token, project_id)

    if merge_requests:
        selected_mr = st.sidebar.selectbox(
            "Select a Merge Request", merge_requests, format_func=lambda mr: f"{mr['title']} (#{mr['id']})"
        )

        if selected_mr:
            st.header(f"Merge Request: {selected_mr['title']}")
            st.write(f"Description: {selected_mr['description']}")

            changes = get_merge_request_changes(
                gitlab_url, private_token, project_id, selected_mr["id"]
            )

            if changes:
                st.subheader("Code Changes")
                for change in changes[:3]:  # Show first 3 files for brevity
                    st.write(f"**File:** {change['new_path']}")
                    st.code(change['diff'], language="diff")

                if openai_api_key:
                    with st.spinner("Reviewing merge request with ChatGPT..."):
                        feedback = review_merge_request(
                            selected_mr["title"], selected_mr["description"], changes
                        )
                        st.subheader("ChatGPT Review Comments")
                        st.write(feedback)

                        if st.button("Post Comment to GitLab"):
                            post_comment_on_merge_request(
                                gitlab_url, private_token, project_id, selected_mr["id"], feedback
                            )
            else:
                st.warning("No changes found in this merge request.")
    else:
        st.warning("No open merge requests found.")
else:
    st.info("Please provide your GitLab token and project ID in the sidebar.")
