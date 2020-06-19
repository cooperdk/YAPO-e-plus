#!/usr/bin/env python
import os
import sys
from videos import *
import YAPO.settings
import os, platform
x=0
os.system('mode con: cols=140 lines=4096')
os.system('cls' if os.name == 'nt' else 'clear')
if platform.system() == "Windows":

    from ctypes import windll, byref
    import ctypes.wintypes as wintypes

    STDOUT = -11

    hdl = windll.kernel32.GetStdHandle(STDOUT)
    rect = wintypes.SMALL_RECT(0, 0, 132, 55) # (left, top, right, bottom)
    windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))
    bufsize = wintypes._COORD(140, 4096) # rows, columns
    windll.kernel32.SetConsoleScreenBufferSize(hdl, bufsize)
    
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    from videos import apps
    from YAPO import pagination

    a = apps
    a = pagination
    if x == 0:
        print("")
        print("____    ____  ___       ______     ______         _______        ")
        print("\   \  /   / /   \     |   _  \   /  __  \       |   ____|   _   ")
        print(" \   \/   / /  ^  \    |  |_)  | |  |  |  |      |  |__    _| |_ ")
        print("  \_    _/ /  /_\  \   |   ___/  |  |  |  |      |   __|  |_   _|")
        print("    |  |  /  _____  \  |  |      |  `--'  |      |  |____   |_|  ")
        print("    |__| /__/     \__\ | _|       \______/       |_______|       ")
        print("")
        print("    For changes to the main branch, please consult README.md.")
        print("=================================================================")
        print("")
        #print("Static files dir is: {}".format(YAPO.settings.STATIC_ROOT))
        print(f"Media files are located in {YAPO.settings.MEDIA_ROOT},\nyou may want to consider backing them up.\n")

    from django.core.management import execute_from_command_line
    x = x + 1
    execute_from_command_line(sys.argv)
