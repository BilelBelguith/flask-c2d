#!/usr/bin/python3


import argparse
import os
from github import Github
from os import walk
import gitlab
# Z99fC_AcdaLpjezbG-hc
# U_AKMhSjFVygKgnDUW9a
# https://git.softtodo.tn
# Devops
parser = argparse.ArgumentParser(description='create new Gitlab Repository')

parser.add_argument('-t', '--token', dest='token',
                    nargs='+', help='Gitlab token access')
parser.add_argument('-u', '--url', dest='url', nargs='+',
                    help='Compagny Gitlab URL')
parser.add_argument('-p', '--projectName', dest='project_name',
                    nargs='+', help='project name')
parser.add_argument('-g', '--groupName', dest='group_name',
                    nargs='+', help='group name')

args = parser.parse_args()

token = args.token[0]
url = args.url[0]
project_name = args.project_name[0]
group_name = args.group_name[0]


# app prammm on args to slect the path to upload depends on CMS ( TYPO3 - WORDPRESS)
# TO UPLOAD the project structure on your git repo
path_to_upload = '/home/bilelbelguith/upload/'
# path_to_upload_precommit='/home/bilel/azerty/az/'


group_id = ''
project_id = ''

# token = input('please enter your token access -> ')
# url = input('please enter your Gitlab URL -> ')
gl = gitlab.Gitlab(private_token=token)

if (url != 'None'):
    gl = gitlab.Gitlab(url, private_token=token)


gl.auth()
# project_name = input ('please enter Project name -> ')

# ask=input('do you want to : \n \t new- create a new group \n \t exist- use a group already existe \n your choose -> ')
group_list = []

# group_name = input('enter Group name for this project -> ')

# list groups name in list
groups_test = gl.groups.list(all=True)
for group_group in groups_test:
    group_list.append(group_group.attributes['name'])

if (group_name not in group_list):
    group = gl.groups.create({'name': group_name, 'path': group_name})
    # print('group created ')
    groups = gl.groups.list(all=True)
    for group in groups:
        if (group.attributes['name'] == group_name):
            # print(group.attributes['id'] , group.attributes['name']  )
            group_id = group.attributes['id']

else:
    # group_name = input('enter Group name for this project -> ')
    groups = gl.groups.list(all=True)
    for group in groups:
        if (group.attributes['name'] == group_name):
            # print(group.attributes['id'] , group.attributes['name']  )
            group_id = group.attributes['id']


response = gl.projects.create({"name": project_name, "namespace_id": group_id})
projects = gl.projects.list(all=True)

for project in projects:
    if (project.attributes['name'] == project_name):
        project_id = project.attributes['id']
project_repo = gl.projects.get(project_id)

files_names_gitlab = []
path_files_gitlab = []
# for (dirpath, dirnames, filenames) in walk(path_to_upload):
#
#    files_names_gitlab = filenames
#    for names in filenames:
#      path = path_to_upload + names
#      path_files_gitlab.append(path)
#
# for i in range(0 , len(files_names_gitlab)):
#    with open(path_files_gitlab[i], 'r') as file:
#      content_gitlab = file.read()
#
#    add_response= project_repo.files.create({'file_path': 'aze/'+files_names_gitlab[i],'branch': 'main' ,'content': '%s'%content_gitlab ,'commit_message': 'Pré_commit'})
#    print(files_names_gitlab[i]  + ' CREATED')



###for (dirpath, dirnames, filenames) in walk(path_to_upload):
###    for names in filenames:
###
###        files_names_gitlab.append(os.path.join(
###            dirpath, names)[len(path_to_upload)::])
###        path_files_gitlab.append(os.path.join(dirpath, names))
###for i in range(0, len(files_names_gitlab)):
###    with open(path_files_gitlab[i], 'r') as file:
###        content_gitlab = file.read()
###    add_response = project_repo.files.create(
###        {'file_path': files_names_gitlab[i], 'branch': 'main', 'content': '%s' % content_gitlab, 'commit_message': 'initial'})
###    print(files_names_gitlab[i] + '=> CREATED')



# files_namesp=[]
# path_filesp= []
# for (dirpath, dirnames, filenames) in walk(path_to_upload_prec):
#
#    for names in filenames:
#        files_namesp.append(os.path.join(dirpath , names)[len(path_to_upload_prec)::])
#        path_filesp.append(os.path.join(dirpath , names))
# for i in range(0 , len(files_namesp)):
#    with open(path_filesp[i], 'r') as file:
#     content = file.read()
#    add_response= project_repo.files.create({'file_path': files_namesp[i],'branch': 'main' ,'content': '%s'%content ,'commit_message': 'Pré_commit'})
#    print(files_namesp[i]  + ' CREATED')
#
#
branch = project_repo.branches.create({'branch': 'develop', 'ref': 'main'})
# Install python-gitlab using (pip install --upgrade python-gitlab) to enable gitlab APIs
print("OK")
#print(f"URL: {url}/{group_name}/{project_name}")