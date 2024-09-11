#!/usr/bin/env python3

import paramiko
import argparse



parser = argparse.ArgumentParser(description="Create a new MySQL database and user via SSH")
    
#parser.add_argument('-sh', '--ssh_host', dest='ssh_host', required=True, help='SSH host')
#parser.add_argument('-sp', '--ssh_port', dest='ssh_port', type=int, required=True, help='SSH port')
#parser.add_argument('-su', '--ssh_user', dest='ssh_user', required=True, help='SSH username')
#parser.add_argument('-ss', '--ssh_password', dest='ssh_password', required=True, help='SSH password')

parser.add_argument('-mh', '--mysql_host', dest='mysql_host', required=True, help='MySQL host')
parser.add_argument('-mp', '--mysql_port', dest='mysql_port', type=int, required=True, help='MySQL port')
parser.add_argument('-mr', '--mysql_root_user', dest='mysql_root_user', required=True, help='MySQL root username')
parser.add_argument('-mrp', '--mysql_root_password', dest='mysql_root_password', required=True, help='MySQL root password')
parser.add_argument('-db', '--new_db_name', dest='new_db_name', required=True, help='New database name')
parser.add_argument('-nu', '--new_user', dest='new_user', required=True, help='New MySQL username')
parser.add_argument('-nup', '--new_user_password', dest='new_user_password', required=True, help='New MySQL user password')

args = parser.parse_args()

def create_mysql_user_and_db(ssh_host, ssh_port, ssh_user, ssh_password, mysql_host, mysql_port, mysql_root_user, mysql_root_password, new_db_name, new_user, new_user_password):
    try:    
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

        mysql_command = f"""
        echo {ssh_password} | sudo -S mysql -h {mysql_host} -P {mysql_port} -u {mysql_root_user} -p'{mysql_root_password}' -e \"
        CREATE DATABASE {new_db_name};
        CREATE USER '{new_user}'@'%' IDENTIFIED BY '{new_user_password}';
        GRANT ALL PRIVILEGES ON {new_db_name}.* TO '{new_user}'@'%';
        FLUSH PRIVILEGES;\"
        """

        stdin, stdout, stderr = ssh.exec_command(mysql_command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        filtered_error = "\n".join(
            line for line in error.splitlines() 
            if "[Warning] Using a password on the command line interface can be insecure." not in line
            and "[sudo] password for" not in line
        )

        ssh.close()
        #error = error.replace(f"[Warning] Using a password on the command line interface can be insecure.\n", "")


        #if filtered_error:
        #    print(f"Error: {filtered_error}")
        #else:
        #    print(f"Database '{new_db_name}' and user '{new_user}' created successfully with all privileges.")

        if "ERROR" in filtered_error:
            if "Can't connect" in filtered_error:
                print("Error: Could not connect to MySQL host. Please check the connection details.")
            elif "database exists" in filtered_error:
                print(f"Error: Database '{new_db_name}' already exists.")
            elif "Access denied" in filtered_error:
                print("Error: Access denied. Please check the MySQL root credentials.")
            elif "CREATE USER failed" in filtered_error:
                print(f"Error: User '{new_user}' already exists. Skipping user creation and Database '{new_db_name}' created successfully")

            else:
                print(f"Error: {filtered_error}")
        else:
            print(f"Database '{new_db_name}' and user '{new_user}' created successfully with all privileges. {new_user_password}")

    except paramiko.SSHException as ssh_error:
        print(f"SSH Error: {ssh_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")


create_mysql_user_and_db(
        ssh_host="192.168.1.220",
        ssh_port="22",
        ssh_user="ansible",
        ssh_password="ansible",

        #ssh_host=args.ssh_host,
        #ssh_port=args.ssh_port,
        #ssh_user=args.ssh_user,
        #ssh_password=args.ssh_password,

        
        #mysql_host="",
        #mysql_port="",
        #mysql_root_user="",
        #mysql_root_password="",

        #new_db_name="",
        #new_user="",
        #new_user_password=""


        mysql_host=args.mysql_host,
        mysql_port=args.mysql_port,
        mysql_root_user=args.mysql_root_user,
        mysql_root_password=args.mysql_root_password,
        new_db_name=args.new_db_name,
        new_user=args.new_user,
        new_user_password=args.new_user_password
    )
