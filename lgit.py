#!/usr/bin/env python3
"""Code a lightweight version of git."""
from argparse import ArgumentParser

from branches import (execute_lgit_branch, execute_lgit_checkout,
                      execute_lgit_merge, execute_lgit_stash)
from commands import (config_lgit, display_lgit_status, execute_lgit_add,
                      execute_lgit_commit, execute_lgit_init, execute_lgit_rm,
                      list_lgit_files, show_lgit_log)
from functions import find_lgit_directory


def parse_arguments():
    """Parse command-line to commands and options of lgit program."""
    # Create the top-level parser with an useful help messages:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        title='These are common lgit commands used',
        dest='command',
        metavar='<command> [<args>]')

    # Create the parser for the "init" command
    subparsers.add_parser('init')

    # Create the parser for the "add" command
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('files', type=str, nargs='+')

    # Create the parser for the "rm" command
    rm_parser = subparsers.add_parser('rm')
    rm_parser.add_argument('files', type=str, nargs='+')

    # Create the parser for the "config" command
    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('--author', type=str, required=True)

    # Create the parser for the "commit" command
    commit_parser = subparsers.add_parser('commit')
    commit_parser.add_argument('-m', metavar='<msg>', type=str, required=True)

    # Create the parser for the "status" command
    subparsers.add_parser('status')

    # Create the parser for the "ls-files" command
    subparsers.add_parser('ls-files')

    # Create the parser for the "log" command
    subparsers.add_parser('log')

    # Create the parser for the "branch" command
    branch_parser = subparsers.add_parser('branch')
    branch_parser.add_argument('branch_name', type=str, nargs='?')

    # Create the parser for the "checkout" command
    checkout_parser = subparsers.add_parser('checkout')
    checkout_parser.add_argument(
        'branch_name', type=str, nargs='?', default='master')

    # Create the parser for the "merge" command
    subparsers.add_parser('merge')

    # Create the parser for the "stash" command
    subparsers.add_parser('stash')

    return parser.parse_args()


def main():
    """Execute the main program."""
    args = parse_arguments()
    lgit_path = find_lgit_directory()
    if args.command == 'init':
        execute_lgit_init()
    elif lgit_path:
        # The current working directory now is where has .lgit directory:
        switcher = {
            "add": execute_lgit_add,
            "rm": execute_lgit_rm,
            "config": config_lgit,
            "commit": execute_lgit_commit,
            "status": display_lgit_status,
            "ls-files": list_lgit_files,
            "log": show_lgit_log,
            "branch": execute_lgit_branch,
            "checkout": execute_lgit_checkout,
            "merge": execute_lgit_merge,
            "stash": execute_lgit_stash
        }
        # Get the function from switcher dictionary:
        switcher[args.command](args, lgit_path)
    else:
        print('fatal: not a git repository (or any of the parent directories)')


if __name__ == "__main__":
    main()
