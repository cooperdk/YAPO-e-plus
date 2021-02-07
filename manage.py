#!/usr/bin/env python

import os
import sys

# import settings


# os.environ("DJANGO_SETTINGS_MODULE", "YAPO.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")


def main_is_frozen ():
    return (hasattr(sys, "frozen"))  # old py2exe


def get_main_dir ():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    # import videos.apps
    # import YAPO.pagination
    # a = apps
    # a = pagination
    SCRIPT_ROOT = get_main_dir()

    try:
        if sys.frozen or sys.importers:
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False

    from django.core.management import execute_from_command_line
    from configuration import Config
    # execute_from_command_line(sys.argv)
    # print(sys.argv)
    if not any(["migrate" in str(sys.argv), "makemigrations" in str(sys.argv), "loaddata" in str(sys.argv),
                "dumpdata" in str(sys.argv), "shell" in str(sys.argv), "help" in str(sys.argv),
                "dumpscript" in str(sys.argv), "sql" in str(sys.argv),
                "showmigrations" in str(sys.argv), "runserver" in str(sys.argv),
                "clean_pyc" in str(sys.argv), "check" in str(sys.argv), "get-clean-titles" in str(sys.argv),
                "convert-tags" in str(sys.argv), "mark-scenes" in str(sys.argv)]):

        print(f"Config: {Config().yapo_url}")
        quit()
        execute_from_command_line([SCRIPT_ROOT, 'runserver', Config().yapo_url, '--noreload'])
    else:
        #if not "runserver" in str(sys.argv):
        #    print("YAPO error -- started without a host in configuration file and without a job to do.\n")
        #    print("Specify if you wish to run the server, migrate, make migrations .\n")
        #    quit()

        execute_from_command_line(sys.argv)
