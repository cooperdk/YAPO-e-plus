import os.path
import subprocess
import _thread

import django.db
import errno
from django.shortcuts import render

import json
import videos.addScenes
import videos.filename_parser as filename_parser
import videos.freeones_search
import videos.tmdb_search
from videos import ffmpeg_process
import urllib.request
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
import videos.const as const
from django.utils.datastructures import MultiValueDictKeyError
import threading

import pathlib


# Aux Functions

def get_scenes_in_folder_recursive(folder, scene_list):
    scenes = list(folder.scenes.all())
    scene_list = list(chain(scene_list, scenes))

    if folder.children.count() == 0:
        return scene_list

    else:
        for child in folder.children.all():
            scene_list = get_scenes_in_folder_recursive(child, scene_list)

        return scene_list


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

    if 'search' in request.query_params:
        search_string = request.query_params['search']
        if search_string:
            search_field = request.query_params['searchField']

            # if request.query_params['pageType']:
            #     if request.query_params['pageType'] == 'DbFolder':
            #         if request.query_params['parent']:
            #             folder = Folder.objects.get(pk=int(request.query_params['parent']))
            #             qs_list = get_folders_recursive(folder, qs_list)
            #             term_is_not_null = True
            #             tmp_list = list()
            #             for i in qs_list:
            #                 if search_string in getattr(i,search_field):
            #                     tmp_list.append(i)
            #
            #             qs_list = tmp_list

            if search_string.startswith('<'):
                string_keyarg = search_field + "__lte"
                search_string = search_string.replace('<', '')
            elif search_string.startswith('>'):
                string_keyarg = search_field + "__gte"
                search_string = search_string.replace('>', '')
            else:
                string_keyarg = search_field + "__icontains"

            if search_string:
                original_queryset = original_queryset.filter(**{string_keyarg: search_string})
                was_searched = True
                # qs_list = [i for i in qs_list if (search_string in i.name)]
        else:
            if request.query_params['pageType']:
                if request.query_params['pageType'] == 'DbFolder':
                    original_queryset = original_queryset.filter(level=0)

    if 'recursive' in request.query_params and request.query_params['recursive'] == 'true':
        print("Recursive is TRUE!!!!")
        folder = Folder.objects.get(pk=int(request.query_params['folders_in_tree']))
        qs_list = get_scenes_in_folder_recursive(folder, qs_list)
        print(qs_list)
        term_is_not_null = True

    else:
        z = False
        try:
            if request.query_params['pageType']:

                if request.query_params['pageType'] == 'DbFolder' and was_searched:
                    z = True
        except MultiValueDictKeyError:
            pass

        if not z:
            for qp in request.query_params:
                # print (qp)
                term_string = request.query_params.get(qp, None)
                # print (term_string)

                if (term_string is not None) and \
                        (term_string != '') and \
                        (qp != 'limit') and \
                        (qp != 'offset') and \
                        (qp != 'ordering') and \
                        (qp != 'recursive') and \
                        (qp != 'sortBy') and \
                        (qp != 'searchField') and \
                        (qp != 'pageType') and \
                        (qp != 'search'):

                    # if qp == 'sortBy':
                    #     sort_by = term_string
                    #     if sort_by == 'random':
                    #         random = True
                    #
                    # else:
                    term_is_not_null = True
                    terms = term_string.split(',')

                    for term in terms:
                        if qs_list:
                            t_list = list()
                            for i in qs_list:
                                if type(getattr(i, qp)) is bool:
                                    if bool(term) == getattr(i, qp):
                                        t_list.append(i)
                                elif (getattr(i, qp)).__class__.__name__ == 'ManyRelatedManager':
                                    print(getattr(i, qp).all())
                                    x = (getattr(i, qp).all())
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
                            qs_list = list(chain(qs_list, original_queryset.filter(**{qp: term})))

    if 'sortBy' in request.query_params:
        sort_by = request.query_params['sortBy']
        if sort_by == 'random':
            random = True
        if 'usage_count' in sort_by:
            term_is_not_null = True
            qs_list = list(original_queryset)

    if term_is_not_null:
        if random:
            shuffle(qs_list)
        else:
            if '-' in sort_by:
                sort_by = sort_by.replace('-', '')
                if sort_by == 'usage_count':
                    try:
                        temp_list = sorted(qs_list, key=lambda k: k.scenes.count(), reverse=True)
                    except AttributeError:
                        temp_list = sorted(qs_list, key=lambda k: k.actors.count(), reverse=True)
                else:
                    temp_list = sorted(qs_list,
                                       key=lambda k: (lambda_attrgetter(sort_by, k) is None,
                                                      lambda_attrgetter(sort_by, k) == "",
                                                      lambda_attrgetter(sort_by, k)), reverse=True)

            else:

                if sort_by == 'usage_count':
                    try:
                        temp_list = sorted(qs_list, key=lambda k: k.scenes.count())
                    except AttributeError:
                        temp_list = sorted(qs_list, key=lambda k: k.actors.count())
                else:
                    temp_list = sorted(qs_list,
                                       key=lambda k: (lambda_attrgetter(sort_by, k) is None,
                                                      lambda_attrgetter(sort_by, k) == "",
                                                      lambda_attrgetter(sort_by, k)))
            return temp_list

        return qs_list
    else:
        if random:
            return original_queryset.order_by('?')
        else:
            return original_queryset.order_by(sort_by)


def scrape_all_actors(force):
    actors = Actor.objects.all()

    for actor in actors:

        if not force:
            if actor.last_lookup is None:
                print("Searching in TMDb")
                videos.tmdb_search.search_person_with_force_flag(actor, False)
                print("Finished TMDb search")
                if actor.gender != 'M':
                    print("Searching in Freeones")
                    videos.freeones_search.search_freeones_with_force_flag(actor, False)
                    print("Finished Freeones search")
            else:
                print("{} was already searched...".format(actor.name))
        else:
            print("Searching in TMDb")
            videos.tmdb_search.search_person_with_force_flag(actor, True)
            print("Finished TMDb search")
            if actor.gender != 'M':
                print("Searching in Freeones")
                videos.freeones_search.search_freeones_with_force_flag(actor, True)
                print("Finished Freeones search")


def tag_all_scenes(ignore_last_lookup):
    filename_parser.parse_all_scenes(ignore_last_lookup)
    return Response(status=200)

    # scenes = Scene.objects.all()
    # scene_count = scenes.count()
    # counter = 1
    #
    # actors = list(Actor.objects.extra(select={'length': 'Length(name)'}).order_by('-length'))
    # actors_alias = list(ActorAlias.objects.extra(select={'length': 'Length(name)'}).order_by('-length'))
    # scene_tags = SceneTag.objects.extra(select={'length': 'Length(name)'}).order_by('-length')
    # websites = Website.objects.extra(select={'length': 'Length(name)'}).order_by('-length')
    #
    # filtered_alias = list()
    #
    # for alias in actors_alias:
    #     if ' ' in alias.name or alias.is_exempt_from_one_word_search:
    #         filtered_alias.append(alias)
    #
    # for scene in scenes:
    #     print("Scene {} out of {}".format(counter, scene_count))
    #     filename_parser.parse_scene_all_metadata(scene, actors, filtered_alias, scene_tags, websites)
    #     counter += 1


# views
class ScrapeActor(views.APIView):
    def get(self, request, format=None):
        search_site = request.query_params['scrapeSite']
        actor_id = request.query_params['actor']
        if request.query_params['force'] == 'true':
            force = True
        else:
            force = False
        print("You are now in the scrape actor API REST view")
        print("Actor to scrape is: " + Actor.objects.get(pk=actor_id).name)
        print("Site to scrape is: " + search_site)

        if search_site == 'TMDb':
            actor_to_search = Actor.objects.get(pk=actor_id)
            success = False
            if force:
                success = videos.tmdb_search.search_person_with_force_flag(actor_to_search, True)
            else:
                success = videos.tmdb_search.search_person_with_force_flag(actor_to_search, False)
            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        elif search_site == 'Freeones':

            actor_to_search = Actor.objects.get(pk=actor_id)
            success = False
            if force:
                success = videos.freeones_search.search_freeones_with_force_flag(actor_to_search, True)
            else:
                success = videos.freeones_search.search_freeones_with_force_flag(actor_to_search, False)

            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


def permenatly_delete_scene_and_remove_from_db(scene):
    success_delete_file = False
    success_delete_media_path = False
    try:
        os.remove(scene.path_to_file)
        print("Successfully deleted scene \'{}\'".format(scene.path_to_file))
        success_delete_file = True
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("File already deleted!")
            success_delete_file = True
        else:
            print("Got OSError while trying to delete {} : {}".format(scene.path_to_file, OSError.errno))

    media_path = os.path.relpath(os.path.join(const.MEDIA_PATH, 'scenes', str(scene.id)))
    print(os.path.dirname(os.path.abspath(__file__)))
    try:
        shutil.rmtree(media_path)
        print("Deleted \'{}\'".format(media_path))
        success_delete_media_path = True
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("Directory \'{}\' already deleted".format(media_path))
            success_delete_media_path = True
        else:
            print("Got OSError while trying to delete {} : {}".format(media_path, OSError))

    if success_delete_file and success_delete_media_path:
        scene.delete()
        print("Removed \'{}\' from database".format(scene.name))


@api_view(['GET', 'POST'])
def tag_multiple_items(request):
    if request.method == 'POST':
        # print("We got a post request!")

        params = request.data['params']

        if params['type'] == 'scene':
            print("Patching scene")

            if params['patchType'] == 'websites':

                website_id = params['patchData'][0]
                website_to_add = Website.objects.get(pk=website_id)
                scenes_to_update = params['itemsToUpdate']

                if params['addOrRemove'] == 'add':

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.add(website_to_add)
                        print("Added Website \'{}\' to scene \'{}\'".format(website_to_add.name, scene_to_update.name))

                        if website_to_add.scene_tags.count() > 0:
                            for tag in website_to_add.scene_tags.all():
                                scene_to_update.scene_tags.add(tag)
                                print("Added Scene Tag \'{}\' to scene \'{}\'".format(tag.name, scene_to_update.name))

                        scene_to_update.save()
                if params['addOrRemove'] == 'remove':
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.remove(website_to_add)
                        print("Removed Website \'{}\' from scene \'{}\'".format(website_to_add.name,
                                                                                scene_to_update.name))
                        if website_to_add.scene_tags.count() > 0:
                            for tag in website_to_add.scene_tags.all():
                                if tag in scene_to_update.scene_tags.all():
                                    scene_to_update.scene_tags.remove(tag)
                                    print(
                                        "Removed Scene Tag \'{}\' from scene \'{}\'".format(tag.name,
                                                                                            scene_to_update.name))
                        scene_to_update.save()

            elif params['patchType'] == 'scene_tags':
                scene_tag_id = params['patchData'][0]
                scene_tag_to_add = SceneTag.objects.get(pk=scene_tag_id)
                scenes_to_update = params['itemsToUpdate']

                if params['addOrRemove'] == 'add':

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.scene_tags.add(scene_tag_to_add)
                        scene_to_update.save()
                        print("Added Scene Tag \'{}\' to scene \'{}\'".format(scene_tag_to_add.name,
                                                                              scene_to_update.name))

                if params['addOrRemove'] == 'remove':
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.scene_tags.remove(scene_tag_to_add)
                        scene_to_update.save()
                        print("Removed Scene Tag \'{}\' from scene \'{}\'".format(scene_tag_to_add.name,
                                                                                  scene_to_update.name))
            elif params['patchType'] == 'actors':
                actor_id = params['patchData'][0]
                actor_to_add = Actor.objects.get(pk=actor_id)
                scenes_to_update = params['itemsToUpdate']

                if params['addOrRemove'] == 'add':

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.add(actor_to_add)
                        print("Added Actor \'{}\' to scene \'{}\'".format(actor_to_add.name, scene_to_update.name))

                        if actor_to_add.actor_tags.count() > 0:
                            for actor_tag in actor_to_add.actor_tags.all():
                                scene_to_update.scene_tags.add(actor_tag.scene_tags.first())
                                print("Added Scene Tag \'{}\' to scene \'{}\'".format(actor_tag.scene_tags.first().name,
                                                                                      scene_to_update.name))

                        scene_to_update.save()

                if params['addOrRemove'] == 'remove':
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.remove(actor_to_add)
                        print("Removed Actor \'{}\' from scene \'{}\'".format(actor_to_add.name, scene_to_update.name))

                        if actor_to_add.actor_tags.count() > 0:
                            for actor_tag in actor_to_add.actor_tags.all():
                                if actor_tag.scene_tags.first() in scene_to_update.scene_tags.all():
                                    scene_to_update.scene_tags.remove(actor_tag.scene_tags.first())
                                    print(
                                        "Removed Scene Tag \'{}\' to scene \'{}\'".format(
                                            actor_tag.scene_tags.first().name,
                                            scene_to_update.name))
                        scene_to_update.save()

            elif params['patchType'] == 'delete':
                scenes_to_update = params['itemsToUpdate']

                if params['permDelete']:
                    print('permDelete true')
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        permenatly_delete_scene_and_remove_from_db(scene_to_update)
                else:
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.delete()
                        print("Removed scene \'{}\' from database".format(scene_to_update.name))

        return Response(status=200)


def clean_dir(type_of_model_to_clean):
    number_of_folders = len(os.listdir(os.path.join(const.MEDIA_PATH, type_of_model_to_clean)))
    index = 1

    for dir_in_path in os.listdir(os.path.join(const.MEDIA_PATH, type_of_model_to_clean)):

        print("Checking {} folder {} out of {}".format(type_of_model_to_clean, index, number_of_folders))
        try:
            dir_in_path_int = int(dir_in_path)

            if type_of_model_to_clean == 'actor':
                try:
                    actor = Actor.objects.get(pk=dir_in_path_int)
                except Actor.DoesNotExist:
                    dir_to_delete = os.path.join(const.MEDIA_PATH, type_of_model_to_clean, dir_in_path)
                    print("Actor id {} is not in the database... Deleting folder {}".format(dir_in_path_int,
                                                                                            dir_to_delete))
                    shutil.rmtree(dir_to_delete)
            elif type_of_model_to_clean == 'scenes':

                try:
                    scene = Scene.objects.get(pk=dir_in_path_int)
                except Scene.DoesNotExist:
                    dir_to_delete = os.path.join(const.MEDIA_PATH, type_of_model_to_clean, dir_in_path)
                    print("Scene id {} is not in the database... Deleting folder {}".format(dir_in_path_int,
                                                                                            dir_to_delete))
                    shutil.rmtree(dir_to_delete)
            index += 1

        except ValueError:
            print("Dir name '{}' Could not be converted to an integer, skipping...".format(dir_in_path))
            index += 1
            pass


@api_view(['GET', 'POST'])
def settings(request):
    if request.method == 'GET':

        if 'pathToVlc' in request.query_params:
            if request.query_params['pathToVlc'] == "":
                print("get method works!")

                f = open('../YAPO/settings.json', 'r')
                x = f.read()
                settings_content = json.loads(x)
                print(settings_content['vlc_path'])
                print(x)
                f.close()
                serializer = SettingsSerializer(x)

                return Response(serializer.data)
            else:
                print(request.query_params['pathToVlc'])

                new_path_to_vlc = os.path.abspath(request.query_params['pathToVlc'])

                if os.path.isfile(new_path_to_vlc):
                    print("Actual path to a file!")
                    # dict = {'vlc_path': new_path_to_vlc}
                    # y = json.dumps(dict)


                    f = open('../YAPO/settings.json', 'r')
                    x = f.read()

                    settings_cont = json.loads(x)
                    settings_cont['vlc_path'] = new_path_to_vlc
                    y = json.dumps(settings_cont)

                    print(y)

                    f = open('../YAPO/settings.json', 'w')
                    f.write(y)
                    f.close()
                    const.VLC_PATH = new_path_to_vlc
                    return Response(status=200)

                else:
                    print("Path does not exist!")

                    return Response(status=500)

        if 'scrapAllActor' in request.query_params:
            if request.query_params['scrapAllActor'] == "True":
                threading.Thread(target=scrape_all_actors,
                                 args=(False,)
                                 ).start()

            return Response(status=200)

        if 'tagAllScenes' in request.query_params:
            if request.query_params['tagAllScenes'] == "true":
                if request.query_params['ignoreLastLookup'] == "true":
                    threading.Thread(target=tag_all_scenes,
                                     args=(True,)).start()
                else:
                    threading.Thread(target=tag_all_scenes,
                                     args=(False,)).start()
                    # _thread.start_new_thread(tag_all_scenes, (), )
                return Response(status=200)

        if 'cleanDatabase' in request.query_params:
            if request.query_params['cleanDatabase']:
                scenes = Scene.objects.all()
                count = scenes.count()
                counter = 1
                # print("Cleaning Scenes...")
                # for scene in scenes:
                #     print("Checking scene {} out of {}".format(counter, count))
                #     if not os.path.isfile(scene.path_to_file):
                #         print("File for scene {} does not exist in path {}".format(scene.name, scene.path_to_file))
                #         permenatly_delete_scene_and_remove_from_db(scene)
                #     counter += 1
                # print("Finished cleaning scenes...")

                print("Cleaning Aliases...")

                aliases = ActorAlias.objects.all()
                count = aliases.count()
                counter = 1
                for alias in aliases:
                    print("Checking Alias {} out of {}".format(counter, count))
                    if alias.actors.count() == 0:
                        alias.delete()
                        print("Alias {} has no actor... deleting".format(alias.name))
                    counter += 1
                print("Finished cleaning aliases...")

                print("Cleaning actor dirs that are no longer in database...")

                clean_dir('actor')
                print("Cleaning scene dirs that are no longer in database...")
                clean_dir('scenes')

        return Response(status=200)


@api_view(['GET'])
def ffmpeg(request):
    if request.method == 'GET':
        if 'generateSampleVideo' in request.query_params:
            if request.query_params['generateSampleVideo']:
                scene_id = request.query_params['sceneId']
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


class AddItems(views.APIView):
    def get(self, request, format=None):

        if request.query_params['folderToAddPath'] != "":
            folders_to_add_path = request.query_params['folderToAddPath']

            for folder_to_add_path in folders_to_add_path.split(','):
                if os.path.isdir(folder_to_add_path):
                    # if the second argument is true - tries to make a sample video when inserting scene to db.
                    if request.query_params['createSampleVideo'] == 'true':
                        videos.addScenes.get_files(folder_to_add_path, True)
                    else:
                        videos.addScenes.get_files(folder_to_add_path, False)
                else:
                    content = {'Path does not exist!': "Can't find path!"}
                    return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=200)

        if request.query_params['actorsToAdd'] != "":
            actors_to_add = request.query_params['actorsToAdd']

            for x in actors_to_add.split(','):
                actor_to_insert = Actor()
                actor_to_insert.strip = x.strip()
                actor_to_insert.name = actor_to_insert.strip
                actor_to_insert.thumbnail = const.UNKNOWN_PERSON_IMAGE_PATH
                try:
                    if not ActorAlias.objects.filter(name=actor_to_insert.name):
                        actor_to_insert.save()
                        print("Added {} To db".format(actor_to_insert.name))
                except django.db.IntegrityError as e:
                    # content = {'something whent wrong': e}
                    print("{} while trying to add {}".format(e, actor_to_insert.name))
                    # return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(status=200)


def play_scene_vlc(scene):
    file_path = os.path.normpath(scene.path_to_file)
    vlc_path = os.path.normpath(const.VLC_PATH)
    p = subprocess.Popen([vlc_path, file_path])
    scene.play_count += 1
    scene.date_last_played = datetime.datetime.now()
    print("Play count for scene '{}' is now '{}' and the date the scene was last played is '{}'".format(scene.name,
                                                                                                        scene.play_count,
                                                                                                        scene.date_last_played))
    scene.save()


@api_view(['GET', 'POST'])
def play_in_vlc(request):
    scene = None
    if request.method == 'GET':
        if 'sceneId' in request.query_params:
            scene_id = request.query_params['sceneId']
            scene = Scene.objects.get(pk=scene_id)
        elif 'actor' in request.query_params and request.query_params['actor'] != '-6':
            actor_id = request.query_params['actor']
            scene = Scene.objects.filter(actors=actor_id).order_by('?').first()
        elif 'sceneTag' in request.query_params and request.query_params['sceneTag'] != '-6':
            scene_tag_id = request.query_params['sceneTag']
            scene = Scene.objects.filter(scene_tags=scene_tag_id).order_by('?').first()
        elif 'website' in request.query_params and request.query_params['website'] != '-6':
            website_id = request.query_params['website']
            scene = Scene.objects.filter(websites=website_id).order_by('?').first()
        elif 'folder' in request.query_params and request.query_params['folder'] != '-6':
            folder_id = request.query_params['folder']
            scene = Scene.objects.filter(folders_in_tree=folder_id).order_by('?').first()
        else:
            scene = Scene.objects.order_by('?').first()

        if scene:
            play_scene_vlc(scene)
            return Response(status=200)
        else:
            return Response(status=500)


class PlayInVlc(views.APIView):
    def get(self, request, format=None):
        scene_id = request.query_params['sceneId']
        scene = Scene.objects.get(pk=scene_id)

        play_scene_vlc(scene)

        return Response(status=200)


def open_file_cross_platform(path):
    if platform.system() == "Windows":
        os.startfile(path)
    else:
        opener = "open" if platform.system() == "Darwin" else "xdg-open"
        subprocess.call([opener, path])


class OpenFolder(views.APIView):
    def get(self, request, format=None):
        path = request.query_params['path']
        open_file_cross_platform(path)
        return Response(status=200)


class AssetAdd(views.APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        my_file = "alala"
        # my_file = request.FILES['file']
        save_path = const.TEMP_PATH
        # os.path.abspath('D:\\aria2')
        save_file_name = 'temp.jpg'

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

        if request.data['file']:
            # print (request.data['file'])
            data = request.data['file']
            if data.startswith('data:image'):
                # base64 encoded image - decode


                format, imgstr = data.split(';base64,')  # format ~= data:image/X,
                ext = format.split('/')[-1]  # guess file extension
                # id = uuid.uuid4()
                # data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)
                with open(save_dest, "wb") as fh:
                    fh.write(base64.decodebytes(imgstr.encode('utf-8')))

                if request.data['type'] == 'Actor':
                    actor = Actor.objects.get(pk=request.data['id'])

                    current_tumb = os.path.join(const.MEDIA_PATH, 'actor/{}/'.format(actor.id), 'profile/profile.jpg')
                    print(current_tumb)

                    rel_path = os.path.relpath(current_tumb, start='videos')
                    as_uri = urllib.request.pathname2url(rel_path)

                    actor.thumbnail = as_uri
                    actor.save()

                    if not os.path.exists(current_tumb):
                        os.makedirs(os.path.dirname(current_tumb))
                    shutil.move(save_dest, current_tumb)

            return Response(status=200)

        return Response(status=500)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']

        print("got file")

        return Response(status=204)


def angualr_index(request):
    return render(request, 'videos/angular/index.html')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'actor_alias': reverse('actor-alias-list-rest', request=request, format=format),
        'actor': reverse('actors-list-rest', request=request, format=format)
    })


class ActorAliasHTMLRest(generics.GenericAPIView):
    queryset = ActorAlias.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        alias = self.get_object()
        return Response(alias.name)


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
        if self.action == 'list':
            return WebsiteIdNameSerailzier
        else:
            return WebsiteSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer


class SceneTagViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = SceneTag.objects.all()

        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == 'list':
            return SceneTagIdNameSerialzier
        else:
            return SceneTagSerializer

    queryset = ActorTag.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    queryset = SceneTag.objects.all()
    serializer_class = SceneTagSerializer


class SceneViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Scene.objects.all()

        return search_in_get_queryset(queryset, self.request)

    def get_serializer_class(self):
        if self.action == 'list':
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
        if self.action == 'list':
            return ActorTagListSerializer
        else:
            return ActorTagSerializer

    queryset = ActorTag.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
        term = 'name'
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
        if self.action == 'list':
            return ActorListSerializer
        else:
            return ActorSerializer

    # filter_backends = (filters.SearchFilter,)
    # ordering_fields = '__all__'
    # search_fields = ('name',)
    queryset = Actor.objects.all()
    # serializer_class = ActorSerializer
