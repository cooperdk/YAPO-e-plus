import os
from os import path
import videos.const
import requests
from videos.models import Scene, Actor, Website, ActorTag, SceneTag
import videos.views

def getSizeAll():
    #queryset.aggregate(Sum('size')).get('column__sum')
    #cursor = connection.cursor()
    #cursor.execute("SELECT SUM(size) AS total FROM videos_scene")[0]
    #row = cursor.fetchall()
    row=Scene.objects.raw("SELECT SUM(size) AS total, id FROM videos_scene") #cursor.fetchone()
    if row[0].total is not None:
        return sizeFormat(row[0].total)
    else:
        return "no space"
        
def sizeFormat(b):

    if b < 1000:
        return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'

def write_actors_to_file():
    actors = Actor.objects.order_by('name')
    actors_string = ""
    numactors=0
    for actor in actors:
        if not(numactors==0):
            actors_string += "," + actor.name
        else:
            actors_string += actor.name
        numactors+=1
    
    file = open("actors.txt", "w")

    file.write(actors_string)
    print('For backup purposes, we just wrote all actors in alphabetical form to actors.txt.\r\nThis can be imported by going to Add>Item Names and clicking "Add Actors".' )
    print("For successful recovery on a new setup, you must remove the actor photos\r\nin video/media/actors and re-scrape, as the actor IDs will have changed.\r\n")
    file.close()

def getStarted():
    size = getSizeAll()
    row=Actor.objects.raw("SELECT COUNT(*) AS total, id FROM videos_actor") #cursor.fetchone()
    if row[0].total is not None:
        act=str(row[0].total)
    row=Scene.objects.raw("SELECT COUNT(*) AS total, id FROM videos_scene") #cursor.fetchone()
    if row[0].total is not None:
        sce=str(row[0].total)
    row=ActorTag.objects.raw("SELECT COUNT(*) AS total, id FROM videos_actortag") #cursor.fetchone()
    if row[0].total is not None:
        acttag=str(row[0].total)
    row=SceneTag.objects.raw("SELECT COUNT(*) AS total, id FROM videos_scenetag") #cursor.fetchone()
    if row[0].total is not None:
        sctag=str(row[0].total)        
    print("\nCurrently, there are "+sce+" videos registered in YAPO e+.\nThey take up "+str(size)+" of disk space.")
    print("There are "+sctag+" tags available for video clips.")
    print("\nThere are " +act+" actors in the database.\nThese actors have "+acttag+" usable tags.\n\n")


    actors = Actor.objects.all()

        # populate_last_folder_name_in_virtual_folders()
    write_actors_to_file()

    print("\n")

    update = "././VERSION.md"
    if path.isfile(update):
        verfile  = open(update, "r") 
        ver = verfile.read()
        ver = str(ver).strip()
        print("--- Version on disk: "+ver)
        try:
            remoteVer = requests.get("https://raw.githubusercontent.com/cooperdk/YAPO-e-plus/master/VERSION.md").text
            remoteVer = remoteVer.strip()
        except:
            remoteVer = "?REQUEST ERROR"
            pass

        #print("Github version: "+str(remoteVer))
        if str(ver)!=str(remoteVer):
            print(chr(9608)+chr(9608)+chr(9608)+f' A new version of YAPO e+ is available ({remoteVer})! '+chr(9608)+chr(9608)+chr(9608))
        print("\r\n")


class ready():


    if not(os.environ.get('SKIP_STARTUP')):
        getStarted()