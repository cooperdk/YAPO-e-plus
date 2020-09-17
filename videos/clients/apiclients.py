import django
import http.client
import os
import os.path
import re
import sys
# import pprint
import urllib
import urllib.request
from datetime import datetime

# import json
from django.db import transaction
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
    # scene_name = scene_name.replace(" ", "%20")

    searched = False
    for scene_tag in this_scene.scene_tags.all():
        if any([scene_tag.name == "TpDB: Match: Good", scene_tag.name == "TpDB: Match: Questionable"]):
            searched = True
    if searched and not force:
        log.sinfo(f"Scene #{this_scene.id} is already searched!")
        return # Scene is searched already, exit

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

        log.sinfo(f"Parser will search for: {parsetext}")
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
        print("Scanning... ", end="")
        response = requests.request('GET', url, headers=headers, params=params)

        try:
            response = response.json()
        except requests.exceptions.RequestException as e:
            pass

        # print (str(response))
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(response)

        if "id" and "title" in str(response):
            found = 1

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
            log.sinfo(f'Not successful scanning with conventional search,\n \
                      Now scanning with secondary parsetext: "{scene_name_formatted}"...')
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
            response = requests.request('GET', url, headers=headers, params=params)
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

            newtitle = ""
            if title:
                newtitle = title
                # print(newtitle)

            # if any([release_date, perflist, site]):
            #    newtitle = f"{newtitle} - "
            #    print (newtitle)

            if (perflist and len(perflist) > 4) and newtitle and \
                    perflist.lower().strip() != newtitle.lower().strip():
                newtitle = f"{perflist} - {newtitle}"
            elif perflist.lower() and not newtitle:
                newtitle = f"{perflist}"
            elif newtitle and not perflist.lower():
                newtitle = f"{newtitle}"

            if release_date:
                newtitle = f"{release_date} - {newtitle}"
                # print(newtitle)

            if site:
                newtitle = f"{site} - {newtitle}"
                # print(newtitle)

            # print(Config().tpdb_autorename.lower())
            if "true" in Config().tpdb_autorename.lower():
                if not this_scene.orig_name:
                    this_scene.orig_name = this_scene.name
                this_scene.name = newtitle
                log.sinfo(f'Scene name is now \"{newtitle}\".')
            else:
                print('Renaming is disabled, but we suggest: \"{newtitle}\".')

            success = True
            # print(f"Description:\n{description}")

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
                        log.sinfo(f"Added {tagcounter} tags from TpDB to this scene.")
            except:
                pass

            try:
                tg = SceneTag.objects.get(name="TpDB: Match: Good")
                tq = SceneTag.objects.get(name="TpDB: Match: Questionable")
                tn = SceneTag.objects.get(name="TpDB: Match: None")
                this_scene.scene_tags.remove(tg)
                this_scene.scene_tags.remove(tq)
                this_scene.scene_tags.remove(tn)
                # tpdbtag.  this_scene.scene_tags.remove(tpdbtag.id)
            except:
                pass
            if found == 1:
                insert_scene_tag(this_scene, "TpDB: Match: Good")
            elif found == 2:
                insert_scene_tag(this_scene, "TpDB: Match: Questionable")
            elif not success:
                insert_scene_tag(this_scene, "TpDB: Match: None")

            insert_scene_tag(this_scene, "TpDB: Scanned")
            # print("Tagged the scene with a TpDB tag.")

            log.sinfo(f"Found and registered data for scene ID {scene_id}")
            print(this_scene)
            this_scene.save(force_update=True)

        else:
            log.sinfo("Scene not found in TpDB")
            this_scene.save(force_update=True)

        return success

    except KeyError:
        success = False
        log.warn(f"Issue(s) occured: {sys.exc_info()}")
        return success
        # pass


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
    if new_actor == "Adrianna Chechik" or new_actor == "Adriana Chechick":
        new_actor = "Adriana Chechik"
    if new_actor == "Alex D":
        new_actor = "Alex D."
    if new_actor == "Alura Tnt Jenson" or new_actor == "Alura 'Tnt' Jenson":
        new_actor = "Alura Jenson"
    if new_actor == "Amia Moretti":
        new_actor = "Amia Miley"
    if new_actor == "Amy Reid":
        new_actor = "Amy Ried"
    if new_actor == "Ana Fox" or new_actor == "Ana Foxx":
        new_actor = "Ana Foxxx"
    if new_actor == "Andreina De Lux" or new_actor == "Andreina De Luxe" or new_actor == "Andreina Dlux":
        new_actor = "Andreina Deluxe"
    if new_actor == "Angela Piaf" or new_actor == "Angel Piaf":
        new_actor = "Angel Piaff"
    if new_actor == "Ani Black Fox" or new_actor == "Ani Black":
        new_actor = "Ani Blackfox"
    if new_actor == "Anikka Albrite":
        new_actor = "Annika Albrite"
    if new_actor == "Anita Bellini":
        new_actor = "Anita Bellini Berlusconi"
    if new_actor == "Anjelica" or new_actor == "Ebbi" or new_actor == "Abby H" or new_actor == "Katherine A":
        new_actor = "Krystal Boyd"
    if new_actor == "Anna Morna":
        new_actor = "Anastasia Morna"
    if new_actor == "April ONeil" or new_actor == "April Oneil" or new_actor == "April O'neil":
        new_actor = "April O'Neil"
    if new_actor == "Ashley Graham":
        new_actor = "Ashlee Graham"
    if new_actor == "Bella Danger":
        new_actor = "Abella Danger"
    if new_actor == "Bibi Jones" or new_actor == "Bibi Jones™":
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
    if new_actor == "Crissy Kay" or new_actor == "Emma Hicks" or new_actor == "Emma Hixx":
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
    if new_actor == "Francesca Di Caprio" or new_actor == "Francesca Dicaprio":
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
    if new_actor == "Jassie Gold" or new_actor == "Jaggie Gold":
        new_actor = "Jessi Gold"
    if new_actor == "Jenna J Ross" or new_actor == "Jenna J. Ross":
        new_actor = "Jenna Ross"
    if new_actor == "Jenny Ferri":
        new_actor = "Jenny Fer"
    if new_actor == "Jessica Blue" or new_actor == "Jessica Cute":
        new_actor = "Jessica Foxx"
    if new_actor == "Jo Jo Kiss":
        new_actor = "Jojo Kiss"
    if new_actor == "Josephine" or new_actor == "Conny" or new_actor == "Conny Carter" or new_actor == "Connie":
        new_actor = "Connie Carter"
    if new_actor == "Kagney Lynn Karter":
        new_actor = "Kagney Linn Karter"
    if new_actor == "Kari Sweets":
        new_actor = "Kari Sweet"
    if new_actor == "Katarina":
        new_actor = "Katerina Hartlova"
    if new_actor == "Kendra May Lust":
        new_actor = "Kendra Lust"
    if new_actor == "Khloe Capri" or new_actor == "Chloe Capri":
        new_actor = "Khloe Kapri"
    if new_actor == "Lara Craft":
        new_actor = "Lora Craft"
    if new_actor == "Lilly LaBeau" or new_actor == "Lilly Labuea" or new_actor == "Lily La Beau" or \
            new_actor == "Lily Lebeau" or new_actor == "Lily Luvs":
        new_actor = "Lily Labeau"
    if new_actor == "Lilly Lit":
        new_actor = "Lilly Ford"
    if new_actor == "Maddy OReilly" or new_actor == "Maddy Oreilly" or new_actor == "Maddy O'reilly":
        new_actor = "Maddy O'Reilly"
    if new_actor == "Maria Rya" or new_actor == "Melena Maria":
        new_actor = "Melena Maria Rya"
    if new_actor == "Moe The Monster Johnson":
        new_actor = "Moe Johnson"
    if new_actor == "Nadya Nabakova" or new_actor == "Nadya Nabokova":
        new_actor = "Bunny Colby"
    if new_actor == "Nancy A." or new_actor == "Nancy A":
        new_actor = "Nancy Ace"
    if new_actor == "Nathaly" or new_actor == "Nathalie Cherie" or new_actor == "Natalie Cherie" \
            or new_actor == "Nathaly Cherie":
        new_actor = "Nathaly Heaven"
    if new_actor == "Nika Noir":
        new_actor = "Nika Noire"
    if new_actor == "Noe Milk" or new_actor == "Noemiek":
        new_actor = "Noemilk"
    if new_actor == "Rebel Lynn (Contract Star)":
        new_actor = "Rebel Lynn"
    if new_actor == "Remy La Croix":
        new_actor = "Remy Lacroix"
    if new_actor == "Riley Jenson" or new_actor == "Riley Anne" or new_actor == "Rilee Jensen":
        new_actor = "Riley Jensen"
    if new_actor == "Sara Luv":
        new_actor = "Sara Luvv"
    if new_actor == "Dylann Vox" or new_actor == "Dylan Vox":
        new_actor = "Skylar Vox"
    if new_actor == "Sedona" or new_actor == "Stefanie Renee":
        new_actor = "Stephanie Renee"
    if new_actor == "Stella Bankxxx" or new_actor == "Stella Ferrari":
        new_actor = "Stella Banxxx"
    if new_actor == "Steven St.Croix":
        new_actor = "Steven St. Croix"
    if new_actor == "Sybil Kailena" or new_actor == "Sybil":
        new_actor = "Sybil A"
    if new_actor == "Tiny Teen" or new_actor == "Tieny Mieny" or new_actor == "Lady Jay" \
            or new_actor == "Tiny Teen / Eva Elfie":
        new_actor = "Eva Elfie"
    if new_actor == "Veronica Vega":
        new_actor = "Veronica Valentine"

    return new_actor
