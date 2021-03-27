"""
This is the scene title/filename renamer.
Default replace format could be:
    '{site} - {date} - {actor} - {title} ({codec}).{ext}'
"""
import os
import re
import shutil
from datetime import datetime
from dateutil.parser import parse as dateparse
import django
import builtins
from configuration import Config
from utils.printing import Logger
from videos import const
from videos import aux_functions as aux
from pathlib import Path

log = Logger()
django.setup()
from videos.models import Actor, Scene, ActorAlias, SceneTag, Website



def rename (scene_id: int, force: bool = False):
    """
    Function to rename a scene to to a default or site specific rename format.
    It basically renames the file just as the title renamer does it.

    Args:
        scene_id (int): The table ID of a scene to scan
        force (bool): Indicates if the operation should be forced. Default is false

    Returns:
        success: bool
    """

    if all([Scene.objects.filter(pk=scene_id).first().orig_name is None, not force]): # checks if the scene was retitled
        log.warn(f'RENAMER: The scene has not been re-titled (with fx the TpDB scanner), you must force this operation.')
        return "notretitled"

    if not Scene.objects.filter(pk=scene_id): # checks if the scene exists
        log.error(f'RENAMER: The scene with ID {scene_id} does not exist!')
        return False

    # This sorts out the original filename
    scene = Scene.objects.get(pk=scene_id)
    fpath = scene.path_to_file
    fdir = scene.path_to_dir
    import os
    justdir, justfile = os.path.split(r""+fpath) # Splits the directory and filename in two variables (raw format)
    justfilenoext = os.path.splitext(justfile)[0]
    justext = os.path.splitext(justfile)[1]

    if not os.path.exists(fpath):
        log.info(f'RENAMER: Scene {scene_id}: Path {fpath} does not exist!')
        return False

    if len(str(scene.actors))>1:
        actlist = []
        for act2 in scene.actors.all():
            actlist.append(act2.name)
        #actlist = scene.actors.values_list
        #actors = ', '.join(str(y) for x in actlist for y in x if len(x) > 0)
        actors = ', '.join(actlist)
    if actlist == None:
        actlist = "Unknown"
    if scene.actors.all().first():
        actor = scene.actors.all().first().name
    else:
        actor = "Unknown"
    res = aux.restest(scene.height)
    if scene.websites.all().first():
        site = scene.websites.all().first().name
    else:
        site = "Unknown"
    if scene.clean_title:
        title = scene.clean_title
    else:
        title = scene.name
    date = str(scene.release_date)
    dd=""
    mm=""
    mmmm=""
    yy=""
    yyyy=""
    usedate = True
    if len(str(date)) > 6:
        date2 = dateparse(date)
        '''
        date = str(date.replace("."," ").replace("-"," ").replace("/"," "))
        regex = [
            (r'\b\d{4} \d{2} \d{2}\b', '%Y %m %d'),
            (r'\b\d{2} \d{2} \d{4}\b', '%d %m %Y'),
            (r'\b\d{2} \d{2} \d{2}\b', '%d %m %y'),
            (r'\b\d{2} \d{2} \d{2}\b', '%y %m %d'),
            (r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}.*?\s\d{2}|\d{4}', '%b %d %Y'),
            (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2}.*?\s\\d{2}|\d{4}', '%b %d %Y'),
            (r'\d{2}[.*?][\s?](January|February|March|April|May|June|July|August|September|October|November|December)[\s?][.*?]\s\d{2}|\d{4}',
             '%b %d %Y'),
            (r'(\d+)[/\.-](\d+)[/\.-](\d+)', '%y %m %d'),
        ]
        date_obj = None
        for r, dateFormat in regex:
            try:
                date_obj = datetime.strptime(date.group(), dateFormat).date()
                print("Date found: {date}")
            except:
                pass
        '''

        if date2:
            dd = date2.strftime("%d")
            mm = date2.strftime("%m")
            mmmm = date2.strftime("%B")
            yy = date2.strftime("%y")
            yyyy = date2.strftime("%Y")
            date = date2.strftime("%Y-%m-%d")

        else:
            log.warn(f"RENAMER: Scene ID {scene.id} - date mismatch ({date})")
            usedate = False
    else:
        log.info(f"RENAMER: Scene ID {scene.id} - date not found ({date}).")
        usedate = False

    renameformat = scene.websites.all().first().filename_format  # find out if the website has it's own rename format
    if len(renameformat) <5:  #T his will tell to get the default rename format
        renameformat = Config().renaming
        renamebase = "default format"
    else:
        renamebase = "website format"
    log.sinfo(f'Renaming scene ID {scene_id} based on {renamebase}...')
    fpath = scene.path_to_file
    renameformat_orig = renameformat
    renameformat = renameformat.replace('<', '{').replace('>', '}')
    if not usedate:
        if any(['{dd}' in renameformat, '{mm}' in renameformat, '{mmmm}' in renameformat,
                '{yy}' in renameformat, '{yyyy}' in renameformat, '{date}' in renameformat]):
            log.warn(f'RENAMER: Scene {scene_id}: Date unusable but required by format. Trying to avoid dates.')
            dd = ""
            mm = ""
            mmmm = ""
            yy = ""
            yyyy = ""
            date = ""

    newname = eval(f"f'''{renameformat}'''")    # This replaces the strings specified by the user with their value.
                                                # Triple quotes are required to allow quotes in the string.
    #print(f"Renaming by format:")
    #print(f"                    {renameformat_orig}")
    #print(f"                    {newname}")
    print(newname + " -> ",end="")
    newname = newname.replace("Unknown - ","").replace("-- - ", "").replace("// / ","").replace("- -- ","").replace("/ // ","")
    for c in r'[]/\;,><&*:%=+@!#^()|?^':
        newname = newname.replace(c, "")
    print(newname)
    iteration = 1
    renamedok = False
    while not renamedok:
        workname = newname
        if iteration > 1:
            workname = workname + f"_{iteration}"
        newfilename = os.path.join(justdir,workname+justext)
        print(f"Testing {newfilename}")
        if not os.path.exists(newfilename):
            renamedok = True
            newnfo = os.path.join(justdir,workname+".nfo")
            if os.path.exists(newnfo):
                print("Renaming NFO")
            else:
                print("No NFO exists, and I cannot rename something that isn't there.")
        else:
            iteration += 1
    print(f'Filename {newfilename} not in use, renaming...')
    try:
        log.sinfo(f"REN: \n{fpath} >\n{newfilename}")
        os.rename(fpath,newfilename)
        renamedname=workname+justext
    except IOError as exc:
        log.error(f"RENAMER: Failure renaming scene {scene_id} ({fpath}): {exc}")
        return False
    if not scene.orig_path_to_file:
        scene.orig_path_to_file = fpath
    scene.path_to_file = newfilename
    scene.save(force_update=True)
    return renamedname





def fstr_eval(_s: str, raw_string=False, eval=builtins.eval):
    r"""str: Evaluate a string as an f-string literal.

    Args:
       _s (str): The string to evaluate.
       raw_string (bool, optional): Evaluate as a raw literal
           (don't escape \). Defaults to False.
       eval (callable, optional): Evaluation function. Defaults
           to Python's builtin eval.

    Raises:
        ValueError: Triple-apostrophes ''' are forbidden.
    """
    # Prefix all local variables with _ to reduce collisions in case
    # eval is called in the local namespace.
    _TA = "'''" # triple-apostrophes constant, for readability
    if _TA in _s:
        raise ValueError("Triple-apostrophes ''' are forbidden. " + \
                         'Consider using """ instead.')

    # Strip apostrophes from the end of _s and store them in _ra.
    # There are at most two since triple-apostrophes are forbidden.
    if _s.endswith("''"):
        _ra = "''"
        _s = _s[:-2]
    elif _s.endswith("'"):
        _ra = "'"
        _s = _s[:-1]
    else:
        _ra = ""
    # Now the last character of s (if it exists) is guaranteed
    # not to be an apostrophe.

    _prefix = 'rf' if raw_string else 'f'
    return eval(_prefix + _TA + _s + _TA) + _ra