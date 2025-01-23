import requests
import streamlit as st
import openai
import urllib3

# Disable SSL warnings for testing (if SSL is disabled)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

    response = requests.get(url, headers=headers, params=params, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch merge requests: {response.status_code}")
        return []


def get_merge_request_details(gitlab_url, private_token, project_id, mr_id):
    """Fetch details and changes (diffs) for a specific MR."""
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}"
    headers = {"PRIVATE-TOKEN": private_token}

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch MR details: {response.status_code}")
        return None


def get_merge_request_changes(gitlab_url, private_token, project_id, mr_id):
    """Fetch changes (diffs) for a specific MR."""
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}/changes"
    headers = {"PRIVATE-TOKEN": private_token}

    response = requests.get(url, headers=headers, verify=False)
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


# Main App Logic
if private_token and project_id:
    # Fetch and display all open merge requests
    st.sidebar.header("Merge Requests")
    merge_requests = get_open_merge_requests(gitlab_url, private_token, project_id)

    if merge_requests:
        # Let user select an MR from the list
        selected_mr = st.sidebar.selectbox(
            "Select a Merge Request", merge_requests, format_func=lambda mr: f"{mr['title']} (#{mr['id']})"
        )

        if selected_mr:
            # Display MR details
            st.header(f"Merge Request: {selected_mr['title']}")
            st.write(f"**Description:** {selected_mr['description']}")
            st.write(f"**Author:** {selected_mr['author']['name']}")
            st.write(f"**State:** {selected_mr['state']}")
            st.write(f"**Created At:** {selected_mr['created_at']}")
            st.write(f"**Web URL:** [View on GitLab]({selected_mr['web_url']})")

            # Fetch and display code changes
            changes = get_merge_request_changes(
                gitlab_url, private_token, project_id, selected_mr["id"]
            )

            if changes:
                st.subheader("Code Changes")
                for change in changes[:3]:  # Show first 3 files for brevity
                    st.write(f"**File:** {change['new_path']}")
                    st.code(change['diff'], language="diff")

                # Add a "Proceed" button to call ChatGPT
                if st.button("Proceed to Review"):
                    with st.spinner("ChatGPT is reviewing the merge request..."):
                        feedback = review_merge_request(
                            selected_mr["title"], selected_mr["description"], changes
                        )
                        st.subheader("ChatGPT Review Comments")
                        st.write(feedback)
            else:
                st.warning("No changes found in this merge request.")
    else:
        st.warning("No open merge requests found.")
else:
    st.info("Please provide your GitLab token and project ID in the sidebar.")
