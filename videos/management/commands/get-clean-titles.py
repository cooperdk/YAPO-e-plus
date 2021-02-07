from django.core.management.base import BaseCommand
from django.utils import timezone
import os
from os import path
import sys
import shutil
import requests
import platform
import videos.aux_functions as aux
from configuration import Config
from utils import Constants
from utils.printing import Logger
from videos.models import Scene, Actor, ActorTag, SceneTag
log = Logger()

class Command(BaseCommand):
    help = 'Scan TpDB for clean scene titles and update the scene database (may be time consuming!)'


    def handle(self, *args, **kwargs):


        from utils import titleparser as tp
        log.sinfo(f'Getting clean scene titles for scanned scenes without any...')
        scenes = Scene.objects.order_by("id")
        row = Scene.objects.raw(
            "SELECT COUNT(*) AS total, id FROM videos_scene"
        )  # cursor.fetchone()
        if row[0].total is not None:
            scenetotal = str(row[0].total)
        print("")
        number = 0

        for scene in scenes:
            number += 1
            #aux.sysclear()
            found = 0
            saved = False
            print(f'Scanning scenes - scene {number} of {scenetotal}...', end="")
            if (not scene.clean_title or scene.clean_title == "") and (len(scene.tpdb_id) > 8):

                # try:
                parsetext = scene.name
                parsedict = tp.search(parsetext)
                if parsedict[3]:
                    parsetext = parsedict[1] + " " + parsedict[2] + " " + parsedict[3]
                elif parsedict[1]:
                    parsetext = parsedict[1] + " " + parsedict[2]
                else:
                    parsetext = parsedict[2]

                print(f"Parser will search for: {parsetext}")
                # if scene.tpdb_id is not None and scene.tpdb_id != "" and len(scene.tpdb_id) > 12:
                #     parsetext = scene.tpdb_id
                url = 'https://api.metadataapi.net/scenes'

                params = {
                    'parse': parsetext,
                    'limit': '1'
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'YAPO e+ 0.73',
                }
                #print("Scanning... ", end="")
                response = requests.request('GET', url, headers=headers, params=params, timeout=8)

                try:
                    response = response.json()
                except requests.exceptions.RequestException as e:
                    print(e)
                    pass

                # print (str(response))
                # pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(response)

                if "id" and "title" in str(response):
                    found = 1

                else:
                    aux.remove_text_inside_brackets(scene.name, brackets="[]")
                    scene_name_formatted = aux.tpdb_formatter(scene.name)
                    print("")
                    print(f'\nNot successful, trying with "{scene_name_formatted}"...')
                    # scene_name = scene_name.replace(" ", "%20")
                    url = 'https://api.metadataapi.net/scenes'
                    params = {
                        'parse': scene_name_formatted,
                        'limit': '1'
                        # 'q': 'eligendi',
                        # 'hash': 'rerum',
                    }
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'User-Agent': 'YAPO e+ 0.73',
                    }
                    response = requests.request('GET', url, headers=headers, params=params, timeout=8)
                    try:
                        response = response.json()
                    except requests.exceptions.RequestException as e:
                        print(e)
                        pass
                    if "id" and "title" in str(response):
                        found = 2

                # except:
                #    pass
                if found == 1 or found == 2:
                    print(f"  --> A result was returned using method {found}.")
                    title = "None"
                    id = "None"
                    url = "None"

                    if "title" in response['data'][0].keys() and ((not scene.clean_title) or (scene.clean_title == "")):
                        title = response['data'][0]['title']
                        scene.clean_title = title
                        print(f"  --> Title: {scene.clean_title}")
                        saved = True
                    if "id" in response['data'][0].keys() and not scene.tpdb_id:
                        id = response['data'][0]['id']
                        scene.tpdb_id = id
                        print(f"  -->    ID: {scene.tpdb_id}")
                        saved = True
                    if "url" in response['data'][0].keys() and not scene.url:
                        url = response['data'][0]['url']
                        scene.url = url
                        print(f"  -->   URL: {scene.url} ", end="")
                        saved = True

                    if saved:
                        scene.save(force_update=True)
            else:
                print("\r", end="")
        print("\nDone.")
