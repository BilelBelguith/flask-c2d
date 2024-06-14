#!/usr/bin/env python3

import paramiko
import argparse

def test_ssh_connection(host,port, username, password):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        client.connect(hostname=host,port=port ,  username=username, password=password)
        client.close()
        return "OK"
    except paramiko.AuthenticationException:
        return "Authentication failed, please verify your credentials"
    except paramiko.SSHException as sshException:
        return f"Unable to establish SSH connection: {sshException}"
    except paramiko.BadHostKeyException as badHostKeyException:
        return f"Unable to verify server's host key: {badHostKeyException}"
    except Exception as e:
        return f"Operation error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test SSH Connection')
    #parser.add_argument('host', help='The SSH server hostname or IP address')
    #parser.add_argument('username', help='The SSH username')
    #parser.add_argument('password', help='The SSH password')

    parser.add_argument('-s', '--hostName', dest='host',nargs='+')
    parser.add_argument('-u', '--username', dest='username',nargs='+')
    parser.add_argument('-p', '--password', dest='password',nargs='+')
    parser.add_argument('-d', '--port', dest='port',nargs='+')



    args = parser.parse_args()
    
    result = test_ssh_connection(args.host[0], args.port[0],args.username[0], args.password[0])
    print(result)
