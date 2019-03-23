#!/usr/bin/env python3
"""Code a lightweight version of git."""
from argparse import ArgumentParser

from commands import (execute_lgit_init, execute_lgit_add, execute_lgit_rm,
                      config_lgit, execute_lgit_commit, display_lgit_status,
                      list_lgit_files, show_lgit_log)
from functions import find_lgit_directory


def parse_arguments():
    """Parse command-line to commands and options of lgit program."""
    # Create the top-level parser with an useful help messages:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        title='These are common lgit commands used',
        dest='command', metavar='<command> [<args>]')

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
            "log": show_lgit_log
        }
        # Get the function from switcher dictionary:
        switcher[args.command](args, lgit_path)
    else:
        print('fatal: not a git repository (or any of the parent directories)')


if __name__ == "__main__":
    main()
