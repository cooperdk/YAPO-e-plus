import os
import os.path
import subprocess
import _thread
import requests
import json
import django.db
from datetime import datetime
import pprint
import urllib
import re
from videos import aux_functions as aux
from utils import titleparser as tp
django.setup()
from configuration import Config
#import urllib.request
from utils.printing import Logger
log = Logger()
#import pycurl, certifi
#from io import BytesIO
#import utils.titleparser as tp
from videos.models import Actor, Scene, ActorAlias, ActorTag, SceneTag


def tpdb (scene_id: int, force: bool):
    title = ""
    site = ""
    date = ""
    perflist = ""
    success = False
    found = 0

    current_scene = Scene.objects.get(pk=scene_id)
    scene_name = current_scene.name
    print(f'Scanning for "{scene_name}" on TpDB...')
    # scene_name = scene_name.replace(" ", "%20")

    TpDB: Scanned
    if "tpdb: scanned" in str(current_scene.scene_tags.all()).lower():
        print ("WARNING: Already searched.\n")


    try:
        parsetext = scene_name
        parsedict = tp.search(parsetext)
        if parsedict[3]:
            parsetext = parsedict[1] + " " + parsedict[2] + " " + parsedict[3]
        elif parsedict[1]:
            parsetext = parsedict[1] + " " + parsedict[2]
        else:
            parsetext = parsedict[2]

        print(f"Parse: {parsetext}")
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
            site_logo = ""
            if "title" in response['data'][0].keys():
                title = response['data'][0]['title']
                print(f"Title is {title}")
            if "description" in response['data'][0].keys():
                description = response['data'][0]['description']
            if "site" in response['data'][0].keys():
                if "name" in response['data'][0]['site'].keys():
                    site = response['data'][0]['site']['name']
                    site_logo = response['data'][0]['site']['logo']
            if "date" in response['data'][0].keys():
                release_date = response['data'][0]['date']
            if "id" in response['data'][0].keys():
                tpdb_id = response['data'][0]['id']
            if description is not None: current_scene.description = description
            if release_date is not None:
                #print(release_date)
                try:
                    release_date=datetime.strptime(release_date, "%Y-%m-%d").date()
                #release_date = strftime(release_date) + " 00:00:00"
                #release_date = datetime.strptime(release_date, "%Y-%m-%d %H:%M:%S")
                    print(release_date)
                except:
                    release_date = None
                if release_date is not None:
                    current_scene.release_date = release_date


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
                print(f"----> PERFORMER: {performer['name'].lower().strip()} - perflist: {perflist.lower().strip()}")
                if not performer['name'].lower().strip() in perflist.lower().strip():
                    if performer['parent'] is not None and performer['parent']['extras'] is not None:
                        performer_extras = performer['parent']['extras']
                        # print(performer_extras['gender'])
                        keyname = ""
                        sp = ""
                        if performer_extras['gender'] is not None and "f" in performer_extras['gender'].lower():
                            print(f"  --> TpDB PERFORMER -> Checking #{{ite}} ({performer['name'].strip()})...")
                            actors = list(Actor.objects.extra(select={ "length": "Length(name)" }).order_by("-length"))
                            sp = ""
                            for scene_performer in actors:

                                keyname=""
                                primary=0
                                sp=scene_performer.name.lower().strip()
                                perf=performer['name'].lower().strip()
                                if sp == perf:
                                    keyname = scene_performer.name
                                    primary = 1
                                    print(f"  --> SM 1: YAPO performer name {scene_performer.name} is keyname")
                                    break


                                #print (f"SC PERF: {sp} - JSON PERF: {perf} - JSON AKA: {alia} - JSON PERF2: {perpn}")


                                #elif "aliases" in performer.keys() and scene_performer.name.lower().strip() in str(performer['aliases'].lower()):
                                    #print(f"{performer['name']} is an alias to an actor already registered to this scene.")
                                #else:
                            if not keyname:

                                akaroot = Actor.objects.all()


                                if 'aliases' in performer.keys():
                                    alia = str(performer['aliases']).lower().strip()

                                    for alias in akaroot:
                                        akanames = [sub.name for sub in alias.actor_aliases.all()]
                                        #print(f"GETTING {alias.name} -> {akanames}")

                                        #print(f"Testing alias: {alias.name} ... \r",end="")
                                        if (alias.name.lower() in perf) or (alias.name.lower() in performer['parent']['name']) or (alias.name.lower() in alia):
                                            keyname = alias.name
                                            primary = 3
                                            print(f"  --> SM 3: YAPO performer {keyname} is keyname (by alias)")
                                elif 'aliases' in performer['parent'].keys():
                                    alia = str(performer['parent']['aliases']).lower().strip()

                                    for alias in akaroot:
                                        akanames = [sub.name for sub in alias.actor_aliases.all()]
                                        #print(f"GETTING {alias.name} -> {akanames}")

                                        #print(f"Testing alias: {alias.name} ... \r",end="")
                                        if (alias.name.lower() in perf) or (alias.name.lower() in performer['parent']['name']) or (alias.name.lower() in alia):
                                            keyname = alias.name
                                            primary = 4
                                            print(f"  --> SM 4: YAPO performer {keyname} is keyname (by alias)")
                                else:
                                    alia = ""


                            if keyname:
                                #actor_to_add = Actor.objects.get(pk=actor_id)
                                print(f"----> CHECKING SCENE ACTORS")
                                if (keyname not in str(current_scene.actors.all()).lower()) and (Actor.objects.filter(name=performer['name']).exists()):
                                    print("  --> ACTOR MATCH")
                                    actor_to_add = Actor.objects.get(name=performer['name'])
                                    keyname = actor_to_add.name
                                    if not current_scene.actors.filter(name=keyname):
                                        aux.addactor(current_scene, actor_to_add)
                                        print(f"  --> ACTOR ADDED TO SCENE: {keyname}")
                                    else:
                                        print(f"  --> ACTOR already in scene.")


                        if performer['parent']['name'] and not keyname:
                            perpn = performer['parent']['name'].lower().strip()
                            if sp == perpn and not keyname:
                                keyname = performer['parent']['name']
                                secondary = 2
                                print(f"  --> SM 2: {keyname} is keyname")
                                break

                            if not keyname:
                                perpn2 = namecheck(perpn)
                                secondary = 3
                                if sp == perpn2.lower().strip():
                                    keyname = perpn2.strip()
                                    print(f"  --> SM 3: TpDB REPLACED {performer['parent']['name']} -> {keyname} is keyname")
                                    break

                        # TODO: Code to add actor to scene


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
                                        if not "tits" in str(actor.actor_tags.all().lower()):
                                            actor.actor_tags.add("Fake tits")
                                            print("Added tag: Fake tits")
                                            added = True
                                    elif faketits == False:
                                        print("No...")
                                        if not "tits" in str(actor.actor_tags.all().lower()):
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
                                    if birthplace is not None:
                                        if "united states" in birthplace.lower():
                                            birthplace = "United States"
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
                                    #print(f"Hair color: {hair}")
                                    if hair is not None:
                                        tags = str(actor.actor_tags.all())
                                        if not actor.actor_tags.filter(name__contains=" hair"):
                                            #if actor.actor_tags.filter(name__contains=" hair"):
                                            #    remtag = actor.actor_tags.filter(name__contains=" hair").values('id')[0]['id']
                                            #    print(f"TO REMOVE --> {remtag}")
                                            #    actor.actor_tags.remove(remtag)
                                            insert_actor_tag(actor, hair + " hair")
                                            print(f"Added tag: {hair} hair")
                                            added = True


                            if performer["parent"]["bio"] is not None and len(performer["parent"]["bio"]) > 72:
                                actor.description = performer["parent"]["bio"]
                                added = True
                                # actor.save()

                            if not actor.gender:
                                actor.gender = "F"
                                added = True

                            if added == True:
                                insert_actor_tag(actor, "TpDB: Tagged")
                                actor.last_lookup = datetime.now()
                            actor.save()
            newtitle = ""
            if title:
                newtitle = title
                #print(newtitle)

           # if any([release_date, perflist, site]):
            #    newtitle = f"{newtitle} - "
            #    print (newtitle)

            if (perflist and len(perflist) > 4) and newtitle and not perflist.lower().strip() == newtitle.lower().strip():
                newtitle = f"{perflist} - {newtitle}"
            elif perflist.lower() and not newtitle:
                newtitle = f"{perflist}"
            elif newtitle and not perflist.lower():
                newtitle = f"{newtitle}"

            if release_date:
                newtitle = f"{release_date} - {newtitle}"
                #print(newtitle)

            if site:
                newtitle = f"{site} - {newtitle}"
                #print(newtitle)

            #print(Config().tpdb_autorename.lower())
            if "true" in Config().tpdb_autorename.lower():
                if not current_scene.orig_name:
                    current_scene.orig_name = current_scene.name
                current_scene.name = newtitle
                print(f"Scene name changed: {newtitle}")
            else:
                print('"Renaming is disabled, but we suggest "{newtitle}".')

            current_scene.save()
            success = True
            # print(f"Description:\n{description}")

            log.info(f"Found and registered data for scene ID {scene_id}")

    except KeyError:
        success = False
        print(f"Issue(s) occured:\n{sys.exc_info()}")
        #pass
    try:
        tg=SceneTag.objects.get(name="TpDB: Match: Good")
        tq=SceneTag.objects.get(name="TpDB: Match: Questionable")
        tn=SceneTag.objects.get(name="TpDB: Match: None")
        current_scene.scene_tags.remove(tg)
        current_scene.scene_tags.remove(tq)
        current_scene.scene_tags.remove(tn)
        current_scene.save()
            #tpdbtag.  current_scene.scene_tags.remove(tpdbtag.id)
    except:
        pass
    if found == 1:
            insert_scene_tag(current_scene, "TpDB: Match: Good")
    elif found == 2:
        insert_scene_tag(current_scene, "TpDB: Match: Questionable")
    elif success == False:
        insert_scene_tag(current_scene, "TpDB: Match: None")

    insert_scene_tag(current_scene, "TpDB: Scanned")
    print("Tagged the scene with a TpDB tag.")

    # TODO: Website logo downloader

    if found:
        if Config().tpdb_website_logos:
            aux.save_website_logo(site_logo, site, False, current_scene)

    return success


def strip_bad_chars(name):
    bad_chars = {" "}
    for char in bad_chars:
        if char in name:
            #print("Before: " + name)
            name = name.replace(char, "")
            #print("Adding Data: " + name)
    return name

def insert_scene_tag(current_scene, tagname):
    if not SceneTag.objects.filter(name=tagname):
        SceneTag.objects.create(name=tagname)

    scene_tag_to_add = SceneTag.objects.get(name=tagname)
    current_scene.scene_tags.add(scene_tag_to_add)

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
    if newActor == "Nathaly" or newActor == "Nathalie Cherie" or newActor == "Natalie Cherie":
        newActor = "Nathaly Cherie"
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
