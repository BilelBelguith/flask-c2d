#!/usr/bin/python3

import requests
import argparse
import gitlab
from gitlab import const


# this script give you hand to add users to a specfic project with the roles you want for each user ( addinf using emails and name of role)

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--emails', dest='email',
                    nargs='+', help='list of emails ')
parser.add_argument('-r', '--roles', dest='roles',
                    nargs='+', help='list of roles ')
parser.add_argument('-t', '--token', dest='token',
                    nargs='+', help='Gitlab token access')
parser.add_argument('-u', '--url', dest='url', nargs='+',
                    help='Compagny Gitlab URL')
parser.add_argument('-p', '--projectName', dest='project_name',
                    nargs='+', help='project name')
args = parser.parse_args()

email_string = args.email[0]
role_string = args.roles[0]
gitlab_url = args.url[0]
private_tokeng = args.token[0]
project_name = args.project_name[0]

# Exemple of entries :
# gitlab_url = 'https://git.softtodo.tn/'
# private_tokeng = 'U_AKMhSjFVygKgnDUW9a'
# groups = Devops
# project_name='test5'

my_list_email = email_string.split(",")
my_role_list = role_string.split(",")
my_id_list = []

gl = gitlab.Gitlab(gitlab_url, private_token=private_tokeng)


for email in my_list_email:
    response = requests.get(f'{gitlab_url}/api/v4/users?search={email}',
                            headers={'Private-Token': private_tokeng})
    if response.status_code != 200:
        print(f"Failed to retrieve user with email {email}.")
        exit()

    # extract user ID from API response
    users = response.json()
    if len(users) == 0:
        print(f"No user found with email {email}")
        exit()
    user_id = users[0]['id']

    print(f"The ID for user with email {email} is {user_id}")
    my_id_list.append(user_id)


print(my_id_list)
print(my_role_list)

if len(my_id_list) != len(my_role_list):
    print("data are missing some values")
    exit()

# gl = gitlab.Gitlab(gitlab_url, private_token=private_tokeng)
projects = gl.projects.list(search=project_name)
print(projects)
project_id = [p for p in projects if p.name == project_name]
print(project_id)
project_id = projects[0].id

project_to_add_users = gl.projects.get(project_id)

for i in range(len(my_id_list)):

    if (my_role_list[i] == 'Guest'):
        project_to_add_users.members.create(
            {'user_id': my_id_list[i], 'access_level': const.GUEST_ACCESS})
    if (my_role_list[i] == 'Reporter'):
        project_to_add_users.members.create(
            {'user_id': my_id_list[i], 'access_level': const.REPORTER_ACCESS})
    if (my_role_list[i] == 'Developer'):
        project_to_add_users.members.create(
            {'user_id': my_id_list[i], 'access_level': const.DEVELOPER_ACCESS})
    if (my_role_list[i] == 'Maintainer'):
        project_to_add_users.members.create(
            {'user_id': my_id_list[i], 'access_level': const.MAINTAINER_ACCESS})



