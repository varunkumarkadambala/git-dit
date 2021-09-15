#!/usr/bin/env python3
import git_util as git
import uuid
from datetime import datetime


# My Functionalities
# F-1 Create a Repo
# 1. Check if branch already exists
# 2. Else create a new empty branch
def init_repo():
    assert git.is_git_repo(), "Not a Git repository"
    if git.branch_in_local('dit-issues'):
        pass
    else:
        git.create_empty_local_branch('dit-issues')
    if git.branch_in_remote('dit-issues'):
        git.pull_issues()
    return "New Issues Branch Initiated in repository"


# Create Issue
# 1. Create an issue id
# 2. Get User Details
# 3. Generate Issue Id
# 4. Create a issue.json file
def add_issue(description):
    issue_id = str(uuid.uuid4())
    issue_json = {"message": description,
                  "status": "Active",
                  "lastModified": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                  "createdBy": git.active_user(),
                  "createdAt": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                  }
    issue = git.create_issue(issue_id, issue_json)
    return issue_id, issue_json


# Add Comment to an issue
def add_comment(issue_id, comment):
    comment_id = str(uuid.uuid4())
    comment_data = {"message": comment,
                    "commentBy": git.active_user(),
                    "commentAt": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    }
    comment = git.create_comment(issue_id, comment_id, comment_data);
    return comment_id, comment


# Delete an Issue - Doesn't really delete the issue, but changes the status to deleted
def delete_issue(id):
    return id, git.update_issue_status(id, 'Deleted')


# Close an Issue
def close_issue(id):
    return id, git.update_issue_status(id, 'Closed')


# View all Issues
def view_issues():
