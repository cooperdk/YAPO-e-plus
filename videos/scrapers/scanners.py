import os
import os.path
import subprocess
import _thread
import requests
import json
import django.db
import datetime
import pprint
import urllib
import re
from videos import aux_functions as aux
django.setup()
from configuration import Config
import urllib.request
from utils.printing import Logger
log = Logger()
import pycurl, certifi
from io import BytesIO

from videos.models import Actor, Scene, ActorAlias, ActorTag, SceneTag


def tpdb (scene_id: int, force: bool):

    success = False
    found = 0

    current_scene = Scene.objects.get(pk=scene_id)
    scene_name = current_scene.name
    print(f'Scanning for "{scene_name}" on TpDB...')
    # scene_name = scene_name.replace(" ", "%20")

    try:

        parsetext = scene_name
        # if current_scene.tpdb_id is not None and current_scene.tpdb_id != "" and len(current_scene.tpdb_id) > 12:
        #     parsetext = current_scene.tpdb_id
        url = 'https://metadataapi.net/api/scenes'

        params = {
            'parse': parsetext,
            #'q': parsetext,
            'limit': '1'
            # 'hash': 'rerum',
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'YAPO e+ 0.7',
        }
        response = requests.request('GET', url, headers=headers, params=params)
        response = response.json()

        # print (str(response))
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(response)



        if "id" and "title" in str(response):
            found = 1

        else:
            scene_name_formatted = aux.tpdb_formatter(scene_name)
            '''
            for actor in current_scene.actors.all():
                if actor.name in scene_name_formatted:
                    scene_name_formatted=scene_name_formatted.replace(actor.name, "")
                else:
                    for alias in actor.actor_aliases.all():
                        if alias.name in scene_name_formatted:
                            scene_name_formatted = scene_name_formatted.replace(alias.name, "")
            '''
            print(f'Not successful scanning with conventional search,\nNow scanning for "{scene_name_formatted}"...')
            # scene_name = scene_name.replace(" ", "%20")
            url = 'https://metadataapi.net/api/scenes'
            params = {
                'parse': scene_name_formatted,
                'limit': '1'
                # 'q': 'eligendi',
                # 'hash': 'rerum',
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'YAPO e+ 0.7',
            }
            response = requests.request('GET', url, headers=headers, params=params)
            response = response.json()
            if "id" and "title" in str(response):
                found = 2
                

        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(response)
        if found == 1 or found == 2:

            print(f"A result was returned using method {found}. Parsing JSON...")

            if "title" in response['data'][0].keys():
                title = response['data'][0]['title']
                print(f"Title is {title}")
            if "description" in response['data'][0].keys():
                description = response['data'][0]['description']
            if "site" in response['data'][0].keys():
                if "name" in response['data'][0]['site'].keys():
                    site = response['data'][0]['site']['name']
            if "date" in response['data'][0].keys():
                release_date = response['data'][0]['date']
            if "id" in response['data'][0].keys():
                tpdb_id = response['data'][0]['id']
            if description is not None: current_scene.description = description
            if release_date is not None: current_scene.release_date = release_date


            if tpdb_id is not None:
                current_scene.tpdb_id = tpdb_id
                success = True
                current_scene.save()

                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(response['data'])
            perflist = ""
            ite = 0
            for performer in response['data'][0]['performers']:
                ite += 1
                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(performer)
                #print(f"Performers: {perflist}")
                print(f"perfname: {performer['name'].lower().strip()} - perflist: {perflist.lower().strip()}")
                if not performer['name'].lower().strip() in perflist.lower().strip():
                    if performer['parent'] is not None and performer['parent']['extras'] is not None:
                        performer_extras = performer['parent']['extras']
                        # print(performer_extras['gender'])

                        if performer_extras['gender'] is not None and "f" in performer_extras['gender'].lower():
                            print(f"({ite}) - TpDB PERFORMER -> {performer['name']}")
                            for scene_performer in current_scene.actors.all():

                                keyname=""
                                sp=scene_performer.name.lower().strip()
                                perf=performer['name'].lower().strip()
                                if sp == perf:
                                    keyname = scene_performer.name
                                    print(f"  --> YAPO_PERF {scene_performer.name} is keyname")

                                if performer['parent']['name']:
                                    perpn = performer['parent']['name'].lower().strip()
                                    if sp in perpn and not keyname:
                                        keyname = performer['parent']['name']
                                        print(f"  -- TpDB SECONDARY {performer['parent']['name']} is keyname")

                                if 'aliases' in performer.keys():
                                    alia= str(performer['aliases'].lower().strip())
                                else:
                                    alia=""
                                #print (f"SC PERF: {sp} - JSON PERF: {perf} - JSON AKA: {alia} - JSON PERF2: {perpn}")


                                #elif "aliases" in performer.keys() and scene_performer.name.lower().strip() in str(performer['aliases'].lower()):
                                    #print(f"{performer['name']} is an alias to an actor already registered to this scene.")
                                #else:
                                if not keyname:
                                    for alias in scene_performer.actor_aliases.all():
                                        #print(f"Testing alias: {alias.name} ... ",end="")
                                        if (alias.name.lower() in perf) or (alia and (alias.name.lower() in alia)):
                                            keyname = alias.name
                                            print(f"  -- YAPO Alias {alias.name} is keyname")

                                if not keyname:
                                    #actor_to_add = Actor.objects.get(pk=actor_id)
                                    print(f"--SCENE ACTORS: {str(current_scene.actors.all())}")
                                    if (performer['name'].lower() not in str(current_scene.actors.all()).lower()) and (Actor.objects.filter(name=performer['name']).exists()):
                                        actor_to_add = Actor.objects.get(name=performer['name'])
                                        current_scene.actors.add(actor_to_add)
                                        keyname = actor_to_add.name
                                        print(f" --> ACTOR ADDED TO SCENE: {keyname}")

                                if not keyname:
                                    print("No actor found")
                                    continue

                                if keyname:
                                    print("Checking for additional data...")

                                #
                            # TODO: Code to add actor to scene
                            #
                            #    else:
                            #        current_scene.actors.add(name=performer['name'])
                            #        current_scene.save()
                                if Actor.objects.filter(name=keyname).exists():
                                    actor = Actor.objects.get(name=keyname)
                                    if len(perflist) > 3 and not actor.name.lower() in perflist.lower():
                                        perflist = perflist + ", " + actor.name
                                    elif len(perflist) < 3:
                                        perflist = actor.name
                                    print(f"Got actor {actor.name} from db...")
                                    added = False

                                    if actor.date_of_birth == None or actor.date_of_birth == "" or actor.date_of_birth == "1970-01-01":
                                        if "birthday" in performer_extras.keys():
                                            dob = performer_extras["birthday"]
                                            if dob is not None:
                                                actor.date_of_birth = performer_extras["birthday"]
                                                print(f"Added info: Birthday: {actor.date_of_birth}")
                                                added = True
                                                # actor.save()
                                            # print(performer_extras.keys())

                                    if "fakeboobs" in performer_extras.keys():
                                        faketits = performer_extras['fakeboobs']

                                        if faketits is not None:
                                            print(f"Fake tits: {faketits}")
                                            if faketits == True:
                                                print("Yes...")
                                                if not "fake tits" in str(actor.actor_tags.all().lower()):
                                                    actor.actor_tags.add("Fake tits")
                                                    print("Added tag: Fake tits")
                                                    added = True
                                            elif faketits == False:
                                                print("No...")
                                                if not "natural tits" in str(actor.actor_tags.all().lower()):
                                                    actor.actor_tags.add("Natural tits")
                                                    print("Added tag: Natural tits")
                                                    added = True
                                            # actor.save()
                                        else:
                                            print("No info on this actor's tits...")

                                    if not actor.ethnicity or actor.ethnicity == "":
                                        if "ethnicity" in performer_extras.keys():
                                            ethnicity = performer_extras['ethnicity']
                                            if ethnicity is not None:
                                                if actor.ethnicity == None or actor.ethnicity == "":
                                                    actor.ethnicity = ethnicity
                                                    print(f"Ethnicity: {ethnicity}")
                                                    added = True
                                                    # actor.save()

                                    if not actor.country_of_origin or actor.country_of_origin == "":
                                        if "birthplace" in performer_extras.keys():
                                            birthplace = performer_extras['birthplace']
                                            if "united states" in birthplace.lower():
                                                birthplace = "United States"
                                            if birthplace is not None:
                                                if actor.country_of_origin == None or actor.country_of_origin == "":
                                                    actor.country_of_origin = birthplace
                                                    print(f"Birthplace: {birthplace}")
                                                    added = True
                                                    # actor.save()
                                    if not actor.weight or actor.weight == 0:
                                        if "weight" in performer_extras.keys():
                                            weight = performer_extras['weight']
                                            if weight is not None:
                                                weight = re.findall(r'[\d]+', weight)
                                                weight = weight[0]
                                                actor.weight = weight
                                                print(f"Weight: {weight} kg")
                                                added = True

                                    if not actor.height or actor.height == 0:
                                        if "height" in performer_extras.keys():
                                            height = performer_extras['height']
                                            if height is not None:
                                                if "cm" in height:
                                                    height = re.findall(r'[\d]+', height)
                                                elif "in" in height:
                                                    height = re.findall(r'[\d]+', height)
                                                    height = int(round(height * 2.54))
                                                else:
                                                    height = int(round(height * 2.54))
                                                height=height[0]
                                                actor.height = height
                                                print(f"Height: {height} cm")
                                                added = True

                                    if "hair_colour" in performer_extras.keys():
                                        hair = performer_extras['hair_colour']
                                        if hair is not None:
                                            hair = hair.replace("Brunette, ", "")
                                            hair = hair.replace("Blonde, ", "")
                                            hair = hair.replace("Redhead, ", "")

                                            print(f"Hair color: {hair}")
                                            if hair is not None:
                                                tags = str(actor.actor_tags.all())
                                                if not hair.lower() in tags.lower():
                                                    if actor.actor_tags.filter(name__contains=" hair"):
                                                        remtag = actor.actor_tags.filter(name__contains=" hair").values('id')[0]['id']
                                                        print(f"TO REMOVE --> {remtag}")
                                                        actor.actor_tags.remove(remtag)
                                                    insert_actor_tag(actor, hair + " hair")
                                                    print(f"Added tag: {hair} hair")
                                                    added = True
                                                else:
                                                    print(f"Didn't add tag: {hair} hair - it exists already.")

                                    if performer["parent"]["bio"] is not None and len(performer["parent"]["bio"]) > 72:
                                        actor.description = performer["parent"]["bio"]
                                        added = True
                                        # actor.save()

                                    if not actor.gender:
                                        actor.gender = "F"
                                        added = True

                                    if added == True:
                                        actor.last_lookup = datetime.datetime.now()
                                    actor.save()
            newtitle = ""
            if site:
                newtitle = site
            if title and not site and not perflist:
                newtitle = f"{title}"
            if perflist and not site and not title:
                newtitle = f"{perflist}"
            if site and not perflist and not title:
                newtitle = f"{site}"
            if perflist and title and not site:
                newtitle = f"{newtitle} - {title}"
            if site and title and not perflist:
                newtitle = f"{newtitle} - {title}"
            if perflist and site and title:
                newtitle = f"{site} - {perflist} - {title}"
            if site and perflist == title:
                newtitle = f"{site} - {perflist}"
            if not site and perflist == title:
                newtitle = f"{perflist}"

            print(newtitle)
            if Config().autorename_scenes == True or force == True:
                current_scene.name = newtitle

            current_scene.save()
            success = True
            # print(f"Description:\n{description}")
            log.info(f"Found and registered data for scene ID {scene_id}")

    except KeyError:
        success = False
        print(f"Issue(s) occured:\n{sys.exc_info()}")
        #pass

    return success


def strip_bad_chars(name):
    bad_chars = {" "}
    for char in bad_chars:
        if char in name:
            #print("Before: " + name)
            name = name.replace(char, "")
            #print("Adding Data: " + name)
    return name

def insert_actor_tag(actor_to_insert, actor_tag_name):
    actor_tag_name = strip_bad_chars(actor_tag_name)

    if not ActorTag.objects.filter(name=actor_tag_name):
        actor_tag = ActorTag()
        actor_tag.name = actor_tag_name

        actor_tag.save()
        actor_to_insert.actor_tags.add(actor_tag)

    else:
        actor_tag = ActorTag.objects.get(name=actor_tag_name)
        actor_to_insert.actor_tags.add(actor_tag)
        actor_tag.save()
