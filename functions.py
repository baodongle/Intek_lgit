"""Make some useful functions for the main program."""
from datetime import datetime
from hashlib import sha1
from os import getcwd, makedirs, walk
from os.path import exists, isdir, isfile, abspath, dirname, join, getmtime, relpath

BUF_SIZE = 65536  # Let's read stuff in 64Kb chunks!


def create_file(file_path):
    """Create a file if it doesn't exist.

    Args:
        file_path: This is the file to be created.
    """
    if not exists(file_path):
        with open(file_path, 'w'):
            pass


def read_file(file_name):
    """ Read contents of file.

    Args:
        file_name: The file need to be read contents.

    Returns: The contents of file.

    """
    with open(file_name, 'r') as file:
        content = file.read()
    return content


def make_directory(dir_path):
    """Create a directory if it doesn't exist.

    Args:
        dir_path: The directory to be created.
    """
    try:
        makedirs(dir_path)
    except FileExistsError:
        pass


def check_lgit_exist():
    """Check if the directory (or its parent) has a .lgit directory."""

    def __check_lgit_path(path):
        """Check lgit file if it's exists."""
        if isfile(path):
            print('fatal: invalid gitfile format: %s' % path)
        elif isdir(path):
            return True
        return False

    if exists('.lgit'):
        lgit_path = abspath('.lgit')
        if __check_lgit_path(lgit_path):
            return True
    else:
        parent_dir = dirname(getcwd())
        lgit_parent = join(parent_dir, '.lgit')
        if __check_lgit_path(lgit_parent):
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
            if not data:  # end of file reached
                break
            sha1_hash.update(data)
    return sha1_hash.hexdigest()


def format_mtime(path_file):
    """Convert modification time of the file to a formatted string.

    Args:
        path_file: The file to be convert the modification time.

    Returns:
        The formatted timestamp of the file's modification time
            represent year, month, day, hour, minute and second.
    """
    timestamp = datetime.fromtimestamp(getmtime(path_file))
    return timestamp.strftime('%Y%m%d%H%M%S')


def get_timestamp_of_current_time():
    """Get the timestamp of the current time.

    Returns:
        timestamp: The timestamp represent year, month, day, hour, minute and second..
        ms_timestamp: The timestamp to milliseconds.

    """
    current_time = datetime.now()
    timestamp = current_time.strftime('%Y%m%d%H%M%S')
    ms_timestamp = current_time.strftime('%Y%m%d%H%M%S.%f')
    return timestamp, ms_timestamp


def check_command_error(command):
    """Check if lgit init have been done yet.

    Args:
        command: This is the command you typed.
    """
    if command != 'init' and not check_lgit_exist():
        print('fatal: not a git repository (or any of the parent directories)')
        return True
    return False


def copy_file_to_another(source, destination):
    """Copy the contents of source file to destination."""
    with open(source, 'rb') as src, open(destination, 'wb+') as dst:
        while True:
            data = src.read(BUF_SIZE)
            if not data:  # end of file reached
                break
            dst.write(data)


def get_files_skip_lgit(directory='.'):
    """ Get all files in a directory.

    This function will generate the file names in a directory
    tree by walking the tree either top-down. For each directory
    in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).

    Args:
        directory: The directory tree to get files.

    Returns:
        The list of file in a directory tree (skip .lgit directory).
    """
    file_paths = []  # List which will store all of the relative filepath.

    # Walk the tree.
    for root, dirs, files in walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d != '.lgit']
        for file_name in files:
            rel_dir = relpath(root, directory)
            if rel_dir == '.':
                rel_file = file_name
            else:
                # Join the two strings in order to form the relative filepath:
                rel_file = join(rel_dir, file_name)
            file_paths.append(rel_file)  # Add it to the list.
    return sorted(file_paths)  # Self-explanatory.


def get_readable_date(timestamp):
    """Format the timestamp to a human-readable date.

    Args:
        timestamp: The timestamp with milliseconds.

    """
    year = int(timestamp[:4])
    month = int(timestamp[4:6])
    day = int(timestamp[6:8])
    hour = int(timestamp[8:10])
    minute = int(timestamp[10:12])
    second = int(timestamp[12:14])
    return datetime(year, month, day, hour, minute,
                    second).strftime('%a %b %d %H:%M:%S %Y')
