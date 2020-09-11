#!/usr/bin/env python

import os
import sys

from configuration import Config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

def main_is_frozen():
   return (hasattr(sys, "frozen")) # old py2exe

def get_main_dir():
   if main_is_frozen():
       return os.path.dirname(sys.executable)
   return os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    #import videos.apps
    #import YAPO.pagination
    #a = apps
    #a = pagination
    SCRIPT_ROOT = get_main_dir()

    try:
        # noinspection PyUnresolvedReferences
        if sys.frozen or sys.importers:
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False

    from django.core.management import execute_from_command_line
    #execute_from_command_line(sys.argv)
    #print(sys.argv)
    if not any(["migrate" in sys.argv, "makemigrations" in sys.argv, "loaddata" in sys.argv,
                "dumpdata" in sys.argv, "shell" in sys.argv, "dumpscript" in sys.argv, "sql" in sys.argv,
                "showmigrations" in sys.argv, "runserver" in sys.argv, "clean_pyc" in sys.argv, "test" in sys.argv]):

        execute_from_command_line([SCRIPT_ROOT, 'runserver', Config().yapo_url, '--noreload'])
    else:
        execute_from_command_line(sys.argv)
