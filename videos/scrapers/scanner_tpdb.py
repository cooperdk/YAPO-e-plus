import datetime
import os
import re
import sys
from typing import Optional, Dict

import urllib3
from rest_framework.response import Response

import logging

from configuration import Config

log = logging.getLogger(__name__)

from rest_framework import status

from utils import Constants, titleparser
from videos.models import Scene, Actor, ActorAlias, Website, SceneTag
from videos.scrapers.scanner_common import scanner_common

class tpdb_actor_response:
    data = None # type: Optional[str]
    bio = None
    image = None
    pid = None

    def __init__(self):
        pass

    @staticmethod
    def parse(actorname, html):
        responseJson = html.json()

        responseData = responseJson.get('data', '')
        if responseData is None or len(str(responseData)) < 16:
            return None

        # We will get back results for a few different actors, so pull out only the one we're queried for.
        # TODO: deal with pagination
        responseData = [x for x in responseData if x['name'] == actorname]
        if len(responseData) == 0:
            return None
        if len(responseData) != 1:
            raise Exception("tpdb response did not include exactly one 'data' entry for actor '%s' (included: '%s')" % (actorname, ",".join(map(lambda x: x.name, responseData))))

        # Merge in keys we're interested in
        rawResponseData = responseData[0]
        cleanResponseData = {}
        for k in ('id', 'bio', 'image', 'thumbnail'):
            cleanResponseData[k] = rawResponseData.get(k, None)
        # Coalesce 'image' and 'thumbnail' values to a single 'image'
        if cleanResponseData['image'] is None:
            cleanResponseData['image'] = cleanResponseData['thumbnail']

        toRet = tpdb_actor_response()
        for k in [x for x in cleanResponseData if x is not None]:
            # fix up 'id' to 'pid'.
            if k == 'id':
                setattr(toRet, 'pid', cleanResponseData[k])
            setattr(toRet, k, cleanResponseData[k])

        return toRet

class scanner_tpdb(scanner_common):

    def tpdb_scan_actor(self, actor, force: bool):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        import videos.aux_functions as aux
        if not aux.is_domain_reachable("api.metadataapi.net"):
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


        log.info(f'Contacting TpDB API for info about {actor.name}.')

        url = 'https://api.metadataapi.net/performers'
        params = { 'q': actor.name }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'YAPO e+ 0.71',
        }

        response = self.web.get_with_retry(url, headers, params)

        success = False
        photo = ""

        parsedResponse = tpdb_actor_response.parse(actor.name, response)
        if parsedResponse is None:
            log.info(f'It seems that TpDB might not know anything about {actor.name}!')
            return False

        # Download the thumbnail if neccessary
        if actor.thumbnail == Constants().unknown_person_image_path or force:
            save_file_name = actor.generateThumbnailPath()
            if parsedResponse.image is not None and ((not os.path.isfile(save_file_name) or force)):
                maxretries = 3
                attempt = 0
                #while attempt < maxretries:
                    #try:
                if self.web.download_image(parsedResponse.image, save_file_name):
                    rel_path = os.path.relpath(save_file_name, start="videos")
                    as_uri = self.web.pathname2url(rel_path)
                    actor.thumbnail = as_uri
                    photo += " [ Photo ]"
                    success = True
                else:
                    log.error(f"DOWNLOAD ERROR: Photo ({actor.name}): {parsedResponse.image}")

        if any([force, not actor.description, len(actor.description) < 128, "freeones" in actor.description.lower()]):
            if parsedResponse.bio is not None and len(parsedResponse.bio) > 72:
                actor.description = aux.strip_html(parsedResponse.bio)
                success = True
                photo += " [ Description ]"

        if parsedResponse.pid  is not None:
            if not actor.tpdb_id or force:
                actor.tpdb_id = parsedResponse.pid
                photo += " [ TpDB ID ]"
                success = True

        if success:
            actor.last_lookup = datetime.datetime.now()
            actor.modified_date = datetime.datetime.now()
            actor.save()
            log.info(f'Information about {actor.name} was successfully gathered from TpDB: {photo}.')
        else:
            save_file_name = actor.generateThumbnailPath()
            if (actor.tpdb_id == parsedResponse.pid) and (len(actor.description) > 125) and (os.path.isfile(save_file_name)):
                if force:
                    log.info(f'It seems that there is no better information about {actor.name} on TpDB.')
                    return True
                else:
                    log.info(f'Your installation has good details about {actor.name}. You can force this operation.')
                    return True

        return success

    def scan_scene(self, scene_id: int, force: bool):
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
            parsedict = titleparser.search(parsetext)
            if parsedict[3]:
                parsetext = parsedict[1] + " " + parsedict[2] + " " + parsedict[3]
            elif parsedict[1]:
                parsetext = parsedict[1] + " " + parsedict[2]
            else:
                parsetext = parsedict[2]

            log.info(f"Parser will search for: {parsetext}")
            url = 'https://api.metadataapi.net/scenes'

            params = {
                'parse': parsetext,
                'limit': '1'
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            response = self.web.get_with_retry(url, headers=headers, params=params)
            response = response.json()

            if "id" and "title" in str(response):
                found = 1
            else:
                self.remove_text_inside_brackets(scene_name, brackets="[]")
                scene_name_formatted = self.tpdb_formatter(scene_name)
                log.info(f'Not successful scanning with conventional search, scanning with secondary parsetext: "{scene_name_formatted}"...')
                url = 'https://api.metadataapi.net/scenes'
                params = {
                    'parse': scene_name_formatted,
                    'limit': '1'
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
                response = self.web.get_with_retry(url, headers=headers, params=params)
                response = response.json()
                if "id" and "title" in str(response):
                    found = 2

            if found == 0:
                log.info(f"Scene not found in TpDB")
                return False

            log.info(f"A result was returned using method {found}. Parsing JSON...")
            respEl = response['data'][0]
            title = respEl.get('title', "")
            description = respEl.get('description', None)
            release_dateStr = respEl.get('date', None)
            tpdb_id = respEl.get('id', None)
            scenetags = respEl.get('tags', [])
            respElSite = respEl.get('site', {'name' : '', 'logo': ''})
            site = respElSite.get('name', "")
            site_logo = respElSite.get('logo', "")

            if description is not None:
                current_scene.description = description

            if release_dateStr is not None:
                try:
                    current_scene.release_date = datetime.datetime.strptime(release_dateStr, "%Y-%m-%d").date()
                except:
                    log.warning(f"Failed to parse release date {release_dateStr}")

            if tpdb_id is not None:
                current_scene.tpdb_id = tpdb_id
                current_scene.save()

            perflist = ""

            for performer in respEl['performers']:
                perf = self.namecheck(performer['name'])
                log.info(f"PERFORMER: {perf} - list: {perflist}")
                if not perf.lower().strip() in perflist.lower().strip():
                    performer_parent = performer.get('parent', {})
                    performer_extras = performer_parent.get('extras', None)
                    if performer_parent is None or performer_extras is None:
                        continue

                    gender = performer_extras.get('gender', None)
                    if gender is None or not "f" in performer_extras['gender'].lower():
                        continue

                    log.info(f"TpDB PERFORMER -> Checking {perf}...")
                    # See if we can find this performer in the database already.
                    keyname = self.resolvePerformer(performer)

                    # If we successfully found the performer, great! Just mark then as 'in this scene' and we're done.
                    if keyname is not None:
                        actor_to_add = Actor.objects.get(name=keyname)
                        self.addactor(current_scene, actor_to_add)
                        continue

                    # Otherwise, we still don't know who this actor is. We should add them to the DB.
                    # Get the name of this new actor
                    keyname = self.namecheck(performer['name'])
                    isUsingParent = False

                    # Not able to get the name? Try the parent.
                    if performer['parent']['name'] and not keyname:
                        keyname = self.namecheck(performer['parent']['name'])
                        isUsingParent = True

                    if keyname is None:
                        log.error("Can't find performer's name")

                    # Then we just need to add the actor to the database.
                    if Config().tpdb_actors:
                        log.info(f"Auto-adding a new actor: {keyname}")

                        # Find the URL to the new actor's image, if possible
                        if 'image' in performer.keys() and isUsingParent == False:
                            img = performer['image']
                        elif 'image' in performer['parent'].keys() and isUsingParent == True:
                            img = performer['parent']['image']
                        else:
                            img = None

                        act = self.createActorForSite(current_scene, keyname, img)
                        act.save()
                    elif Config().tpdb_actors == False:
                        log.info(f"We could add the actor {keyname}, but auto-adding is disabled")

                # At this point, we have an actor in the database, corresponding to the actor named by 'keyname'.
                # Populate this actor with any further info we got from TPDB.
                actor = Actor.objects.get(name=keyname) # type: Actor
                if len(perflist) > 3 and not actor.name.lower() in perflist.lower():
                    perflist = perflist + ", " + actor.name
                elif len(perflist) < 3:
                    perflist = actor.name

                added = self.setActorPropertiesFromPerformerExtras(actor, performer_extras)

                if actor.description == "":
                    desc = performer["parent"].get("bio", "")
                    if len(desc) > 72:
                        actor.description = desc
                        added = True

                # We only support 'F' gender, so it's safe to assume here.
                if not actor.gender:
                    actor.gender = "F"
                    added = True

                if added == True:
                    self.insert_actor_tag(actor, "TpDB: Info added")
                    actor.last_lookup = datetime.datetime.now()
                    log.info(f"Some information about {actor.name} was added to the profile.")
                    actor.save()

            self.associateSceneWithWebsite(current_scene, site, site_logo)
            self.renameSceneIfEnabled(self.suggestSceneName(title, site, perflist))
            current_scene.save()
            self.addSceneTags(current_scene, scenetags)
            self.setMatchTag(current_scene, found)
            current_scene.save()

            log.info(f"Found and registered data for scene ID {scene_id}")
            return True

        except KeyError as e:
            log.exception(f"Issue(s) occured", e)
            return False


    def tpdb_formatter(self, name):

        name = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', '', name)
        name = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', '', name)
        name = re.sub(r'\d{1,2}\.{0,1}\s{0,1}(January|February|March|April|May|June|July|August|September|October|November|December)\s{0,1}.\d{4}', '', name)
        name = re.sub(r'(\d+)[/.-](\d+)[/.-](\d+)', '', name)
        name = re.sub(r'\W', ' ', name)
        name = ' '.join(name.split())

        name = name.replace("(", " ")
        name = name.replace(")", " ")
        name = name.replace("[", " ")
        name = name.replace("]", " ")
        name = name.replace("!", " ")
        name = name.replace("?", " ")
        name = self.remove_text_inside_brackets(name)
        name = re.sub(' +', ' ', name)

        return name

    def setFakeTits(self, owner: Actor, areFake : bool):
        if areFake == True:
            if not "tits" in str(owner.actor_tags.all().lower()):
                owner.actor_tags.add("Fake tits")
        elif areFake == False:
            if not "tits" in str(owner.actor_tags.all().lower()):
                owner.actor_tags.add("Natural tits")
        # TODO/FIXME : what if a previous result specified natrual, but the current specifies fake - will the owner get both fake and natural tags?

    def setActorCountryOfOrigin(self, owner : Actor, birthplace : str):
        if "united states" in birthplace.lower():
            birthplace = "United States"
            owner.country_of_origin = birthplace

    def setActorWeight(self, owner: Actor, weight : str):
        # TODO: units?
        weight = re.findall(r'[\d]+', weight)
        weight = weight[0]
        owner.weight = weight

    def setActorHeight(self, owner : Actor, height : str):
        heightVal = re.findall(r'[\d]+', height)
        heightVal = heightVal[0]
        if not "cm" in height:
            heightVal = int(round(float(heightVal) * 2.54))
        owner.height = heightVal

    def setActorHairColour(self, owner : Actor, hair : str):
        hair = hair.replace("Brunette, ", "")
        hair = hair.replace("Blonde, ", "")
        hair = hair.replace("Redhead, ", "")
        if not owner.actor_tags.filter(name__contains=" hair"):
            self.insert_actor_tag(owner, hair + " hair".capitalize())

    def setActorPropertiesFromPerformerExtras(self, actor : Actor, performer_extras : Dict[str, any]):
        added = False

        if not actor.has_valid_date_of_birth():
            dob = performer_extras.get("birthday", None)
            if dob is not None:
                actor.date_of_birth = dob
                added = True

        if 'fakeboobs' in performer_extras.keys():
            self.setFakeTits(actor, performer_extras['fakeboobs'])
            added = True

        if not actor.has_valid_ethnicity():
            ethnicity = performer_extras.get('ethnicity', None)
            if ethnicity is not None:
                actor.ethnicity = ethnicity
                added = True

        if not actor.has_valid_country_of_origin():
            birthplace = performer_extras.get('birthplace', None)
            if birthplace is not None:
                self.setActorCountryOfOrigin(actor, birthplace)
                added = True

        if not actor.has_valid_weight():
            weight = performer_extras.get('weight', None)
            if weight is not None:
                self.setActorWeight(actor, weight)
                added = True

        if not actor.has_valid_height():
            height = performer_extras.get('height', None)
            if height is not None:
                self.setActorHeight(actor, height)
                added = True

        hair = performer_extras.get('hair_colour', None)
        if hair is not None:
            self.setActorHairColour(actor, hair)
            added = True

        return added

    def setMatchTag(self, current_scene, found):
        tg = SceneTag.objects.get(name="TpDB: Match: Good")
        tq = SceneTag.objects.get(name="TpDB: Match: Questionable")
        tn = SceneTag.objects.get(name="TpDB: Match: None")
        current_scene.scene_tags.remove(tg)
        current_scene.scene_tags.remove(tq)
        current_scene.scene_tags.remove(tn)
        current_scene.save()

        if found == 1:
            self.insert_scene_tag(current_scene, "TpDB: Match: Good")
        elif found == 2:
            self.insert_scene_tag(current_scene, "TpDB: Match: Questionable")
        elif found == 0:
            self.insert_scene_tag(current_scene, "TpDB: Match: None")

        self.insert_scene_tag(current_scene, "TpDB: Scanned")

    def associateSceneWithWebsite(self, current_scene: Scene, siteName: str, site_logo):
        website = list((Website.objects.find(name=siteName)).all())
        if len(website) == 0:
            log.warning(f"This website couldn't be found: {siteName}")
            return

        website = website[0]

        if not current_scene.websites.filter(name=siteName):
            log.info(f"Adding website: {website.name} to the scene {current_scene.name}")
            current_scene.websites.add(website)
        else:
            log.info("Website already registered to scene.")

        if Config().tpdb_website_logos:
            self.web.save_website_logo(site_logo, siteName, False, current_scene.id)

    def suggestSceneName(self, title: str, site: str, perflist: str):
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

        return newtitle

    def resolvePerformer(self, performerToFind):
        nameToFind = self.namecheck(performerToFind['name'])

        # First, search the actors list.
        actors = list(Actor.objects.extra(select={"length": "Length(name)"}).order_by("-length"))
        for scene_performer in actors:
            keyname = ""
            if not keyname:
                sp = scene_performer.name
                if sp.lower() == nameToFind.lower():
                    primary = 1
                    log.info(f"SM 1: YAPO performer name {sp} matches checked TpDB name")
                    return scene_performer.name

        # If we can't find this actor yet, try aliases.
        aliasesInDatabase = ActorAlias.objects.all()
        aliasesToFind = performerToFind.get('aliases', [])
        for aliasInDatabase in aliasesInDatabase:
            # Does this alias match the name of this performer?
            if aliasInDatabase.name.lower() == nameToFind.lower():
                primary = 3
                return scene_performer.name

            # Does the alias match any of this performer's aliases?
            for aliasToFind in aliasesToFind:
                if aliasInDatabase.name.lower() == aliasToFind.lower():
                    primary = 3
                    return scene_performer.name

            # Does this alias match any of the performer parent's aliases?
            # TODO: check this code, not sure if I broke it?
            parentAliasesToFind = performerToFind.get('parent', {}).get('aliases', [])
            for parentAliasToFind in parentAliasesToFind:
                if aliasInDatabase.name.lower() == parentAliasToFind.lower():
                    primary = 3
                    return scene_performer.name

        return None

    def createActorForSite(self, scene, actorName, actorImageURL = None):
        act = Actor(name = actorName)
        act.date_added = datetime.datetime.now()
        act.thumbnail = Constants().unknown_person_image_path
        act.save()

        # Add this actor to this scene
        self.addactor(scene, act)

        # Download the actor's image, if possible
        if actorImageURL:
            self.web.download_image(actorImageURL, act.generateThumbnailPath())
            act.thumbnail = act.getThumbnailPathURL()
            act.save()

        log.info(f"Actor {act.name} created and added to scene")

        log.info(f"Scraping additional info about {act.name}...")
        scraper_tmdb.search_person_with_force_flag(act, True)
        scraper_freeones.search_freeones_with_force_flag(act, True)

        return act

    def addSceneTags(self, current_scene, scenetags):
        tagcounter = 0
        for tag in scenetags:
            if tagcounter == Config().tpdb_tags:
                break
            log.info(f'[ {tag["tag"].capitalize()} ]')
            self.insert_scene_tag(current_scene, tag["tag"].capitalize())
            tagcounter += 1
        log.info(f"Added {tagcounter} tags from TpDB to this scene.")

    def renameSceneIfEnabled(self, current_scene : Scene, newtitle):
        if "true" not in Config().tpdb_autorename.lower():
            log.info(f'Renaming is disabled, but we suggest: \"{newtitle}\".')
            return
        if not current_scene.orig_name:
            current_scene.orig_name = current_scene.name
        current_scene.name = newtitle
        log.info(f'Scene name is now \"{newtitle}\".')
