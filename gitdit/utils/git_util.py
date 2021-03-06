# Git Basic Functions using os module
import os
import json


# Check if in a working git repository
def is_git_repo():
    cmd = 'git rev-parse --is-inside-work-tree'
    stream = os.popen(cmd)
    output = stream.read()
    return output == 'true\n'


# Check if branch is present in repo
def branch_in_local(branch):
    cmd = 'git branch --list {0}'.format(branch)
    exp_output = '* ' + branch + '\n'
    stream = os.popen(cmd)
    output = stream.read()
    return output == exp_output


# Get Current Branch
def current_branch():
    cmd = 'git rev-parse --abbrev-ref HEAD'
    stream = os.popen(cmd)
    output = stream.read()
    return output.split('\n')[0]


def fetch_branch_from_remote(branch):
    current = current_branch()
    cmd = "git checkout -b {} origin/{} > /dev/null 2>&1".format(branch, branch)
    stream = os.popen(cmd)
    output = stream.read()
    cmd = 'git checkout ' + current + '> /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    return

# Create empty local branch
def create_empty_local_branch(branch):
    current = current_branch()
    cmd = 'git checkout --orphan {0} > /dev/null 2>&1;git reset --hard;'.format(branch)
    stream = os.popen(cmd)
    output = stream.read()
    with open("README.txt", "w") as file:
        file.write("This branch stores all the issues for the decentralised issue tracker")
    cmd = 'git add README.txt;git commit -m "Creating Empty Branch for issue tracker";git checkout {0} > /dev/null 2>&1'.format(current)
    stream = os.popen(cmd)
    output = stream.read()
    return output


# Check if branch is present in remote
def branch_in_remote(branch):
    cmd = 'git ls-remote --heads origin {}'.format(branch)
    exp_output = branch + '\n'
    stream = os.popen(cmd)
    output = stream.read()
    output = output.split('/')[-1]
    return output == exp_output


# Git pull remote to local
def pull_issues():
    current = current_branch()
    # cmd = 'git checkout git-issues > /dev/null 2>&1 ; git pull origin git-issues > /dev/null 2>&1; git checkout {} > ' \
    #       '/dev/null 2>&1'.format(current)
    cmd = 'git checkout git-issues ; git pull origin git-issues ; git checkout {}'.format(current)
    stream = os.popen(cmd)
    output = stream.read()
    print(output)
    return output


def active_user():
    cmd = 'git config user.name'
    stream = os.popen(cmd)
    output = stream.read()
    return output.split('\n')[0]


def create_issue(issue_id, data):
    current = current_branch()
    cmd = 'git checkout git-issues > /dev/null 2>&1 '
    process = os.popen(cmd)
    process = process.read()
    if not os.path.exists('issues'):
        os.makedirs('issues')
    new_dir = 'issues/' + issue_id
    os.mkdir(new_dir)
    json_path = new_dir + '/issue.json'
    with open(json_path, "w") as outfile:
        json.dump(data, outfile)
    cmd = 'git add {0};git commit -m "Creating issue {1}";git checkout {2} > /dev/null 2>&1 '.format(json_path, issue_id, current)
    stream = os.popen(cmd)
    output = stream.read()
    return output


def create_comment(issue_id, comment_id, data):
    current = current_branch()
    cmd = 'git checkout git-issues > /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    new_dir = 'issues/' + issue_id + '/comments/'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    json_path = new_dir + comment_id + '.json'
    with open(json_path, "w") as outfile:
        json.dump(data, outfile)
    cmd = 'git add ' + json_path + ';git commit -m "Creating Comment ' + comment_id + '";git checkout ' + current + '> /dev/null 2>&1 '
    stream = os.popen(cmd)
    output = stream.read()
    return output


def update_issue_status(id, status):
    current = current_branch()
    cmd = 'git checkout git-issues > /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    json_path = 'issues/' + str(id) + '/issue.json'
    if not os.path.exists(json_path):
        print("Issue does not exist")
        return None
    with open(json_path, "r") as jsonFile:
        data = json.load(jsonFile)
    data["status"] = status
    with open(json_path, "w") as jsonFile:
        json.dump(data, jsonFile)
    cmd = 'git add ' + json_path + ';git commit -m "Updating issue ' + str(id) + '";git checkout ' + current + '> /dev/null 2>&1'
    stream = os.popen(cmd)
    output = stream.read()
    return output


def fetch_issues():
    current = current_branch()
    cmd = 'git checkout git-issues > /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    issues = []
    if not os.path.exists('issues'):
        return issues
    for issue in os.listdir('issues'):
        json_path = 'issues/' + str(issue) + '/issue.json'
        if os.path.exists(json_path):
            with open(json_path, "r") as jsonFile:
                data = json.load(jsonFile)
                data["id"] = str(issue)
                issues.append(data)

    cmd = 'git checkout ' + current + '> /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    return issues


def fetch_comments(id):
    current = current_branch()
    cmd = 'git checkout git-issues > /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    comments = []
    comments_dir = 'issues/' + str(id) + '/comments/'
    if not os.path.exists(comments_dir):
        return comments
    for comment in os.listdir(comments_dir):
        try:
            json_path = comments_dir + comment
            with open(json_path, "r") as jsonFile:
                data = json.load(jsonFile)
                data["id"] = str(comment)[:-5]
                comments.append(data)
        except:
            continue
    cmd = 'git checkout ' + current + ' > /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    return comments


def push_issues():
    current = current_branch()
    cmd = 'git checkout git-issues > /dev/null 2>&1; git push origin git-issues;'
    stream = os.popen(cmd)
    output = stream.read()
    cmd = 'git checkout ' + current + '> /dev/null 2>&1'
    process = os.popen(cmd)
    process = process.read()
    return output


