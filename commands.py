"""Present commands in lgit program."""
from os import environ, getcwd
from os.path import exists, isfile

from functions import (make_directory, create_file, copy_file_to_another,
                       format_mtime, get_files_in_dir, hashing_sha1_file)


def execute_lgit_init():
    """Initialize version control in the current directory."""

    def __create_lgit_folders():
        """Create directories in .lgit structure."""
        lgit_folders = [
            '.lgit', '.lgit/objects', '.lgit/commits', '.lgit/snapshots'
        ]
        for folder in lgit_folders:
            make_directory(folder)

    def __create_lgit_files():
        """Create files in .lgit structure."""
        lgit_files = ['.lgit/index', '.lgit/config']
        for file in lgit_files:
            create_file(file)

    def __init_config():
        """Initialize the name of the author in the file config."""
        with open('.lgit/config', 'w') as config:
            config.write(environ['LOGNAME'])

    if exists('.lgit'):
        print("Reinitialized existing Git repository in {}/.lgit/".format(
            getcwd()))
    else:
        print("Initialized empty Git repository in {}/.lgit/".format(getcwd()))
    __create_lgit_folders()
    __create_lgit_files()
    __init_config()


def execute_lgit_add(args):
    """Add file contents to the index."""

    def __add_file_to_lgit_database(file, hash_value):
        """Store a copy of the file contents in the lgit database."""
        dir_path = '.lgit/objects/{}/'.format(hash_value[:2])
        make_directory(dir_path)
        copy_file_to_another(file, dir_path + hash_value[2:])

    def __update_index(file, hash_value):
        timestamp = format_mtime(file)
        with open('.lgit/index', 'r+') as index:
            content_index = index.readlines()
            index.seek(0)
            added = False
            for line in content_index:
                if line[138:] == file + '\n':
                    index.write(timestamp)
                    index.seek(42, 1)
                    index.write(hash_value)
                    added = True
                else:
                    index.seek(len(line), 1)
            if not added:
                empty_hash = ' ' * 40
                index.write('%s %s %s %s %s' % (
                    timestamp, hash_value, hash_value, empty_hash, file))

    file_paths = []
    if '.' in args.files or '*' in args.files:
        file_paths = get_files_in_dir('.')
    else:
        for path in args.files:
            if isfile(path):
                file_paths.append(path)
            else:
                file_paths.extend(get_files_in_dir(path))

    for path in file_paths:
        sha1_value = hashing_sha1_file(path)
        __add_file_to_lgit_database(path, sha1_value)
        __update_index(path, sha1_value)
