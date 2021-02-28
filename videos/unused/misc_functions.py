# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import django

django.setup()

from videos.models import *
# coding=<UTF-8>

def strip_char(objects, char_to_strip):
    """
    Args:
        objects:
        char_to_strip:
    """
    for o in objects:
        if char_to_strip in o.name:
            print("Before: {o.name}")
            o.name = o.name.replace(char_to_strip, "")
            print("After: {o.name}")
            o.save()


def fix_profile_images(actors):
    """
    Args:
        actors:
    """
    for actor in actors:
        path_to_check = os.path.join(
            "E:","djangoProject",
            "YAPO",
            "videos",
            "../static",
            "images",
            "actor",
            actor.name,
            "profile",
            "profile.jpg",
        )
        print(path_to_check)
        if os.path.isfile(path_to_check):
            rel_path = os.path.relpath(
                path_to_check, os.path.join("E:","djangoProject","YAPO","videos")
            )
            print(rel_path)
            actor.thumbnail = rel_path
            actor.save()
        else:
            print("No Image")
            actor.thumbnail = Config().unknown_person_image_path
            actor.save()


def main():
    print("Hello")
    #
    # actor_tags = ActorTag.objects.all()
    # strip_char(actor_tags, )
    actors = Actor.objects.all()
    scenes = Scene.objects.all()
    for scene in scenes:
        add_scene_to_folder_view(scene)

        # populate_last_folder_name_in_virtual_folders()
        write_actors_to_file()
        clean_empty_folders()
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

        # get_files(TEST_PATH)

    fix_profile_images(actors)


# print ("name?")
# if __name__ = "__main__":
#    clean_taling_spaces()
#    main()
# print("name.")
