# Git Basic Functions using os module
import os
import json


# Check if in a working git repository
def is_git_repo():
    cmd = 'git rev-parse --is-inside-work-tree'
    stream = os.popen(cmd)
    output = stream.read()
    return output == 'true\n'


def current_branch():
    cmd = 'git rev-parse --abbrev-ref HEAD'
    stream = os.popen(cmd)
    output = stream.read()
    return output.split('\n')[0]


# Check if branch is present in repo
def branch_in_local(branch):
    cmd = 'git branch --list ' + branch
    exp_output = '* ' + branch + '\n'
    stream = os.popen(cmd)
    output = stream.read()
    return output == exp_output


# Create empty local branch
def create_empty_local_branch(branch):
    current = current_branch()
    cmd = 'git checkout --orphan dit-issues;git reset --hard;' \
          'echo "This branch stores all the issues for the decentralised issue tracker" > README.txt;' \
          'git add README.txt;git commit -m "Creating Empty Branch dit-issues";git checkout ' + current
    stream = os.popen(cmd)
    output = stream.read()
    return output


# Check if branch is present in remote
def branch_in_remote(branch):
    cmd = 'git ls-remote --heads origin ' + branch
    exp_output = branch + '\n'
    stream = os.popen(cmd)
    output = stream.read()
    output = output.split('/')[-1]
    return output == exp_output


# Git pull remote to local
def pull_issues():
    cmd = 'git checkout dit-issues; git pull origin dit-issues'
    stream = os.popen(cmd)
    output = stream.read()
    return output


def active_user():
    cmd = 'git config user.name'
    stream = os.popen(cmd)
    output = stream.read()
    return output.split('\n')[0]


def create_issue(issue_id, data):
    current = current_branch()
    cmd = 'git checkout dit-issues'
    process = os.popen(cmd)
    process = process.read()
    if not os.path.exists('issues'):
        os.makedirs('issues')
    new_dir = 'issues/' + issue_id
    os.mkdir(new_dir)
    json_path = new_dir + '/issue.json'
    with open(json_path, "w") as outfile:
        json.dump(data, outfile)
    cmd = 'git add ' + json_path + ';git commit -m "Creating issue ' + issue_id + '";git checkout ' + current
    stream = os.popen(cmd)
    output = stream.read()
    return output


def create_comment(issue_id, comment_id, data):
    current = current_branch()
    cmd = 'git checkout dit-issues'
    process = os.popen(cmd)
    process = process.read()
    new_dir = 'issues/' + issue_id + '/comments/'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    json_path = new_dir + comment_id + '.json'
    with open(json_path, "w") as outfile:
        json.dump(data, outfile)
    cmd = 'git add ' + json_path + ';git commit -m "Creating Comment ' + comment_id + '";git checkout ' + current
    stream = os.popen(cmd)
    output = stream.read()
    return output


def update_issue_status(id, status):
    current = current_branch()
    cmd = 'git checkout dit-issues'
    process = os.popen(cmd)
    process = process.read()
    json_path = 'issues/' + id + '/issue.json'
    with open(json_path, "r") as jsonFile:
        data = json.load(jsonFile)
    data["status"] = status
    with open(json_path, "w") as jsonFile:
        json.dump(data, jsonFile)
    cmd = 'git add ' + json_path + ';git commit -m "Deleting issue ' + id + '";git checkout ' + current
    stream = os.popen(cmd)
    output = stream.read()
    return output


def fetch_issues():
    current = current_branch()
    cmd = 'git checkout dit-issues'
    process = os.popen(cmd)
    process = process.read()
