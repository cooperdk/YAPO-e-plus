#!/usr/bin/env python
import os
import sys
from videos import *
import YAPO.settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    from videos import apps
    from YAPO import pagination

    a = apps
    a = pagination

    print("Static files dir is: {}".format(YAPO.settings.STATIC_ROOT))
    print("Media files dir is: {}".format(YAPO.settings.MEDIA_ROOT))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
