import os
from os import path
import sys
import videos.const
import requests
from videos.models import Scene, Actor, Website, ActorTag, SceneTag
import videos.aux_functions as aux
import videos.views



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
    actors = Actor.objects.order_by("id")  # name
    actors_string = ""
    numactors = 0
    for actor in actors:

        if not (numactors == 0):
            actors_string += "," + actor.name
        else:
            actors_string += actor.name
        numactors += 1

    file = open("actors.txt", "w")

    file.write(actors_string)
    print(
        'For backup purposes, we just wrote all actors in alphabetical form to actors.txt.\r\nThis can be imported by going to Add>Item Names and clicking "Add Actors".'
    )
    print(
        "For successful recovery on a new setup, you must remove the actor photos\r\nin video/media/actors and re-scrape, as the actor IDs will have changed.\r\n"
    )
    file.close()

'''
    actors = Actor.objects.order_by("id")
    for actor in actors:
        actor.tattoos = actor.tattoos.capitalize()

        tattoos = str(actor.tattoos).strip()
        tattoos1 = tattoos.replace(";", ",")
        tattoos1 = tattoos1.replace(" and ", ",")
        tattoos1 = tattoos1.replace("-", ",")
        tattoos1 = tattoos1.replace(":", ",")

        tattoos = tattoos1.split(",")

        numTattoos = len(tattoos)
        print(f"Actor: {actor.name} - {str(numTattoos)} tattoos",end="")

        if (numTattoos == 0 or numTattoos is None) or (
            tattoos1.lower().strip() == "none"
            or tattoos1.lower().strip() == "no tattoos"
            or tattoos[0].lower().strip() == "none"
            or tattoos[0].lower().strip() == "no tattoos"
            or tattoos[0].lower().strip() == "n/a"
        ):
            aux.insert_actor_tag(actor, "No tattoos")

        if numTattoos == 1 and (
            tattoos[0].lower().strip() == "none"
            or tattoos1.lower().strip() == "none"
            or tattoos1.lower().strip() == "no tattoos"
            or tattoos[0].lower().strip() == "no tattoos"
            or tattoos[0].lower().strip() == "n/a"
            or tattoos1.lower().strip() == "n/a"
       ):
            aux.insert_actor_tag(actor, "No tattoos")

        if numTattoos == 1 and (
            tattoos1.lower().strip() == "various" or tattoos[0].lower().strip() == "various"
        ):
            aux.insert_actor_tag(actor, "Some tattoos")

        elif numTattoos == 1 and (
            tattoos1.lower().strip() != "various"
            and tattoos[0].lower().strip() != "various"
            and tattoos[0].lower().strip() != "none"
            and tattoos[0].lower().strip() != "none"
            and tattoos[0].lower().strip() != "unknown"
            and tattoos[0].lower().strip() != "no tattoos"
            and tattoos[0].lower().strip() != "n/a"
        ):
            aux.insert_actor_tag(actor, "One tattoo")

        if numTattoos >= 2 and numTattoos <= 4:
            aux.insert_actor_tag(actor, "Few tattoos")

        if numTattoos > 4 and numTattoos <= 6:
            aux.insert_actor_tag(actor, "Some tattoos")

        if numTattoos > 6 and numTattoos <= 8:
            aux.insert_actor_tag(actor, "Lots of tattoos")

        if numTattoos > 8:
            aux.insert_actor_tag(actor, "Massive amount of tattoos")

        if (actor.tattoos and tattoos1) and actor.tattoos.lower() != tattoos1.lower():
            actor.tattoos = tattoos1
'''

def getStarted():
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
    print(
        "\nCurrently, there are "
        + sce
        + " videos registered in YAPO e+.\nThey take up "
        + str(size)
        + " of disk space."
    )
    print("There are " + sctag + " tags available for video clips.")
    print(
        "\nThere are "
        + act
        + " actors in the database.\nThese actors have "
        + acttag
        + " usable tags.\n\n"
    )

    actors = Actor.objects.all()

    # populate_last_folder_name_in_virtual_folders()
    write_actors_to_file()

    print("\n")

    update = "././VERSION.md"
    if path.isfile(update):
        verfile = open(update, "r")
        ver = verfile.read()
        ver = str(ver).strip()
        print("--- Version on disk: " + ver)
        try:
            remoteVer = requests.get(
                "https://raw.githubusercontent.com/cooperdk/YAPO-e-plus/master/VERSION.md"
            ).text
            remoteVer = remoteVer.strip()
        except:
            remoteVer = "?REQUEST ERROR"
            pass

        # print("Github version: "+str(remoteVer))
        if str(ver) != str(remoteVer):
            print(
                chr(9608)
                + chr(9608)
                + chr(9608)
                + f" A new version of YAPO e+ is available ({remoteVer})! "
                + chr(9608)
                + chr(9608)
                + chr(9608)
            )
        print("\r\n")

class ready:

    try:
        if not 'migrat' in sys.argv:
            getStarted()
    except:
        pass
