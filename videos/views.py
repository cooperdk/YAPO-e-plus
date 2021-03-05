import os
import re
import os.path
from pathlib import Path
import subprocess
import django.db
import errno
from django.shortcuts import render
import requests
import requests.packages.urllib3
import videos.addScenes
import videos.filename_parser as filename_parser
import videos.scrapers.freeones as scraper_freeones
import videos.scrapers.imdb as scraper_imdb
import videos.clients.tmdb as scraper_tmdb
import videos.clients.apiclients as apiclients
#import videos.scrapers.googleimages as scraper_images
from configuration import Config, Constants
from videos import ffmpeg_process
import urllib.request
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.db.models import Count
import mimetypes
from datetime import timedelta
from datetime import datetime
# For REST framework

import platform
from rest_framework.decorators import api_view
from rest_framework.response import Response
from videos.serializers import *
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets, views
from rest_framework.parsers import FileUploadParser
from rest_framework import filters
from itertools import chain
import base64
import shutil
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from operator import attrgetter
from random import shuffle
from django.utils.datastructures import MultiValueDictKeyError
import threading
import videos.startup
# import pathlib
from utils.printing import Logger
log = Logger()
import urllib3
import urllib.request
import http.client
import json
http.client._MAXHEADERS = 1000

def timer(start: datetime, stop: datetime):
    import time
    from datetime import datetime
    delta = stop - start
    result = time.gmtime(delta.total_seconds())
    hr = "hour" if result.tm_hour == 1 else "hours"
    mn = "minute" if result.tm_min == 1 else "minutes"
    sc = "second" if result.tm_sec == 1 else "seconds"
    if result.tm_hour > 0:
        return f"{result.tm_hour} {hr}, {result.tm_min} {mn} and {result.tm_sec} {sc}"
    elif result.tm_min > 0:
        return f"{result.tm_min} {mn} and {result.tm_sec} {sc}"
    else:
        return f"{result.tm_sec} {sc}"

def get_scenes_in_folder_recursive(folder, scene_list):
    scenes = list(folder.scenes.all())
    scene_list = list(chain(scene_list, scenes))

    if folder.children.count() == 0:
        return scene_list

    else:
        for child in folder.children.all():
            scene_list = get_scenes_in_folder_recursive(child, scene_list)

        return scene_list


def onlyChars(input):
    valids = "".join(character for character in input if character.isalpha())
    return valids


def get_folders_recursive(folder, folder_list):
    # scenes = list(folder.scenes.all())
    # scene_list = list(chain(scene_list, scenes))

    if folder.children.count() == 0:
        return list()

    else:

        for child in folder.children.all():
            temp_list = get_folders_recursive(child, folder_list)

            folders = list(folder.children.all())
            # folder_list = list(chain(folder_list, folders))
            folder_list = list(chain(folders, temp_list))

        return folder_list


def lambda_attrgetter(string, x):
    y = attrgetter(string)

    return y(x)


def search_in_get_queryset(original_queryset, request):
    qs_list = list()
    term_is_not_null = False
    random = False
    sort_by = "name"
    was_searched = False

    if "search" in request.query_params:
        search_string = request.query_params["search"]
        if search_string:
            search_field = request.query_params["searchField"]

            if search_string.startswith("<"):
                string_keyarg = "{search_field}__lte"
                search_string = search_string.replace("<", "")
            elif search_string.startswith(">"):
                string_keyarg = "{search_field}__gte"
                search_string = search_string.replace(">", "")
            else:
                string_keyarg = f"{search_field}__icontains"

            if search_string:
                original_queryset = original_queryset.filter(
                    **{string_keyarg: search_string}
                )
                was_searched = True
        else:
            if request.query_params["pageType"]:
                if request.query_params["pageType"] == "DbFolder":
                    original_queryset = original_queryset.filter(level=0)

    if (
        "recursive" in request.query_params
        and request.query_params["recursive"] == "true"
    ):
        print("Recursive is TRUE!!!!")
        print(request.query_params["folders_in_tree"])
        folder = Folder.objects.get(pk=int(request.query_params["folders_in_tree"]))
        qs_list = get_scenes_in_folder_recursive(folder, qs_list)
        print(qs_list)
        term_is_not_null = True

    else:
        z = False
        try:
            if request.query_params["pageType"]:

                if request.query_params["pageType"] == "DbFolder" and was_searched:
                    z = True
        except MultiValueDictKeyError:
            pass

        if not z:
            for qp in request.query_params:
                # print (qp)
                term_string = request.query_params.get(qp, None)
                # print (term_string)

                if (
                    (term_string is not None)
                    and (term_string != "")
                    and (qp != "limit")
                    and (qp != "offset")
                    and (qp != "ordering")
                    and (qp != "recursive")
                    and (qp != "sortBy")
                    and (qp != "searchField")
                    and (qp != "format")
                    and (qp != "pageType")
                    and (qp != "search")
                ):

                    term_is_not_null = True
                    terms = term_string.split(",")

                    for term in terms:
                        if qs_list:
                            t_list = list()
                            for i in qs_list:
                                if type(getattr(i, qp)) is bool:
                                    if bool(term) == getattr(i, qp):
                                        t_list.append(i)
                                elif (
                                    getattr(i, qp)
                                ).__class__.__name__ == "ManyRelatedManager":
                                    print(getattr(i, qp).all())
                                    x = getattr(i, qp).all()
                                    for item in getattr(i, qp).all():
                                        if item.id == term:
                                            t_list.append(i)
                                            break
                                elif (getattr(i, qp)) == term:
                                    t_list.append(i)
                                    # if term in getattr(i, qp).all():
                                    #     t_list.append(i)
                            qs_list = t_list
                        else:
                            qs_list = list(
                                chain(qs_list, original_queryset.filter(**{qp: term}))
                            )

    if "sortBy" in request.query_params:
        sort_by = request.query_params["sortBy"]
        if sort_by == "random":
            random = True
        if "usage_count" in sort_by:
            term_is_not_null = True
            # qs_temp1 = original_queryset.values()
            # qs_list = qs_temp1
            qs_list = list(original_queryset)

    if term_is_not_null:
        if random:
            shuffle(qs_list)
        else:
            if "-" in sort_by:
                sort_by = sort_by.replace("-", "")
                if sort_by == "usage_count":
                    try:
                        temp_list = sorted(
                            qs_list, key=lambda k: k.scenes.count(), reverse=True
                        )
                    except AttributeError:
                        temp_list = sorted(
                            qs_list, key=lambda k: k.actors.count(), reverse=True
                        )
                else:
                    temp_list = sorted(
                        qs_list,
                        key=lambda k: (
                            lambda_attrgetter(sort_by, k) is None,
                            lambda_attrgetter(sort_by, k) == "",
                            lambda_attrgetter(sort_by, k),
                        ),
                        reverse=True,
                    )

            else:

                if sort_by == "usage_count":
                    try:
                        temp_list = sorted(qs_list, key=lambda k: k.scenes.count())
                    except AttributeError:
                        temp_list = sorted(qs_list, key=lambda k: k.actors.count())
                else:
                    temp_list = sorted(
                        qs_list,
                        key=lambda k: (
                            lambda_attrgetter(sort_by, k) is None,
                            lambda_attrgetter(sort_by, k) == "",
                            lambda_attrgetter(sort_by, k),
                        ),
                    )
            return temp_list

        return qs_list
    else:
        if random:
            return original_queryset.order_by("?")
        else:
            return original_queryset.order_by(sort_by)

def tpdb_scanner(force):
    ### This is the TpDB scanner. It calls the TpDB function in videos.scanners

    scenes = Scene.objects.all()
    for scene in scenes:
        success = apiclients.tpdb(scene.id, force)
        if not success: log.error('TPDB: SCAN: There was an error scanning scene ID {scene.id}.')
    return Response(status=200)

def populate_tag(searchtag, tagtype, force) -> int:
    """
    Function to scan a scene using the YAPO Tags API (api.porn-organizer.org/records/tags).
    Populates a single scene or actor tag with description and images from the YAPO API.

    Args:
        searchtag (int): The row ID of a tag to scan
        tagtype (str): Indicates if the tag is a SceneTag or ActorTag
        force (bool): Indicates if the operation should be forced

    Returns:
        int: Success/Error code
    """

    import videos.aux_functions as aux
    tag = None
    found = 0
    response = None
    if not aux.is_domain_reachable("https://api.porn-organizer.org/records/tags/"):
        return 3


    if tagtype == "ActorTag":
        tag = ActorTag.objects.filter(pk=searchtag)[0]
        scf = "actor"
    elif tagtype == "SceneTag":
        tag = SceneTag.objects.filter(pk=searchtag)[0]
        scf = "scene"
    if not tag:
        return 0
    searchtagname=tag.name
    if tag.yapo_id and not force:
        return 2

    log.sinfo(f'Adding data to the {scf} tag "{tag.name}"')

    url="https://api.porn-organizer.org/records/tags"
    params = {'filter': (f'tag,eq,{searchtagname.lower()}'),
              'join': 'taggroups',
              'join': 'aliases' }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'YAPO 0.7.6',
    }
    print("Downloading tag information... ", end="")
    response = requests.request('GET', url, headers=headers, params=params) #, params=params
    print("\n")
    try:
        response = response.json()
    except:
        pass
    #print(response)
    if "tag" and "id" in str(response):

        #get tag from main tag json
        yapoid = response["records"][0]["id"]
        image = response["records"][0]["image"]
        desc = response["records"][0]["description"]
        found=1
    else:
        print("No primary tag name found, looking for aliases...")

        url = "https://api.porn-organizer.org/records/aliases"
        params = { 'filter': (f'alias,eq,{searchtagname.lower()}'),
                    'join': 'tags' }
        headers = {
                'Content-Type': 'application/json',
                'Accept'      : 'application/json',
                'User-Agent'  : 'YAPO 0.7.6',
        }
        print("Downloading tag information... ", end="")
        response = requests.request('GET', url, headers=headers, params=params)  # , params=params
        print("\n")
        try:
            response = response.json()
        except:
            pass

        if "tags_id" and "alias" in str(response):

            #get tag from alias json
            yapoid=image=response["records"][0]["tags_id"]["id"]
            image=response["records"][0]["tags_id"]["image"]
            desc=response["records"][0]["tags_id"]["description"]
            found=1
        else:
            return 0
    try:
        if image and len(image)<5:
            found=4
        if image and len(image)>5:
            img=json.loads(image)
            #print("img: " + str(img))
            imgsave=img[0]["name"]
            imgthumb=img[0]["thumbnail"]
            imgsave = imgsave.replace("\\\\", "").split("/")[1]
            imgthumb = imgthumb.replace("\\\\", "").split("/")[1]
            #log.sinfo(f"Downloading tag image {imgsave} with thumbnail...")
            suf=Path(imgsave).suffix
            folder = os.path.join(Config().site_media_path, 'tags', scf, str(tag.id))
            fimg = os.path.join(folder,"tagimg.jpg")
            fthumb = os.path.join(folder,"tagthumb.jpg")
            if not os.path.isdir(folder):
                os.makedirs(folder)

            aux.download_image("http://api.porn-organizer.org/photos/"+imgsave,fimg)

            if aux.download_image("http://api.porn-organizer.org/thumbs/"+imgthumb,fthumb):
                relpath = os.path.relpath(fthumb, start="data")
                asuri = urllib.request.pathname2url(relpath)
                tag.thumbnail = asuri
    except Exception as e:
        log.warn(f'YAPOAPI: TAG: Error occured when getting image')

    if yapoid:
        tag.yapo_id = yapoid
    if desc:
        tag.description = desc

    if searchtag == "SceneTag":
        foundx=False
        try:
            extags = tag.aliases.split(",")
            for x in response["records"]["aliases"]:
                foundx=False
                for extag in extags:
                    if x[alias] == extag.strip():
                        foundx=True
                        break
                    else:
                        foundx=False
                if not foundx:
                    extag.append(x[alias])
            tag.aliases = ",".join(extag)
        except:
            log.warn("TAGS: Error while enumerating tag aliases.")
    tag.save()

    if found==4:
        return 4

    return 1

def populate_websites(force):
    ### Populates website logos, URLs and checks YAPO website names against TpDB names.
    ### Force will re-download logos.

    import videos.aux_functions as aux
    if not aux.is_domain_reachable("https://api.metadataapi.net/sites"):
        return Response(status=500)
    log.sinfo(f"Traversing websites for logos...")
    nexturl = 'https://api.metadataapi.net/sites?page=1'
    while nexturl:
        params = {'limit': 99999}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'YAPO 0.7.6',
        }
        print("Downloading site information... ", end="")
        response = requests.request('GET', nexturl, headers=headers, params=params) #, params=params
        print("\n")
        try:
            response = response.json()
        except:
            pass
        print("\n")
        websites = Website.objects.all()
        for site in websites:
            oldname = site.name
            found = False
            for tpdb in response['data']: #[0]:
                found = False
                tsid = tpdb['id']
                tsn = tpdb['name']
                tss = tpdb['short_name']
                tsurl = tpdb['url']
                tslogo = tpdb['logo']
                if site.name == tsn:
                    found = True
                if (site.name != tsn) and (site.name.lower() == tsn.lower()):
                    log.info(f'Renaming site "{site.name}" to "{tsn}" for consistency')
                    site.name = tsn
                    found = True
                if (site.name.lower() == tss.lower()) and (site.name.lower() != tsn.lower()):
                    log.info(f'Renaming site "{site.name}" to "{tsn}" because it is truncated')
                    site.name = tsn
                    found = True
                if found:
                    try:
                        newname = site.name
                        if not tss.lower() in site.website_alias.lower():
                            if len(site.website_alias) > 1:
                                site.website_alias += f",{tss.lower()}"
                            else:
                                site.website_alias = tss.lower()
                        if not site.url:
                            site.url = tsurl
                        if not site.tpdb_id:
                            site.tpdb_id = int(tsid)
                        aux.save_website_logo(tslogo, site.name, force)
                        site.save()
                    except:
                        log.error(
                            f'Attempting to rename {oldname} to {newname} resulted in an error. New name probably already exists!')
                        break
                    print("\n")
        nexturl = response['links']['next']
        print(f"Getting next JSON page ({nexturl})...")
    return Response(status=200)


def tpdb_scan_actor(actor, force: bool):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    import videos.aux_functions as aux
    if not aux.is_domain_reachable("api.metadataapi.net/performers"):
        return Response(status=500)

    photo = actor.thumbnail
    desc = actor.description
    url = 'https://api.metadataapi.net/performers'
    log.sinfo(f'Contacting TpDB API for info about {actor.name}.')
    params = { 'q': actor.name }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'YAPO 0.7.6',
    }
    response = requests.request('GET', url, headers=headers, params=params)  # , params=params
    #print("\n")
    if response.status_code < 300:
        try:
            response = response.json()
        except:
            pass
        pid = ""
        img = ""
        bio = ""
        desc = ""
        changed = False
        success = False
        photo = ""
        if all([response['data'], len(str(response['data'])) > 15]):
            #print("1")
            try:
                if 'id' in response['data'][0].keys():
                    pid = response['data'][0]['id']
                    #print("id")
                if 'image' in response['data'][0].keys():
                    img = response['data'][0]['image']
                    #print("i")
                elif 'thumbnail' in response['data'][0].keys():
                    img = response['data'][0]['thumbnail']
                    #print("t")
                if 'bio' in response['data'][0].keys():
                    desc = response['data'][0]['bio']
                    #print("d")
                if actor.thumbnail == Constants().unknown_person_image_path or force:
                    save_path = os.path.join(Config().site_media_path, 'actor', str(actor.id), 'profile')
                    save_file_name = os.path.join(save_path, 'profile.jpg')
                    if img and (not os.path.isfile(save_file_name) or force):
                        if not os.path.exists(save_path):
                            os.makedirs(save_path)
                        if aux.download_image(img, save_file_name):
                            rel_path = os.path.relpath(save_file_name, start="data")
                            as_uri = urllib.request.pathname2url(rel_path)
                            actor.thumbnail = as_uri
                            photo += " [ Photo ]"
                            success = True
                        else:
                            log.swarn(f"DOWNLOAD ERROR: Photo ({actor.name}): {img}")

                if any([force, not actor.description, len(actor.description) < 128, "freeones" in actor.description.lower()]):
                    if desc:
                        if len(desc) > 72:
                            actor.description = aux.strip_html(desc)
                            changed = True
                            success = True
                            photo += " [ Description ]"
                if pid:
                    if not actor.tpdb_id or force:
                        actor.tpdb_id = pid
                        photo += " [ TpDB ID ]"
                        changed = True
                        success = True
                if success:
                    actor.last_lookup = datetime.datetime.now()
                    actor.modified_date = datetime.datetime.now()
                    actor.save()
                    log.sinfo(f'Information about {actor.name} was successfully gathered from TpDB: {photo}.')
                else:
                    save_path = os.path.join(Config().site_media_path, 'actor', str(actor.id), 'profile')
                    save_file_name = os.path.join(save_path, 'profile.jpg')

                    if not force and ((actor.tpdb_id == pid) and (len(actor.description) > 125) and (os.path.isfile(save_file_name))):
                        success = True
                        log.sinfo(f'Your installation has good details about {actor.name}. You can force this operation.')

                    elif force and ((actor.tpdb_id == pid) and (len(actor.description) > 125) and (os.path.isfile(save_file_name))):
                        success = True
                        log.sinfo(f'It seems that there is no better information about {actor.name} on TpDB.')
                return success

            except:
                success = False
                log.warn(f'Error downloading a photo for and/or getting information about {actor.name}!')
                return success

        else:
            log.swarn(f'It seems that TpDB might not know anything about {actor.name}!')
            success = False
            return success
    else:
        log.warn(f"An error occured while retrieving data about {actor.name}.")
        success = False
        return success

def scrape_all_actors(force):
    actors = Actor.objects.all()

    for actor in actors:
        if not force:
            if actor.last_lookup is None:
                print("Searching in TMDb")
                scraper_tmdb.search_person_with_force_flag(actor, False)
                print("Finished TMDb search")
                print("Searching TpDB...")
                tpdb_scan_actor(actor, False)
                print("Finished TpDB search")
                print("Searching IMDB...")
                scraper_imdb.search_imdb_with_force_flag(actor, False)
                print("Finished IMDB Search")
                if actor.gender != "M":
                    print("Searching in Freeones")
                    scraper_freeones.search_freeones_with_force_flag(actor, True)
                    print("Finished Freeones search")
            else:
                print(f"{actor.name} was already searched...                                                                        \r",end="")
        else:
            print("Searching TMDb...")
            scraper_tmdb.search_person_with_force_flag(actor, True)
            print("Finished TMDb search")
            print("Searching TpDB...")
            tpdb_scan_actor(actor, True)
            print("Finished TpDB search")
            print("Searching IMDB...")
            scraper_imdb.search_imdb_with_force_flag(actor, True)
            print("Finished IMDB Search")
            if actor.gender != "M":
                print("Searching Freeones")
                scraper_freeones.search_freeones_with_force_flag(actor, True)
                print("Finished Freeones search.")
    print("\rDone scraping actors.                                                                                               ")
    return Response(status=200)


def tag_all_scenes(ignore_last_lookup):
    if Config().current_setting_version < 3:

        for actorTag in ActorTag.objects.all():
            if not SceneTag.objects.filter(name=actorTag.name):
                SceneTag.objects.create(name=actorTag.name)

            scene_tag_to_add = SceneTag.objects.get(name=actorTag.name)
            actorTag.scene_tags.add(scene_tag_to_add)
            scenetag=SceneTag.objects.filter(name=actorTag.name)
            print(
                f"Added scene tag {scenetag} to actor tag {actorTag.name}"
            )
    filename_parser.parse_all_scenes(False)
    return Response(status=200)


def tag_all_scenes_ignore_last_lookup(ignore_last_lookup):
    if Config().current_setting_version < 3:

        for actorTag in ActorTag.objects.all():
            if not SceneTag.objects.filter(name=actorTag.name):
                SceneTag.objects.create(name=actorTag.name)

            scene_tag_to_add = SceneTag.objects.get(name=actorTag.name)
            actorTag.scene_tags.add(scene_tag_to_add)
            scenetag=SceneTag.objects.filter(name=actorTag.name)
            print(
                f"Added scene tag {scenetag} to actor tag {actorTag.name}"
            )

    filename_parser.parse_all_scenes(True)

    return Response(status=200)


class getTags(views.APIView):
    def get(self, request, format=None) -> HttpResponse:
        """Function to scan a scene using the TpDB API (metadataapi.net).

        Args:
            request (list): A list of parameters sent from the UI
            force (bool): Indicates if the operation should be forced

        Returns:
            HttpResponse (object)
        """
        tagid=request.query_params["tag_id"]
        tagtype=request.query_params["tag_type"]
        if request.query_params["force"] == "true":
            force = True
        else:
            force = False

        success=populate_tag(tagid,tagtype,force)

        if success == 1:
            return HttpResponse("Successfully registered data for the tag.", status=200)
        elif success == 2:
            return HttpResponse("The tag has already been scanned, and you didn't force the scan.", status=403)
        elif success == 3:
            return HttpResponse("The YAPO Tags API is unreachable. Try again later.", status=503)
        elif success == 4:
            return HttpResponse("Successfully registered data for the tag, but there was no image.", status=200)
        else:
            return HttpResponse("This tag was not found using The YAPO Tags API.", status=404)

class scanScene(views.APIView):
    def get(self, request, format=None):

        search_site = request.query_params["scanSite"]
        scene_id = request.query_params["scene"]

        if request.query_params["force"] == "true":
            force = True
        else:
            force = False
        if Config().debug=="true":
            log.sinfo("Now entering the TPDB scene scanner API REST view")

        success = apiclients.tpdb(scene_id, force)

        if success == 1:
            return HttpResponse("Successfully scanned the scene.", status=200)
        elif success == 2:
            return HttpResponse("The file has already been scanned, and you didn't force the scan.", status=403)
        else:
            return HttpResponse("The scene was not found using The Porn Database's API.", status=404)


class ScrapeActor(views.APIView):

    def get(self, request, format=None):
        search_site = request.query_params["scrapeSite"]
        actor_id = request.query_params["actor"]
        if request.query_params["force"] == "true":
            force = True
        else:
            force = False
        if Config().debug=="true":
            log.sinfo("Now entering the scrape actor API REST view")
        print(f"Scanning for {Actor.objects.get(pk=actor_id).name} on {search_site}")

        if search_site == "TMDb":
            actor_to_search = Actor.objects.get(pk=actor_id)
            success = False
            if force:
                success = scraper_tmdb.search_person_with_force_flag(
                    actor_to_search, True
                )
            else:
                success = scraper_tmdb.search_person_with_force_flag(
                    actor_to_search, False
                )
            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif search_site == "TpDB":

            actor_to_search = Actor.objects.get(pk=actor_id)
            success = False
            if force:
                success = tpdb_scan_actor(actor_to_search, True)
            else:
                success = tpdb_scan_actor(actor_to_search, False)

            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif search_site == "Freeones":

            actor_to_search = Actor.objects.get(pk=actor_id)
            success = False
            if force:
                success = scraper_freeones.search_freeones_with_force_flag(
                    actor_to_search, True
                )
            else:
                success = scraper_freeones.search_freeones_with_force_flag(
                    actor_to_search, False
                )

            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif search_site == "IMDB":

            actor_to_search = Actor.objects.get(pk=actor_id)
            success = False
            if force:
                success = scraper_imdb.search_imdb_with_force_flag(
                    actor_to_search, True
                )
            else:
                success = scraper_imdb.search_imdb_with_force_flag(
                    actor_to_search, False
                )

            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)





def permanently_delete_scene_and_remove_from_db(scene):
    success_delete_file = False
    success_delete_media_path = False
    try:
        os.remove(scene.path_to_file)
        print(f"Successfully deleted scene '{scene.path_to_file}'")
        success_delete_file = True
    except OSError as e:
        if e.errno == errno.ENOENT:
            print(
                f"File {scene.path_to_file} already deleted! [Err No:{e.errno}, Err File:{e.filename} Err:{e.strerror}]"
            )
            success_delete_file = True
        else:
            print(
                f"Got OSError while trying to delete {scene.path_to_file} : Error number:{e.errno} Error Filename:{e.filename} Error:{e.strerror}"
            )

    media_path = os.path.relpath(
        os.path.join(Config().site_media_path, "scenes", str(scene.id))
    )
    print(os.path.dirname(os.path.abspath(__file__)))
    try:
        shutil.rmtree(media_path)
        print(f"Deleted '{media_path}'")
        success_delete_media_path = True
    except OSError as e:
        if e.errno == errno.ENOENT:
            print(f"Directory '{media_path}' already deleted")
            success_delete_media_path = True
        else:
            print(
                f"Got OSError while trying to delete {scene.path_to_file} : Error number:{e.errno} Error Filename:{e.filename} Error:{e.strerror}"
            )

    if success_delete_file and success_delete_media_path:
        scene.delete()
        print(f"Removed '{scene.name}' from database")


def checkDupeHash(hash):
    from django.db import connection

    cursor = connection.cursor()

    cursor.execute("SELECT count(*) from videos_scene WHERE hash = %s", [hash])
    dupecount = cursor.fetchone()
    # print ("Checked " + hash + " - " + str(dupecount[0]) + "\n")
    return dupecount[0]


@api_view(["GET", "POST"])
def tag_multiple_items(request):
    if request.method == "POST":
        # print("We got a post request!")

        params = request.data["params"]

        if params["type"] == "scene":
            print("Patching scene")

            if params["patchType"] == "websites":

                website_id = params["patchData"][0]
                website_to_add = Website.objects.get(pk=website_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.add(website_to_add)
                        print(
                            f"Added Website '{website_to_add.name}' to scene '{scene_to_update.name}'"
                        )

                        if website_to_add.scene_tags.count() > 0:
                            for tag in website_to_add.scene_tags.all():
                                scene_to_update.scene_tags.add(tag)
                                print(
                                    f"Added Scene Tag '{tag.name}' to scene '{scene_to_update.name}'"
                                )

                        scene_to_update.save()
                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.remove(website_to_add)
                        print(
                            f"Removed Website '{website_to_add.name}' from scene '{scene_to_update.name}'"
                        )
                        if website_to_add.scene_tags.count() > 0:
                            for tag in website_to_add.scene_tags.all():
                                if tag in scene_to_update.scene_tags.all():
                                    scene_to_update.scene_tags.remove(tag)
                                    print(
                                        f"Removed Scene Tag '{tag.name}' from scene '{scene_to_update.name}'"
                                    )
                        scene_to_update.save()

            elif params["patchType"] == "scene_tags":
                scene_tag_id = params["patchData"][0]
                scene_tag_to_add = SceneTag.objects.get(pk=scene_tag_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.scene_tags.add(scene_tag_to_add)
                        scene_to_update.save()
                        print(
                            f"Added Scene Tag '{scene_tag_to_add.name}' to scene '{scene_to_update.name}'"
                        )

                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.scene_tags.remove(scene_tag_to_add)
                        scene_to_update.save()
                        print(
                            f"Removed Scene Tag '{scene_tag_to_add.name}' from scene '{scene_to_update.name}'"
                        )
            elif params["patchType"] == "actors":
                actor_id = params["patchData"][0]
                actor_to_add = Actor.objects.get(pk=actor_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.add(actor_to_add)
                        print(
                            f"Added Actor '{actor_to_add.name}' to scene '{scene_to_update.name}'"
                        )

                        if actor_to_add.actor_tags.count() > 0:
                            for actor_tag in actor_to_add.actor_tags.all():
                                scene_to_update.scene_tags.add(
                                    actor_tag.scene_tags.first()
                                )
                                print(
                                    f"Added Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{scene_to_update.name}'"
                                )

                        scene_to_update.save()

                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.remove(actor_to_add)
                        print(
                            f"Removed Actor '{actor_to_add.name}' from scene '{scene_to_update.name}'"
                        )

                        if actor_to_add.actor_tags.count() > 0:
                            for actor_tag in actor_to_add.actor_tags.all():
                                if (
                                    actor_tag.scene_tags.first()
                                    in scene_to_update.scene_tags.all()
                                ):
                                    scene_to_update.scene_tags.remove(
                                        actor_tag.scene_tags.first()
                                    )
                                    print(
                                        f"Removed Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{scene_to_update.name}'"
                                    )
                        scene_to_update.save()

            elif params["patchType"] == "delete":
                scenes_to_update = params["itemsToUpdate"]

                if params["permDelete"]:
                    print("permDelete true")
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        permanently_delete_scene_and_remove_from_db(scene_to_update)
                else:
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.delete()
                        print(
                            f"Removed scene '{scene_to_update.name}' from database"
                        )

            elif params["patchType"] == "playlists":
                playlist_id = params["patchData"][0]
                playlist_to_add = Playlist.objects.get(pk=playlist_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.playlists.add(playlist_to_add)
                        print(
                            f"Scene '{scene_to_update.name}' was added to playlist '{playlist_to_add.name}'"
                        )
                        scene_to_update.save()
                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.playlists.remove(playlist_to_add)
                        print(
                            f"Scene '{scene_to_update.name}' was removed to playlist '{playlist_to_add.name}'"
                        )
                        scene_to_update.save()

            else:
                scenes_to_update = params["itemsToUpdate"]
                for x in scenes_to_update:
                    scene_to_update = Scene.objects.get(pk=x)
                    patch_type = params["patchType"]
                    patch_data = params["patchData"]
                    setattr(scene_to_update, patch_type, patch_data)
                    # scene_to_update[patch_type] = patch_data

                    print(
                        f"Set scene's '{scene_to_update}' attribute '{patch_type}' to '{patch_data}'"
                    )
                    scene_to_update.save()

        elif params["type"] == "actor":
            if params["patchType"] == "actor_tags":
                actor_tag_id = params["patchData"][0]
                actor_tag_to_add = ActorTag.objects.get(pk=actor_tag_id)
                actors_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in actors_to_update:
                        actor_to_update = Actor.objects.get(pk=x)
                        actor_to_update.actor_tags.add(actor_tag_to_add)
                        actor_to_update.save()
                        print(
                            f"Added Actor Tag '{actor_tag_to_add.name}' to actor {actor_to_update.name}"
                        )
                elif params["addOrRemove"] == "remove":

                    for x in actors_to_update:
                        actor_to_update = Actor.objects.get(pk=x)
                        actor_to_update.actor_tags.remove(actor_tag_to_add)
                        actor_to_update.save()
                        print(
                            f"Removed Actor Tag '{actor_tag_to_add.name}' to actor {actor_to_update.name}"
                        )
            else:
                actors_to_update = params["itemsToUpdate"]
                for x in actors_to_update:
                    actor_to_update = Actor.objects.get(pk=x)
                    patch_type = params["patchType"]
                    patch_data = params["patchData"]
                    setattr(actor_to_update, patch_type, patch_data)
                    # scene_to_update[patch_type] = patch_data

                    print(
                        f"Set actors's '{actor_to_update}' attribute '{patch_type}' to '{patch_data}'"
                    )
                    actor_to_update.save()

        return Response(status=200)


def clean_dir(type_of_model_to_clean):
    number_of_folders = len(
        os.listdir(os.path.join(Config().site_media_path, type_of_model_to_clean))
    )
    index = 1

    for dir_in_path in os.listdir(
        os.path.join(Config().site_media_path, type_of_model_to_clean)
    ):

        print(f"Checking {type_of_model_to_clean} folder {index} out of {number_of_folders}\r", end="")
        try:
            dir_in_path_int = int(dir_in_path)

            if type_of_model_to_clean == "actor":
                try:
                    actor = Actor.objects.get(pk=dir_in_path_int)
                except Actor.DoesNotExist:
                    dir_to_delete = os.path.join(
                        Config().site_media_path, type_of_model_to_clean, dir_in_path
                    )
                    print(
                        f"Actor id {dir_in_path_int} is not in the database... Deleting folder {dir_to_delete}"
                    )
                    shutil.rmtree(dir_to_delete)
            elif type_of_model_to_clean == "scenes":

                try:
                    scene = Scene.objects.get(pk=dir_in_path_int)
                except Scene.DoesNotExist:
                    dir_to_delete = os.path.join(
                        Config().site_media_path, type_of_model_to_clean, dir_in_path
                    )
                    print(
                        f"Scene id {dir_in_path_int} is not in the database... Deleting folder {dir_to_delete}"
                    )
                    shutil.rmtree(dir_to_delete)
            elif type_of_model_to_clean == "websites":

                try:
                    website = Website.objects.get(pk=dir_in_path_int)
                except Website.DoesNotExist:
                    dir_to_delete = os.path.join(
                        Config().site_media_path, type_of_model_to_clean, dir_in_path
                    )
                    print(
                        f"Website id {dir_in_path_int} is not in the database... Deleting folder {dir_to_delete}"
                    )
                    shutil.rmtree(dir_to_delete)
            index += 1

        except ValueError:
            print(
                f"Dir name '{dir_in_path}' is not a database reference, skipping..."
            )
            index += 1
            pass

def sizeformat (b: int) -> str: # returns a human-readable filesize depending on the file's size
    if b < 1000:
        return f"{b} bytes"
    elif b < 1000000:
        return f"{b/1000:.1f} kilobytes"
    elif b < 1000000000:
        return f"{b/1000000:.1f} megabytes"
    elif b < 1000000000000:
        return f"{b/1000000000:.1f} gigabytes"
    else:
        return f"{b/1000000000000:.1f} terabytes"


@api_view(["GET", "POST"])
def settings(request):
    if request.method == "GET":

        #print(f"REQ: {str(request.query_params)}")

        if "pathToVlc" in request.query_params:
            if request.query_params["pathToVlc"] == "":

                serializer = SettingsSerializer(Config().get_old_settings_as_json())

                return Response(serializer.data)

            else:

                new_path_to_vlc = os.path.abspath(request.query_params["pathToVlc"]).replace("\\","/")
                log.info(f'VLC path set to {request.query_params["pathToVlc"]}')

                if os.path.isfile(new_path_to_vlc):
                    Config().vlc_path = new_path_to_vlc
                    Config().save()
                    return Response(status=200)

                else:
                    print("Error: VLC path does not exist!")

                    return Response(status=500)

        if "yapo_url" in request.query_params:

            if request.query_params["yapo_url"]:

                if request.query_params["yapo_url"] != "":

                    new_yapo_url = request.query_params["yapo_url"]

                else:

                    new_yapo_url = "none"

                log.info(f'YAPO URL set to {new_yapo_url}')
                Config().yapo_url = new_yapo_url
                Config().save()

                return Response(status=200)
        if "renaming" in request.query_params:

            if request.query_params["renaming"]:

                if request.query_params["renaming"] != "":

                    new_renaming = request.query_params["renaming"]

                else:

                    new_renaming = "none"

                log.info(f'Renaming format set to "{new_renaming}"')
                Config().renaming = new_renaming
                Config().save()

                return Response(status=200)

        '''
        if all(["pathToVlc" not in request.query_params, "enable_tpdb" not in request.query_params,
                "tpdb_websitelogos" not in request.query_params, "tpdb_enable_autorename" not in request.query_params,
                "tpdb_enable_addactors" not in request.query_params, "tpdb_enable_addphoto" not in request.query_params]):


        '''

        if "tpdb_settings" in request.query_params:

            if "tpdb_enabled" in request.query_params:
                log.info(f'TpDB set to {request.query_params["tpdb_enabled"]}')
                Config().tpdb_enabled = request.query_params["tpdb_enabled"]
                #print(f"CONFIG: tbdb_enabled = {Config().tpdb_enabled}")
                if Config().tpdb_enabled == 'false':
                    Config().tpdb_website_logos  = 'false'
                    Config().tpdb_autorename  = 'false'
                    Config().tpdb_actors  = 'false'
                    Config().tpdb_photos  = 'false'
                    Config().tpdb_websites = 'false'
                    Config().tpdb_tags = 0
                else:
                    if "tpdb_websitelogos" in request.query_params: Config().tpdb_website_logos = request.query_params["tpdb_websitelogos"]
                    if "tpdb_autorename" in request.query_params: Config().tpdb_autorename = request.query_params["tpdb_autorename"]
                    if "tpdb_actors" in request.query_params: Config().tpdb_actors = request.query_params["tpdb_actors"]
                    if "tpdb_photos" in request.query_params: Config().tpdb_photos = request.query_params["tpdb_photos"]
                    if "tpdb_websites" in request.query_params: Config().tpdb_websites = request.query_params["tpdb_websites"]
                    if "tpdb_tags" in request.query_params: Config().tpdb_tags = request.query_params["tpdb_tags"]
                Config().save()
                return Response(status=200)

        if "populate_websites" in request.query_params:
            if request.query_params["populate_websites"] == "True":
                if request.query_params["force"] == "true":
                    force = True
                else:
                    force = False
                threading.Thread(target=populate_websites, args=(force,)).start()
                return Response(status=200)

        if "tpdb_scan_all" in request.query_params:
            if request.query_params["tpdb_scan_all"] == "True":
                if request.query_params["force"] == "true":
                    force = True
                else:
                    force = False
                threading.Thread(target=tpdb_scanner, args=(force,)).start()

                return Response(status=200)

        if "scrapAllActors" in request.query_params:
            if request.query_params["scrapAllActors"] == "True":
                start = datetime.datetime.now()
                if request.query_params["force"] == "true":
                    force = True
                else:
                    force = False
                #scrape_all_actors(force)
                threading.Thread(target=scrape_all_actors, args=(force,)).start()
                #log.timer("Actor scraping", start, datetime.datetime.now())
                #return HttpResponse (f'Done scraping actors in {timer(start,datetime.datetime.now())}.')


                return Response(status=200)

        if "tagAllScenesIgnore" in request.query_params:

            threading.Thread(
                target=tag_all_scenes_ignore_last_lookup, args=(True,)
            ).start()
            # _thread.start_new_thread(tag_all_scenes_ignore_last_lookup, (), )
            return Response(status=200)

        elif "tagAllScenes" in request.query_params:

            threading.Thread(target=tag_all_scenes, args=(False,)).start()
            # _thread.start_new_thread(tag_all_scenes, (), )
            return Response(status=200)

        if "checkDupes" in request.query_params:
            if request.query_params["checkDupes"] == "True":
                print("Checking database for duplicates by hash...")
                start = datetime.datetime.now()
                total_saved = 0
                total_deleted = 0
                anumber = 0
                dupes=Scene.objects.values('hash').annotate(name_count=Count('hash')).exclude(name_count=1)
                log.info(f'There are {len(dupes)} duplicate scenes in your collection.')
                for scene_1 in dupes: #was: Scene.objects.all():
                    anumber += 1
                    amount=scene_1['name_count']-1
                    origscene=Scene.objects.filter(hash=scene_1['hash']).order_by('id')[:1][0]
                    sceneinfo=Scene.objects.filter(hash=scene_1['hash']).order_by('-id')[:amount]
                    nom=''
                    if amount!=1: nom = 's'
                    log.sinfo(f'Scene {origscene.pk} has {amount} duplicate{nom}.')
                    for scene_2 in sceneinfo:
                        if origscene.path_to_file == scene_2.path_to_file and not (scene_1.pk == scene_2.pk):
                            log.warn(f'Scene IDs {scene_1.pk} and {scene_2.pk} refer to the same file: {scene_1.path_to_file}')
                            break
                        if (not origscene.pk == scene_2.pk) or (not origscene.path_to_file == scene_2.path_to_file):
                            # if scene_2.path_to_file == scene_1.path_to_file:
                            #    print("!!! Found duplicate scene (exact path): " +
                            #    str(scene_1.id) + " - " + scene_1.name + "\nFile path: " + scene_1.path_to_file +
                            #    "\nis duplicate of " +
                            #    str(scene_2.id) + " - " + scene_2.name + "\nFile path: " + scene_2.path_to_file)
                            if scene_2.hash == origscene.hash and origscene.size == scene_2.size:
                                total_deleted += 1
                                total_saved = total_saved + scene_2.size
                                log.info(f'Confirmed! Removing duplicate scene ID {scene_2.pk} (hash: {scene_2.hash})')
                                # print("Passing ID " + str(scene_2.id) + " to delete function...")
                                permanently_delete_scene_and_remove_from_db(scene_2)
                            else:
                                log.warn('The scenes with ID {origscene.pk} and {scene_2.pk} are not identical!')
                if total_deleted > 0:
                    # print(f"Deleted {total_deleted} files, saving {sizeformat(total_saved)}")
                    log.info(f"Deleted {total_deleted} files, saving {sizeformat(total_saved)}")
                print('')
                log.timer("Duplicate check", start, datetime.datetime.now())
                return HttpResponse (f'Deleted {total_deleted} files, saving {sizeformat(total_saved)} in {timer(start,datetime.datetime.now())}.')
                #return Response(status=200)

        # populate_last_folder_name_in_virtual_folders()
        #    write_actors_to_file()
        #    clean_empty_folders()
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

        # get_files(TEST_PATH)

        if "cleanDatabase" in request.query_params:
            if request.query_params["cleanDatabase"]:
                start = datetime.datetime.now()
                scenes = Scene.objects.all()
                count = scenes.count()
                counter = 1
                print("Cleaning Scenes...")  # CooperDK This was enabled
                for scene in scenes:
                    print(f"Checking scene {counter} out of {count}\r", end="")
                    if not os.path.isfile(scene.path_to_file):
                        print(
                            f"File for scene {scene.name} does not exist in path {scene.path_to_file}"
                        )
                        permanently_delete_scene_and_remove_from_db(scene)
                    counter += 1
                print("\nFinished cleaning scenes...")

                print("Cleaning Aliases...")

                aliases = ActorAlias.objects.all()
                count = aliases.count()
                counter = 1
                for alias in aliases:
                    print(f"Checking Alias {counter} out of {count}\r", end="")
                    if alias.actors.count() == 0:
                        alias.delete()
                        print(f"Alias {alias.name} has no actor... deleting")
                    counter += 1
                print("\nFinished cleaning aliases...")

                print("Cleaning actor dirs that are no longer in database...")

                clean_dir("actor")
                print("Cleaning scene dirs that are no longer in database...")
                clean_dir("scenes")

                print("Cleaning website dirs that are no longer in database...")
                clean_dir("websites")
                log.timer("Database Cleanup", start, datetime.datetime.now())
                return HttpResponse (f'Performed database cleanup in {timer(start,datetime.datetime.now())}.')


        if "folderToScan" in request.query_params:
            start = datetime.datetime.now()
            if request.query_params["folderToScan"] != "":
                local_folder = LocalSceneFolders.objects.get(
                    id=int(request.query_params["folderToScan"])
                )
                videos.addScenes.get_files(local_folder.name, False)
            else:
                all_folders = LocalSceneFolders.objects.all()
                for folder in all_folders:
                    videos.addScenes.get_files(folder.name, False)
            log.timer("Folder scan", start, datetime.datetime.now())
            #print("\nDone.")
            return HttpResponse (f'Completed folder scan in {timer(start,datetime.datetime.now())}.')


@api_view(["GET"])
def ffmpeg(request):
    if request.method == "GET":
        if "generateSampleVideo" in request.query_params:
            if request.query_params["generateSampleVideo"]:
                scene_id = request.query_params["sceneId"]
                scene = Scene.objects.get(pk=scene_id)
                if scene.duration is None:
                    success_probe = ffmpeg_process.ffprobe_get_data_without_save(scene)
                    if success_probe:
                        success = ffmpeg_process.ffmpeg_create_sammple_video(scene)

                        if success:
                            return Response(status=200)
                        else:
                            return Response(status=500)

                success = ffmpeg_process.ffmpeg_create_sammple_video(scene)
                if success:
                    return Response(status=200)
                else:
                    return Response(status=500)


def add_comma_seperated_items_to_db(string_of_comma_seperated_items, type_of_item):
    for x in string_of_comma_seperated_items.split(","):

        if type_of_item == "actor":
            object_to_insert = Actor()
            object_to_insert.thumbnail = Config().unknown_person_image_path
        elif type_of_item == "scene tag":
            object_to_insert = SceneTag()
        elif type_of_item == "website":
            object_to_insert = Website()

        object_to_insert.strip = x.strip()
        object_to_insert.name = object_to_insert.strip

        try:
            if type_of_item == "actor":
                if not ActorAlias.objects.filter(name=object_to_insert.name):
                    object_to_insert.save()
                    print(
                        f"Added {type_of_item} {object_to_insert.name} To db"
                    )
            else:
                object_to_insert.save()
                print(f"Added {type_of_item} {object_to_insert.name} To db")
        except django.db.IntegrityError as e:
            # content = {'something whent wrong': e}
            print(
                f"{e} while trying to add {type_of_item} {object_to_insert.name}"
            )
            # return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddItems(views.APIView):
    def get(self, request, format=None):

        if request.query_params["folderToAddPath"] != "":
            folders_to_add_path = request.query_params["folderToAddPath"]
            for folder_to_add_path in folders_to_add_path.split(","):
                folder_to_add_path_stripped = folder_to_add_path.strip()
                if os.path.isdir(folder_to_add_path_stripped):
                    # if the second argument is true - tries to make a sample video when inserting scene to db.
                    temp = os.path.abspath(folder_to_add_path_stripped)

                    try:
                        if platform.system() == "Windows":
                            for test in Folder.objects.all():
                                if temp.lower() in test.name.lower(): # Check f the new folder exists in the set of registered paths
                                    raise Exception(f'Folder already registered')
                        if request.query_params["createSampleVideo"] == "true":
                            videos.addScenes.get_files(folder_to_add_path_stripped, True)
                        else:
                            videos.addScenes.get_files(folder_to_add_path_stripped, False)
                        local_scene_folder = LocalSceneFolders(name=temp)
                        local_scene_folder.save()
                        log.info(
                            f"Added folder {temp} to folder list..."
                        )
                    except (django.db.IntegrityError, Exception) as e:
                        log.error(
                            f"{e} while trying to add {temp} to folder list"
                        )



                else:
                    content = {"Path does not exist!": "Can't find path!"}
                    return Response(
                        content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        if request.query_params["actorsToAdd"] != "":
            add_comma_seperated_items_to_db(
                request.query_params["actorsToAdd"], "actor"
            )

        if request.query_params["sceneTagsToAdd"] != "":
            add_comma_seperated_items_to_db(
                request.query_params["sceneTagsToAdd"], "scene tag"
            )

        if request.query_params["websitesToAdd"] != "":
            add_comma_seperated_items_to_db(
                request.query_params["websitesToAdd"], "website"
            )

        return Response(status=200)


def play_scene_vlc(scene, random):
    file_path = os.path.normpath(scene.path_to_file)
    if platform.system() == "Windows":
        vlc_path = Config().vlc_path
    else:
        vlc_path = "vlc"
    p = subprocess.Popen([vlc_path, file_path])
    scene.play_count += 1
    scene.date_last_played = datetime.datetime.now()
    print(
        f"Play count for scene '{scene.name}' is now '{scene.play_count}' and the date the scene was last played is '{scene.date_last_played}'"
    )
    scene.save()

    for scene_tag in scene.scene_tags.all():
        scene_tag.play_count += 1
        print(
            f"Play count for scene tag '{scene_tag.name}' is now '{scene_tag.play_count}'"
        )
        scene_tag.save()

    for actor in scene.actors.all():
        actor.play_count += 1
        print(f"Play count for actor '{actor.name}' is now '{actor.play_count}'")
        actor.save()

    for website in scene.websites.all():
        website.play_count += 1
        print(
            f"Play count for site '{website.name}' is now '{website.play_count}'"
        )
        website.save()

    if random:
        if not Playlist.objects.filter(name="Random Plays"):
            pls = Playlist(name="Random Plays")
            pls.save()

        pls = Playlist.objects.filter(name="Random Plays").first()
        if not pls.scenes.filter(id=scene.id):
            pls.scenes.add(scene)
            pls.save()
            print(f"Added scene '{scene.name}' to Random Plays playlist.")
        else:
            print(f"Scene '{scene.name}' already in playlist Random Plays.")


@api_view(["GET", "POST"])
def play_in_vlc(request):
    scene = None
    random = True

    if request.method == "GET":
        if "sceneId" in request.query_params:
            scene_id = request.query_params["sceneId"]
            scene = Scene.objects.get(pk=scene_id)
            random = False
        elif "actor" in request.query_params and request.query_params["actor"] != "-6":
            actor_id = request.query_params["actor"]
            scene = Scene.objects.filter(actors=actor_id).order_by("?").first()
        elif (
            "sceneTag" in request.query_params
            and request.query_params["sceneTag"] != "-6"
        ):
            scene_tag_id = request.query_params["sceneTag"]
            scene = Scene.objects.filter(scene_tags=scene_tag_id).order_by("?").first()
        elif (
            "website" in request.query_params
            and request.query_params["website"] != "-6"
        ):
            website_id = request.query_params["website"]
            scene = Scene.objects.filter(websites=website_id).order_by("?").first()
        elif (
            "folder" in request.query_params and request.query_params["folder"] != "-6"
        ):
            folder_id = request.query_params["folder"]
            scene = (
                Scene.objects.filter(folders_in_tree=folder_id).order_by("?").first()
            )
        elif (
            "playlist" in request.query_params
            and request.query_params["playlist"] != "-6"
        ):
            playlist_id = request.query_params["playlist"]
            scene = Scene.objects.filter(playlists=playlist_id).order_by("?").first()
        else:
            scene = Scene.objects.order_by("?").first()

        if scene:
            play_scene_vlc(scene, random)
            return Response(status=200)
        else:
            return Response(status=500)


class PlayInVlc(views.APIView):
    def get(self, request, format=None):
        scene_id = request.query_params["sceneId"]
        scene = Scene.objects.get(pk=scene_id)

        play_scene_vlc(scene)

        return Response(status=200)

def dorename(scene_id: int, force: bool):
    from utils import scenerenamer as renamer
    result = renamer.rename(scene_id, force)
    return result

class renameScene(views.APIView):
    def get (self, request, format=None):
        from utils import scenerenamer as renamer
        scene_id = request.query_params["sceneId"]
        force = request.query_params["force"]

        result = dorename(scene_id, force)
        if not result:
            return Response(status=500)
        else:
            return Response(status=200)

def open_file_cross_platform(path):
    if platform.system() == "Windows":
        #os.startfile(path)
        # This command will open the location of the file with the file selected
        # explorer.exe /select,"C:\Folder\subfolder\file.txt"
        print('explorer.exe /select "' + path + '"')
        subprocess.Popen(r'explorer.exe /select,"' + path + '"')

    else:
        opener = "open" if platform.system() == "Darwin" else "xdg-open"
        subprocess.call([opener, path])


class OpenFolder(views.APIView):
    def get(self, request, format=None):
        path = request.query_params["path"]
        open_file_cross_platform(path)
        return Response(status=200)


class AssetAdd(views.APIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(self, request, format=None):
        # my_file = request.FILES['file']
        save_path = Config().temp_path

        # os.path.abspath('D:\\aria2')
        save_file_name = "temp.jpg"

        save_dest = os.path.join(save_path, save_file_name)
        #
        # if request.FILES['file']:
        #     # multi part file upload
        #     print ("multiPart")
        #     current_path = os.path.dirname(__file__)
        #     # filename = '/static/myfile.jpg'
        #     filename = save_dest
        #     with open(filename, 'wb+') as temp_file:
        #         for chunk in my_file.chunks():
        #             temp_file.write(chunk)
        #
        #     my_saved_file = open(filename)  # there you go
        #     return Response(status=200)

        if request.data["file"]:
            # print (request.data['file'])
            data = request.data["file"]
            if data.startswith("data:image"):
                # base64 encoded image - decode
                format, imgstr = data.split(";base64,")  # format ~= data:image/X,
                ext = format.split("/")[-1]  # guess file extension
                # id = uuid.uuid4()
                # data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)
                with open(save_dest, "wb") as fh:
                    fh.write(base64.decodebytes(imgstr.encode("utf-8")))

                if request.data["type"] == "Actor":
                    actor = Actor.objects.get(pk=request.data["id"])

                    current_tumb = os.path.abspath(os.path.join(
                        Config().site_media_path,
                        "actor",
                        f"{actor.id}",
                        "profile",
                        "profile.jpg",
                    ))
                    log.sinfo(f"Profile thumbnail set: {current_tumb}")

                    rel_path = os.path.relpath(current_tumb, start="data")
                    as_uri = urllib.request.pathname2url(rel_path)

                    actor.thumbnail = as_uri
                    actor.save()

                    try:
                        if not os.path.exists(current_tumb):
                            os.makedirs(os.path.dirname(current_tumb))
                        shutil.move(save_dest, current_tumb)
                    except (IOError, OSError) as exc:
                        log.warn(f"PROFILEPIC: {exc}")
            return Response(status=200)

        return Response(status=500)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data["file"]

        print("got file")

        return Response(status=204)

def angular_index(request):

    return render(request, os.path.join("videos","angular","index.html"))


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "actor_alias": reverse(
                "actor-alias-list-rest", request=request, format=format
            ),
            "actor": reverse("actors-list-rest", request=request, format=format),
        }
    )


class ActorAliasHTMLRest(generics.GenericAPIView):
    queryset = ActorAlias.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        alias = self.get_object()
        return Response(alias.name)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PlaylistListSerializer
        else:
            return PlaylistSerializer


class LocalSceneFoldersViewSet(viewsets.ModelViewSet):
    queryset = LocalSceneFolders.objects.all()
    serializer_class = LocalSceneFoldersSerializer


class FolderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Folder.objects.all()

        return search_in_get_queryset(queryset, self.request)

    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class WebsiteViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Website.objects.all()

        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == "list":
            return WebsiteIdNameSerailzier
        else:
            return WebsiteSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer


class SceneTagViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = SceneTag.objects.all()

        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == "list":
            return SceneTagIdNameSerialzier
        else:
            return SceneTagSerializer

    queryset = ActorTag.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    queryset = SceneTag.objects.all()
    serializer_class = SceneTagSerializer


class SceneViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Scene.objects.all()
        # queryset = self.get_serializer_class().setup_eager_loading(queryset,queryset)
        queryset = SceneListSerializer.setup_eager_loading(queryset, queryset)
        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == "list":
            return SceneListSerializer
        else:
            return SceneSerializer

    queryset = Scene.objects.all()
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)

    # serializer_class = SceneSerializer


class ActorTagViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = ActorTag.objects.all()

        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == "list":
            return ActorTagListSerializer
        else:
            return ActorTagSerializer

    queryset = ActorTag.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    # serializer_class = ActorTagSerializer


class ActorAliasViewSet(viewsets.ModelViewSet):
    """
      This viewset automatically provides `list`, `create`, `retrieve`,
      `update` and `destroy` actions.

      Additionally we also provide an extra `highlight` action.
    """

    def get_queryset(self):
        # random order
        # queryset = Actor.objects.all().order_by('?')
        term = "name"
        queryset = ActorAlias.objects.all()

        # **{term: term}
        res_qs = search_in_get_queryset(queryset, self.request)

        return res_qs

    queryset = ActorAlias.objects.all()
    serializer_class = ActorAliasSerializer


class ActorViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # random order
        # queryset = Actor.objects.all().order_by('?')

        queryset = Actor.objects.all()

        # **{term: term}
        res_qs = search_in_get_queryset(queryset, self.request)
        return res_qs

    def get_serializer_class(self):
        if self.action == "list":
            return ActorListSerializer
        else:
            return ActorSerializer

    # filter_backends = (filters.SearchFilter,)
    # ordering_fields = '__all__'
    # search_fields = ('name',)
    queryset = Actor.objects.all()
    # serializer_class = ActorSerializer


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data

@api_view(["GET", "POST"])
def display_video(request):

    sceneid = request.path
    sceneid = sceneid.split('/')[-1]
    scene = Scene.objects.get(pk=sceneid)
    pathname = scene.path_to_file
    path = pathname
    size = os.path.getsize(path)
    now = datetime.datetime.now()
    if scene.date_last_played is not None:
        then = scene.date_last_played
    else:
        then = datetime.datetime.now() - timedelta(hours = 12)
    if now > then + timedelta(hours=2):
        log.sinfo(f"Playback: [{pathname}] ({size//1048576} MB)")#1048576 is 1024^2
        scene.play_count+=1
        scene.date_last_played=datetime.datetime.now()
        scene.save()
        log.sinfo(f"Playback count {scene.play_count} for scene ID {scene.id}. Last played date/time updated.")


    range_header = request.META.get('HTTP_RANGE', '').strip()     #request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 8 # 8M per piece, the maximum volume of the response body
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
                 # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
    #except requests.exceptions.ConnectionError
    #    print("Error")
    #    pass

    '''
        from django.http import StreamingHttpResponse
        from wsgiref.util import FileWrapper
        from datetime import timedelta
        import mimetypes
        
        cont = 0
     
        def read_video(path):
            
            with open(path, 'rb') as f:
                while True:
                    data = f.read(10 * 1024)
                    if data:
                        yield data
                        cont = 1
                    else:
                        break
    
        #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #if x is None:
            #return HttpResponse("No Video")
        sceneid = x.path
        sceneid = sceneid.split('/')[-1]
        print (f"Requesting scene ID {sceneid}...\r", end="")
        scene = Scene.objects.get(pk=sceneid)
        pathname = scene.path_to_file
        size = scene.size
        
        now = datetime.datetime.now()
        if scene.date_last_played is not None:
            then = scene.date_last_played
        else:
            then = datetime.datetime.now() - timedelta(hours = 12)
        if now > then + timedelta(hours=3):
            print (f"Playback: [{pathname}] ({size//1048576} MB)")#1048576 is 1024^2
            scene.play_count+=1
            scene.date_last_played=datetime.datetime.now()
            scene.save()
            print(f"Play count for scene {scene.id} is now {scene.play_count} and the last played date and time is updated.")
        
            response = StreamingHttpResponse(FileWrapper(open(pathname, 'rb'), 8192),
                content_type=mimetypes.guess_type(pathname)[0]) #(open(pathname, 'rb')) #(read_video(pathname), status=206)
            #response = StreamingHttpResponse(read_video(pathname)) #(open(pathname, 'rb')) #(read_video(pathname), status=206)
            #response['Content-Length'] = size
            #response['Content-Disposition'] = "attachment; filename=%s" % filename
        #response["Content-Range"] = 'bytes 0-%s' % (size)
        #response['Content-Disposition'] = f'attachement; filename="{pathname}"'
    except:
        print("Error")
    return response
'''