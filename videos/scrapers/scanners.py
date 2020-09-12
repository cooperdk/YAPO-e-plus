import os.path
import http.client
import http.client
import os
import os.path
import sys
from datetime import datetime

import django.db

http.client._MAXHEADERS = 1000
import re
from videos import aux_functions as aux
from utils import titleparser as tp
import videos.scrapers.freeones as scraper_freeones
import videos.scrapers.tmdb as scraper_tmdb
django.setup()
from configuration import Config, Constants
import logging
log = logging.getLogger(__name__)
from videos.models import Actor, Scene, ActorAlias, ActorTag, SceneTag, Website

def tpdb (scene_id: int, force: bool):
    title = ""
    site = ""
    found = 0

    current_scene = Scene.objects.get(pk=scene_id)
    scene_name = current_scene.name

    searched = False
    for scene_tag in current_scene.scene_tags.all():
        if any([scene_tag.name == "TpDB: Match: Good", scene_tag.name == "TpDB: Match: Questionable"]):
            searched = True
    if searched and not force:
        log.info(f"Scene #{current_scene.id} is already searched!")
        return

    log.info(f'Scanning for "{scene_name}" on TpDB...')

    try:
        parsetext = scene_name
        parsedict = tp.search(parsetext)
        if parsedict[3]:
            parsetext = parsedict[1] + " " + parsedict[2] + " " + parsedict[3]
        elif parsedict[1]:
            parsetext = parsedict[1] + " " + parsedict[2]
        else:
            parsetext = parsedict[2]

        log.info(f"Parser will search for: {parsetext}")
        # if current_scene.tpdb_id is not None and current_scene.tpdb_id != "" and len(current_scene.tpdb_id) > 12:
        #     parsetext = current_scene.tpdb_id
        url = 'https://api.metadataapi.net/scenes'

        params = {
            'parse': parsetext,
            #'q': parsetext,
            'limit': '1'
            # 'hash': 'rerum',
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'YAPO e+ 0.71',
        }
        response = aux.get_with_retry(url, headers=headers, params=params)
        response = response.json()

        if "id" and "title" in str(response):
            found = 1

        else:
            aux.remove_text_inside_brackets(scene_name, brackets="[]")
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
            log.info(f'Not successful scanning with conventional search, scanning with secondary parsetext: "{scene_name_formatted}"...')
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
                'User-Agent': 'YAPO e+ 0.71',
            }
            response = aux.get_with_retry(url, headers=headers, params=params)
            response = response.json()
            if "id" and "title" in str(response):
                found = 2

        if found == 1 or found == 2:
            description = None
            release_dateStr = None
            scenetags = []
            site_logo = ""

            log.info(f"A result was returned using method {found}. Parsing JSON...")

            if "title" in response['data'][0].keys():
                title = response['data'][0]['title']
            if "description" in response['data'][0].keys():
                description = response['data'][0]['description']
            if "site" in response['data'][0].keys():
                if "name" in response['data'][0]['site'].keys():
                    site = response['data'][0]['site']['name']
                    site_logo = response['data'][0]['site']['logo']
                if "tags" in response['data'][0].keys():
                    scenetags = response['data'][0]['tags']
            if "date" in response['data'][0].keys():
                release_dateStr = response['data'][0]['date']
            if "id" in response['data'][0].keys():
                tpdb_id = response['data'][0]['id']
            if description is not None:
                current_scene.description = description
            if release_dateStr is not None:
                try:
                    current_scene.release_date=datetime.strptime(release_dateStr, "%Y-%m-%d").date()
                except:
                    log.warning(f"Failed to parse release date {release_dateStr}")

            if tpdb_id is not None:
                current_scene.tpdb_id = tpdb_id
                current_scene.save()

            perflist = ""
            ite = 0

            for performer in response['data'][0]['performers']:
                perf = namecheck(performer['name'])
                perforiginal = performer['name']
                perpn = ""
                primary = 0
                secondary = 0
                ite += 1
                log.info(f"PERFORMER: {perf} - list: {perflist}")
                if not perf.lower().strip() in perflist.lower().strip():
                    if performer['parent'] is not None and performer['parent']['extras'] is not None:
                        performer_extras = performer['parent']['extras']
                        keyname = ""
                        actoradded = False
                        if performer_extras['gender'] is not None and "f" in performer_extras['gender'].lower():
                            log.info(f"TpDB PERFORMER -> Checking #{ite} ({perf})...")
                            actors = list(Actor.objects.extra(select={ "length": "Length(name)" }).order_by("-length"))
                            for scene_performer in actors:
                                keyname=""
                                primary=0
                                sp=scene_performer.name
                                if sp.lower() == perforiginal.lower():
                                    keyname = sp
                                    primary = 1
                                    log.info(f"SM 1: YAPO performer name {scene_performer.name} is keyname")
                                    break

                                if not keyname:
                                    sp = scene_performer.name
                                    perf=namecheck(perf)
                                    if sp.lower()==perf.lower():
                                        keyname = scene_performer.name
                                        primary = 1
                                        log.info(f"SM 1: YAPO performer name {sp} matches checked TpDB name")
                                        break


                            if not keyname:
                                akaroot = ActorAlias.objects.all()

                                if not keyname and 'aliases' in performer.keys():
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

                            if keyname.strip() != "":
                                log.info(f"CHECKING SCENE ACTORS")
                                keyname = namecheck(keyname)
                                if (keyname.lower() not in str(current_scene.actors.all()).lower()) and (Actor.objects.filter(name=keyname).exists()):
                                    log.info("  --> ACTOR MATCH")
                                    actor_to_add = Actor.objects.get(name=keyname)
                                    keyname = actor_to_add.name
                                    if not current_scene.actors.filter(name=keyname):
                                        aux.addactor(current_scene, actor_to_add)
                                        log.info(f"  --> ACTOR ADDED TO SCENE: {keyname}")
                                    else:
                                        log.info(f"  --> ACTOR already in scene.")

                            if not keyname:
                                perpn = performer['name']
                                perpn = namecheck(perpn)
                                secondary = 2
                                keyname = perpn
                                log.info(f"  --> SM 2: TpDB REPLACED {performer['name']} -> {keyname} is keyname")

                            if performer['parent']['name'] and not keyname:
                                perpn = performer['parent']['name']
                                perpn = namecheck(perpn)
                                keyname = perpn
                                secondary = 3
                                log.info(f"  --> SM 3: {keyname} is keyname")

                            if (Config().tpdb_actors) and (perpn) and (keyname) and (primary == 0):
                                # If an actor is found on TpDB, but doesn't exist in YAPO
                                log.info(f"Auto-adding a new actor: {perpn}")
                                if 'image' in performer.keys() and secondary == 2:
                                    log.info(f"Perf img check: {performer.keys()}")
                                    img = performer['image']
                                elif 'image' in performer['parent'].keys() and secondary == 3:
                                    log.info(f"Perf img check: {performer['parent'].keys()}")
                                    img = performer['parent']['image']
                                act = Actor()
                                act.name = perpn
                                act.date_added = datetime.now()
                                act.thumbnail = Constants().unknown_person_image_path
                                act.save()
                                actoradded = True
                                aux.addactor(current_scene, act)
                                if act.thumbnail == Constants().unknown_person_image_path:
                                    save_path = os.path.join(Config().site_media_path, 'actor', str(act.id), 'profile')
                                    save_file_name = os.path.join(save_path, 'profile.jpg')
                                    if img and not os.path.isfile(save_file_name):
                                        if not os.path.exists(save_path):
                                            os.makedirs(save_path)
                                        aux.download_image(img, save_file_name)
                                        as_uri = aux.pathname2url(save_file_name)
                                        act.thumbnail = as_uri
                                        act.save()

                                log.info(f"  --> ACTOR CREATED AND ADDED TO SCENE: {act.name}")
                            elif Config().tpdb_actors == False:
                                log.info(f"We could add the actor {act.name}, but auto-adding is disabled")

                            if actoradded and perpn:
                                log.info(f"Scraping additional info about {act.name}...")
                                scraper_tmdb.search_person_with_force_flag(act, True)
                                scraper_freeones.search_freeones_with_force_flag(act, True)

                        if (keyname.strip() != "") and (Actor.objects.filter(name=keyname).exists()):
                            actor = Actor.objects.get(name=keyname)
                            if len(perflist) > 3 and not actor.name.lower() in perflist.lower():
                                perflist = perflist + ", " + actor.name
                            elif len(perflist) < 3:
                                perflist = actor.name
                            added = False

                            if actor.date_of_birth == None or actor.date_of_birth == "" or actor.date_of_birth == "1970-01-01":
                                if "birthday" in performer_extras.keys():
                                    dob = performer_extras["birthday"]
                                    if dob is not None:
                                        actor.date_of_birth = performer_extras["birthday"]
                                        added = True

                            if "fakeboobs" in performer_extras.keys():
                                faketits = performer_extras['fakeboobs']

                                if faketits is not None:
                                    if faketits == True:
                                        if not "tits" in str(actor.actor_tags.all().lower()):
                                            actor.actor_tags.add("Fake tits")
                                            added = True
                                    elif faketits == False:
                                        if not "tits" in str(actor.actor_tags.all().lower()):
                                            actor.actor_tags.add("Natural tits")
                                            added = True

                            if not actor.ethnicity or actor.ethnicity == "":
                                if "ethnicity" in performer_extras.keys():
                                    ethnicity = performer_extras['ethnicity']
                                    if ethnicity is not None:
                                        if actor.ethnicity == None or actor.ethnicity == "":
                                            actor.ethnicity = ethnicity
                                            added = True

                            if not actor.country_of_origin or actor.country_of_origin == "":
                                if "birthplace" in performer_extras.keys():
                                    birthplace = performer_extras['birthplace']
                                    if birthplace is not None:
                                        if "united states" in birthplace.lower():
                                            birthplace = "United States"
                                        if actor.country_of_origin == None or actor.country_of_origin == "":
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
                                            added = True

                            if performer["parent"]["bio"] is not None and len(performer["parent"]["bio"]) > 72:
                                actor.description = performer["parent"]["bio"]
                                added = True

                            if not actor.gender:
                                actor.gender = "F"
                                added = True

                            if added == True:
                                insert_actor_tag(actor, "TpDB: Info added")
                                actor.last_lookup = datetime.now()
                            actor.save()

                            if added:
                                log.info(f"Some information about {actor.name} was added to the profile.")

            if found:
                try:
                    website = Website.objects.get(name=site)
                except:
                    website = "none"
                if not current_scene.websites.filter(name=site):
                    if website != "none":
                        log.info(f"Adding website: {website.name} to the scene {current_scene.name}")
                        current_scene.websites.add(website)
                    else:
                        log.warning(f"This website couldn't be found: {site}")
                else:
                    log.info("Website already registered to scene.")
                if Config().tpdb_website_logos:
                    aux.save_website_logo(site_logo, site, False, current_scene.id)

            newtitle = ""
            if title:
                newtitle = title

            if (perflist and len(perflist) > 4) and newtitle and not perflist.lower().strip() == newtitle.lower().strip():
                newtitle = f"{perflist} - {newtitle}"
            elif perflist.lower() and not newtitle:
                newtitle = f"{perflist}"
            elif newtitle and not perflist.lower():
                newtitle = f"{newtitle}"

            if site:
                newtitle = f"{site} - {newtitle}"

            if "true" in Config().tpdb_autorename.lower():
                if not current_scene.orig_name:
                    current_scene.orig_name = current_scene.name
                current_scene.name = newtitle
                log.info(f'Scene name is now \"{newtitle}\".')
            else:
                log.info(f'Renaming is disabled, but we suggest: \"{newtitle}\".')

            current_scene.save()
            success = True

            if found:
                tagcounter = 0
                maxtags = int(Config().tpdb_tags)
                if maxtags > 0:
                    log.info(f'Inserting tags: ')
                    for tag in scenetags:
                        if tagcounter < maxtags:
                            tagcounter += 1
                            log.info(f'[ {tag["tag"].capitalize()} ]')
                            insert_scene_tag(current_scene, tag["tag"].capitalize())
                        else:
                            break
                    log.info(f"Added {tagcounter} tags from TpDB to this scene.")

            tg = SceneTag.objects.get(name="TpDB: Match: Good")
            tq = SceneTag.objects.get(name="TpDB: Match: Questionable")
            tn = SceneTag.objects.get(name="TpDB: Match: None")
            current_scene.scene_tags.remove(tg)
            current_scene.scene_tags.remove(tq)
            current_scene.scene_tags.remove(tn)
            current_scene.save()

            if found == 1:
                insert_scene_tag(current_scene, "TpDB: Match: Good")
            elif found == 2:
                insert_scene_tag(current_scene, "TpDB: Match: Questionable")
            elif success == False:
                insert_scene_tag(current_scene, "TpDB: Match: None")

            insert_scene_tag(current_scene, "TpDB: Scanned")

            log.info(f"Found and registered data for scene ID {scene_id}")

            return success
        else:
            log.info(f"Scene not found in TpDB")

    except KeyError:
        log.warning(f"Issue(s) occured: {sys.exc_info()}")
        return False

def insert_scene_tag(current_scene, tagname):
    if not SceneTag.objects.filter(name=tagname):
        SceneTag.objects.create(name=tagname)

    scene_tag_to_add = SceneTag.objects.get(name=tagname)
    current_scene.scene_tags.add(scene_tag_to_add)

def insert_actor_tag(actor_to_insert, actor_tag_name):
    actor_tag_name = aux.strip_bad_chars(actor_tag_name)

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

    newActor = actor.strip()

    if newActor == "Abby Lee":
        newActor = "Abby Lee Brazil"
    if newActor == "Abby Rains":
        newActor = "Abbey Rain"
    if newActor == "Ms Addie Juniper":
        newActor = "Addie Juniper"
    if newActor == "Adrianna Chechik" or newActor == "Adriana Chechick":
        newActor = "Adriana Chechik"
    if newActor == "Alex D":
        newActor = "Alex D."
    if newActor == "Alura Tnt Jenson" or newActor == "Alura 'Tnt' Jenson":
        newActor = "Alura Jenson"
    if newActor == "Amia Moretti":
        newActor = "Amia Miley"
    if newActor == "Amy Reid":
        newActor = "Amy Ried"
    if newActor == "Ana Fox" or newActor == "Ana Foxx":
        newActor = "Ana Foxxx"
    if newActor == "Andreina De Lux" or newActor == "Andreina De Luxe" or newActor == "Andreina Dlux":
        newActor = "Andreina Deluxe"
    if newActor == "Angela Piaf" or newActor == "Angel Piaf":
        newActor = "Angel Piaff"
    if newActor == "Ani Black Fox" or newActor == "Ani Black":
        newActor = "Ani Blackfox"
    if newActor == "Anikka Albrite":
        newActor = "Annika Albrite"
    if newActor == "Anita Bellini":
        newActor = "Anita Bellini Berlusconi"
    if newActor == "Anjelica" or newActor == "Ebbi" or newActor == "Abby H" or newActor == "Katherine A":
        newActor = "Krystal Boyd"
    if newActor == "Anna Morna":
        newActor = "Anastasia Morna"
    if newActor == "April ONeil" or newActor == "April Oneil" or newActor == "April O'neil":
        newActor = "April O'Neil"
    if newActor == "Ashley Graham":
        newActor = "Ashlee Graham"
    if newActor == "Bella Danger":
        newActor = "Abella Danger"
    if newActor == "Bibi Jones" or newActor == "Bibi Jones™":
        newActor = "Britney Beth"
    if newActor == "Bridgette B.":
        newActor = "Bridgette B"
    if newActor == "Capri Cavalli":
        newActor = "Capri Cavanni"
    if newActor == "Ce Ce Capella":
        newActor = "CeCe Capella"
    if newActor == "Charli Red":
        newActor = "Charlie Red"
    if newActor == "Charlotte Lee":
        newActor = "Jaye Summers"
    if newActor == "Chloe Cherry":
        newActor = "Chloe Couture"
    if newActor == "Criss Strokes":
        newActor = "Chris Strokes"
    if newActor == "Christy Charming":
        newActor = "Paula Shy"
    if newActor == "CléA Gaultier":
        newActor = "Clea Gaultier"
    if newActor == "Crissy Kay" or newActor == "Emma Hicks" or newActor == "Emma Hixx":
        newActor = "Emma Hix"
    if newActor == "Crystal Rae":
        newActor = "Cyrstal Rae"
    if newActor == "Doris Ivy":
        newActor = "Gina Gerson"
    if newActor == "Eden Sin":
        newActor = "Eden Sinclair"
    if newActor == "Elsa Dream":
        newActor = "Elsa Jean"
    if newActor == "Eve Lawrence":
        newActor = "Eve Laurence"
    if newActor == "Francesca Di Caprio" or newActor == "Francesca Dicaprio":
        newActor = "Francesca DiCaprio"
    if newActor == "Guiliana Alexis":
        newActor = "Gulliana Alexis"
    if newActor == "Grace Hartley":
        newActor = "Pinky June"
    if newActor == "Hailey Reed":
        newActor = "Haley Reed"
    if newActor == "Josephina Jackson":
        newActor = "Josephine Jackson"
    if newActor == "Jane Doux":
        newActor = "Pristine Edge"
    if newActor == "Jade Indica":
        newActor = "Miss Jade Indica"
    if newActor == "Jassie Gold" or newActor == "Jaggie Gold":
        newActor = "Jessi Gold"
    if newActor == "Jenna J Ross" or newActor == "Jenna J. Ross":
        newActor = "Jenna Ross"
    if newActor == "Jenny Ferri":
        newActor = "Jenny Fer"
    if newActor == "Jessica Blue" or newActor == "Jessica Cute":
        newActor = "Jessica Foxx"
    if newActor == "Jo Jo Kiss":
        newActor = "Jojo Kiss"
    if newActor == "Josephine" or newActor == "Conny" or newActor == "Conny Carter" or newActor == "Connie":
        newActor = "Connie Carter"
    if newActor == "Kagney Lynn Karter":
        newActor = "Kagney Linn Karter"
    if newActor == "Kari Sweets":
        newActor = "Kari Sweet"
    if newActor == "Katarina":
        newActor = "Katerina Hartlova"
    if newActor == "Kendra May Lust":
        newActor = "Kendra Lust"
    if newActor == "Khloe Capri" or newActor == "Chloe Capri":
        newActor = "Khloe Kapri"
    if newActor == "Lara Craft":
        newActor = "Lora Craft"
    if newActor == "Lilly LaBeau" or newActor == "Lilly Labuea" or newActor == "Lily La Beau" or \
            newActor == "Lily Lebeau" or newActor == "Lily Luvs":
        newActor = "Lily Labeau"
    if newActor == "Lilly Lit":
        newActor = "Lilly Ford"
    if newActor == "Maddy OReilly" or newActor == "Maddy Oreilly" or newActor == "Maddy O'reilly":
        newActor = "Maddy O'Reilly"
    if newActor == "Maria Rya" or newActor == "Melena Maria":
        newActor = "Melena Maria Rya"
    if newActor == "Moe The Monster Johnson":
        newActor = "Moe Johnson"
    if newActor == "Nadya Nabakova" or newActor == "Nadya Nabokova":
        newActor = "Bunny Colby"
    if newActor == "Nancy A." or newActor == "Nancy A":
        newActor = "Nancy Ace"
    if newActor == "Nathaly" or newActor == "Nathalie Cherie" or newActor == "Natalie Cherie" or newActor == "Nathaly Cherie":
        newActor = "Nathaly Heaven"
    if newActor == "Nika Noir":
        newActor = "Nika Noire"
    if newActor == "Noe Milk" or newActor == "Noemiek":
        newActor = "Noemilk"
    if newActor == "Rebel Lynn (Contract Star)":
        newActor = "Rebel Lynn"
    if newActor == "Remy La Croix":
        newActor = "Remy Lacroix"
    if newActor == "Riley Jenson" or newActor == "Riley Anne" or newActor == "Rilee Jensen":
        newActor = "Riley Jensen"
    if newActor == "Sara Luv":
        newActor = "Sara Luvv"
    if newActor == "Dylann Vox" or newActor == "Dylan Vox":
        newActor = "Skylar Vox"
    if newActor == "Sedona" or newActor == "Stefanie Renee":
        newActor = "Stephanie Renee"
    if newActor == "Stella Bankxxx" or newActor == "Stella Ferrari":
        newActor = "Stella Banxxx"
    if newActor == "Steven St.Croix":
        newActor = "Steven St. Croix"
    if newActor == "Sybil Kailena" or newActor == "Sybil":
        newActor = "Sybil A"
    if newActor == "Tiny Teen" or newActor == "Tieny Mieny" or newActor == "Lady Jay" \
            or newActor == "Tiny Teen / Eva Elfie":
        newActor = "Eva Elfie"
    if newActor == "Veronica Vega":
        newActor = "Veronica Valentine"

    return newActor
