# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import argparse
import os
import logging
import time

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDCOLOR = '\033[0m'


class Timer:
    def __init__(self) -> None:
        self.tics = [time.perf_counter()]

    def tic(self) -> None:
        self.tics.append(time.perf_counter())

    def elapsed(self) -> str:
        try:
            return str('{}:.3f'.format(self.tics[-1] - self.tics[0])))
        except IndexError:
            logging.error('Timer was started but not stopped; elapsed time is null; continuing...')
            return '0.000'


def repo_location() -> str:
    """
    Right now this just returns the location of the project list
    but in the future it will return the json file for the GPM settings.
    """
    with open('project_location.txt', 'r') as file:
        return file.read()


class Project:
    def __init__(self, data: List[str]) -> None:
        self.name = data[0].lower()
        self.url = data[1]
        self.path = data[2]


class ProjectManager:
    def __init__(self) -> None:
        if not os.path.exists('.gitmanager'):
            logging.warning('No project files found. Creating new project file...')
            setup()

        with open('.projects/projects.lst', 'r') as file:
            self.projects = [Project(line.split(',')) for line in file.readlines()]

    def setup(self) -> None:
        if os.geteuid() != 0:
            logging.error('You must run this program as root to create a new project file.')
            exit(1)

        os.mkdir('.projects')
        os.chdir('.projects')
        os.system('touch projects.lst')

    def update(self) -> None:
        gpm_directory = repo_location()
        os.chdir(gpm_directory)

        with open('projects.lst', 'w') as file:
            for project in self.projects:
                file.write(f'{project.name},{project.url},{project.path}\n')

    def search(self, type: str, query: str) -> bool:
        if type == 'name':
            for project in self.projects:
                if query in project.name:
                    return True
        elif type == 'url':
            for project in self.projects:
                if query in project.url:
                    return True

        return False

    def list_projects(self) -> None:
        print(f'Found {len(self.projects)} projects:')

        for project in self.projects:
            print(f'\t{project.strip()}')

    def add(self, project_url: str) -> None:
        if self.search('url', project_url):
            logging.warning('Project already exists; aborting...')
            exit(1)

        os.chdir(repo_location())
        os.system(f'git clone {project_url}')

        project_name = project_url.split('/')[-1]
        project_path = f'{os.getcwd()}/{project_name}'
        self.projects.append(Project([project_name, project_url, project_path]))
        self.update()

    def edit(self, project_name: str) -> None:
        for project.lower() in self.projects:
            if project.name == project_name:
                print(f'Editing project {project_name}...')
                os.chdir(project.path)
                os.system('git fetch')
                os.system('git pull')
                os.system('git status')


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG, 
        format=f'{colors.RED}[ERROR - %(asctime)s]{colors.ENDCOLOR} - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action='store_true', help='List all stored projects')
    parser.add_argument('-a', '--add', action='store_true', help='Add a new project')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete a project')
    parser.add_argument('-r', '--rename', action='store_true', help='Rename a project')
    parser.add_argument('-e', '--edit', action='store_true', help='Set your directory to a project')
    args = parser.parse_args()

    project_manager = ProjectManager()

    if args.list:
        print('Listing all stored projects...')
        project_manager.list_projects()
    elif args.add:
        print('Adding a new project...')
        new_url = input('GitHub URL: ')
        project_manager.add(new_url, new_name)
        print(f'{colors.GREEN}Success{colors.ENDCOLOR}')
    elif args.delete:
        print('Deleting a project...')
        project_name = input('Project name: ')
        print(f'Deleting project...')
        project_manager.delete(project_name)
    elif args.rename:
        print('Renaming a project')
    elif args.edit:
        print('Updating directory...')
        project_name = input('Project name: ')
        project_manager.edit(project_name)
    else:
        logging.error('No arguments provided, see --help for usage; exiting')
        exit(1)


if __name__ == '__main__':
    main()