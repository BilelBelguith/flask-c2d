#!/usr/bin/python3

import argparse
import os
import subprocess
import pexpect

parser = argparse.ArgumentParser(description='setup env , project , webserver')

parser.add_argument('-u', '--userName', dest='user_name',nargs='+', help='user name for ssh cnx')
parser.add_argument('-p', '--userPass', dest='user_pass',nargs='+', help='user password for ssh cnx')
parser.add_argument('-s', '--hostName', dest='host_name',nargs='+', help='host name for ssh cnx')
parser.add_argument('-d', '--port'    , dest='port'     ,nargs='+', help='port number for ssh cnx')
parser.add_argument('--php' , dest='php_version' , nargs='+' , help='php version')
parser.add_argument('--composer' , dest='composer_version' , nargs='+' , help='composer version')  
parser.add_argument('--path' , dest='path' , nargs='+' , help='project path')  
parser.add_argument('--name' , dest='name' , nargs='+' , help='project name')  
parser.add_argument('--projectversion' , dest='projectversion' , nargs='+' , help='project version')  
parser.add_argument('--webserver' , dest='webserver' , nargs='+' , help='project web server')  
parser.add_argument('--dns' , dest='dns' , nargs='+' , help='project domaine name')  


#check env depends on project type ( typo3 => coposer + php / fpm check)
#                                    WP  => wordpress version / php fpm              

args = parser.parse_args()
user_name=args.user_name[0]
user_pass=args.user_pass[0]
host_name=args.host_name[0]
port=args.port[0]
php_version=args.php_version[0]
composer_version=args.composer_version[0]

path=args.path[0]
name=args.name[0]
projectversion=args.projectversion[0]
webserver=args.webserver[0]
dns=args.dns[0]


hosts_file_path = "/etc/ansible/hosts"
password_file_path="./playbooks/pass.txt"

hosts_content = """  
[web_servers]
web_server1 ansible_host=%s ansible_port=%s ansible_user=%s
""" %(host_name,port,user_name)




try:
    # Read the password from the file
    with open(password_file_path, 'r') as password_file:
        sudo_password = password_file.read().strip()

    # Prepare the sudo command to write to a file with the password included
    sudo_command = ["sudo", "-S", "tee", hosts_file_path]

    # Run the sudo command, providing the sudo password and hosts content as input
    subprocess.run(sudo_command, input=f"{sudo_password}\n{hosts_content}", check=True, text=True)

except FileNotFoundError:
    print("Error: Password file not found.")
except subprocess.CalledProcessError as e:
    print("Error running or writing to file:", e)


def ssh_copy_id(username, server_address, password):
    try:
        # Construct the ssh-copy-id command
        command = f'ssh-copy-id {username}@{server_address}'

        child = pexpect.spawn(command)
        index = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'password:', pexpect.EOF, pexpect.TIMEOUT])

        if index == 0:
            child.sendline('yes')
            child.expect('password:')
            child.sendline(password)
        elif index == 1:
            child.sendline(password)

        child.interact()

    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"Error: {str(e)}")


#add_ssh_key = ["ssh-copy-id" f"{user_name}@{host_name}"]
        
ssh_copy_id(user_name, host_name, user_pass)     
playbook_command_env = ["ansible-playbook",
                    "./playbooks/env-check-typo3-project.yaml",
                    "--extra-vars", f"ansible_ssh_pass={user_pass} ansible_sudo_pass={user_pass}",
                    "-e",f"php_version={php_version} composer_version={composer_version} ",
                    ]


playbook_command_create = ["ansible-playbook",
                    "./playbooks/create_typo3_project.yaml",
                    "--extra-vars", f"ansible_ssh_pass={user_pass} ansible_sudo_pass={user_pass}",
                    "-e",f"project_path={path} project_name={name} project_version={projectversion} web_server={webserver} domain_name={dns} php_version={php_version} ",
                    ]

#try:
#    subprocess.run(playbook_command_env, check=True)
#    print("Env is well set and project created")
#    subprocess.run(playbook_command_create, check=True)
#    print("OK")
#
#except subprocess.CalledProcessError as e:
#    print(f"Env is not that good check needed: {str(e)}" )

def run_playbook_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("OK")
    else:
        print(f"Error: {result.stderr}")

try:
    run_playbook_command(playbook_command_env)
    run_playbook_command(playbook_command_create)
except subprocess.CalledProcessError as e:
    print(f"Env is not that good, check needed: {str(e)}")



    