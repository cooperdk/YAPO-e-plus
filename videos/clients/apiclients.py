#import django
import http.client
import os
import os.path
import re
import sys
# import pprint
import urllib
import urllib.request
from datetime import datetime
from videos.scrapers.sites.bangbros import getinfo as bb_getinfo
# import json
#from django.db import transaction
# import subprocess
# import _thread
import requests

import videos.clients.tmdb as scraper_tmdb
import videos.scrapers.freeones as freeones
from configuration import Config, Constants
from utils import titleparser as tp
from utils.printing import Logger
from videos import aux_functions as aux

#django.setup()
from videos.models import Actor, Scene, ActorAlias, ActorTag, SceneTag, Website

http.client._MAXHEADERS = 1000
log = Logger()


def tpdb(scene_id: int, force: bool):
    """Function to scan a scene using the TpDB API (metadataapi.net).

    Args:
        scene_id (int): The table ID of a scene to scan
        force (bool): Indicates if the operation should be forced

    Returns:
        success: bool
    """
    title = ""
    site = ""
    date = ""
    perflist = ""
    success = False
    found = 0

    if not aux.is_domain_reachable("api.metadataapi.net") or not aux.checkTpDB():
        return False

    this_scene = Scene.objects.get(pk=scene_id)
    scene_name = this_scene.name
    searched = 0

    bbcheck = bb_getinfo(scene_id, scene_name)
    if bbcheck:
        scene_name = f'{bbcheck[1]} - {bbcheck[3]} - {bbcheck [2]}'

    for scene_tag in this_scene.scene_tags.all():
        if scene_tag.name == "TpDB: Match: None":
            this_scene.tpdb_scanned = True
            this_scene.tpdb_scanned_match = False
            this_scene.tpdb_scanned_unsure = False
            try:
                this_scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Match: None"))
            except:
                pass

        if scene_tag.name == "TpDB: Match: Questionable":
            this_scene.tpdb_scanned = True
            this_scene.tpdb_scanned_match = True
            this_scene.tpdb_scanned_unsure = True
            try:
                this_scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Match: Questionable"))
            except:
                pass

        if scene_tag.name == "TpDB: Match: Good":
            this_scene.tpdb_scanned = True
            this_scene.tpdb_scanned_match = True
            this_scene.tpdb_scanned_unsure = False
            try:
                this_scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Match: Good"))
            except:
                pass


    if this_scene.tpdb_scanned_match:
        searched = 2

    if searched and not force:
        log.sinfo(f"Scene #{this_scene.id} was already checked by the TpDB scanner. To re-scan, use force.")
        return 2  # Scene is searched already, exit

    log.sinfo(f'Scanning for "{scene_name}" on TpDB...')

    try:
        parsetext = scene_name
        parsedict = tp.search(parsetext)
        if parsedict[3]:
            parsetext = parsedict[1] + " " + parsedict[2] + " " + parsedict[3]
        elif parsedict[1]:
            parsetext = parsedict[1] + " " + parsedict[2]
        else:
            parsetext = parsedict[2]

        log.sinfo(f"I'm going to search for: {parsetext}")
        # if this_scene.tpdb_id is not None and this_scene.tpdb_id != "" and len(this_scene.tpdb_id) > 12:
        #     parsetext = this_scene.tpdb_id
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

        response = requests.request('GET', url, headers=headers, params=params, timeout=5)

        try:
            response = response.json()
        except requests.exceptions.RequestException as e:
            pass

        # print (str(response))
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(response)

        if "id" and "title" in str(response):
            found = 1
            print ("\n")

        else:
            aux.remove_text_inside_brackets(scene_name, brackets="[]")
            scene_name_formatted = aux.tpdb_formatter(scene_name)
            '''
            for actor in this_scene.actors.all():
                if actor.name in scene_name_formatted:
                    scene_name_formatted=scene_name_formatted.replace(actor.name, "")
                else:
                    for alias in actor.actor_aliases.all():
                        if alias.name in scene_name_formatted:
                            scene_name_formatted = scene_name_formatted.replace(alias.name, "")
            '''
            #log.sinfo(f'\nParse unsuccessful, trying an alternative method.')
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
            response = requests.request('GET', url, headers=headers, params=params, timeout=5)
            try:
                response = response.json()
            except requests.exceptions.RequestException as e:
                pass
            if "id" and "title" in str(response):
                found = 2

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(response)
        if found == 1 or found == 2:

            print(f"  --> A result was returned using method {found}. Parsing JSON...")
            site_logo = ""
            if "title" in response['data'][0].keys():
                title = response['data'][0]['title']
                print(f"  --> Title is {title}")
            if "description" in response['data'][0].keys():
                description = response['data'][0]['description']
            if "site" in response['data'][0].keys():
                if "name" in response['data'][0]['site'].keys():
                    site = response['data'][0]['site']['name']
                    site_logo = response['data'][0]['site']['logo']
                if "tags" in response['data'][0].keys():
                    scenetags = response['data'][0]['tags']
            if "date" in response['data'][0].keys():
                release_date = response['data'][0]['date']
            if "id" in response['data'][0].keys():
                tpdb_id = response['data'][0]['id']
            if description is not None:
                this_scene.description = description
            if release_date is not None:
                # print(release_date)
                try:
                    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

                # release_date = strftime(release_date) + " 00:00:00"
                # release_date = datetime.strptime(release_date, "%Y-%m-%d %H:%M:%S")
                    print(f'Release date: {release_date}')
                except:
                    release_date = None
                if release_date is not None:
                    this_scene.release_date = release_date

            if tpdb_id is not None:
                this_scene.tpdb_id = tpdb_id
                print(f'TpDB ID: {tpdb_id}')
                success = True
            print(this_scene)

            this_scene.save(force_update=True)

                # pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(response['data'])
            perflist = ""
            ite = 0
            perf = ""
            for performer in response['data'][0]['performers']:
                perf = namecheck(performer['name'])
                perforiginal = performer['name']
                perpn = ""
                keyname = ""
                primary = 0
                secondary = 0
                ite += 1
                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(performer)
                #print(f"Performers: {perflist}")
                print(f"----> PERFORMER: {perf} - list: {perflist}")
                if not perf.lower().strip() in perflist.lower().strip():
                    if performer['parent'] is not None and performer['parent']['extras'] is not None:
                        performer_extras = performer['parent']['extras']
                        # print(performer_extras['gender'])
                        keyname = ""
                        actoradded = False
                        sp = ""
                        if performer_extras['gender'] is not None and "f" in performer_extras['gender'].lower():
                            print(f"  --> TpDB PERFORMER -> Checking #{ite} ({perf})...")
                            actors = list(Actor.objects.extra(select={"length": "Length(name)"}).order_by("-length"))
                            sp = ""
                            for scene_performer in actors:

                                keyname = ""
                                primary = 0
                                sp = scene_performer.name
                                if sp.lower() == perforiginal.lower():
                                    keyname = sp
                                    primary = 1
                                    print(f"  --> SM 1: YAPO performer name {scene_performer.name} is keyname")
                                    break

                                if not keyname:
                                    sp = scene_performer.name
                                    perf = namecheck(perf)
                                    if sp.lower() == perf.lower():
                                        keyname = scene_performer.name
                                        primary = 1
                                        print(f"  --> SM 1: YAPO performer name {sp} matches checked TpDB name")
                                        break

                            if not keyname:

                                akaroot = ActorAlias.objects.all()

                                if not keyname and 'aliases' in performer.keys():
                                    alia = str(performer['aliases']).lower().strip()

                                    for alias in akaroot:

                                        if not keyname and alias.name.lower() == perf.lower():
                                            keyname = alias.name
                                            primary = 3
                                            break
                                        if not keyname and alias.name.lower() == performer['name']:
                                            keyname = alias.name
                                            primary = 3
                                            break
                                        if not keyname:
                                            for alia in performer['aliases']:
                                                if alias.name.lower() == alia.lower():
                                                    keyname = alias.name
                                                    primary = 3
                                                    break
                                        if not keyname and 'aliases' in performer['parent'].keys:
                                            for alia in performer['parent']['aliases']:
                                                if alias.name.lower() == alia.lower():
                                                    keyname = alias.name
                                                    primary = 3
                                                    break
                                        else:
                                            alia = ""

                            # print("keyname " + keyname)
                            if keyname.strip() != "":
                                # actor_to_add = Actor.objects.get(pk=actor_id)
                                print("----> CHECKING SCENE ACTORS")
                                keyname = namecheck(keyname)
                                if (keyname.lower() not in str(this_scene.actors.all()).lower()) and \
                                        (Actor.objects.filter(name=keyname).exists()):
                                    print("  --> ACTOR MATCH")
                                    actor_to_add = Actor.objects.get(name=keyname)
                                    keyname = actor_to_add.name
                                    if not this_scene.actors.filter(name=keyname):
                                        aux.addactor(this_scene, actor_to_add)
                                        print(f"  --> ACTOR ADDED TO SCENE: {keyname}")
                                    else:
                                        print("  --> ACTOR already in scene.")

                            # print("keyname " + keyname)
                            if not keyname:
                                perpn = performer['name']
                                perpn = namecheck(perpn)
                                secondary = 2
                                # print ("perpn sec " + perpn + " sp lwr " + sp)
                                keyname = perpn
                                print(f"  --> SM 2: TpDB REPLACED {performer['name']} -> {keyname} is keyname")

                                # print("keyname " + keyname)
                            if performer['parent']['name'] and not keyname:
                                perpn = performer['parent']['name']
                                perpn = namecheck(perpn)
                                # print("perpn thd " + perpn + " sp lwr " + sp)
                                keyname = perpn
                                secondary = 3
                                print(f"  --> SM 3: {keyname} is keyname")
                            # print("keyname " + keyname + " - perf name " + perpn)
                            if Config().tpdb_actors and perpn and keyname and (primary == 0):
                                # If an actor is found on TpDB, but doesn't exist in YAPO
                                log.info(f"Auto-adding a new actor: {perpn}")
                                # try:
                                if 'image' in performer.keys() and secondary == 2:
                                    print(f"Perf img check: {performer.keys()}")
                                    img = performer['image']
                                elif 'image' in performer['parent'].keys() and secondary == 3:
                                    print(f"Perf img check: {performer['parent'].keys()}")
                                    img = performer['parent']['image']
                                act = Actor()
                                act.name = perpn
                                act.date_added = datetime.now()
                                act.thumbnail = Constants().unknown_person_image_path
                                act.save()
                                actoradded = True
                                aux.addactor(this_scene, act)
                                if act.thumbnail == Constants().unknown_person_image_path:
                                    # print(f"No image, downloading ({img}) - ", end="")
                                    save_path = os.path.join(Config().site_media_path, 'actor', str(act.id),
                                                             'profile')
                                    # print("Profile pic path: " + save_path)
                                    save_file_name = os.path.join(save_path, 'profile.jpg')
                                    if img and not os.path.isfile(save_file_name):
                                        if not os.path.exists(save_path):
                                            os.makedirs(save_path)
                                        aux.download_image(img, save_file_name)
                                        rel_path = os.path.relpath(save_file_name, start="videos")
                                        as_uri = urllib.request.pathname2url(rel_path)
                                        act.thumbnail = as_uri

                                act.save()
                                log.sinfo(f"  --> ACTOR CREATED AND ADDED TO SCENE: {act.name}")
                                # except:
                                    # log.error(f'Couldn\'t add {perpn} - possibly exists already even though she didn\'t turn up...')
                                    # break
                            elif not Config().tpdb_actors:
                                log.info(f"We could add the actor {act.name}, but auto-adding is disabled.")

                            if actoradded and perpn:
                                log.sinfo(f"Scraping additional info about {act.name}...")
                                success = scraper_tmdb.search_person_with_force_flag(
                                    act, True)
                                success = freeones.search_freeones_with_force_flag(
                                        act, True)

                        if (keyname.strip() != "") and (Actor.objects.filter(name=keyname).exists()):
                            actor = Actor.objects.get(name=keyname)
                            if len(perflist) > 3 and not actor.name.lower() in perflist.lower():
                                perflist = perflist + ", " + actor.name
                            elif len(perflist) < 3:
                                perflist = actor.name
                            # print(f"Got actor {actor.name} from db...")
                            added = False

                            if actor.date_of_birth is None or actor.date_of_birth == "" \
                                    or actor.date_of_birth == "1970-01-01":

                                if "birthday" in performer_extras.keys():
                                    dob = performer_extras["birthday"]
                                    if dob is not None:
                                        actor.date_of_birth = performer_extras["birthday"]
                                        # print(f"Added info: Birthday: {actor.date_of_birth}")
                                        added = True
                                        # actor.save()
                                    # print(performer_extras.keys())

                            if "fakeboobs" in performer_extras.keys():
                                faketits = performer_extras['fakeboobs']

                                if faketits is not None:
                                    if faketits:
                                        if "tits" not in str(actor.actor_tags.all().lower()):
                                            actor.actor_tags.add("Fake tits")
                                            added = True
                                    elif not faketits:
                                        print("No...")
                                        if "tits" not in str(actor.actor_tags.all().lower()):
                                            actor.actor_tags.add("Natural tits")
                                            added = True

                            if not actor.ethnicity or actor.ethnicity == "":
                                if "ethnicity" in performer_extras.keys():
                                    ethnicity = performer_extras['ethnicity']
                                    if ethnicity is not None:
                                        if actor.ethnicity is None or actor.ethnicity == "":
                                            actor.ethnicity = ethnicity
                                            added = True

                            if not actor.country_of_origin or actor.country_of_origin == "":
                                if "birthplace" in performer_extras.keys():
                                    birthplace = performer_extras['birthplace']
                                    if birthplace is not None:
                                        if "united states" in birthplace.lower():
                                            birthplace = "United States"
                                        if actor.country_of_origin is None or actor.country_of_origin == "":
                                            actor.country_of_origin = birthplace
                                            added = True
                            if not actor.weight or actor.weight == 0:
                                if "weight" in performer_extras.keys():
                                    weight = performer_extras['weight']
                                    if weight is not None:
                                        weight = re.findall(r'[\d]+', weight)
                                        weight = weight[0]
                                        actor.weight = weight
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
                                        added = True

                            if "hair_colour" in performer_extras.keys():
                                hair = performer_extras['hair_colour']
                                if hair is not None:
                                    hair = hair.replace("Brunette, ", "")
                                    hair = hair.replace("Blonde, ", "")
                                    hair = hair.replace("Redhead, ", "")
                                    if hair is not None:
                                        if not actor.actor_tags.filter(name__contains=" hair"):
                                            insert_actor_tag(actor, hair + " hair".capitalize())
                                            print(f"Added tag: {hair.capitalize()} hair")
                                            added = True

                            if performer["parent"]["bio"] is not None and len(performer["parent"]["bio"]) > 72:
                                actor.description = performer["parent"]["bio"]
                                added = True

                            if not actor.gender:
                                actor.gender = "F"
                                added = True

                            if added:
                                insert_actor_tag(actor, "TpDB: Info added")
                                actor.last_lookup = datetime.now()
                            actor.save()

                            if added:
                                log.sinfo(f"Some information about {actor.name} was added to the profile.")

            if found:

                try:
                    website = Website.objects.get(name=site)
                except:
                    website = "none"
                if not this_scene.websites.filter(name=site):
                    if website != "none":
                        log.sinfo(f"Adding website: {website.name} to the scene {this_scene.name}")
                        this_scene.websites.add(website)
                    else:
                        log.warn(f"This website couldn't be found: {site}")
                        aux.save_website_logo(site_logo, site, False, this_scene.id)
                else:
                    print("Website already registered to scene.")
                    aux.save_website_logo(site_logo, site, False, this_scene.id)
            #try:
            newtitle = ""
            if title:
                this_scene.clean_title = title

            if bbcheck:
                this_scene.release_id = bbcheck[0]

            if perflist: actors = perflist
            else: actors = "Unknown"
            if this_scene.actors.all().first(): actor = this_scene.actors.all().first().name
            else: actor = "Unknown"
            if this_scene.websites.all().first(): site = this_scene.websites.all().first().name
            else: site = "Unknown"
            res = aux.restest(this_scene.height)
            if release_date:
                dd = release_date.strftime("%d")
                mm = release_date.strftime("%m")
                mmmm = release_date.strftime("%B")
                yy = release_date.strftime("%y")
                yyyy = release_date.strftime("%Y")



            if this_scene.websites.all().first():
                renameformat = this_scene.websites.all().first().filename_format  # find out if the website has it's own rename format
            if len(renameformat) < 5:  # This will tell to get the default rename format
                renameformat = Config().renaming
                renamebase = "default format"
            else:
                renamebase = "website format"
            renameformat = renameformat.replace('<', '{').replace('>', '}')
            log.sinfo(f'Renaming scene ID {scene_id} based on {renamebase}...')

            if not release_date:
                if any(['{dd}' in renameformat, '{mm}' in renameformat, '{mmmm}' in renameformat,
                        '{yy}' in renameformat, '{yyyy}' in renameformat]):
                    log.warn(
                        f'TpDB: Scene {this_scene.id} - ERROR! Date unusable but required by the renaming format. Inserting placeholders.')
                questiondate()

            newtitle = eval(f"f'''{renameformat}'''")
            log.sinfo(f'{newtitle}')

            '''
            if (perflist and len(perflist) > 4) and newtitle and \
                    perflist.lower().strip() != newtitle.lower().strip():
                newtitle = f"{perflist} - {newtitle}"
            elif perflist.lower() and not newtitle:
                newtitle = f"{perflist}"
            elif newtitle and not perflist.lower():
                newtitle = f"{newtitle}"

            if release_date is not None:
                newtitle = f"{release_date} - {newtitle}"
                # print(newtitle)

            if site:
                newtitle = f"{site} - {newtitle}"
                # print(newtitle)
            '''

            # print(Config().tpdb_autorename.lower())
            if "true" in Config().tpdb_autorename.lower():
                if not this_scene.orig_name:
                    this_scene.orig_name = this_scene.name
                this_scene.name = newtitle
                log.sinfo(f'Scene name is now \"{newtitle}\".')
            else:
                print(f'Renaming is disabled, but we suggest: \"{newtitle}\".')

            success = True
            # print(f"Description:\n{description}")
            #except:
            #    log.error(f'An error occured while trying to give scene {this_scene.id} a new title!')
            try:
                if found:
                    tagcounter = 0
                    maxtags = int(Config().tpdb_tags)
                    if maxtags > 0:
                        print(f"Max tags set to {maxtags}")
                        print('Inserting tags: ', end="")
                        for tag in scenetags:
                            if tagcounter < maxtags:
                                tagcounter += 1
                                print(f'[ {tag["tag"].capitalize()} ]', end="")
                                insert_scene_tag(this_scene, tag["tag"].capitalize())
                            else:
                                break
                        print("\n")
                        if Config().debug=="true":
                            log.sinfo(f"Added {tagcounter} tags from TpDB to this scene.")
            except:
                pass


            if found == 1:
                this_scene.tpdb_scanned = True
                this_scene.tpdb_scanned_match = True
                this_scene.tpdb_scanned_unsure = False
            elif found == 2:
                this_scene.tpdb_scanned = True
                this_scene.tpdb_scanned_match = True
                this_scene.tpdb_scanned_unsure = True
            elif not success:
                this_scene.tpdb_scanned = True
                this_scene.tpdb_scanned_match = False
                this_scene.tpdb_scanned_unsure = False

            # print("Tagged the scene with a TpDB tag.")
            if Config().debug=="true":
                log.sinfo(f"Found and registered data for scene ID {scene_id}")
            if found == 2:
                log.info(f"Scene ID {scene_id} may have incorrect data, marked that in the database. Please check manually.")
            #print(this_scene)
            this_scene.save(force_update=True)
            return 1

        else:
            log.sinfo(f"Scene {scene_id} was not found in TpDB.")
            this_scene.save(force_update=True)
            return 0

    except KeyError:
        success = False
        log.warn(f"Issue(s) occured: {sys.exc_info()}")
        return success
        # pass


def questiondate():
    dd = "??"
    mm = "??"
    mmmm = "????"
    yy = "??"
    yyyy = "????"


def strip_bad_chars(name):
    bad_chars = {" "}
    for char in bad_chars:
        if char in name:
            # print("Before: " + name)
            name = name.replace(char, "")
            # print("Adding Data: " + name)
    return name


def insert_scene_tag(this_scene, tagname):
    if not SceneTag.objects.filter(name=tagname):
        SceneTag.objects.create(name=tagname)

    scene_tag_to_add = SceneTag.objects.get(name=tagname)
    this_scene.scene_tags.add(scene_tag_to_add)


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


def namecheck(actor: str):

    new_actor = actor.strip()

    if new_actor == "Abby Lee":
        new_actor = "Abby Lee Brazil"
    if new_actor == "Abby Rains":
        new_actor = "Abbey Rain"
    if new_actor == "Ms Addie Juniper":
        new_actor = "Addie Juniper"
    if new_actor in ["Adrianna Chechik", "Adriana Chechick"]:
        new_actor = "Adriana Chechik"
    if new_actor == "Alex D":
        new_actor = "Alex D."
    if new_actor in ["Alura Tnt Jenson", "Alura 'Tnt' Jenson"]:
        new_actor = "Alura Jenson"
    if new_actor == "Amia Moretti":
        new_actor = "Amia Miley"
    if new_actor == "Amy Reid":
        new_actor = "Amy Ried"
    if new_actor in ["Ana Fox", "Ana Foxx"]:
        new_actor = "Ana Foxxx"
    if new_actor in ["Andreina De Lux", "Andreina De Luxe", "Andreina Dlux"]:
        new_actor = "Andreina Deluxe"
    if new_actor in ["Angela Piaf", "Angel Piaf"]:
        new_actor = "Angel Piaff"
    if new_actor in ["Ani Black Fox", "Ani Black"]:
        new_actor = "Ani Blackfox"
    if new_actor == "Anikka Albrite":
        new_actor = "Annika Albrite"
    if new_actor == "Anita Bellini":
        new_actor = "Anita Bellini Berlusconi"
    if new_actor in ["Anjelica", "Ebbi", "Abby H", "Katherine A"]:
        new_actor = "Krystal Boyd"
    if new_actor == "Anna Morna":
        new_actor = "Anastasia Morna"
    if new_actor in ["April ONeil", "April Oneil", "April O'neil"]:
        new_actor = "April O'Neil"
    if new_actor == "Ashley Graham":
        new_actor = "Ashlee Graham"
    if new_actor == "Bella Danger":
        new_actor = "Abella Danger"
    if new_actor in ["Bibi Jones", "Bibi Jones™"]:
        new_actor = "Britney Beth"
    if new_actor == "Bridgette B.":
        new_actor = "Bridgette B"
    if new_actor == "Capri Cavalli":
        new_actor = "Capri Cavanni"
    if new_actor == "Ce Ce Capella":
        new_actor = "CeCe Capella"
    if new_actor == "Charli Red":
        new_actor = "Charlie Red"
    if new_actor == "Charlotte Lee":
        new_actor = "Jaye Summers"
    if new_actor == "Chloe Cherry":
        new_actor = "Chloe Couture"
    if new_actor == "Criss Strokes":
        new_actor = "Chris Strokes"
    if new_actor == "Christy Charming":
        new_actor = "Paula Shy"
    if new_actor == "CléA Gaultier":
        new_actor = "Clea Gaultier"
    if new_actor in ["Crissy Kay", "Emma Hicks", "Emma Hixx"]:
        new_actor = "Emma Hix"
    if new_actor == "Crystal Rae":
        new_actor = "Cyrstal Rae"
    if new_actor == "Doris Ivy":
        new_actor = "Gina Gerson"
    if new_actor == "Eden Sin":
        new_actor = "Eden Sinclair"
    if new_actor == "Elsa Dream":
        new_actor = "Elsa Jean"
    if new_actor == "Eve Lawrence":
        new_actor = "Eve Laurence"
    if new_actor in ["Francesca Di Caprio", "Francesca Dicaprio"]:
        new_actor = "Francesca DiCaprio"
    if new_actor == "Guiliana Alexis":
        new_actor = "Gulliana Alexis"
    if new_actor == "Grace Hartley":
        new_actor = "Pinky June"
    if new_actor == "Hailey Reed":
        new_actor = "Haley Reed"
    if new_actor == "Josephina Jackson":
        new_actor = "Josephine Jackson"
    if new_actor == "Jane Doux":
        new_actor = "Pristine Edge"
    if new_actor == "Jade Indica":
        new_actor = "Miss Jade Indica"
    if new_actor in ["Jassie Gold", "Jaggie Gold"]:
        new_actor = "Jessi Gold"
    if new_actor in ["Jenna J Ross", "Jenna J. Ross"]:
        new_actor = "Jenna Ross"
    if new_actor == "Jenny Ferri":
        new_actor = "Jenny Fer"
    if new_actor in ["Jessica Blue", "Jessica Cute"]:
        new_actor = "Jessica Foxx"
    if new_actor == "Jo Jo Kiss":
        new_actor = "Jojo Kiss"
    if new_actor in ["Josephine", "Conny", "Conny Carter", "Connie"]:
        new_actor = "Connie Carter"
    if new_actor == "Kagney Lynn Karter":
        new_actor = "Kagney Linn Karter"
    if new_actor == "Kari Sweets":
        new_actor = "Kari Sweet"
    if new_actor == "Katarina":
        new_actor = "Katerina Hartlova"
    if new_actor == "Kendra May Lust":
        new_actor = "Kendra Lust"
    if new_actor in ["Khloe Capri", "Chloe Capri"]:
        new_actor = "Khloe Kapri"
    if new_actor == "Lara Craft":
        new_actor = "Lora Craft"
    if new_actor in [
        "Lilly LaBeau",
        "Lilly Labuea",
        "Lily La Beau",
        "Lily Lebeau",
        "Lily Luvs",
    ]:
        new_actor = "Lily Labeau"
    if new_actor == "Lilly Lit":
        new_actor = "Lilly Ford"
    if new_actor in ["Maddy OReilly", "Maddy Oreilly", "Maddy O'reilly"]:
        new_actor = "Maddy O'Reilly"
    if new_actor in ["Maria Rya", "Melena Maria"]:
        new_actor = "Melena Maria Rya"
    if new_actor == "Moe The Monster Johnson":
        new_actor = "Moe Johnson"
    if new_actor in ["Nadya Nabakova", "Nadya Nabokova"]:
        new_actor = "Bunny Colby"
    if new_actor in ["Nancy A.", "Nancy A"]:
        new_actor = "Nancy Ace"
    if new_actor in [
        "Nathaly",
        "Nathalie Cherie",
        "Natalie Cherie",
        "Nathaly Cherie",
    ]:
        new_actor = "Nathaly Heaven"
    if new_actor == "Nika Noir":
        new_actor = "Nika Noire"
    if new_actor in ["Noe Milk", "Noemiek"]:
        new_actor = "Noemilk"
    if new_actor == "Rebel Lynn (Contract Star)":
        new_actor = "Rebel Lynn"
    if new_actor == "Remy La Croix":
        new_actor = "Remy Lacroix"
    if new_actor in ["Riley Jenson", "Riley Anne", "Rilee Jensen"]:
        new_actor = "Riley Jensen"
    if new_actor == "Sara Luv":
        new_actor = "Sara Luvv"
    if new_actor in ["Dylann Vox", "Dylan Vox"]:
        new_actor = "Skylar Vox"
    if new_actor in ["Sedona", "Stefanie Renee"]:
        new_actor = "Stephanie Renee"
    if new_actor in ["Stella Bankxxx", "Stella Ferrari"]:
        new_actor = "Stella Banxxx"
    if new_actor == "Steven St.Croix":
        new_actor = "Steven St. Croix"
    if new_actor in ["Sybil Kailena", "Sybil"]:
        new_actor = "Sybil A"
    if new_actor in [
        "Tiny Teen",
        "Tieny Mieny",
        "Lady Jay",
        "Tiny Teen / Eva Elfie",
    ]:
        new_actor = "Eva Elfie"
    if new_actor == "Veronica Vega":
        new_actor = "Veronica Valentine"

    return new_actor
