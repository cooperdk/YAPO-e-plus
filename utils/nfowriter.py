'''
This is the scene NFO writer.
It will take a scene ID as argument and write a .nfo file bases on the metadata for the scene.
Later, it will be possible to package a scene together with it's thumb, video contact sheet and .nfo file
and a number of shots from the video (as "fanart").
'''

import os
import shutil
import datetime
import django
from configuration import Config
from utils.printing import Logger
from videos import const
from pathlib import Path

log = Logger()
django.setup()
from videos.models import Actor, Scene, ActorAlias, SceneTag, Website

def generate_nfo (scene_id: int, force: bool = False):
    """Function to generate a .NFO file from scene metadata.

    Args:
        scene_id (int): The table ID of a scene to scan
        force (bool): Indicates if the operation should be forced

    Returns:
        success: bool
    """

    if not Scene.objects.filter(pk=scene_id): # checks if the scene exists
        log.error(f'NFOGEN: The scene with ID {scene_id} does not exist!')
        return False

    # This will convert the video scene path to the same path with a .nfo extension
    scene = Scene.objects.get(pk=scene_id)
    fpath = scene.path_to_file
    file = Path(fpath)
    nfopath = os.path.join(file.parents[0], file.stem + '.nfo')
    if not os.path.exists(nfopath) or force:
        log.info(f'Writing NFO for {fpath}...')

    else:

    nfo-items = ('title', 'studio', 'releasedate' 'plot', 'aired', 'userrating', 'uniqueid', 'dateadded',
                'datemodified', 'actor', 'fileinfo', 'tag')




### Helper functions

def tag(tagname,tablevel, open)
    tag = "<"+tagname.lower().strip()
    if not tagname.open:
        tag += ">"
    return tag


def closetag():
    return ">"


def tablevels(tablevel):
    for (i in tablevel-1):
        tab = tab + chr(9)
    return tab