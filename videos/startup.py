import os
from os import path
import sys
import shutil
import requests
import platform
import webbrowser
from videos.models import Scene, Actor, ActorTag, SceneTag, Folder
from django.db.models import Count
import videos.aux_functions as aux
from configuration import Config
from utils import Constants
from colorama import init
from utils.printing import Logger
init()
log = Logger()


def banner():

    SCRIPT_ROOT = get_main_dir()

    SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
    compiled = False
    try:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False

    if platform.system() == "Windows":
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
    print("\t       ____    ____  ___       ______     ______         _______        ")
    print("\t       \   \  /   / /   \     |   _  \   /  __  \       |   ____|   _   ")
    print("\t        \   \/   / /  ^  \    |  |_)  | |  |  |  |      |  |__    _| |_ ")
    print("\t         \_    _/ /  /_\  \   |   ___/  |  |  |  |      |   __|  |_   _|")
    print("\t           |  |  /  _____  \  |  |      |  `--'  |      |  |____   |_|  ")
    print("\t           |__| /__/     \__\ | _|       \______/       |_______|       ")
    print("\t")
    print("\t                     \033[37m\033[44mYET ANOTHER PORN ORGANIZER - extended\033[49m")
    print("\t\033[1m\033[37m\033[40m       =================================================================")
    print("\t\033[0;10r")
    print(f"\033[22mExecuting YAPO from: {SCRIPT_ROOT}", end="")
    if compiled:
        print(f" (frozen/compiled build)")
    else:
        print(f" (running in a Python environment)")
    print(f"Database dir is:       {Config().database_dir}")
    print(f"Config dir is:         {Config().config_path}")
    print(f"Image storage dir is:  {Config().site_media_path}\n")


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

def dupes() -> int:
    dupes = Scene.objects.values('hash').annotate(name_count=Count('hash')).exclude(name_count=1)
    if not any([len(dupes)==0, len(dupes)==1]):
        log.info(f'There are {len(dupes)} duplicate scenes in your collection. Use the duplicate checker to clean them out.')
    elif len(dupes)==1:
        log.info(f'There is one duplicate scene in your collection. Use the duplicate checker to clean them out.')

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
    print(f"Actors dumped to {actortxt}")


def configcheck ():
    settings = os.path.join(Config().config_path, Constants().default_yaml_settings_filename)
    if not path.isfile(settings):
        log.info("No config file found, so one has been generated.\n")
        Config().save()
    else:
        print(f"Configuration loaded from {settings}\n")

def vercheck(): # Check the local version against Github
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
        verprint = f"\n--- Version {ver.strip()}"
        try:
            remoteVer = requests.get(
                "https://raw.githubusercontent.com/cooperdk/YAPO-e-plus/develop/VERSION.md"
            ).text
            remoteVer = remoteVer.strip()
        except:
            remoteVer = "?REQUEST ERROR"
        if not compiled:
            # print("Github version: "+str(remoteVer))
            if LooseVersion(ver) < LooseVersion(remoteVer):
                verprint = (f'VERCHK: A newer version of YAPO e+ is available ({remoteVer})')
                #verprint += (f'\n    A newer version of YAPO e+ is available ({remoteVer})')
            if LooseVersion(ver) == LooseVersion(remoteVer):
                verprint = "VERCHK: No new version available)"
            if LooseVersion(ver) > LooseVersion(remoteVer):
                verprint = "VERCHK: Your version is a dev copy newer than the Github version"
        else:
            verprint = (f"    This is a compiled build of version {ver}. The latest Git version is {remoteVer}.")

        log.info(verprint)

def stats (): # Prints statistics about videos and metadata
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
    print(f"Scenes: {sce} ({size} on disk). Scene tags available: {sctag}")
    print(f"Actors: {act} Actor tags available: {acttag}.\n")

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
        ffprobe = os.path.exists(os.path.abspath(os.path.join(dir_to_check, 'ffprobe.exe')))
        if not all([ffmpeg, ffprobe]):
            print("\n")
            print("You don't have a copy of FFMPEG in your YAPO system.")
            print("I am going to install a copy of FFPMEG (4.3.1 static, GPL, Non-Free, YAPO build).")
            print(f"It will be placed at {dir_to_check}")
            input("Press enter to acknowledge... >")
            print("Getting https://porn-organizer.org/dl/ffmpeg-latest.zip...",end="")
            try:
                #print("Downloading... ",end="")
                dload.save_unzip("https://porn-organizer.org/dl/ffmpeg-latest.zip", dir_to_check, True)
                #print("\nFFMpeg and supplement tools copied.", end="")
                #print(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest', 'bin', 'ffmpeg.exe')))
                #shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-latest', 'ffmpeg.exe')), os.path.abspath(dir_to_check))
                #print(" - ffprobe", end="")
                #shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-latest', 'ffprobe.exe')), os.path.abspath(dir_to_check))
                #print(" - ffplay", end="")
                #shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-latest', 'ffplay.exe')), os.path.abspath(dir_to_check))
                #print("\nRemoving temp dir... ", end="")
                #shutil.rmtree(os.path.abspath(os.path.join(dir_to_check, 'https://porn-organizer.org/dl/ffmpeg-latest')))
                #print("\nDone.")
                #input("Press enter to boot YAPO. >")
            except:
                print(f"An error may have occured, please download FFMPEG manually")
                print(f"(preferably from the above link) and place it in {dir_to_check}")
                input("YAPO will exit now. Press enter to acknowledge... >")
                sys.exit()


def startup_sequence():

    banner()

    configcheck()
    vercheck()
    print("")
    stats()
    backupper()
    write_actors_to_file()
    mem = int(aux.getMemory())
    cpu = aux.getCPU()
    cpucnt = aux.getCPUCount()
    global videoProcessing
    print(f"\nYou have {aux.get_human_readable_size(mem)} available. CPU speed is {cpu} GHz and you have {cpucnt} cores available.")
    print(f"Video processing configuration is {Config().videoprocessing}.\n")
    if ((mem >> 30) >= 2 or cpu > 1.2) and Config().videoprocessing != True:
        Config().videoprocessing = True
        log.sinfo("Video processing enabled, you have the computer to handle it.")
        print("\n")
    elif ((mem >> 30) < 2 or cpu < 1.2) and Config().videoprocessing != False:
        Config().videoprocessing = False
        log.sinfo("Video processing disabled, your computer specification is too low.")
        print("\n")
    ffmpeg_check()
    dupes()
    #aux.populate_actors()


    if not "no-browser" in str(sys.argv):
        site = Config().yapo_url
        if ":" in site:
            if "http://" not in site:
                site="http://" + site + "/"
            print (f"Site to open: {site}\n")
            webbrowser.get().open_new_tab(site)

"""
class ready:
    import time

    try:
        if not any(['migrat' in str(sys.argv), 'get-clean-titles' in str(sys.argv), 'convert-tags' in str(sys.argv),
                 'mark-scenes' in str(sys.argv), 'dumpdata' in str(sys.argv), 'loaddata' in str(sys.argv)]):
            print("\nExecuting startup-sequence...")
            time.sleep(3)
            startup_sequence()
        if any(['migrat' in str(sys.argv), 'get-clean-titles' in str(sys.argv), 'convert-tags' in str(sys.argv),
                'mark-scenes' in str(sys.argv)]):
            log.info(f'YAPO is in migration/maintenance mode.\nSuppressing startup-sequence. The web GUI is disabled.')
            print("\n")
    except:
        pass
"""