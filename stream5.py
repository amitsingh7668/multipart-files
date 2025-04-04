import requests
import streamlit as st
import openai
import urllib3

# Disable SSL warnings for testing (if SSL is disabled)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to fetch open merge requests from GitLab
def get_open_merge_requests(gitlab_url, private_token, project_id):
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests"
    headers = {"PRIVATE-TOKEN": private_token}
    params = {"state": "opened", "per_page": 100}
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch merge requests: {response.status_code}")
        return []

# Function to get changes (diffs) for a specific MR
def get_merge_request_changes(gitlab_url, private_token, project_id, mr_iid):
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes"
    headers = {"PRIVATE-TOKEN": private_token}

    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        return response.json().get("changes", [])
    else:
        st.error(f"Failed to fetch changes for MR {mr_iid}: {response.status_code}")
        return []

# Function to generate ChatGPT feedback based on MR details
def review_merge_request(mr_title, mr_description, changes):
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

# Function to post feedback as a comment on the GitLab MR
def post_comment_on_merge_request(gitlab_url, private_token, project_id, mr_iid, comment):
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    headers = {"PRIVATE-TOKEN": private_token}
    data = {"body": comment}
    
    response = requests.post(url, headers=headers, json=data, verify=False)
    
    if response.status_code == 201:
        comment_url = f"{gitlab_url}/{project_id}/merge_requests/{mr_iid}#note_{response.json()['id']}"
        return f"Comment posted successfully! [View the comment on GitLab]({comment_url})"
    else:
        st.error(f"Failed to post comment on MR {mr_iid}: {response.status_code}")
        return None

# Main Streamlit function
def main():
    st.title("GitLab Merge Request Reviewer with ChatGPT")
    
    # Sidebar inputs
    st.sidebar.header("Configuration")
    gitlab_url = st.sidebar.text_input("GitLab URL", value="https://gitlab.com")
    private_token = st.sidebar.text_input("GitLab Private Token", type="password")
    project_id = st.sidebar.text_input("GitLab Project ID")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    
    # Set OpenAI API key
    if openai_api_key:
        openai.api_key = openai_api_key
    
    # When user provides GitLab token and project ID
    if private_token and project_id:
        # Fetch and display all open merge requests
        st.sidebar.header("Merge Requests")
        merge_requests = get_open_merge_requests(gitlab_url, private_token, project_id)
        
        if merge_requests:
            # Let user select an MR from the list
            selected_mr = st.sidebar.selectbox(
                "Select a Merge Request", merge_requests, format_func=lambda mr: f"{mr['title']} (IID #{mr['iid']})"
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
                    gitlab_url, private_token, project_id, selected_mr["iid"]
                )
                
                if changes:
                    st.subheader("Code Changes")
                    for change in changes[:3]:  # Show first 3 files for brevity
                        st.write(f"**File:** {change['new_path']}")
                        st.code(change['diff'], language="diff")
                    
                    # Call ChatGPT to review MR
                    if st.button("Proceed to Review"):
                        with st.spinner("ChatGPT is reviewing the merge request..."):
                            feedback = review_merge_request(
                                selected_mr["title"], selected_mr["description"], changes
                            )
                            st.subheader("ChatGPT Review Comments")
                            st.write(feedback)
                            
                            # Ask user if the feedback is good
                            if st.radio("Is the feedback good?", ("Yes", "No")) == "Yes":
                                # Post feedback to GitLab
                                if st.button("Post Feedback to GitLab"):
                                    comment_acknowledgment = post_comment_on_merge_request(
                                        gitlab_url, private_token, project_id, selected_mr["iid"], feedback
                                    )
                                    if comment_acknowledgment:
                                        st.success(comment_acknowledgment)
                            else:
                                # If feedback is not good, let the user correct it
                                modified_feedback = st.text_area("Modify the feedback:", value=feedback)
                                if st.button("Retry with Modified Feedback"):
                                    comment_acknowledgment = post_comment_on_merge_request(
                                        gitlab_url, private_token, project_id, selected_mr["iid"], modified_feedback
                                    )
                                    if comment_acknowledgment:
                                        st.success(comment_acknowledgment)
                else:
                    st.warning("No changes found in this merge request.")
        else:
            st.warning("No open merge requests found.")
    else:
        st.info("Please provide your GitLab token and project ID in the sidebar.")

if __name__ == "__main__":
    main()
