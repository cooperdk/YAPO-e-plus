import os
from datetime import datetime
import django
import tmdbsimple as tmdb
import videos.aux_functions as aux
from configuration import Config
from utils import Constants
from utils.printing import Logger
log = Logger()
django.setup()

from videos.models import Actor, ActorAlias

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

tmdb.API_KEY = '04308f6d1c14608e9f373b84ad0e4e4c'

def search_person(actor_in_question, alias, force):
    """Function to search for an actor using the TMDB API.

    Args:
        actor_in_question (object): An object containing data for the actor to search
        alias (bool): True if the search should be done on aliases
        force (bool) True if the operation should be forced

    Returns:
        success: bool
    """
    sucesss = False
    print(f"\033[KLooking for: {actor_in_question.name}\r",end="")
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
            ### This is just for image downloading.
            if person_info['profile_path'] is not None:
                picture_link = f"https://image.tmdb.org/t/p/original/{person_info['profile_path']}"
                if aux.url_is_alive(picture_link):
                    if actor_in_question.thumbnail == Constants().unknown_person_image_path or force:
                        print(f"\033[KTrying to get image from TMDB: {picture_link}\r",end="")
                        if aux.url_is_alive(picture_link):
                            aux.save_actor_profile_image_from_web(picture_link,actor_in_question,force)
                        else:
                            print("\033[KSeems as there's no photo at this link.\r",end="")


            person_aka = person_info['also_known_as']
            if person_info['biography'] is not None:
                if not (actor_in_question.description) or (len(actor_in_question.description)<48):
                    actor_in_question.description = person_info['biography']
                print("\033[KThere's no description or it's too short, so added it from TMDB.\r",end="")
            else:
                actor_in_question.description = ""
            if not person_info['birthday'] == "":
                actor_in_question.date_of_birth = person_info['birthday']
                print(f"\033[KAdded Birthday to: {actor_in_question.name}", end="")         
            if not actor_in_question.gender:
                person_gender = person_info['gender']
                if person_gender == 2:
                    actor_in_question.gender = 'M'
                    print(f"\033[KAdded Gender to: {actor_in_question.name}\r",end="")
                elif person_gender == 1:
                    actor_in_question.gender = 'F'
                    print(f"\033[KAdded Gender to: {actor_in_question.name}\r",end="")
            if person_info['homepage']:
                actor_in_question.official_pages = person_info['homepage']
                print(f"\033[KAdded Homepage to: {actor_in_question.name}\r",end="")

            actor_in_question.tmdb_id = person_info['id']
            actor_in_question.imdb_id = person_info['imdb_id']

            if actor_in_question.thumbnail == Config().unknown_person_image_path or force:
                if person_info['profile_path'] is not None:
                    picture_link = f"https://image.tmdb.org/t/p/original/{person_info['profile_path']}"
                    print(f"\033[KTrying to get image from TMDB: {picture_link}\r",end="")
                    if aux.url_is_alive(picture_link):
                        aux.save_actor_profile_image_from_web(picture_link,actor_in_question,force)

                    else:
                        print("\033[KSeems as there's no photo at this link.\r",end="")
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

            #actor_in_question.save()
 
            actor_in_question.last_lookup = datetime.now()
            actor_in_question.save()
            break

    if not sucesss:
        print (f"\033[KActor: {actor_in_question.name} could not be found on TMDb\r")
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
    print(f"\033[KLooking for: {actor_in_question.name}\r",end="")
    if force:
        print("\033[KForce flag is true, ignoring last lookup")
        success = search_person(actor_in_question, None, force)
    elif not actor_in_question.last_lookup:
        print(f"\033[KActor: {actor_in_question.name} was not yet searched... Searching now!\r",end="")
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
