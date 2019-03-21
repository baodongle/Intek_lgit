#!/usr/bin/env python3
"""Code a lightweight version of git."""
from argparse import ArgumentParser

from commands import execute_lgit_init, execute_lgit_add
from functions import check_command_error


def create_argparser():
    """Create parser to parse commands and options."""
    # Create the top-level parser with an useful help messages:
    parser = ArgumentParser(usage='./lgit.py <command> [<args>]')
    subparsers = parser.add_subparsers(
        title='These are common lgit commands used', dest='command')

    # Create the parser for the "init" command
    subparsers.add_parser('init')

    # Create the parser for the "add" command
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('files', type=str, nargs='+')

    # Create the parser for the "rm" command
    rm_parser = subparsers.add_parser('rm')
    rm_parser.add_argument('files', type=str, nargs='?')

    # Create the parser for the "config" command
    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('--author', nargs=1, required=True)

    # Create the parser for the "commit" command
    commit_parser = subparsers.add_parser('commit')
    commit_parser.add_argument('-m', dest='<msg>', nargs=1, required=True)

    # Create the parser for the "status" command
    subparsers.add_parser('status')

    # Create the parser for the "ls-files" command
    subparsers.add_parser('ls-files')

    # Create the parser for the "log" command
    subparsers.add_parser('log')

    return parser


def main():
    """Execute the main program."""
    parser = create_argparser()
    # Parse arguments:
    args = parser.parse_args()
    if args.command == 'init':
        execute_lgit_init()
    else:
        check_command_error(args.command)
        switcher = {
            "add": execute_lgit_add,
            # "rm": execute_lgit_remove,
            # "config": config_lgit,
            # "commit": execute_lgit_commit,
            # "status": display_lgit_status,
            # "ls-files": list_lgit_files,
            # "log": show_lgit_log
        }
        # Get the function from switcher dictionary:
        switcher[args.command](args)


if __name__ == "__main__":
    main()
