#!/usr/bin/env python
# manage.py:
# it provides the command-line utility for administrative tasks such as running the server, applying migrations, creating apps, etc.
"""Django's command-line utility for administrative tasks."""
# Import the os module to interact with the operating system
import os
# Import the sys module to interact with the Python interpreter
import sys


def main():
    """Run administrative tasks."""
    # Set the default settings module for the Django project
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pj5001_dj.settings")
    # Import the execute_from_command_line function to handle command-line arguments
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        #  Raise an error if Django cannot be imported, with a helpful error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command-line utility with the provided arguments
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
