#!/usr/bin/env python3
from os import environ, makedirs
from os.path import exists, join


def create_main_lgit(path=None):
    if path:
        path_lgit = join(path, '.lgit')
    else:
        path_lgit = '.lgit'
    try:
        makedirs(path_lgit, 0o755)
    except FileExistsError:
        pass
    return path_lgit


def execute_lgit_init(path=None):
    lgit_folders = ['objects', 'commits', 'snapshots']
    lgit_files = ['index', 'config']
    main_lgit = create_main_lgit(path)

    for folder in lgit_folders:
        try:
            makedirs(join(main_lgit, folder), 0o755)
        except FileExistsError:
            pass

    for file in lgit_files:
        file_path = join(main_lgit, file)
        if not exists(file_path):
            with open(file_path, 'w') as f:
                if file == 'config':
                    f.write(environ['LOGNAME'] + '\n')


def main():
    execute_lgit_init()


if __name__ == "__main__":
    main()
