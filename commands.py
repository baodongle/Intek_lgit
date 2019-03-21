"""Present commands in lgit program."""
from os import environ, _exit, unlink, rmdir
from os.path import exists, isfile, isdir, abspath

from functions import (make_directory, create_file, copy_file_to_another,
                       format_mtime, get_files_in_dir, hashing_sha1_file)


def execute_lgit_init():
    """Initialize version control in the current directory."""

    def _create_lgit_folders():
        """Create directories in .lgit structure."""
        lgit_folders = [
            '.lgit', '.lgit/objects', '.lgit/commits', '.lgit/snapshots'
        ]
        for folder in lgit_folders:
            make_directory(folder)

    def _create_lgit_files():
        """Create files in .lgit structure."""
        lgit_files = ['.lgit/index', '.lgit/config']
        for file in lgit_files:
            create_file(file)

    def _init_config():
        """Initialize the name of the author in the file config."""
        with open('.lgit/config', 'w') as config:
            config.write(environ['LOGNAME'])

    if exists('.lgit'):
        print(
            "Reinitialized existing Git repository in %s/" % abspath('.lgit'))
    else:
        print("Initialized empty Git repository in %s/" % abspath('.lgit'))
    _create_lgit_folders()
    _create_lgit_files()
    _init_config()


def execute_lgit_add(args):
    """Add file contents to the index."""

    def _add_file_to_lgit_database(file, hash_value):
        """Store a copy of the file contents in the lgit database."""
        dir_path = '.lgit/objects/{}/'.format(hash_value[:2])
        make_directory(dir_path)
        copy_file_to_another(file, dir_path + hash_value[2:])

    def _update_index(file, hash_value):
        """Update the file information in the index file."""
        timestamp = format_mtime(file)
        with open('.lgit/index', 'br+') as index:
            content_index = index.readlines()
            print(content_index)
            index.seek(0)
            added = False
            for line in content_index:
                if line.endswith((file + '\n').encode()):
                    index.write(timestamp.encode())
                    index.seek(42, 1)
                    index.write(hash_value.encode())
                    added = True
                else:
                    index.seek(len(line), 1)
            if not added:
                empty_hash = ' ' * 40
                line_index = '%s %s %s %s %s\n' % (
                    timestamp, hash_value, hash_value, empty_hash, file)
                index.write(line_index.encode())

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
        _add_file_to_lgit_database(path, sha1_value)
        _update_index(path, sha1_value)


def execute_lgit_rm(args):
    """Remove a file from the working directory and the index."""

    def _remove_file_index(a_file):
        """Remove the information of the tracked a_file.

        Args:
            a_file: The tracked file.

        Returns:
            Boolean (True/False): if a_file exist in the index file.

        """
        with open('.lgit/index', 'r+') as index:
            contents = index.readlines()
            had_file = False
            for line in contents:
                if line.endswith(a_file + '\n'):
                    contents.remove(line)
                    had_file = True
            index.truncate(0)
            index.write(''.join(contents))
        return had_file

    for file in args.files:
        if isdir(file):
            print("fatal: not removing '%s' recursively" % file)
            _exit(1)
        if exists(file):
            # If the file exists in the index file:
            hash_value = hashing_sha1_file(file)
            directory = '.lgit/object/' + hash_value[:2]
            file_data = '.lgit/object/' + hash_value[2:]
            if _remove_file_index(file):
                unlink(file)
                unlink(file_data)
                try:
                    rmdir(directory)
                except OSError:
                    pass

            else:
                print("fatal: pathspec '%s' did not match any files" % file)
                _exit(1)
        else:
            print("fatal: pathspec '%s' did not match any files" % file)
            _exit(1)


def config_lgit(args):
    """Set a user for authoring the commits."""
    with open('.lgit/config', 'w') as config:
        config.write(args.author + '\n')


def execute_lgit_commit(args):
    """Create a commit with the changes currently staged."""
    pass


def display_lgit_status(args):
    """Show the working tree status."""
    pass


def list_lgit_files(args):
    """Show information about files in the index and the working tree."""
    pass


def show_lgit_log(args):
    """Show the commit history."""
    pass
