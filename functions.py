"""Make some useful functions for the main program."""
from hashlib import sha1
from os import getcwd
from os.path import exists, isdir, isfile, abspath, dirname, join, getmtime
from time import strftime

BUF_SIZE = 65536  # Let's read stuff in 64Kb chunks!


def create_file(file_path):
    """Create a file if it doesn't exist.

    Args:
        file_path: This is the file to be created.
    """
    if not exists(file_path):
        with open(file_path, 'w'):
            pass


def check_lgit_exist():
    """Check if the directory (or its parent) has a .lgit directory."""

    def check_lgit_path(path):
        """Check lgit file if it's exists."""
        if isfile(path):
            print('fatal: invalid gitfile format: {}'.format(path))
        elif isdir(path):
            return True
        return False

    if exists('.lgit'):
        lgit_path = abspath('.lgit')
        if check_lgit_path(lgit_path):
            return True
    else:
        parent_dir = dirname(getcwd())
        lgit_parent = join(parent_dir, '.lgit')
        if check_lgit_path(lgit_parent):
            return True
    return False


def hashing_sha1_file(path_file):
    """Hashing a file with SHA1.

    Args:
        path_file: This is the file to SHA1 hashing.
    """
    # First construct a hash object:
    sha1_hash = sha1()
    with open(path_file, 'rb') as file:
        while True:
            data = file.read(BUF_SIZE)
            if not data:
                break
            sha1_hash.update(data)
    return sha1_hash.hexdigest()


def format_mtime(path_file):
    """Convert modification time of the file to a formatted string.

    Args:
        path_file: This is the file to be convert the modification time.

    Returns: The formatted timestamp of modification time of the file.
    """
    return strftime('%Y%m%d%H%M%S', getmtime(path_file))


def raise_command_error(command):
    """Check if lgit init have been done yet.

    Args:
        command: This is the command you typed.
    """
    if command != 'init' and not check_lgit_exist():
        print('fatal: not a git repository (or any of the parent directories)')
        return True
    return False
