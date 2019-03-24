"""Implement git's branches and merging."""
from os import environ, unlink, listdir, stat
from os.path import exists, isfile, isdir

from functions import (make_directory, read_file, copy_file_to_another,
                       format_mtime, get_files_skip_lgit, hashing_sha1_file,
                       get_timestamp_of_current_time, get_readable_date,
                       get_current_branch)


def execute_lgit_init():
    """Initialize version control in the current directory."""

    def _create_lgit_folders():
        """Create directories in .lgit structure."""
        lgit_folders = [
            '.lgit', '.lgit/objects', '.lgit/commits', '.lgit/snapshots',
            '.lgit/refs', '.lgit/refs/heads'
        ]
        for folder in lgit_folders:
            make_directory(folder)

    def _create_index_files():
        """Create lgit's index file."""
        try:
            with open('.lgit/index', 'w'):
                pass
        except PermissionError:
            pass

    def _init_config():
        """Initialize the name of the author in the file config."""
        try:
            with open('.lgit/config', 'w') as config:
                config.write(environ['LOGNAME'])
        except (PermissionError, FileNotFoundError):
            pass

    def _init_head():
        """Create lgit's HEAD file."""
        try:
            with open('.lgit/HEAD', 'w') as head:
                head.write('ref: refs/heads/master')
        except (PermissionError, FileNotFoundError):
            pass

    if exists('.lgit'):
        print("Git repository already initialized.")
    _create_lgit_folders()
    _create_index_files()
    _init_config()
    _init_head()


def execute_lgit_add(args, lgit_path):
    """Add file contents to the index."""

    def _add_file_to_lgit_database(a_file, hash_value):
        """Store a copy of the file contents in the lgit database."""
        dir_path = lgit_path + '/.lgit/objects/%s/' % hash_value[:2]
        make_directory(dir_path)
        copy_file_to_another(a_file, dir_path + hash_value[2:])

    def _update_index(a_file, hash_value):
        """Update the file information in the index file."""
        timestamp = format_mtime(a_file)
        try:
            with open(lgit_path + '/.lgit/index', 'rb+') as index:
                content_index = index.readlines()
                index.seek(0)
                added = False
                for line in content_index:
                    if line.endswith((a_file + '\n').encode()):
                        index.write(timestamp.encode())
                        index.seek(42, 1)
                        index.write(hash_value.encode())
                        added = True
                    else:
                        index.seek(len(line), 1)
                if not added:
                    empty_hash = ' ' * 40
                    line_index = '%s %s %s %s %s\n' % (
                        timestamp, hash_value, hash_value, empty_hash, a_file)
                    index.write(line_index.encode())
        except PermissionError:
            pass

    file_paths = []
    if '.' in args.files or '*' in args.files:
        file_paths = get_files_skip_lgit()
    else:
        for file in args.files:
            if isfile(file):
                file_paths.append(file)
            else:
                file_paths.extend(get_files_skip_lgit(file))

    for file_path in file_paths:
        sha1_value = hashing_sha1_file(file_path)
        _add_file_to_lgit_database(file_path, sha1_value)
        _update_index(file_path, sha1_value)


def execute_lgit_rm(args, lgit_path):
    """Remove a file from the working directory and the index."""

    def _remove_file_index(a_file):
        """Remove the information of the tracked a_file.

        Args:
            a_file: The tracked file.

        Returns:
            True/False: if a_file exist in the index file.

        """
        try:
            with open(lgit_path + '/.lgit/index', 'r+') as index:
                contents = index.readlines()
                had_file = False
                for line in contents:
                    if line.endswith(a_file + '\n'):
                        contents.remove(line)
                        had_file = True
                index.truncate(0)
                index.write(''.join(contents))
            return had_file
        except (PermissionError, FileNotFoundError):
            pass

    for file in args.files:
        if isdir(file):
            exit("fatal: not removing '%s' recursively" % file)
        if exists(file):
            if _remove_file_index(file):
                unlink(file)
            else:
                exit("fatal: pathspec '%s' did not match any files" % file)
        else:
            exit("fatal: pathspec '%s' did not match any files" % file)


def config_lgit(args, lgit_path):
    """Set a user for authoring the commits."""
    try:
        with open(lgit_path + '/.lgit/config', 'w') as config:
            config.write(args.author + '\n')
    except PermissionError:
        pass


def execute_lgit_commit(args, lgit_path):
    """Create a commit with the changes currently staged."""
    timestamp_now, ms_timestamp_now = get_timestamp_of_current_time()

    def _create_commit_object(message):
        """Create the commit object when commit the changes."""

        # Get the author name for the commits:
        author = read_file(lgit_path + '/.lgit/config').strip('\n')
        # If the config file is empty:
        if not author:
            exit()
        try:
            with open(lgit_path + '/.lgit/commits/%s' % ms_timestamp_now,
                      'w') as commit:
                # Write file in the commits directory:
                commit.write(
                    '%s\n%s\n\n%s\n\n' % (author, timestamp_now, message))
        except PermissionError:
            pass

    def _update_index_and_snapshot():
        """Update the index file and create snapshots."""
        try:
            with open(lgit_path + '/.lgit/index', 'rb+') as index, open(
                    lgit_path + '/.lgit/snapshots/%s' % ms_timestamp_now,
                    'ab+') as snapshot:
                content_index = index.readlines()
                index.seek(0)
                for line in content_index:
                    hash_value = line[56:96]
                    file_path = line[138:]
                    snapshot.write(hash_value + b' ' + file_path)
                    index.seek(97, 1)
                    index.write(hash_value)
                    index.seek(len(line) - 137, 1)
        except PermissionError:
            pass

    def _update_branch_head():
        """Update the head of the current branch."""
        branch = get_current_branch(lgit_path + '/.lgit/HEAD')
        try:
            with open(lgit_path + '/.lgit/refs/heads/%s' % branch,
                      'w') as file:
                file.write(ms_timestamp_now)
        except PermissionError:
            pass

    # If the command 'add' has been never called:
    if not stat(lgit_path + '/.lgit/index').st_size:
        display_lgit_status(args, lgit_path)  # Show untracked files.
    else:
        _create_commit_object(args.m)
        _update_index_and_snapshot()
        _update_branch_head()


def display_lgit_status(args, lgit_path):
    """Show the working tree status."""

    def _print_status_header():
        """Print the header of the status."""
        print('On branch master')
        # If the command 'add' has been never called:
        if args.command == 'commit' and not stat(lgit_path +
                                                 '/.lgit/index').st_size:
            print('\nInitial commit\n')
        # If the command 'commit' has been never called:
        if args.command == 'status' and not listdir(lgit_path +
                                                    '/.lgit/commits'):
            print('\nNo commits yet\n')

    def _report_changes_to_be_committed(files):
        """Print information about changes to be committed."""
        print('Changes to be committed:')
        print('  (use "./lgit.py reset HEAD ..." to unstage)\n')
        for file in files:
            print('\tmodified:', file)
        print()

    def _report_changes_not_staged_for_commit(files):
        """Print information about changes not staged for commit."""
        print('Changes not staged for commit:')
        print('  (use "./lgit.py add ..." to update what will be committed)')
        print('''  (use "./lgit.py checkout -- ..." to discard changes in
            working directory)\n''')
        for file in files:
            print('\tmodified:', file)
        print('''\nno changes added to commit (use "./lgit.py add and/or
            "./lgit.py commit -a")''')

    def _report_untracked_files(files):
        """Report the untracked files when call the status command.

        Args:
            files: The files that are present in the working in the working
                directory, but have never been lgit add'ed.

        """

        print('Untracked files:')
        print(
            '  (use "./lgit.py add ..." to include in what will be committed)',
            end='\n\n')
        for file in files:
            print('\t' + file)
        print()
        # print('nothing added to commit but untracked files present
        # (use "./lgit.py add" to track)')

    def _update_index(file):
        """Update the index of the file in the working directory.

        Returns: Index of line that contains the information of file.
        """
        content_index = read_file(lgit_path + '/.lgit/index').split('\n')
        hash_value = hashing_sha1_file(file)
        timestamp, _ = get_timestamp_of_current_time()
        try:
            with open(lgit_path + '/.lgit/index', 'rb+') as index:
                current_line = None
                for line in content_index:
                    if line[138:] == file:
                        current_line = '%s %s %s' % (timestamp, hash_value,
                                                     line[56:])
                        index.write((timestamp + ' ' + hash_value).encode())
                        break
                    else:
                        index.seek(len(line) + 1, 1)
            return current_line
        except PermissionError:
            pass

    def _classify_files():
        """Classify files in the working directory to 3 groups."""
        list_files = get_files_skip_lgit()
        untracked_files = []
        files_to_be_committed = []
        files_not_staged_for_commit = []
        for file in list_files:
            info_file = _update_index(file)
            if info_file:
                if info_file[56:96] != info_file[15:55]:
                    files_not_staged_for_commit.append(file)
                if info_file[97:137] != info_file[56:96]:
                    files_to_be_committed.append(file)
            else:
                untracked_files.append(file)
        return (untracked_files, files_to_be_committed,
                files_not_staged_for_commit)

    _print_status_header()
    untracked, to_be_committed, not_staged_for_commit = _classify_files()
    if to_be_committed:
        _report_changes_to_be_committed(to_be_committed)
    if not_staged_for_commit:
        _report_changes_not_staged_for_commit(not_staged_for_commit)
    if untracked:
        _report_untracked_files(untracked)


def list_lgit_files(args, lgit_path):
    """Show information about files in the index and the working tree."""

    content_index = read_file(lgit_path + '/.lgit/index').split('\n')
    list_files = []
    for line in content_index:
        list_files.append(line[138:])
    for file in sorted(list_files):
        if file != '':
            print(file)


def show_lgit_log(args, lgit_path):
    """Show the commit history."""

    def _display_commit(file):
        """Display each commit."""
        content = read_file(lgit_path + '/.lgit/commits/%s' % file).split('\n')
        print('commit ' + file)
        print('Author: ' + content[0])
        print('Date: ' + get_readable_date(file), end='\n\n')
        print('    %s\n' % content[3])

    list_commits = listdir(lgit_path + '/.lgit/commits')
    list_commits.sort(reverse=True)
    for commit in list_commits:
        _display_commit(commit)


def execute_lgit_branch(args, lgit_path):
    """List or create branches."""

    def _create_branch(name):
        # If branch name exists:
        if exists(lgit_path + '/.lgit/refs/heads/' + name):
            exit("fatal: A branch named '%s' already exists." % name)
        # Create new branch:
        snapshots = listdir(lgit_path + '/.lgit/snapshots')
        with open(lgit_path + '/.lgit/refs/heads/%s' % name, 'w') as branch:
            if snapshots:
                branch.write(max(snapshots))

    def _list_branches():
        branch = get_current_branch(lgit_path + '/.lgit/HEAD')
        for file in listdir(lgit_path + '/.lgit/refs/heads'):
            if file == branch:
                print('*', file)
            else:
                print(' ', file)

    if args.branch_name:
        # If call branch command without ever have commit yet:
        if not listdir(lgit_path + '/.lgit/refs/heads'):
            exit("fatal: Not a valid object name: 'master'.")
        _create_branch(args.branch_name)
    else:
        _list_branches()


def execute_lgit_checkout(args, lgit_path):
    """Switch branches or restore working tree files."""
    list_branches = listdir(lgit_path + '/.lgit/refs/heads')
    if list_branches:
        if args.branch_name not in list_branches:
            print("error: pathspec '%s' did not match any file(s) known to git"
                  % args.branch_name)
        else:
            branch = get_current_branch(lgit_path + '/.lgit/HEAD')
            if args.branch_name == branch:
                if branch != 'master':
                    print("Already on '%s'" % branch)


def execute_lgit_merge(args, lgit_path):
    """Merge one branch onto another."""


def execute_lgit_stash(args, lgit_path):
    """Stash the changes in a dirty working directory away."""
