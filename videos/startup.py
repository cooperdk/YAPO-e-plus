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
        print(f"--- Version on disk: {ver}")
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
        log.info('\n')


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


def add_scene_to_folder_view (scene_to_add):
    # scene_path = os.path.normpath(scene_to_add.path_to_dir)

    path = os.path.normpath(scene_to_add.path_to_dir)

    # drive, path = os.path.splitdrive(scene_path)

    print(path)
    folders = []
    while scene_to_add < 99999999:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()

    # print (drive)
    is_first = True
    parent = ""
    # for folder in folders:
    #     print (folder)
    path_with_ids = []
    recursive_add_folders(None, folders, scene_to_add, path_with_ids)


def recursive_add_folders (parent, folders, scene_to_add, path_with_ids):
    if len(folders) != 0:
        if parent is None:
            path_with_ids = []
            if not Folder.objects.filter(name=folders[0]):
                temp = Folder.objects.create(name=folders[0])
                print(f"Created virtual folder: {temp.name}")
                parent = Folder.objects.get(name=folders[0])
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()
                path_with_ids.append(
                    { "name": parent.last_folder_name_only, "id": parent.id }
                )
                # print ("Parent Name is {}, Path with Id's are {}".format(parent.name, path_with_ids.encode('utf-8')))
                # print(json.dumps(path_with_ids))
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
                # print ("Last folder name is : {}".format(folders[0]))
                del folders[0]

            else:
                parent = Folder.objects.get(name=folders[0])
                path_with_ids.append(
                    { "name": parent.last_folder_name_only, "id": parent.id }
                )
                # print ("Parent Name is {}, Path with Id's are {}".format(parent.name, path_with_ids.encode('utf-8')))
                # print(json.dumps(path_with_ids))
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
                # print ("Last folder name is : {}".format(folders[0]))
                del folders[0]

            recursive_add_folders(parent, folders, scene_to_add, path_with_ids)
        else:
            folder_to_add = os.path.join(parent.name, folders[0])
            parent_children = parent.get_children()

            if_in_children = False
            for child in parent_children:
                if child.name == folder_to_add:
                    if_in_children = True
                    parent = child
                    break

            if not if_in_children:
                parent = Folder.objects.create(name=folder_to_add, parent=parent)
                print(f"Created virtual folder: {parent.name}")
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()

            if parent.last_folder_name_only is None:
                parent.last_folder_name_only = folders[0]
                parent.save()
            path_with_ids.append(
                { "name": parent.last_folder_name_only, "id": parent.id }
            )
            # print ("Parent Name is {}, Path with Id's are {}".format(parent.name.encode('utf-8'),
            #                                                          path_with_ids))
            # print(json.dumps(path_with_ids))
            if parent.path_with_ids is None:
                parent.path_with_ids = json.dumps(path_with_ids)
                parent.save()
            # print ("Last folder name is : {}".format(folders[0]))
            del folders[0]
            recursive_add_folders(parent, folders, scene_to_add, path_with_ids)
    else:
        if not parent.scenes.filter(name=scene_to_add.name):
            parent.scenes.add(scene_to_add)
            print(
                f"Added Scene: {scene_to_add.name} to virtual folder {parent.name}"
            )
            parent.save()


def getStarted ():
    stats()
    backupper()
    write_actors_to_file()
    mem = int(auxf.getMemory())
    cpu = auxf.getCPU()
    cpucnt = auxf.getCPUCount()
    global videoProcessing
    print(f"\nYou have {mem} GB available. CPU speed is {cpu} GHz and you have {cpucnt} cores available.")
    if mem <= 1:
        print("Since you have only about a gigabyte of memory, video processing will be disabled.")
        videoProcessing = False
    if mem >= 2:
        print("Since you have sufficient memory, video processing features will be enabled.")
        videoProcessing = True
    print("\n")
    verCheck()


class ready:

    try:
        if not 'migra' in sys.argv:
            print("Not in migration mode.")
            getStarted()
        else:
            print("In migration mode.")
    except:
        pass
