import os
import urllib
from datetime import datetime

import django
import tmdbsimple as tmdb
import urllib.request as urllib
import videos.const as const
import videos.aux_functions as aux
from django.utils import timezone
django.setup()

from videos.models import Actor, ActorAlias

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

tmdb.API_KEY = '04308f6d1c14608e9f373b84ad0e4e4c'

MEDIA_PATH = os.path.join('videos', 'media')


def search_person(actor_in_question, alias, force):
    sucesss = False
    print("Looking for: " + actor_in_question.name)
    search = tmdb.Search()
    # response = search.person(query="Harmony Rose", include_adult='true')
    if not alias:
        response = search.person(query=actor_in_question.name, include_adult='true')
    else:
        response = search.person(query=alias.name, include_adult='true')

    for s in search.results:
        if s['adult']:
            sucesss = True
            # save image locally
            # urllib.urlretrieve("https://image.tmdb.org/t/p/original/" +
            #                  s['profile_path'], person_name + "Profile.jpg")

            if actor_in_question.id is None:
                actor_in_question.save()
            person = tmdb.People(str(s['id']))
            person_info = person.info()

            person_aka = person_info['also_known_as']
            if person_info['biography'] is not None:
                actor_in_question.description = person_info['biography']
                print("Added description to " + actor_in_question.name)
            else:
                actor_in_question.description = ""
            if not person_info['birthday'] == "":
                actor_in_question.date_of_birth = person_info['birthday']
                print("Added Birthday to " + actor_in_question.name)
            if not actor_in_question.gender:
                person_gender = person_info['gender']
                if person_gender == 2:
                    actor_in_question.gender = 'M'
                    print("Added Gender to " + actor_in_question.name)
                elif person_gender == 1:
                    actor_in_question.gender = 'F'
                    print("Added Gender to " + actor_in_question.name)
            if person_info['homepage']:
                actor_in_question.official_pages = person_info['homepage']
                print("Added Homepage to " + actor_in_question.name)

                actor_in_question.tmdb_id = person_info['id']
                actor_in_question.imdb_id = person_info['imdb_id']

            if actor_in_question.thumbnail == const.UNKNOWN_PERSON_IMAGE_PATH or force:
                if person_info['profile_path'] is not None:

                    picture_link = "https://image.tmdb.org/t/p/original/" + person_info['profile_path']

                    aux.save_actor_profile_image_from_web(picture_link,actor_in_question,force)

                    # save_path = os.path.join(MEDIA_PATH,
                    #                          'actor/' + actor_in_question.name + '/profile/')
                    # if not os.path.exists(save_path):
                    #     os.makedirs(save_path)
                    #
                    # save_file_name = os.path.join(save_path, 'profile.jpg')
                    # if not os.path.isfile(save_file_name):
                    #     urllib.urlretrieve(picture_link, save_file_name)
                    #
                    #     rel_path = os.path.relpath(save_file_name, start='videos')
                    #     as_uri = urllib.pathname2url(rel_path)
                    #
                    #     actor_in_question.thumbnail = as_uri

            for aka in person_aka:
                aka = aka.lstrip()
                aka = aka.rstrip()
                alias = ActorAlias()
                alias.name = aka
                # alias.actor = actor_in_question
                if not actor_in_question.actor_aliases.filter(name=aka):
                    try:
                        alias.save()
                        actor_in_question.actor_aliases.add(alias)
                    except django.db.IntegrityError as e:
                        print(e)

            actor_in_question.save()
            actor_in_question.last_lookup = datetime.now()
            actor_in_question.save()
            break

    if not sucesss:
        print ("Actor {} could not be found on TMdB".format(actor_in_question.name))
    return sucesss


def search_alias(actor_in_question, alias, force):
    success = False
    if force:
        success = search_person(actor_in_question, alias,force)
    elif not actor_in_question.last_lookup:
        success = search_person(actor_in_question, alias,force)
    return success


def search_person_with_force_flag(actor_in_question, force):
    success = False
    print("Looking for " + actor_in_question.name)
    if force:
        print("Force flag is true, ignoring last lookup")
        success = search_person(actor_in_question, None, force)
    elif not actor_in_question.last_lookup:
        print("Actor " + actor_in_question.name + " was not yet searched... Searching now")
        success = search_person(actor_in_question, None, force)

    return success


def main():
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    actors = Actor.objects.all()
    for actor in actors:
        actor.name = actor.name.rstrip()

        search_person_with_force_flag(actor, False)


if __name__ == "__main__":
    main()
