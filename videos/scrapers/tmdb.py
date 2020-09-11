import os
from datetime import datetime

import django
import tmdbsimple as tmdb

import videos.aux_functions as aux
from utils import Constants

django.setup()

from videos.models import Actor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

tmdb.API_KEY = '04308f6d1c14608e9f373b84ad0e4e4c'

MEDIA_PATH = os.path.join('videos', 'media')

# Search for an actor on TMDB. Return False if the actor was not found.
def search_person(actor_in_question, alias, force) -> bool:

    print(f"Looking for: {actor_in_question.name}")
    search = tmdb.Search()
    if not alias:
       search.person(query=actor_in_question.name, include_adult='true')
    else:
       search.person(query=alias.name, include_adult='true')

    # We're only interesed in 'adult' results.
    results = [ x for x in search.results if x.get('adult', False) ]

    if len(results) == 0:
        print (f"Actor: {actor_in_question.name} could not be found on TMDb\r\n")
        return False

    person_info_list = map(lambda x: tmdb.People(str(x['id'])).info(), results)
    add_search_results_to_actor(actor_in_question, force, person_info_list)

    return True

def add_search_results_to_actor(actor_in_question: Actor, force: bool, person_info_list) -> None:
    for person_info in person_info_list:
        add_search_result_to_actor(actor_in_question, force, person_info)

    actor_in_question.last_lookup = datetime.now()
    actor_in_question.save()

def add_search_result_to_actor(actor_in_question: Actor, force: bool, person_info: dict) -> None:
    if actor_in_question.id is None:
        actor_in_question.save()

    actor_in_question.tmdb_id = person_info['id']
    actor_in_question.imdb_id = person_info['imdb_id']

    # Image download
    if actor_in_question.thumbnail == Constants().unknown_person_image_path or force:
        if person_info['profile_path'] is not None:
            picture_link = f"https://image.tmdb.org/t/p/original/{person_info['profile_path']}"
            print(f"Trying to get image from TMDB: {picture_link}")
            aux.save_actor_profile_image_from_web(picture_link, actor_in_question, force)

    if person_info['biography'] is not None:
        if not actor_in_question.description or (len(actor_in_question.description) < 48):
            actor_in_question.description = person_info['biography']
        print("There's no description or it's too short, so added it from TMDB.")

    if not person_info['birthday'] == "":
        actor_in_question.date_of_birth = person_info['birthday']
        print(f"Added Birthday to: {actor_in_question.name}")

    if not actor_in_question.gender:
        person_gender = person_info['gender']
        if person_gender == 2:
            actor_in_question.gender = 'M'
            print(f"Added Gender to: {actor_in_question.name}")
        elif person_gender == 1:
            actor_in_question.gender = 'F'
            print(f"Added Gender to: {actor_in_question.name}")

    if person_info['homepage']:
        actor_in_question.official_pages = person_info['homepage']
        print(f"Added Homepage to: {actor_in_question.name}")

    for aka in person_info['also_known_as']:
        actor_in_question.createOrAddAlias(aka.strip())

def search_alias(actor_in_question, alias, force):
    success = False
    if force:
        success = search_person(actor_in_question, alias,force)
    elif not actor_in_question.last_lookup:
        success = search_person(actor_in_question, alias,force)
    return success


def search_person_with_force_flag(actor_in_question, force):
    success = False
    print(f"Looking for: {actor_in_question.name}")
    if force:
        print("Force flag is true, ignoring last lookup")
        success = search_person(actor_in_question, None, force)
    elif not actor_in_question.last_lookup:
        print(f"Actor: {actor_in_question.name} was not yet searched... Searching now!")
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
