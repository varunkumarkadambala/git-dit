#!/usr/bin/env python3
import git_util as git
import uuid
import sys
from datetime import datetime
import argparse

argparser = argparse.ArgumentParser(description="Decentralised Issue Tracker")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "init":
        init_repo(args)
    elif args.command == "new":
        add_issue(args)
    elif args.command == "comment":
        add_comment(args)
    elif args.command == "delete":
        delete_issue(args)
    elif args.command == "close":
        close_issue(args)
    elif args.command == "show":
        view_issues(args)
    elif args.command == "get-comments":
        view_comments(args)


# My Functionalities
# F-1 Create a Repo
# 1. Check if branch already exists
# 2. Else create a new empty branch
argsp = argsubparsers.add_parser("init", help="Initialize a new branch for issue tracking.")


def init_repo(args):
    assert git.is_git_repo(), "Not a Git repository"
    if git.branch_in_local('git-issues'):
        pass
    else:
        git.create_empty_local_branch('git-issues')
    if git.branch_in_remote('git-issues'):
        git.pull_issues()
    return "New Issues Branch Initiated in repository"


# Create Issue
# 1. Create an issue id
# 2. Get User Details
# 3. Generate Issue Id
# 4. Create a issue.json file
argsp = argsubparsers.add_parser("new", help="Create a new issue")
argsp.add_argument("message",
                   help="Description for reporting the issue")


def add_issue(args):
    issue_id = str(uuid.uuid4())
    issue_json = {"message": args.message,
                  "status": "Active",
                  "lastModified": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                  "createdBy": git.active_user(),
                  "createdAt": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                  }
    issue = git.create_issue(issue_id, issue_json)
    return issue_id, issue_json, issue


# Add Comment to an issue
# 1. Generate Comment Id
# 2. Create the json for comment data
argsp = argsubparsers.add_parser("comment", help="Add a new comment for an issue")
argsp.add_argument("message",
                   help="Description for the comment on the issue")
argsp.add_argument("id",
                   help="ID of the issue to be commented on")


def add_comment(args):
    comment_id = str(uuid.uuid4())
    comment_data = {"message": args.message,
                    "commentBy": git.active_user(),
                    "commentAt": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    }
    comment = git.create_comment(args.id, comment_id, comment_data)
    return comment_id, comment_data, comment


# Delete an Issue - Doesn't really delete the issue, but changes the status to deleted
argsp = argsubparsers.add_parser("delete", help="Delete an issue")
argsp.add_argument("id",
                   help="ID of the issue to be deleted")


def delete_issue(args):
    return args.id, git.update_issue_status(id, 'Deleted')


# Close an Issue
argsp = argsubparsers.add_parser("close", help="Close an issue")
argsp.add_argument("id",
                   help="ID of the issue to be closed")


def close_issue(args):
    return args.id, git.update_issue_status(id, 'Closed')


# View all Issues
argsp = argsubparsers.add_parser("show", help="View all issues")


def view_issues(args):
    issues = git.fetch_issues()
    str_fmt = "{:<45} {:<25} {:<8}"
    print(str_fmt.format('Issue', 'Created by', 'Status'))
    for issue in issues:
        print(str_fmt.format(issue['message'], issue['createdBy'], issue['status']))
    return issues


# View all Comments on an issues
argsp = argsubparsers.add_parser("get-comments", help="View all comments on an issue")
argsp.add_argument("id",
                   help="ID of the issue")


def view_comments(args):
    comments = git.fetch_comments(args.id)
    str_fmt = "{:<45} {:<25}"
    print(str_fmt.format('Comment', 'Comment by'))
    for comment in comments:
        print(str_fmt.format(comment['message'], comment['commentBy']))
    return comments
