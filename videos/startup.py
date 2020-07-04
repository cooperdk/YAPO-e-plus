import os
from os import path
import sys
import json
import shutil
import requests
from videos.models import Scene, Actor, ActorTag, SceneTag, Folder
import videos.aux_functions as aux
import YAPO.settings


def maybeMoveConfigJson():
    import YAPO.settings as settings
    src = os.path.abspath(os.path.join(YAPO.settings.BASE_DIR, 'settings.json'))
    dest = YAPO.settings.CONFIG_JSON
    if path.isfile(src):
        shutil.move(src, dest)
        print("\n███ Your configuration file was moved to  ({0})! ███".format(dest))


def getSizeAll():
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


def sizeFormat(b):

    if b < 1000:
        return "%i" % b + "B"
    elif 1000 <= b < 1000000:
        return "%.1f" % float(b / 1000) + "KB"
    elif 1000000 <= b < 1000000000:
        return "%.1f" % float(b / 1000000) + "MB"
    elif 1000000000 <= b < 1000000000000:
        return "%.1f" % float(b / 1000000000) + "GB"
    elif 1000000000000 <= b:
        return "%.1f" % float(b / 1000000000000) + "TB"


def write_actors_to_file():

    #actors = Actor.objects.all()
    actors = Actor.objects.order_by("id")  # name
    actors_string = ""
    numactors = 0
    for actor in actors:

        if not (numactors == 0):
            actors_string += "," + actor.name
        else:
            actors_string += actor.name
        numactors += 1

    with open("actors.txt", "w") as file:
        file.write(actors_string)

    print("For backup purposes, we just wrote all actors in alphabetical form to actors.txt.")
    print("To recover actor data, please consult the guide.")

def verCheck():
    update = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "VERSION.md"))

    if path.isfile(update):
        with open(update, "r") as verfile:
            ver = verfile.read()
        ver = str(ver).strip()
        print("--- Version on disk: " + ver)
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
            print(f"███ A new version of YAPO e+ is available ({remoteVer})! ███")
        print("\r\n")


def stats():
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

    print("\nCurrently, there are {0} videos registered in YAPO e+.\nThey take up {1} of disk space.".format(sce, str(size)))
    print("There are {0} tags available for video clips.".format(sctag))
    print("\nThere are {0} actors in the database.\nThese actors have {1} usable tags.\n\n".format(act, acttag))

def backupper():
    import YAPO.settings as settings
    src = settings.DATABASES['default']['NAME']
    dest = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db_BACKUP.sqlite3"))
    shutil.copy(src, dest)
    print("Performed a database backup to " + dest + "\n")


def add_scene_to_folder_view(scene_to_add):
    # scene_path = os.path.normpath(scene_to_add.path_to_dir)

    path = os.path.normpath(scene_to_add.path_to_dir)

    # drive, path = os.path.splitdrive(scene_path)

    print(path)
    folders = []
    while scene_to_add<99999999:
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


def recursive_add_folders(parent, folders, scene_to_add, path_with_ids):
    if len(folders) != 0:
        if parent is None:
            path_with_ids = []
            if not Folder.objects.filter(name=folders[0]):
                temp = Folder.objects.create(name=folders[0])
                print("Created virtual folder: " + temp.name)
                parent = Folder.objects.get(name=folders[0])
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()
                path_with_ids.append(
                    {"name": parent.last_folder_name_only, "id": parent.id}
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
                    {"name": parent.last_folder_name_only, "id": parent.id}
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
                print("Created virtual folder: " + parent.name)
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()

            if parent.last_folder_name_only is None:
                parent.last_folder_name_only = folders[0]
                parent.save()
            path_with_ids.append(
                {"name": parent.last_folder_name_only, "id": parent.id}
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
                "Added Scene: "
                + scene_to_add.name
                + " to virtual folder "
                + parent.name
            )
            parent.save()


def getStarted():

    #scenes = Scene.objects.all()
    #for scene in scenes:
    #    add_scene_to_folder_view(scene)
    maybeMoveConfigJson()
    stats()
    backupper()
    write_actors_to_file()
    mem = int(aux.getMemory())
    cpu = aux.getCPU()
    cpucnt = aux.getCPUCount()
    global videoProcessing
    print("\nYou have " + str(mem) + " GB available. CPU speed is " +
          str(cpu) + " GHz and you have " + str(cpucnt) + " cores available.")
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
        if not 'migrat' in sys.argv:
            print("Not in migration mode.")
            getStarted()
        else:
            print("In migration mode.")
    except:
        pass
