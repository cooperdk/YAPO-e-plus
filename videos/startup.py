import os
from os import path
import sys
#import json
import shutil
import requests
import platform
import webbrowser

from videos.models import Scene, Actor, ActorTag, SceneTag, Folder
import videos.aux_functions as aux
from configuration import Config
from utils import Constants
from colorama import init
from utils.printing import Logger

init()
log = Logger()

def banner():

    SCRIPT_ROOT = get_main_dir()

    try:
        if sys.frozen or sys.importers:
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False

    if platform.system() == "Windows":
        import win32console
        #os.system('mode con: cols=140 lines=4096')
        os.system('cls')
        cmd = 'color 07'
        os.system(cmd)
        #cmd = 'mode con: cols=140 lines=4096'
        #os.system(cmd)
        cmd = 'mode 140,52'
        os.system(cmd)

        from ctypes import windll, byref
        import ctypes.wintypes as wintypes

        STDOUT = -11

        hdl = windll.kernel32.GetStdHandle(STDOUT)
        rect = wintypes.SMALL_RECT(0, 0, 140, 52)  # (left, top, right, bottom)
        windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))
        bufsize = wintypes._COORD(140, 4096)  # rows, columns
        windll.kernel32.SetConsoleScreenBufferSize(hdl, bufsize)

        cmd = os.path.join(SCRIPT_ROOT, 'consetbuffer') + '/X 140 /Y 2048'
        cmd = 'color 07'
        os.system(cmd)
    else:
        os.system('clear')
    print("\033[40m\033[1m\033[32m")
    print("\t____    ____  ___       ______     ______         _______        ")
    print("\t\   \  /   / /   \     |   _  \   /  __  \       |   ____|   _   ")
    print("\t \   \/   / /  ^  \    |  |_)  | |  |  |  |      |  |__    _| |_ ")
    print("\t  \_    _/ /  /_\  \   |   ___/  |  |  |  |      |   __|  |_   _|")
    print("\t    |  |  /  _____  \  |  |      |  `--'  |      |  |____   |_|  ")
    print("\t    |__| /__/     \__\ | _|       \______/       |_______|       ")
    print("\t")
    print("\t              \033[37m\033[44mYET ANOTHER PORN ORGANIZER - extended\033[49m")
    print("\t\033[1m\033[37m\033[40m=================================================================")
    print("\t\033[0;10r")
    print(f"\033[22mExecuting YAPO from: {SCRIPT_ROOT}", end="")
    if compiled:
        print(f" (frozen/compiled build)")
    else:
        print(f" (running in a Python environment)")
    print(f"Database dir is:     {Config().database_dir}")
    print(f"Config dir is:       {Config().config_path}")
    print(f"Media files dir is:  {Config().site_media_path}")
    print("Consider making regular backup of the db, config and media directories.\n")


def main_is_frozen():
    return hasattr(sys, "frozen") # old py2exe

def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.realpath(__file__))



def getsizeall () -> str: # Retrieves the total amount of bytes of registered scenes
    row = Scene.objects.raw(
        "SELECT SUM(size) AS total, id FROM videos_scene"
    )  # cursor.fetchone()
    if row[0].total is not None:
        return sizeformat(row[0].total)
    else:
        return "no space"


def sizeformat (b: int) -> str: # returns a human-readable filesize depending on the file's size
    if b < 1000:
        return f"{b}B"
    elif b < 1000000:
        return f"{b/1000:.1f}KB"
    elif b < 1000000000:
        return f"{b/1000000:.1f}MB"
    elif b < 1000000000000:
        return f"{b/1000000000:.1f}GB"
    else:
        return f"{b/1000000000000:.1f}TB"



def write_actors_to_file(): # Method to dump all actors alphabetically in a ready-to-insert manner.
    actortxt = os.path.join(Config().data_path, "actors_dump.txt")
    actors = Actor.objects.order_by("id")  # name
    actors_string = ",".join(actor.name for actor in actors)
    numactors = len(actors)

    with open(actortxt, "w") as file:
        file.write(actors_string)

    print("For backup purposes, we just wrote all actors in alphabetical form to:")
    print(actortxt)
    print("To recover actor data, please consult the guide.")


def configcheck ():
    settings = os.path.join(Config().config_path, Constants().default_yaml_settings_filename)
    if not path.isfile(settings):
        log.info("There is no config file, so one has been generated.")
        Config().save()


def vercheck (): # Check the local version against Github
    from distutils.version import LooseVersion
    try:
        if sys.frozen or sys.importers:
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False


    #dirname of dirname of file results in parent directory
    update = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION.md"))

    if path.isfile(update):
        with open(update, "r") as verfile:
            ver = verfile.read()
        ver = str(ver).strip()
        print(f"--- Version {ver}")
        try:
            remoteVer = requests.get(
                "https://raw.githubusercontent.com/cooperdk/YAPO-e-plus/develop/VERSION.md"
            ).text
            remoteVer = remoteVer.strip()
        except:
            remoteVer = "?REQUEST ERROR"
            pass

        if not compiled:
            # print("Github version: "+str(remoteVer))
            if LooseVersion(ver) < LooseVersion(remoteVer):
                log.info(f'A newer version of YAPO e+ is available ({remoteVer})!')
            if ver == remoteVer:
                print("No new version available.")

        else:

            log.info("This is a frozen build of version {ver}. The latest GIT version is {remoteVer}.")



def stats (): # Prints statistics about your videos and metadata
    size = getsizeall()
    row = Actor.objects.raw(
        "SELECT COUNT(*) AS total, id FROM videos_actor"
    )  # cursor.fetchone()
    if row[0].total is not None:
        act = str(row[0].total)
    row = Scene.objects.raw(
        "SELECT COUNT(*) AS total, id FROM videos_scene"
    )  # cursor.fetchone()
    if row[0].total is not None:
        sce = str(row[0].total)
    row = ActorTag.objects.raw(
        "SELECT COUNT(*) AS total, id FROM videos_actortag"
    )  # cursor.fetchone()
    if row[0].total is not None:
        acttag = str(row[0].total)
    row = SceneTag.objects.raw(
        "SELECT COUNT(*) AS total, id FROM videos_scenetag"
    )  # cursor.fetchone()
    if row[0].total is not None:
        sctag = str(row[0].total)
    # TODO assign that all values got read correctly and have a valid value!

    print(f"\nCurrently, there are {sce} videos registered in YAPO e+.\nThey take up {size} of disk space.")
    print(f"There are {sctag} tags available for video clips.")
    print(f"\nThere are {act} actors in the database.\nThese actors have {acttag} usable tags.\n\n")


def backupper (): # Generates a backup of the database
    src = Config().database_path
    dest = os.path.join(Config().database_dir, "db.sqlite3.backup")
    shutil.copy(src, dest)
    print(f"Performed a database backup to {dest}\n")

def ffmpeg_check():
    import dload
    if platform.system() == "Windows":
        dir_to_check = os.path.join(Config().site_path, 'ffmpeg')
        ffmpeg = os.path.exists(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg.exe')))
        ffplay = os.path.exists(os.path.abspath(os.path.join(dir_to_check, 'ffplay.exe')))
        ffprobe = os.path.exists(os.path.abspath(os.path.join(dir_to_check, 'ffprobe.exe')))
        if not all([ffmpeg, ffplay, ffprobe]):
            print("\n")
            print("You don't have a copy of FFMPEG in your YAPO system.")
            print("I am going to install a copy of FFPMEG (4.3.1 static, YAPO build).")
            print(f"It will be placed at {dir_to_check}")
            input("Press enter to acknowledge... >")
            print("Getting https://porn-organizer.org/dl/ffmpeg-latest.zip...")
            try:
                print("Downloading... ",end="")
                dload.save_unzip("https://porn-organizer.org/dl/ffmpeg-latest.zip", dir_to_check, True)
                print("\nCopying ffmpeg", end="")
                print(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest', 'bin', 'ffmpeg.exe')))
                shutil.move(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest', 'bin', 'ffmpeg.exe')), os.path.abspath(dir_to_check))
                print(" - ffplay", end="")
                shutil.move(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest', 'bin', 'ffplay.exe')), os.path.abspath(dir_to_check))
                print(" - ffprobe", end="")
                shutil.move(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest', 'bin', 'ffprobe.exe')), os.path.abspath(dir_to_check))
                print("\nRemoving temp dir... ", end="")
                shutil.rmtree(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest')))
                print("\nDone.")
            except:
                print(f"An error occured, please download FFMPEG manually from the above link")
                print(f"and place it in {dir_to_check}")
                input("YAPO will exit now. Press enter to acknowledge... >")
                sys.exit()


def startup_sequence():

    banner()
    print("")
    configcheck()
    print("")
    vercheck()
    print("")
    stats()
    backupper()
    write_actors_to_file()
    mem = int(aux.getMemory())
    cpu = aux.getCPU()
    cpucnt = aux.getCPUCount()
    global videoProcessing
    print(f"\nYou have {mem} GB available. CPU speed is {cpu} GHz and you have {cpucnt} cores available.")

    if mem >= 2 and cpu > 1.2:
        print("\nSince you have sufficient hardware, video processing features will be enabled.")
        Config().videoprocessing = True
        log.info("Video processing enabled, sufficient hardware specifications")
        print("\n")
    else:
        print("\nSince you have insufficient hardware, video processing will be disabled.")
        Config().videoprocessing = False
        log.info("Video processing disabled, too low hardware specification")
        print("\n")

    ffmpeg_check()

    #aux.populate_actors()

    if "runserver" in sys.argv[1]:
        site = Config().yapo_url
        if ":" in site:
            if not "http://" in site:
                site="http://" + site + "/"
            print (f"Site to open: {site}\n")
            webbrowser.get().open_new_tab(site)
        else:
            print('You\'re missing a defined port number in the /config/settings.yml variable "yapo_url".\n\
If you want YAPO to open your browser automatically, this needs to be set in settings.\n')



class ready:
    import time
    #startup_sequence()

    try:
        if not 'migrat' in str(sys.argv):
            print("Not in migration mode. Executing startup sequence...")
            time.sleep(2)
            startup_sequence()
        else:
            log.info(f'User entered migration mode.')
            print("\n")
    except:
        pass
