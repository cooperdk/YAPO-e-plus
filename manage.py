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

def main_is_frozen():
   return (hasattr(sys, "frozen")) # old py2exe

def get_main_dir():
   if main_is_frozen():
       return os.path.dirname(sys.executable)
   return os.path.dirname(os.path.realpath(__file__))


SCRIPT_ROOT = get_main_dir()

try:
   if sys.frozen or sys.importers:
      SCRIPT_ROOT = os.path.dirname(sys.executable)
      compiled = True
except AttributeError:
   SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
   compiled = False

x = 0
#if os.name == 'nt':
#    os.system('mode con: cols=140 lines=4096')
#    os.system('cls')
#else:
#    os.system('clear')

if platform.system() == "Windows":
    from ctypes import windll, byref
    import ctypes.wintypes as wintypes

    STDOUT = -11

    hdl = windll.kernel32.GetStdHandle(STDOUT)
    rect = wintypes.SMALL_RECT(0, 0, 132, 55)  # (left, top, right, bottom)
    windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))
    bufsize = wintypes._COORD(140, 4096)  # rows, columns
    windll.kernel32.SetConsoleScreenBufferSize(hdl, bufsize)

    bannerdisp = False

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    #import videos.apps
    #import YAPO.pagination



    #a = apps
    #a = pagination
    if x==0:
        print("")
        print("____    ____  ___       ______     ______         _______        ")
        print("\   \  /   / /   \     |   _  \   /  __  \       |   ____|   _   ")
        print(" \   \/   / /  ^  \    |  |_)  | |  |  |  |      |  |__    _| |_ ")
        print("  \_    _/ /  /_\  \   |   ___/  |  |  |  |      |   __|  |_   _|")
        print("    |  |  /  _____  \  |  |      |  `--'  |      |  |____   |_|  ")
        print("    |__| /__/     \__\ | _|       \______/       |_______|       ")
        print("")
        print("              YET ANOTHER PORN ORGANIZER - extended")
        print("=================================================================")
        print(f"Executing YAPO from: {SCRIPT_ROOT}",end="")
        if compiled:
            print(f" (frozen build)",end="")
        else:
            print(f" (Running with Python)",end="")
        if x==1:
            print(f" - listener")
        print(f"Database dir is:     {Config().database_dir}")
        print(f"Config dir is:       {Config().config_path}")
        print(f"Media files dir is:  {Config().site_media_path}")
        print("Consider making regular backup of the db, config and media directories.\n")
        #bannerdisp = True
    from django.core.management import execute_from_command_line

    x =+ 1
    execute_from_command_line(sys.argv)
