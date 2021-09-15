# Initiate a new project
import os
import json
import uuid
from datetime import datetime


def git_init():
    current_dir = os.getcwd()
    directory = '.git_dit'
    path = os.path.join(current_dir, directory)
    if not os.path.exists(path):
        os.makedirs(path)
    # After Creating folder a new json file must also be included
    json_data = json.load(open("project.json"))
    json_string = json.dumps(json_data)
    json_file = 'main.json'
    json_path = os.path.join(path, json_file)
    json_write = open(json_path, "w")
    json_write.write(json_string)
    json_write.close()
    print(json_path)
    print(json_string)
    return


def create_issue(desc):
    # Generate an id and create a new json content for the issue
    issue_id = str(uuid.uuid4())
    json_data = json.load(open("issue.json"))
    json_data['issueId'] = issue_id
    json_data['description'] = desc
    json_data['status'] = 'Active'
    json_data['createdOn'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    json_data['lastModified'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    json_string = json.dumps(json_data)
    # Store the json data in a new file
    current_dir = os.getcwd()
    json_file = '.git_dit/' + issue_id + '.json'
    json_path = os.path.join(current_dir, json_file)
    json_write = open(json_path, "w")
    json_write.write(json_string)
    json_write.close()
    print(json_data)
    # Update the main json
    return


def update_issue(id,desc):
    # Load the json data
    current_dir = os.getcwd()
    json_path = '.git_dit/' + id + '.json'
    json_data = json.load(open(json_path))
    json_data['description'] = desc
    json_data['lastModified'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    json_string = json.dumps(json_data)
    # Update the file
    json_write = open(json_path, "w")
    json_write.write(json_string)
    json_write.close()
    print(json_data)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Output")
    #git_init()
    create_issue("This is a Sample Issue")
    # update_issue("d1a05216-0559-4dd1-9dee-808e72f035c3", "This is a modified Issue")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
