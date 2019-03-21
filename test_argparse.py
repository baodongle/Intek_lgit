#!/usr/bin/env python3
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from commands import *


def create_argparser():
    # Create the top-level parser with an useful help messages:
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(
        title='These are common lgit commands used',
        dest='command',
        metavar='<command> [<args>]')

    # Create the parser for the "init" command
    init_parser = subparsers.add_parser(
        'init',
        help='Create an empty Git repository or reinitialize an existing one')
    init_parser.add_argument('directory', type=str, nargs='?')

    # Create the parser for the "add" command
    add_parser = subparsers.add_parser(
        'add', help='Add file contents to the index')
    add_parser.add_argument('file', type=str, nargs='?')

    # Create the parser for the "rm" command
    rm_parser = subparsers.add_parser(
        'rm', help='Remove files from the working tree and from the index')
    rm_parser.add_argument('file', type=str, nargs='?')

    # Create the parser for the "config" command
    config_parser = subparsers.add_parser(
        'config', help='Get and set repository or global options')
    config_parser.add_argument('--author', nargs=1, required=True)

    # Create the parser for the "commit" command
    commit_parser = subparsers.add_parser(
        'commit', help='Record changes to the repository')
    commit_parser.add_argument('-m', dest='<msg>', nargs=1, required=True)

    # Create the parser for the "status" command
    subparsers.add_parser('status', help='Show the working tree status')

    # Create the parser for the "ls-files" command
    subparsers.add_parser(
        'ls-files',
        help='Show information about files in the index and the working tree')

    # Create the parser for the "log" command
    subparsers.add_parser('log', help='Show commit logs')

    return parser


def main():
    parser = create_argparser()
    # Parse arguments:
    args = parser.parse_args()

    switcher = {
        "init": execute_lgit_init,
        "add": execute_lgit_add,
        "rm": execute_lgit_remove,
        "config": config_lgit,
        "commit": execute_lgit_commit,
        "status": display_lgit_status,
        "ls-files": list_lgit_files,
        "log": show_lgit_log
    }
    # Get the function from switcher dictionary:
    switcher[args.command](args)


if __name__ == "__main__":
    main()
