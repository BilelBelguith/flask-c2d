# setup env by running ansible env check 
#create and inject inventory file (/etc/ansible/hosts)
#create project depends on type and version (path specific or default /var/www/html/projectname)
#create web conf depends on server type nginx or apache2 (inject file on specific path or default /etc/apache2/site-enabled/file.conf)
#set ssl for dns
import argparse
import os
import subprocess
import pexpect

parser = argparse.ArgumentParser(description='setup env , project , webserver')

parser.add_argument('-u', '--userName', dest='user_name',nargs='+', help='user name for ssh cnx')
parser.add_argument('-p', '--userPass', dest='user_pass',nargs='+', help='user password for ssh cnx')
parser.add_argument('-s', '--hostName', dest='host_name',nargs='+', help='host name for ssh cnx')


#check env depends on project type ( typo3 => coposer + php / fpm check)
#                                    WP  => wordpress version / php fpm              

args = parser.parse_args()
user_name=args.user_name[0]
user_pass=args.user_pass[0]
host_name=args.host_name[0]

hosts_file_path = "/etc/ansible/hosts"
password_file_path="../playbooks/pass.txt"

hosts_content = """  
[web_servers]
web_server1 ansible_host=%s ansible_user=%s
""" %(host_name,user_name)

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

        # Start the command using pexpect
        child = pexpect.spawn(command)

        # Handle the different expected outputs
        index = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'password:', pexpect.EOF, pexpect.TIMEOUT])

        if index == 0:
            # Accept the fingerprint
            child.sendline('yes')
            child.expect('password:')
            child.sendline(password)
        elif index == 1:
            # Send the password
            child.sendline(password)

        # Print the output from the command
        child.interact()

    except pexpect.exceptions.ExceptionPexpect as e:
        # Print the error if the command fails
        print(f"Error: {str(e)}")


#add_ssh_key = ["ssh-copy-id" f"{user_name}@{host_name}"]
        
ssh_copy_id(user_name, host_name, user_pass)     
playbook_command = ["ansible-playbook", "../playbooks/env-check-typo3-project.yaml", "--extra-vars", f"ansible_ssh_pass={user_pass} ansible_sudo_pass={user_pass}" , "-v"]

try:
    subprocess.run(playbook_command, check=True)
    print("Env is well set.")
except subprocess.CalledProcessError:
    print("Env is not that good.")


    