#!/usr/bin/python3

import subprocess
import argparse
import sys

def create_typo3_project(project_name, project_version, project_path):
    try:
        # Command to create TYPO3 project using Composer
        command = [
            'composer',
            'create-project',
            f'typo3/cms-base-distribution:^{project_version}',
            project_path
        ]

        # Run the Composer command
        subprocess.run(command, check=True)

        print(f"TYPO3 project '{project_name}' created successfully at '{project_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create TYPO3 project. {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create TYPO3 project using Composer')
    parser.add_argument('-n', '--name', required=True, help='Name of the project')
    parser.add_argument('-v', '--version', required=True, help='Version of TYPO3')
    parser.add_argument('-p', '--path', required=True, help='Path where the project should be created')
    args = parser.parse_args()

    project_name = args.name
    project_version = args.version
    project_path = args.path

    project_path_ptoject = project_path+'/'+project_name

    create_typo3_project(project_name, project_version, project_path_ptoject )
