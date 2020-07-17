import os
from os import path
import sys
import json
import shutil
import requests

from utils.printing import Logger
from videos.models import Scene, Actor, ActorTag, SceneTag, Folder
import videos.const as vc
import videos.aux_functions as auxf
import YAPO.settings as settings
from configuration import Config
log = Logger()

def getSizeAll () -> str:
    # queryset.aggregate(Sum('size')).get('column__sum')
    # cursor = connection.cursor()
    # cursor.execute("SELECT SUM(size) AS total FROM videos_scene")[0]
    # row = cursor.fetchall()
    row = Scene.objects.raw(
        "SELECT SUM(size) AS total, id FROM videos_scene"
    )  # cursor.fetchone()
    if row[0].total is not None:
        return sizeFormat(row[0].total)
    else:
        return "no space"


def sizeFormat (b: int) -> str:
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


def write_actors_to_file():
    actortxt = os.path.join(Config().data_path, "actors_dump.txt")
    actors = Actor.objects.order_by("id")  # name
    actors_string = ",".join(actor.name for actor in actors)
    numactors = len(actors)

    with open(actortxt, "w") as file:
        file.write(actors_string)

    print("For backup purposes, we just wrote all actors in alphabetical form to:")
    print(actortxt)
    print("To recover actor data, please consult the guide.")


def verCheck ():
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



def stats ():
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


def backupper ():
    src = Config().database_path
    dest = os.path.join(Config().database_dir, "db.sqlite3.backup")
    shutil.copy(src, dest)
    print(f"Performed a database backup to {dest}\n")


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
