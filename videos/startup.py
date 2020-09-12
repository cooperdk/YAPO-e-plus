import os
from os import path
import sys
import shutil
import requests
import platform
import webbrowser

from videos.models import Scene, Actor, ActorTag, SceneTag
import videos.aux_functions as aux
from configuration import Config
from colorama import init

import logging

log = logging.getLogger(__name__)

init()

def isCompiled():
    try:
        # noinspection PyUnresolvedReferences
        if sys.frozen or sys.importers:
            return True
    except AttributeError:
        return False

def banner():
    if hasattr(sys, "frozen") or isCompiled():
        SCRIPT_ROOT = os.path.dirname(sys.executable)
    else:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

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

    log.info(f"Executing YAPO from: {SCRIPT_ROOT}")
    if isCompiled():
        log.info(f"This is a frozen/compiled build.")
    else:
        log.info(f"Running in a Python environment.")
    log.info(f"Database dir is:     {Config().database_dir}")
    log.info(f"Config dir is:       {Config().config_path}")
    log.info(f"Media files dir is:  {Config().site_media_path}")

# Retrieves the total amount of bytes of registered scenes
def getsizeall () -> str:
    row = Scene.objects.raw("SELECT SUM(size) AS total, id FROM videos_scene")
    if row[0].total is not None:
        return sizeformat(row[0].total)
    else:
        return sizeformat(0)

# returns a human-readable filesize depending on the file's size
def sizeformat (b: int) -> str:
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

# Dump all actors alphabetically in a ready-to-insert manner.
def write_actors_to_file():
    actortxt = os.path.join(Config().data_path, "actors_dump.txt")
    actors = Actor.objects.order_by("id")
    actors_string = ",".join(actor.name for actor in actors)

    with open(actortxt, "w") as file:
        file.write(actors_string)

    log.info(f"For backup purposes, we just wrote all actors in alphabetical form to {actortxt}. " +
            + "To recover actor data, please consult the guide.")


def configcheck ():
    settings = Config().configfile_path
    if not path.isfile(settings):
        log.warning("There is no config file, so one has been generated.")
        Config().save()

# Check the local version against Github
def vercheck():
    if isCompiled():
        log.warning("Since this build is frozen, an update check is nor performed.")

    #dirname of dirname of file results in parent directory
    update = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION.md"))

    if not path.isfile(update):
        log.warning(f"Unable to check update status, file {update} does not exist")
        return

    # Parse the version string out of the VERSION.md file
    with open(update, "r") as verfile:
        currentVersion = verfile.read()
    currentVersion = str(currentVersion).strip()
    log.info(f"This is version {currentVersion} of YAPO.")
    try:
        remoteVer = requests.get("https://raw.githubusercontent.com/cooperdk/YAPO-e-plus/develop/VERSION.md").text
        remoteVer = remoteVer.strip()
    except requests.exceptions.BaseHTTPError as f:
        log.warning(f"Unable to check for updates: {f}")
        return

    if currentVersion != remoteVer:
        log.warning(f'A new version of YAPO e+ is available. You are running {currentVersion} but {remoteVer} is available.')

# Prints statistics about your videos and metadata
def stats():
    size = getsizeall()
    row = Actor.objects.raw("SELECT COUNT(*) AS total, id FROM videos_actor")
    if row[0].total is not None:
        act = str(row[0].total)
    row = Scene.objects.raw("SELECT COUNT(*) AS total, id FROM videos_scene")
    if row[0].total is not None:
        sce = str(row[0].total)
    row = ActorTag.objects.raw("SELECT COUNT(*) AS total, id FROM videos_actortag")
    if row[0].total is not None:
        acttag = str(row[0].total)
    row = SceneTag.objects.raw("SELECT COUNT(*) AS total, id FROM videos_scenetag")
    if row[0].total is not None:
        sctag = str(row[0].total)
    # TODO assign that all values got read correctly and have a valid value!

    log.info(f"Currently, there are {sce} videos registered in YAPO e+, taking up {size} of disk space.")
    log.info(f"There are {sctag} tags available for video clips.")
    log.info(f"There are {act} actors in the database. These actors have {acttag} usable tags.")


# Generates a backup of the database
def backupper():
    src = Config().database_path
    dest = os.path.join(Config().database_dir, "db.sqlite3.backup")
    shutil.copy(src, dest)
    log.info(f"Performed a database backup to {dest}")

def ffmpeg_check():
    import dload
    if platform.system() != "Windows":
        # TODO: this check should be done on Linux, too.
        log.warning("This is not Windows. Assuming that ffmpeg is installed correctly.")
    dir_to_check = os.path.join(Config().site_path, 'ffmpeg')

    allFound = True
    for executable in ('ffmpeg.exe', 'ffplay.exe', 'ffprobe.exe'):
        if not os.path.exists(os.path.abspath(os.path.join(dir_to_check, executable))):
            allFound = False

    if not allFound:
        print("You don't have a copy of FFMPEG in your YAPO system.")
        print("I am going to install a copy of FFPMEG (4.3, static).")
        print(f"It will be placed at {dir_to_check}")
        input("Press enter to acknowledge... >")
        print("Getting https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200628-4cfcfb3-win64-static.zip...")
        try:
            print("Download... ",end="")
            dload.save_unzip("https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200628-4cfcfb3-win64-static.zip", dir_to_check, True)
            print("CP ffmpeg... ", end="")
            print(os.path.abspath(os.path.join(dir_to_check, 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200628-4cfcfb3-win64-static', 'bin', 'ffmpeg.exe')))
            shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-20200628-4cfcfb3-win64-static', 'bin', 'ffmpeg.exe')), os.path.abspath(dir_to_check))
            print("CP ffplay... ", end="")
            shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-20200628-4cfcfb3-win64-static', 'bin', 'ffplay.exe')), os.path.abspath(dir_to_check))
            print("CP ffprobe... ", end="")
            shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-20200628-4cfcfb3-win64-static', 'bin', 'ffprobe.exe')), os.path.abspath(dir_to_check))
            print("RM temp dir... ", end="")
            shutil.rmtree(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-20200628-4cfcfb3-win64-static')))
            print("Done.")
        except:
            print(f"An error occured, please download FFMPEG manually from the above link")
            print(f"and place it in {dir_to_check}")
            input("YAPO will exit now. Press enter to acknowledge... >")
            sys.exit()


def startup_sequence():

    banner()
    configcheck()
    vercheck()
    stats()
    backupper()
    write_actors_to_file()

    mem = int(aux.getMemory())
    cpu = aux.getCPU()
    cpucnt = aux.getCPUCount()
    log.info(f"You have {mem} GB available. CPU speed is {cpu} GHz and you have {cpucnt} cores available.")

    if mem >= 2 and cpu > 1.2:
        log.info("Video processing enabled, sufficient hardware specifications")
        Config().videoprocessing = True
    else:
        log.warning("Since you have insufficient hardware, video processing will be disabled.")
        Config().videoprocessing = False

    ffmpeg_check()

    if "runserver" in sys.argv[1]:
        site = Config().yapo_url
        if ":" in site:
            if not "http://" in site:
                site = "http://" + site + "/"
            webbrowser.get().open_new_tab(site)
        else:
            log.warning("You're missing a defined port number in the /config/settings.yml variable 'yapo_url'. If you want YAPO to open your browser automatically, this needs to be set in settings.")

class ready:
    import time

    if not 'migrat' in str(sys.argv):
        time.sleep(2)
        startup_sequence()
    else:
        log.info(f'User entered migration mode.')
