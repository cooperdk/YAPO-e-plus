import os.path
import subprocess
import _thread

import django.db

from django.shortcuts import render

import videos.addScenes
import videos.filename_parser as filename_parser
import videos.freeones_search
import videos.tmdb_search
from videos import ffmpeg_process
import urllib.request
# For REST framework

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

import threading
import pathlib


# Aux Functions
def search_in_get_queryset(original_queryset, request):
    qs_list = list()
    term_is_not_null = False
    random = False
    sort_by = "name"

    for qp in request.query_params:
        # print (qp)
        term_string = request.query_params.get(qp, None)
        # print (term_string)

        if (term_string is not None) and \
                (term_string != '') and \
                (qp != 'limit') and \
                (qp != 'offset') and \
                (qp != 'ordering') and \
                (qp != 'search'):

            if qp == 'sortBy':
                sort_by = term_string
                if sort_by == 'random':
                    random = True
            else:
                term_is_not_null = True
                terms = term_string.split(',')

                for term in terms:
                    qs_list = list(chain(qs_list, original_queryset.filter(**{qp: term})))

    if term_is_not_null:
        if random:
            shuffle(qs_list)
        else:
            if '-' in sort_by:
                sort_by = sort_by.replace('-', '')
                sorted(qs_list, key=attrgetter(sort_by), reverse=True)
            else:
                sorted(qs_list, key=attrgetter(sort_by))

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
                print("Searching in TMDB")
                videos.tmdb_search.search_person_with_force_flag(actor, True)
                print("Finished TMDB search")
                if actor.gender != 'M':
                    print("Searching in Freeones")
                    videos.freeones_search.search_freeones_with_force_flag(actor, True)
                    print("Finished Freeones search")
            else:
                print("{} was already searched...".format(actor.name))
        else:
            print("Searching in TMDB")
            videos.tmdb_search.search_person_with_force_flag(actor, True)
            print("Finished TMDB search")
            if actor.gender != 'M':
                print("Searching in Freeones")
                videos.freeones_search.search_freeones_with_force_flag(actor, True)
                print("Finished Freeones search")


def tag_all_scenes():
    scenes = Scene.objects.all()
    scene_count = scenes.count()
    counter = 1

    actors = list(Actor.objects.extra(select={'length': 'Length(name)'}).order_by('-length'))
    actors_alias = list(ActorAlias.objects.extra(select={'length': 'Length(name)'}).order_by('-length'))
    scene_tags = SceneTag.objects.extra(select={'length': 'Length(name)'}).order_by('-length')
    websites = Website.objects.extra(select={'length': 'Length(name)'}).order_by('-length')

    filtered_alias = list()

    for alias in actors_alias:
        if ' ' in alias.name or alias.is_exempt_from_one_word_search:
            filtered_alias.append(alias)

    for scene in scenes:
        print("Scene {} out of {}".format(counter, scene_count))
        filename_parser.parse_scene_all_metadata(scene, actors, filtered_alias, scene_tags, websites)
        counter += 1


# views
class ScrapeActor(views.APIView):
    def get(self, request, format=None):
        search_site = request.query_params['scrapeSite']
        actor_id = request.query_params['actor']
        print("You are now in the scrape actor API REST view")
        print("Actor to scrape is " + Actor.objects.get(pk=actor_id).name)
        print("Site to scrape is " + search_site)

        if search_site == 'TMDB':
            actor_to_search = Actor.objects.get(pk=actor_id)

            success = videos.tmdb_search.search_person_with_force_flag(actor_to_search, True)

            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        elif search_site == 'freeOnes':

            actor_to_search = Actor.objects.get(pk=actor_id)

            success = videos.freeones_search.search_freeones_with_force_flag(actor_to_search, True)

            if success:
                return Response(status=200)

            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'POST'])
def tag_multiple_items(request):
    if request.method == 'POST':
        print("We got a post request!")

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
                        scene_to_update.save()

                if params['addOrRemove'] == 'remove':
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.websites.remove(website_to_add)
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

                if params['addOrRemove'] == 'remove':
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.scene_tags.remove(scene_tag_to_add)
                        scene_to_update.save()
            elif params['patchType'] == 'actors':
                actor_id = params['patchData'][0]
                actor_to_add = Actor.objects.get(pk=actor_id)
                scenes_to_update = params['itemsToUpdate']

                if params['addOrRemove'] == 'add':

                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.add(actor_to_add)
                        scene_to_update.save()

                if params['addOrRemove'] == 'remove':
                    for x in scenes_to_update:
                        scene_to_update = Scene.objects.get(pk=x)
                        scene_to_update.actors.remove(actor_to_add)
                        scene_to_update.save()

        return Response(status=200)


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
                    dict = {'vlc_path': new_path_to_vlc}
                    y = json.dumps(dict)
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
            if request.query_params['tagAllScenes'] == "True":
                threading.Thread(target=tag_all_scenes, ).start()
                # _thread.start_new_thread(tag_all_scenes, (), )
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
                actor_to_insert.name = x.title()
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


class PlayInVlc(views.APIView):
    def get(self, request, format=None):
        scene_id = request.query_params['sceneId']
        scene = Scene.objects.get(pk=scene_id)

        play_scene_vlc(scene)

        return Response(status=200)


class OpenFolder(views.APIView):
    def get(self, request, format=None):
        path = request.query_params['path']
        os.startfile(path)
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

                    current_tumb = os.path.join(const.MEDIA_PATH, 'actor/{}/'.format(actor.name), 'profile/profile.jpg')
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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

    filter_backends = (filters.SearchFilter,)
    # ordering_fields = '__all__'
    search_fields = ('name',)
    queryset = Actor.objects.all()
    # serializer_class = ActorSerializer
