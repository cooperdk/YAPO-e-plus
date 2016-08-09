import os
import re

import django

django.setup()

from videos.models import Actor, Scene, ActorAlias, SceneTag, Website

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")


# def parse_all_scenes():
#     for scene in Scene.objects.all():
#         parse_scene_all_metadata(scene)


def parse_scene_all_metadata(scene, actors, actors_alias, scene_tags, websites):
    print("Parsing scene's: {} path: {} for actors,tags,and websites ...".format(scene.name, scene.path_to_file))

    scene_path = scene.path_to_file.lower()

    # remove dates from scene path (Maybe later parse dates for scene release dates, right now release dates formats
    # are not consistan through the files)
    scene_path = re.sub(r'"(.*)(\w+ \d{1,2}, \d{4})"', r'\1', scene_path)

    scene_path = parse_website_in_scenes(scene, scene_path, websites)

    scene_path = parse_actors_in_scene(scene, scene_path, actors, actors_alias)

    scene_path = parse_scene_tags_in_scene(scene, scene_path, scene_tags)

    print("Finished parsing scene's {} path...".format(scene.name))


def parse_actors_in_scene(scene_to_parse, scene_path, actors, actors_alias):
    # MyModel.objects.extra(select={'length':'Length(name)'}).order_by('length')

    for actor in actors:
        # If actor name is only one word or exempt from being searched even though it is one word.
        # print("Checking actor {}".format(actor.name))
        if actor.name.count(' ') > 0 or actor.is_exempt_from_one_word_search:

            regex_search_term = get_regex_search_term(actor.name, ' ')

            if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
                # print (actor.name + " is in " + scene_path + "\n")
                # scene_path = scene_path.replace(actor.name.lower(), '')
                scene_path = re.sub(regex_search_term, '', scene_path, flags=re.IGNORECASE)
                # print ("Trimmed scene path is: " + scene_path + "\n")
                add_actor_to_scene(actor, scene_to_parse)
                # else:
                # print (actor.name + " is one word name")

    for alias in actors_alias:
        # print("Checking alias {}".format(alias.name))
        actor_in_alias = alias.actors.first()
        if actor_in_alias:
            if alias.name.count(' ') > 0 or actor_in_alias.is_exempt_from_one_word_search:
                regex_search_term = get_regex_search_term(alias.name, ' ')

                if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
                    # print (alias.name + " is in " + scene_path + "\n")
                    # scene_path = scene_path.replace(alias.name.lower(), '')
                    scene_path = re.sub(regex_search_term, '', scene_path, flags=re.IGNORECASE)
                    # print ("Trimmed scene path is: " + scene_path + "\n")

                    print(alias.name + "is alias for" + actor_in_alias.name)
                    add_actor_to_scene(actor_in_alias, scene_to_parse)
                    # else:
                    # print(alias.name + " is one word alias")

    return scene_path


def add_actor_to_scene(actor_to_add, scene_to_add_to):
    # if not Scene.objects.filter(pk=scene_to_add_to.pk, actors__pk=actor_to_add.pk):
    if not scene_to_add_to.actors.filter(pk=actor_to_add.pk):

        print("Adding " + actor_to_add.name + " to scene" + scene_to_add_to.name + "\n")
        scene_to_add_to.actors.add(actor_to_add)
        scene_to_add_to.save()
    else:
        print(actor_to_add.name + "is already registered in " + scene_to_add_to.name + "\n")


def get_regex_search_term(name, delimiter):
    name_split_list = name.split(delimiter)
    is_first_iteration = True
    regex_search_term = ""
    for part_of_name in name_split_list:

        if is_first_iteration:
            regex_search_term = regex_search_term + part_of_name
            is_first_iteration = False
        else:
            regex_search_term = regex_search_term + ".{0,1}" + part_of_name
            # print ("regex search term is: "  + regex_search_term)
            # regex_search_term =  "r\"" + regex_search_term + "\""
    return regex_search_term


def parse_scene_tags_in_scene(scene, scene_path, scene_tags):
    for scene_tag in scene_tags:
        regex_search_term = get_regex_search_term(scene_tag.name, '.')

        if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
            scene_path = re.sub(regex_search_term, '', scene_path, flags=re.IGNORECASE)
            if not scene.scene_tags.filter(name=scene_tag.name):
                print("Adding {} to scene {}".format(scene_tag.name, scene.name))
                # print("Adding " + scene_tag.name + " to scene" + scene.name + "\n")
                scene.scene_tags.add(scene_tag)
            else:
                print("{} is already in {}".format(scene_tag.name, scene.name))
    return scene_path


def parse_website_in_scenes(scene, scene_path, websites):
    for website in websites:
        regex_search_term = get_regex_search_term(website.name, '.')

        if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
            scene_path = re.sub(regex_search_term, '', scene_path, flags=re.IGNORECASE)
            if not scene.websites.filter(name=website.name):
                print("Adding " + website.name + " to scene" + scene.name + "\n")
                scene.websites.add(website)
            else:
                print(website.name + " is already in" + scene.name + "\n")
    return scene_path


def clean_taling_spaces():
    actors_to_clean = Actor.objects.all()
    for a_to_clean in actors_to_clean:
        a_to_clean.name = a_to_clean.name.rstrip()
        a_to_clean.save()

    alias_to_clean = ActorAlias.objects.all()
    for al_to_clean in alias_to_clean:
        al_to_clean.name = al_to_clean.name.rstrip()
        al_to_clean.save()

    scene_tags_to_clean = SceneTag.objects.all()
    for s_to_clean in scene_tags_to_clean:
        s_to_clean.name = s_to_clean.name.rstrip()
        s_to_clean.save()


def main():
    all_scenes = Scene.objects.all()
    for scene in all_scenes:
        parse_scene_all_metadata(scene)


if __name__ == "__main__":
    # clean_taling_spaces()
    main()
