import os
from os import path
import sys
#import json
import shutil
import requests
import platform
from utils.printing import Logger
from videos.models import Scene, Actor, ActorTag, SceneTag, Folder
import videos.aux_functions as auxf
from configuration import Config
log = Logger()

def getSizeAll () -> str: # Retrieves the total amount of bytes of registered scenes
    row = Scene.objects.raw(
        "SELECT SUM(size) AS total, id FROM videos_scene"
    )  # cursor.fetchone()
    if row[0].total is not None:
        return sizeFormat(row[0].total)
    else:
        return "no space"


def sizeFormat (b: int) -> str: # returns a human-readable filesize depending on the file's size
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


def verCheck (): # Check the local version against Github

    try:
        if sys.frozen or sys.importers:
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False

    if not compiled:
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

            # print("Github version: "+str(remoteVer))
            if str(ver) != str(remoteVer):
                log.info(f'███ A new version of YAPO e+ is available ({remoteVer})! ███')
    else:
        print("Since this build is frozen, an update check is nor performed.")

def stats (): # Prints statistics about your videos and metadata
    size = getSizeAll()
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
            print("You don't have a copy of FFMPEG in your YAPO system.")
            print("I am going to install a copy of FFPMEG (4.3, static).")
            print(f"It will be placed at ")
            input("Press enter to acknowledge... >")
            print("Getting https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.3-win64-static.zip...")
            try:
                print("Download... ",end="")
                dload.save_unzip("https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.3-win64-static.zip", dir_to_check, True)
                print("CP ffmpeg... ", end="")
                print(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-4.3-win64-static', 'bin', 'ffmpeg.exe')))
                shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-4.3-win64-static', 'bin', 'ffmpeg.exe')), os.path.abspath(dir_to_check))
                print("CP ffplay... ", end="")
                shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-4.3-win64-static', 'bin', 'ffplay.exe')), os.path.abspath(dir_to_check))
                print("CP ffprobe... ", end="")
                shutil.move(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-4.3-win64-static', 'bin', 'ffprobe.exe')), os.path.abspath(dir_to_check))
                print("RM temp dir... ", end="")
                shutil.rmtree(os.path.abspath(os.path.join(dir_to_check, 'ffmpeg-4.3-win64-static')))
                print("Done.")
            except:
                print(f"An error occured, please download FFMPEG manually from the above link")
                print(f"and place it in {dir_to_check}")
                input("YAPO will exit now. Press enter to acknowledge... >")
                sys.exit()
def getStarted ():

    print("")
    verCheck()
    print("")
    stats()
    backupper()
    write_actors_to_file()
    mem = int(auxf.getMemory())
    cpu = auxf.getCPU()
    cpucnt = auxf.getCPUCount()
    global videoProcessing
    print(f"\nYou have {mem} GB available. CPU speed is {cpu} GHz and you have {cpucnt} cores available.")

    if mem >= 2 and cpu > 1.2:
        print("Since you have sufficient hardware, video processing features will be enabled.")
        Config().videoprocessing = True
        log.info("Video processing enabled, sufficient hardware specifications")
    else:
        print("Since you have insufficient hardware, video processing will be disabled.")
        Config().videoprocessing = False
        log.info("Video processing disabled, too low hardware specification")
    print("\n\n")

    ffmpeg_check()

class ready:

    try:
        if not 'migrat' in str(sys.argv[1:]):
            print("Not in migration mode. Executing startup sequence.")
            getStarted()
        else:
            log.info(f'User entered migration mode with the "{sys.argv[1]}" command.')
            print("\n")
    except:
        log.warn("An error occured while testing if the user is in migration mode or not.")
        pass
