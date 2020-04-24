import os
import videos.const
import urllib.request
from videos.models import Scene
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
    print("\nThe videos registered totally take up "+str(size)+".\n\n")


class ready():


    if not(os.environ.get('SKIP_STARTUP')):
        getStarted()