import os
import videos.const
import urllib.request
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
    print("\nThere are " +act+" actors in the database.\nThese actors have "+acttag+" usable tags.")



    print("\n")
class ready():


    if not(os.environ.get('SKIP_STARTUP')):
        getStarted()