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
    print(f'For backup purposes, we just wrote {numactors} actors in alphabetical form to actors.txt.\nThis can be imported by going to Add>Item Names and clicking "Add Actors".' )
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
        print("Version on disk: "+ver+", ",end="")
        remoteVer = requests.get("https://raw.githubusercontent.com/cooperdk/YAPO-e-plus/master/VERSION.md").text
        remoteVer = remoteVer.strip()
        print("Github version: "+str(remoteVer))
        if str(ver)!=str(remoteVer):
            print("*** A new version of YAPO e+ is available!")
        print("\r\n")


class ready():


    if not(os.environ.get('SKIP_STARTUP')):
        getStarted()