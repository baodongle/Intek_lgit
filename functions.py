"""Make some useful functions for the main program."""
from datetime import datetime
from hashlib import sha1
from os import getcwd, makedirs, walk
from os.path import isdir, isfile, dirname, join, getmtime, relpath

BUF_SIZE = 65536  # Let's read stuff in 64Kb chunks!


def read_file(file_name):
    """ Read contents of file.

    Args:
        file_name: The file need to be read contents.

    Returns: The contents of file.

    """
    try:
        with open(file_name, 'r') as file:
            content = file.read()
        return content
    except (PermissionError, FileNotFoundError):
        pass


def make_directory(dir_path):
    """Create a directory if it doesn't exist.

    Args:
        dir_path: The directory to be created.

    """
    try:
        makedirs(dir_path)
    except FileExistsError:
        pass


def write_file(file_name, content):
    """Write the content into a file."""
    try:
        with open(file_name, 'w') as file:
            file.write(content)
    except PermissionError:
        pass


def find_lgit_directory():
    """Check if the directory (or its parent) has a .lgit directory.

    Returns: Full path of the directory that has .lgit directory in it.

    """

    current_path = getcwd()
    for _ in range(2):  # Check 2 levels.
        if isfile(current_path + '/.lgit'):
            exit('fatal: invalid gitfile format: %s/.lgit' % current_path)
        if isdir(current_path + '/.lgit'):
            return current_path
        current_path = dirname(current_path)
    return None


def hashing_sha1_file(path_file):
    """Hashing a file with SHA1.

    Args:
        path_file: This is the file to SHA1 hashing.
    """
    # First construct a hash object:
    sha1_hash = sha1()
    try:
        with open(path_file, 'rb') as file:
            while True:
                data = file.read(BUF_SIZE)
                if not data:  # end of file reached
                    break
                sha1_hash.update(data)
        return sha1_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        pass


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
        timestamp:      The timestamp represent year, month, day, hour, minute
                            and second.
        ms_timestamp:   The timestamp to milliseconds.

    """
    current_time = datetime.now()
    timestamp = current_time.strftime('%Y%m%d%H%M%S')
    ms_timestamp = current_time.strftime('%Y%m%d%H%M%S.%f')
    return timestamp, ms_timestamp


def copy_file_to_another(source, destination):
    """Copy the contents of source file to destination."""
    try:
        with open(source, 'rb') as src, open(destination, 'wb+') as dst:
            while True:
                data = src.read(BUF_SIZE)
                if not data:  # end of file reached
                    break
                dst.write(data)
    except (PermissionError, FileNotFoundError):
        pass


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


def get_current_branch(head_file):
    """Get the current lgit branch from head_file

    Returns: Name of the current lgit branch.
    """
    content_head = read_file(head_file)
    return content_head.strip('\n').split('/')[-1]
