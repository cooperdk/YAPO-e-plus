#!/usr/bin/env python

import sys, os

#os.environ("DJANGO_SETTINGS_MODULE", "YAPO.settings")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

import platform
import sys
import YAPO.settings
#import settings
from configuration import Config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    #import videos.apps
    #import YAPO.pagination
    #a = apps
    #a = pagination

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
