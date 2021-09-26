#!/usr/bin/env python3
from gitdit.utils import git_util as git
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
    elif args.command == "issue":
        add_issue(args)
    elif args.command == "comment":
        add_comment(args)
    elif args.command == "delete":
        delete_issue(args)
    elif args.command == "close":
        close_issue(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "push":
        push_issues(args)


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
argsp = argsubparsers.add_parser("issue", help="Create a new issue")
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
    print("Created Issue with id {}".format(issue_id))
    return issue_id, issue_json, issue


# Add Comment to an issue
# 1. Generate Comment Id
# 2. Create the json for comment data
argsp = argsubparsers.add_parser("comment", help="Add a new comment for an issue")
argsp.add_argument("message",
                   help="Description for the comment on the issue")
argsp.add_argument("-i", "--issue_id", dest="id",
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
argsp.add_argument("type", choices=['issue', 'comment'])
argsp.add_argument("-i", "--issue_id", dest="id",
                   help="ID of the issue to be deleted")


def delete_issue(args):
    assert args.type == "issue"
    return args.id, git.update_issue_status(args.id, 'Deleted')


# Close an Issue
argsp = argsubparsers.add_parser("close", help="Close an issue")
argsp.add_argument("type", choices=['issue', 'comment'])
argsp.add_argument("-i", "--issue_id", dest="id",
                   help="ID of the issue to be  closed")


def close_issue(args):
    assert args.type == "issue"
    return args.id, git.update_issue_status(args.id, 'Closed')


# View all Issues
argsp = argsubparsers.add_parser("show", help="View all issues")
argsp.add_argument("type", choices=['issues', 'comments'])
argsp.add_argument("-i", "--issue_id", dest="id",
                   help="ID of the issue to be deleted")


def cmd_show(args):
    if args.type == "issues":
        view_issues(args)
    elif args.type == "comments":
        view_comments(args)


def view_issues(args):
    issues = git.fetch_issues()
    issues = sorted(issues, key=lambda issue: issue['status'])
    str_fmt = "{:<40} {:<45} {:<15} {:<8}"
    print(str_fmt.format('IssueId', 'Description', 'Created by', 'Status'))
    for issue in issues:
        print(str_fmt.format(issue['id'],issue['message'], issue['createdBy'], issue['status']))
    return issues


def view_comments(args):
    comments = git.fetch_comments(args.id)
    str_fmt = "{:<40} {:<45} {:<25}"
    print(str_fmt.format('CommentId', 'Comment', 'Comment by'))
    for comment in comments:
        print(str_fmt.format(comment['id'], comment['message'], comment['commentBy']))
    return comments


# Push all issues to remote
argsp = argsubparsers.add_parser("push", help="Push all issues to remote")


def push_issues(args):
    return git.push_issues()


# Pull all issues from remote to local
argsp = argsubparsers.add_parser("pull", help="Pull all issues from remote to local")


def pull_issues(args):
    return git.pull_issues()
