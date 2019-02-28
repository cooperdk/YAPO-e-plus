#!/usr/bin/env python
import os
import sys
from videos import *
import YAPO.settings
import os
x=0
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    from videos import apps
    from YAPO import pagination

    a = apps
    a = pagination
    os.system('cls' if os.name == 'nt' else 'clear')
    if x == 0:
        print("")
        print("____    ____  ___       ______     ______         _______        ")
        print("\   \  /   / /   \     |   _  \   /  __  \       |   ____|   _   ")
        print(" \   \/   / /  ^  \    |  |_)  | |  |  |  |      |  |__    _| |_ ")
        print("  \_    _/ /  /_\  \   |   ___/  |  |  |  |      |   __|  |_   _|")
        print("    |  |  /  _____  \  |  |      |  `--'  |      |  |____   |_|  ")
        print("    |__| /__/     \__\ | _|       \______/       |_______|       ")
        print("")
        print("    For changes to the main branch, please consult the guide.")
        print("=================================================================")
        print("")
        print("Static files dir is: {}".format(YAPO.settings.STATIC_ROOT))
        print("Media files dir is: {}".format(YAPO.settings.MEDIA_ROOT))

    from django.core.management import execute_from_command_line
    x = x + 1
    execute_from_command_line(sys.argv)
