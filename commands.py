"""Present commands in lgit program."""
from os import environ, makedirs

from functions import create_file, check_lgit_exist


def execute_lgit_init():
    """Initialize version control in the current directory."""

    def create_lgit_folders():
        """Create directories in .lgit structure."""
        lgit_folders = ['.lgit', '.lgit/objects',
                        '.lgit/commits', '.lgit/snapshots']
        for folder in lgit_folders:
            try:
                makedirs(folder, 0o755)
            except FileExistsError:
                pass

    def create_lgit_files():
        """Create files in .lgit structure."""
        lgit_files = ['.lgit/index', '.lgit/config']
        for file in lgit_files:
            create_file(file)

    def init_config():
        """Initialize the name of the author in the file config."""
        with open('.lgit/config', 'w') as config:
            config.write(environ['LOGNAME'])

    if not check_lgit_exist():
        create_lgit_folders()
        create_lgit_files()
        init_config()


def execute_lgit_add():
    """Add file contents to the index."""
