import math
import re
import os.path
import subprocess
import traceback

import django.db

from django.shortcuts import render
import requests
import requests.packages.urllib3
import videos.addScenes
import videos.filename_parser as filename_parser

from videos.scrapers.freeones import scanner_freeones
from videos.scrapers.imdb import scanner_imdb
from videos.scrapers.scanner_common import scanner_common
from videos.scrapers.scanner_tpdb import scanner_tpdb
from videos.scrapers.tmdb import scanner_tmdb

from videos import ffmpeg_process
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import mimetypes
from datetime import timedelta
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
import videos.const as const
from django.utils.datastructures import MultiValueDictKeyError
import threading
import videos.startup
import logging
log = logging.getLogger(__name__)
import http.client

http.client._MAXHEADERS = 1000

def get_scenes_in_folder_recursive(folder, scene_list):
    scenes = list(folder.scenes.all())
    scene_list = list(chain(scene_list, scenes))

    for child in folder.children.all():
        scene_list = get_scenes_in_folder_recursive(child, scene_list)

    return scene_list

def get_folders_recursive(folder, folder_list):
    folder_list = []

    for child in folder.children.all():
        temp_list = get_folders_recursive(child, folder_list)

        folders = list(folder.children.all())
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
        log.warning("Recursive is TRUE!!!!")
        log.info(request.query_params["folders_in_tree"])
        folder = Folder.objects.get(pk=int(request.query_params["folders_in_tree"]))
        qs_list = get_scenes_in_folder_recursive(folder, qs_list)
        log.info(qs_list)
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
                term_string = request.query_params.get(qp, None)

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
                                    log.info(getattr(i, qp).all())
                                    x = getattr(i, qp).all()
                                    for item in getattr(i, qp).all():
                                        if item.id == term:
                                            t_list.append(i)
                                            break
                                elif (getattr(i, qp)) == term:
                                    t_list.append(i)
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
            qs_list = list(original_queryset)

    if term_is_not_null:
        if random:
            shuffle(qs_list)
            return qs_list
        else:
            if "-" in sort_by:
                reverseSort = True
            else:
                reverseSort = False
            sort_by = sort_by.replace("-", "")

            if sort_by == "usage_count":
                temp_list = sorted(qs_list, reverse=reverseSort, key=lambda k: k.actors.count())
            else:
                temp_list = sorted(qs_list, reverse=reverseSort,
                    key=lambda k: (
                        lambda_attrgetter(sort_by, k) is None,
                        lambda_attrgetter(sort_by, k) == "",
                        lambda_attrgetter(sort_by, k),
                    )
                )

            return temp_list
    else:
        if random:
            return original_queryset.order_by("?")
        else:
            return original_queryset.order_by(sort_by)

def populate_websites(force):

    ### Populates website logos, URLs and checks YAPO website names against TpDB names.
    ### Force will re-download logos.

    import videos.aux_functions as aux
    if not aux.is_domain_reachable("api.metadataapi.net"):
        return Response(status=500)

    log.info(f"Traversing websites for logos...")

    # if current_scene.tpdb_id is not None and current_scene.tpdb_id != "" and len(current_scene.tpdb_id) > 12:
    #     parsetext = current_scene.tpdb_id
    url = 'https://api.metadataapi.net/sites'

    params = {'limit': 99999}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'YAPO e+ 0.71',
    }
    response = requests.request('GET', url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()

    websites = Website.objects.all()
    for site in websites:
        oldname = site.name
        for tpdb in response['data']:
            found = False
            tsid = tpdb['id']
            tsn = tpdb['name']
            tss = tpdb['short_name']
            tsurl = tpdb['url']
            tslogo = tpdb['logo']

            if site.name == tsn:
                found = True

            if (site.name != tsn) and (site.name.lower() == tsn.lower()):
                log.warning(f'Renaming site "{site.name}" to "{tsn}" for consistency')
                site.name = tsn
                found = True

            if (site.name.lower() == tss.lower()) and (site.name.lower() != tsn.lower()):
                log.warning(f'Renaming site "{site.name}" to "{tsn}" because it is truncated')
                site.name = tsn
                found = True

            if found:
                newname = site.name
                try:
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
                    log.error(f'Attempting to rename {oldname} to {newname} resulted in an error. New name probably already exists!')
                    break
    log.info("Done.")

    return Response(status=200)

def scrape_all_actors(force):
    try:
        _scrape_all_actors(force)
    except Exception as e:
        log.exception(f"While attempting to scrape actors: {e} at {traceback.format_exc()}")

def _scrape_all_actors(force):
    actors = Actor.objects.all()

    for actor in actors:
        if not force and actor.last_lookup is not None:
            log.info(f"{actor.name} was already searched")
            return Response(status=200)

        for scanner in ( scanner_tmdb(), scanner_tpdb(), scanner_imdb(), scanner_freeones() ):
            scanner.search_person_with_force_flag(actor, force)

    log.info("Done scraping actors.")
    return Response(status=200)

def tag_all_scenes(ignore_last_lookup):
    if Config().current_setting_version < 3:
        for actorTag in ActorTag.objects.all():
            if not SceneTag.objects.filter(name=actorTag.name):
                SceneTag.objects.create(name=actorTag.name)

            scene_tag_to_add = SceneTag.objects.get(name=actorTag.name)
            actorTag.scene_tags.add(scene_tag_to_add)
            scenetag=SceneTag.objects.filter(name=actorTag.name)
            log.info(f"Added scene tag {scenetag} to actor tag {actorTag.name}")

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
            log.info(f"Added scene tag {scenetag} to actor tag {actorTag.name}")

    filename_parser.parse_all_scenes(True)
    return Response(status=200)

# views

class scanScene(views.APIView):
    def get(self, request, format=None):

        search_site = request.query_params["scanSite"]
        scene_id = request.query_params["scene"]

        if request.query_params["force"] == "true":
            force = True
        else:
            force = False
        log.info("Now entering the TPDB scene scanner API REST view")

        success = scanner_tpdb().scan_scene(scene_id, force)

        if success:
            return Response(status=200)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ScrapeActor(views.APIView):

    def get(self, request, format=None):
        search_site = request.query_params["scrapeSite"]
        actor_id = request.query_params["actor"]
        if request.query_params["force"] == "true":
            force = True
        else:
            force = False

        log.info("Now entering the scrape actor API REST view")
        log.info(f"Scanning for {Actor.objects.get(pk=actor_id).name} on {search_site}")

        actor_to_search = Actor.objects.get(pk=actor_id)
        scanner = scanner_common.createForSite(search_site)
        if scanner is None:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        success = scanner.search_person_with_force_flag(actor_to_search, force)
        if success:
            return Response(status=200)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def permanently_delete_scene_and_remove_from_db(scene):
    success_delete_file = deletePath(scene.path_to_file)
    success_delete_media_path = deletePath(scene.get_media_dir(createIfNotExisting = False))

    if success_delete_file and success_delete_media_path:
        scene.delete()
        log.info(f"Removed '{scene.name}' from database")

# Deletes a path, returning True if the path does not exist, or False if some error occured.
def deletePath(pathToDelete):
    if not os.path.exists(pathToDelete):
        return True

    try:
        shutil.rmtree(pathToDelete)
        log.info(f"Deleted '{pathToDelete}'")
        return True
    except OSError as e:
        log.error(f"Got OSError while trying to delete {e.filename} : Error number:{e.errno} Error:{e.strerror}")
        return False

def checkDupeHash(hash):
    from django.db import connection

    cursor = connection.cursor()

    cursor.execute("SELECT count(*) from videos_scene WHERE hash = %s", [hash])
    dupecount = cursor.fetchone()
    return dupecount[0]

@api_view(["GET", "POST"])
def tag_multiple_items(request):
    if request.method == "POST":

        params = request.data["params"]

        if params["type"] == "scene":
            log.info("Patching scene")

            if params["patchType"] == "websites":

                website_id = params["patchData"][0]
                website_to_add = Website.objects.get(pk=website_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.add(website_to_add)
                        log.info(f"Added Website '{website_to_add.name}' to scene '{scene_to_update.name}'")

                        if website_to_add.scene_tags.count() > 0:
                            for tag in website_to_add.scene_tags.all():
                                scene_to_update.scene_tags.add(tag)
                                log.info(f"Added Scene Tag '{tag.name}' to scene '{scene_to_update.name}'")

                        scene_to_update.save()
                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.remove(website_to_add)
                        log.info(f"Removed Website '{website_to_add.name}' from scene '{scene_to_update.name}'")
                        if website_to_add.scene_tags.count() > 0:
                            for tag in website_to_add.scene_tags.all():
                                if tag in scene_to_update.scene_tags.all():
                                    scene_to_update.scene_tags.remove(tag)
                                    log.info(f"Removed Scene Tag '{tag.name}' from scene '{scene_to_update.name}'")
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
                        log.info(f"Added Scene Tag '{scene_tag_to_add.name}' to scene '{scene_to_update.name}'")

                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.scene_tags.remove(scene_tag_to_add)
                        scene_to_update.save()
                        log.info(f"Removed Scene Tag '{scene_tag_to_add.name}' from scene '{scene_to_update.name}'")
            elif params["patchType"] == "actors":
                actor_id = params["patchData"][0]
                actor_to_add = Actor.objects.get(pk=actor_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.add(actor_to_add)
                        log.info(f"Added Actor '{actor_to_add.name}' to scene '{scene_to_update.name}'")

                        if actor_to_add.actor_tags.count() > 0:
                            for actor_tag in actor_to_add.actor_tags.all():
                                scene_to_update.scene_tags.add(
                                    actor_tag.scene_tags.first()
                                )
                                log.info(f"Added Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{scene_to_update.name}'")

                        scene_to_update.save()

                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.remove(actor_to_add)
                        log.info(f"Removed Actor '{actor_to_add.name}' from scene '{scene_to_update.name}'")

                        if actor_to_add.actor_tags.count() > 0:
                            for actor_tag in actor_to_add.actor_tags.all():
                                if (
                                    actor_tag.scene_tags.first()
                                    in scene_to_update.scene_tags.all()
                                ):
                                    scene_to_update.scene_tags.remove(
                                        actor_tag.scene_tags.first()
                                    )
                                    log.info(f"Removed Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{scene_to_update.name}'")
                        scene_to_update.save()

            elif params["patchType"] == "delete":
                scenes_to_update = params["itemsToUpdate"]

                if params["permDelete"]:
                    log.warning("permDelete true")
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        permanently_delete_scene_and_remove_from_db(scene_to_update)
                        log.info(f"Removed scene '{scene_to_update.name}'")
                else:
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.delete()
                        log.info(f"Removed scene '{scene_to_update.name}' from database")

            elif params["patchType"] == "playlists":
                playlist_id = params["patchData"][0]
                playlist_to_add = Playlist.objects.get(pk=playlist_id)
                scenes_to_update = params["itemsToUpdate"]

                if params["addOrRemove"] == "add":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.playlists.add(playlist_to_add)
                        log.info(f"Scene '{scene_to_update.name}' was added to playlist '{playlist_to_add.name}'")
                        scene_to_update.save()
                if params["addOrRemove"] == "remove":
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.playlists.remove(playlist_to_add)
                        log.info(f"Scene '{scene_to_update.name}' was removed to playlist '{playlist_to_add.name}'")
                        scene_to_update.save()
            else:
                scenes_to_update = params["itemsToUpdate"]
                for x in scenes_to_update:
                    scene_to_update = Scene.objects.get(pk=x)
                    patch_type = params["patchType"]
                    patch_data = params["patchData"]
                    setattr(scene_to_update, patch_type, patch_data)

                    log.info(f"Set scene's '{scene_to_update}' attribute '{patch_type}' to '{patch_data}'")
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
                        log.info(f"Added Actor Tag '{actor_tag_to_add.name}' to actor {actor_to_update.name}")
                elif params["addOrRemove"] == "remove":
                    for x in actors_to_update:
                        actor_to_update = Actor.objects.get(pk=x)
                        actor_to_update.actor_tags.remove(actor_tag_to_add)
                        actor_to_update.save()
                        log.info(f"Removed Actor Tag '{actor_tag_to_add.name}' to actor {actor_to_update.name}")
            else:
                actors_to_update = params["itemsToUpdate"]
                for x in actors_to_update:
                    actor_to_update = Actor.objects.get(pk=x)
                    patch_type = params["patchType"]
                    patch_data = params["patchData"]
                    setattr(actor_to_update, patch_type, patch_data)
                    log.info(f"Set actors's '{actor_to_update}' attribute '{patch_type}' to '{patch_data}'")
                    actor_to_update.save()

        return Response(status=200)

def clean_dir(modelType : ModelWithMediaContent):
    dir_to_clean = os.path.join(Config().site_media_path, modelType.get_media_dir_static())
    number_of_folders = len(os.listdir(dir_to_clean))
    index = 1

#    modelTypeName = str(modelType.name.field).split('.')[-2:-1][0]

    for dir_in_path in os.listdir(dir_to_clean):
#        log.info(f"Checking {modelTypeName} folder {index} out of {number_of_folders}")

        # The original Yapo-e-plus code skips any directory names which are not integers, so we do too.
        try:
            dir_in_path_int = int(dir_in_path)
        except ValueError:
            log.error(f"Dir name '{dir_in_path}' Could not be converted to an integer, skipping...")
            index += 1
            continue

        dir_with_path = os.path.join(dir_to_clean, dir_in_path)

        if len(modelType.objects.filter(pk=dir_in_path_int)) == 0:
            log.warning(f"ID {dir_in_path_int} is not in the database... Deleting folder {dir_with_path}")
            shutil.rmtree(dir_with_path)

        index += 1


# returns a human-readable filesize depending on the file's size
def sizeformat (b: int) -> str:
    if b < 1024:
        return f"{b} bytes"
    elif b < math.pow(1024, 2):
        return f"{b/1024:.1f} kilobytes"
    elif b < math.pow(1024, 3):
        return f"{b/math.pow(1024, 2):.1f} megabytes"
    elif b < math.pow(1024, 4):
        return f"{b/math.pow(1024, 3):.1f} gigabytes"
    else:
        return f"{b/math.pow(1024, 4):.1f} terabytes"

@api_view(["GET", "POST"])
def settings(request):
    if request.method == "GET":
        if "pathToVlc" in request.query_params:
            if request.query_params["pathToVlc"] == "":
                serializer = SettingsSerializer(Config().get_old_settings_as_json())
                return Response(serializer.data)

            new_path_to_vlc = os.path.abspath(request.query_params["pathToVlc"]).replace("\\","/")
            log.info(f'VLC path set to {request.query_params["pathToVlc"]}')

            if os.path.isfile(new_path_to_vlc):
                Config().vlc_path = new_path_to_vlc
                Config().save()
                return Response(status=200)

            log.error("VLC path does not exist!")
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

        if "tpdb_settings" in request.query_params:
            if "tpdb_enabled" in request.query_params:
                log.info(f'TpDB set to {request.query_params["tpdb_enabled"]}')
                Config().tpdb_enabled = request.query_params["tpdb_enabled"]
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

                def tpdb_scanner_thread(forceScan):
                    allScenes = Scene.objects.all()
                    for sceneToScan in allScenes:
                        scanner_tpdb().scan_scene(sceneToScan.id, forceScan)
                threading.Thread(target=tpdb_scanner_thread, args=(force,)).start()

                return Response(status=200)

        if "scrapeAllActors" in request.query_params:
            if request.query_params["scrapeAllActors"] == "True":
                if request.query_params["force"] == "true":
                    force = True
                else:
                    force = False
                threading.Thread(target=scrape_all_actors, args=(force,)).start()

                return Response(status=200)

        if "tagAllScenesIgnore" in request.query_params:
            threading.Thread(
                target=tag_all_scenes_ignore_last_lookup, args=(True,)
            ).start()
            return Response(status=200)

        elif "tagAllScenes" in request.query_params:
            threading.Thread(target=tag_all_scenes, args=(False,)).start()
            return Response(status=200)

        if "checkDupes" in request.query_params:
            if request.query_params["checkDupes"] == "True":
                log.info("Checking database for duplicates by hash...")
                total_saved = 0
                total_deleted = 0
                anumber = 0
                for scene_1 in Scene.objects.all():
                    anumber += 1
                    log.info(f"Checked {anumber}...")
                    if checkDupeHash(scene_1.hash) > 1:
                        log.info(f"Scene {scene_1.id} at least one dupe, scanning...")
                        for scene_2 in Scene.objects.all():
                            if scene_1.path_to_file == scene_2.path_to_file:
                                log.warning(f"Scene IDs {scene_1.pk} and {scene_2.pk} refer to the same file: {scene_1.path_to_file}")
                                break
                            if (not scene_1.pk == scene_2.pk) or (not scene_1.path_to_file == scene_2.path_to_file):
                                if scene_2.hash == scene_1.hash:
                                    total_deleted += 1
                                    total_saved = total_saved + scene_2.size
                                    log.warning(f"Confirmed! Duplicate scene info: {scene_2.id} - {scene_2.path_to_file} Hash: {scene_2.hash}")
                                    permanently_delete_scene_and_remove_from_db(scene_2)
                if total_deleted > 0:
                    log.info(f"Deleted {total_deleted} files, saving {sizeformat(total_saved)}")
                return Response(status=200)

        if "cleanDatabase" in request.query_params:
            if request.query_params["cleanDatabase"]:
                scenes = Scene.objects.all()
                count = scenes.count()
                counter = 1
                log.info("Cleaning Scenes...")
                for scene in scenes:
                    log.info(f"Checking scene {counter} out of {count}")
                    if not os.path.isfile(scene.path_to_file):
                        log.info(f"File for scene {scene.name} does not exist in path {scene.path_to_file}")
                        permanently_delete_scene_and_remove_from_db(scene)
                    counter += 1
                log.info("Finished cleaning scenes...")

                log.info("Cleaning Aliases...")
                aliases = ActorAlias.objects.all()
                count = aliases.count()
                counter = 1
                for alias in aliases:
                    log.info(f"Checking Alias {counter} out of {count}")
                    if alias.actors.count() == 0:
                        alias.delete()
                        log.info(f"Alias {alias.name} has no actor... deleting")
                    counter += 1
                log.info("Finished cleaning aliases...")

                log.info("Cleaning actor dirs that are no longer in database...")
                clean_dir(Actor)
                log.info("Cleaning scene dirs that are no longer in database...")
                clean_dir(Scene)
                log.info("Cleaning website dirs that are no longer in database...")
                clean_dir(Website)
                return Response(status=200)

        if "folderToScan" in request.query_params:
            if request.query_params["folderToScan"] != "":
                local_folder = LocalSceneFolders.objects.get(
                    id=int(request.query_params["folderToScan"])
                )
                videos.addScenes.get_files(local_folder.name, False)
            else:
                all_folders = LocalSceneFolders.objects.all()
                for folder in all_folders:
                    videos.addScenes.get_files(folder.name, False)
            log.info("Done.")
            return Response(status=200)

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
            object_to_insert.thumbnail = const.UNKNOWN_PERSON_IMAGE_PATH
        elif type_of_item == "scene tag":
            object_to_insert = SceneTag()
        elif type_of_item == "website":
            object_to_insert = Website()
        else:
            raise Exception("Unknown type_of_item")

        object_to_insert.strip = x.strip()
        object_to_insert.name = object_to_insert.strip

        try:
            if type_of_item == "actor":
                if not ActorAlias.objects.filter(name=object_to_insert.name):
                    object_to_insert.save()
                    log.info(f"Added {type_of_item} {object_to_insert.name} To db")
            else:
                object_to_insert.save()
                log.info(f"Added {type_of_item} {object_to_insert.name} To db")
        except django.db.IntegrityError as e:
            log.error(f"{e} while trying to add {type_of_item} {object_to_insert.name}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddItems(views.APIView):
    def get(self, request, format=None):

        if request.query_params["folderToAddPath"] != "":
            folders_to_add_path = request.query_params["folderToAddPath"]

            for folder_to_add_path in folders_to_add_path.split(","):
                folder_to_add_path_stripped = folder_to_add_path.strip()
                if not os.path.isdir(folder_to_add_path_stripped):
                    content = {"Path does not exist!": "Can't find path!"}
                    return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # if the second argument is true - tries to make a sample video when inserting scene to db.
                if request.query_params["createSampleVideo"] == "true":
                    videos.addScenes.get_files(folder_to_add_path_stripped, True)
                else:
                    videos.addScenes.get_files(folder_to_add_path_stripped, False)

                temp = os.path.abspath(folder_to_add_path_stripped)
                local_scene_folder = LocalSceneFolders(name=temp)
                try:
                    local_scene_folder.save()
                    log.info(f"Added folder {local_scene_folder.name} to folder list...")
                except django.db.IntegrityError as e:
                    log.error(f"{e} while trying to add {local_scene_folder.name} to folder list")

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
    subprocess.Popen([vlc_path, file_path])
    scene.play_count += 1
    scene.date_last_played = datetime.datetime.now()
    log.info(
        f"Play count for scene '{scene.name}' is now '{scene.play_count}' and the date the scene was last played is '{scene.date_last_played}'"
    )
    scene.save()

    for scene_tag in scene.scene_tags.all():
        scene_tag.play_count += 1
        log.info(f"Play count for scene tag '{scene_tag.name}' is now '{scene_tag.play_count}'")
        scene_tag.save()

    for actor in scene.actors.all():
        actor.play_count += 1
        log.info(f"Play count for actor '{actor.name}' is now '{actor.play_count}'")
        actor.save()

    for website in scene.websites.all():
        website.play_count += 1
        log.info(f"Play count for site '{website.name}' is now '{website.play_count}'")
        website.save()

    if random:
        if not Playlist.objects.filter(name="Random Plays"):
            pls = Playlist(name="Random Plays")
            pls.save()

        pls = Playlist.objects.filter(name="Random Plays").first()
        if not pls.scenes.filter(id=scene.id):
            pls.scenes.add(scene)
            pls.save()
            log.info(f"Added scene '{scene.name}' to Random Plays playlist.")
        else:
            log.info(f"Scene '{scene.name}' already in playlist Random Plays.")


@api_view(["GET", "POST"])
def play_in_vlc(request):
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

        play_scene_vlc(scene, False)

        return Response(status=200)

def open_file_cross_platform(path):
    if platform.system() == "Windows":
        os.startfile(path)
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
        reqDataFile = request.data.get("file", None)
        reqDataType = request.data.get("type", None)
        reqDataID = request.data.get("id", None)

        if None in (reqDataFile, reqDataType, reqDataID):
            return Response(status=500)

        return self.handle_post_request(reqDataFile, reqDataType, reqDataID)

    def handle_post_request(self, dataFile, dataType, dataID):
        # The only object we support updating here is Actor.
        if dataType != "Actor":
            return Response(status=500)

        # Get the object to update, bailing if it doesn't exist
        actor = Actor.objects.get(pk=dataID)

        # We expect a base64-encoded image.
        if not dataFile.startswith("data:image"):
            return Response(status=500)

        # Decode the image to a temporary file
        save_dest = os.path.join(Config.temp_path, "temp.jpg")
        try:
            format, imgstr = dataFile.split(";base64,")
            with open(save_dest, "wb") as fh:
                fh.write(base64.decodebytes(imgstr.encode("utf-8")))

            # set the actor's thumbnail path, and copy the temporary file to the new location.
            thumnbail_path = actor.generateThumbnailPath()
            if os.path.exists(thumnbail_path):
                os.remove(thumnbail_path)
            shutil.move(save_dest, thumnbail_path)

            actor.thumbnail = actor.getThumbnailPathURL()
            actor.save()
        finally:
            # Delete the temporary file before we return
            if os.path.exists(save_dest):
                os.remove(save_dest)

        return Response(status=200)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data["file"]

        log.info("got file")

        return Response(status=status.HTTP_204_NO_CONTENT)

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

class LogViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = LogEntry.objects.all()

        return search_in_get_queryset(queryset, self.request)
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer

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

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    queryset = SceneTag.objects.all()
    serializer_class = SceneTagSerializer


class SceneViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Scene.objects.all()
        queryset = SceneListSerializer.setup_eager_loading(queryset, queryset)
        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == "list":
            return SceneListSerializer
        else:
            return SceneSerializer

    queryset = Scene.objects.all()

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

class ActorAliasViewSet(viewsets.ModelViewSet):
    """
      This viewset automatically provides `list`, `create`, `retrieve`,
      `update` and `destroy` actions.

      Additionally we also provide an extra `highlight` action.
    """

    def get_queryset(self):
        # random order
        queryset = ActorAlias.objects.all()
        res_qs = search_in_get_queryset(queryset, self.request)

        return res_qs

    queryset = ActorAlias.objects.all()
    serializer_class = ActorAliasSerializer


class ActorViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # random order
        queryset = Actor.objects.all()
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

    if now > then + timedelta(hours=3):
        log.info(f"Requesting scene ID {sceneid}...")
        log.info(f"Playback: [{pathname}] ({sizeformat(size)})")
        scene.play_count+=1
        scene.date_last_played=datetime.datetime.now()
        scene.save()
        log.info(f"Play count for scene {scene.id} is now {scene.play_count} and the last played date and time is updated.")

    range_header = request.META.get('HTTP_RANGE', '').strip()
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
