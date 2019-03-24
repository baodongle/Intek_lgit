"""Implement git's branches and merging."""
from os import listdir, rmdir, unlink
from os.path import dirname, exists

from functions import (format_mtime, get_current_branch, make_directory,
                       read_file, write_file)


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
        for file in sorted(listdir(lgit_path + '/.lgit/refs/heads')):
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

    def _report_error(list_file):
        print('''error: Your local changes to the following files would be
        overwritten by checkout:''')
        for file_name in list_file:
            print('\t' + file_name)
        print('''Please, commit your changes or stash them before you can
        switch branches.''')
        print('Aborting')

    def _remove_files_in_index():
        """Remove all files in lgit's index."""
        for index in content_index:
            file_name = index[138:]
            unlink(file_name)
            # If there's any empty directory in directory 'file_name':
            try:
                while '/' in file_name:
                    file_name = dirname(file_name)
                    rmdir(file_name)
                rmdir(file_name)
            except OSError:
                pass

    def _create_working_files(file_path, content):
        # Create tree directory that the file in it:
        if '/' in file_path:
            parent_paths = file_path.split('/')[:-1]
            for i in range(len(parent_paths) - 1):
                make_directory('/'.join(parent_paths[:i + 1]))
        # Create new file:
        write_file(file_path, content)

    def _setup_for_new_branch(commit):
        new_content_index = ''
        content_snap = read_file(lgit_path +
                                 '/.lgit/snapshots/%s' % commit).split('\n')
        for line_snap in content_snap:
            content = read_file(lgit_path + '/.lgit/objects/%s/%s' %
                                (line_snap[:2], line_snap[2:40]))
            file_name = content_snap[41:]
            _create_working_files(file_name, content)
            timestamp = format_mtime(file_name)
            new_content_index += (timestamp + (' ' + line_snap[:40]) * 3 + ' '
                                  + file_name + '\n')
            write_file(lgit_path + '/.lgit/index', new_content_index)

    def _update_head_file(branch_name):
        content = 'ref: refs/head/%s' % branch_name
        write_file(lgit_path + '/.lgit/HEAD', content)

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
            else:
                last_commit = read_file(lgit_path + '/.lgit/refs/heads/%s' %
                                        args.branch_name).split('\n')[0]
                current_stage = read_file(
                    lgit_path + '/.lgit/refs/heads/%s' % branch).split('\n')[0]
                if last_commit != current_stage:
                    content_index = read_file(lgit_path +
                                              '/.lgit/index').split('\n')
                    # List files has change without 'commit' command:
                    error_files = []
                    for line in content_index:
                        file = line[138:]
                        if line[15:55] != line[97:137]:
                            error_files.append(file)
                    if error_files:
                        _report_error(error_files)
                        exit()
                    else:
                        _remove_files_in_index()
                        _setup_for_new_branch(last_commit)
                _update_head_file(args.branch_name)
                print("Switch to branch '%s'" % args.branch_name)
    else:
        print('fatal: You are on a branch yet to be born')


def execute_lgit_merge(args, lgit_path):
    """Merge one branch onto another."""


def execute_lgit_stash(args, lgit_path):
    """Stash the changes in a dirty working directory away."""
