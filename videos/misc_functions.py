# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import django

django.setup()

from videos.models import *
import videos.const as const


# coding=<UTF-8>


def strip_char(objects, char_to_strip):
    for o in objects:
        if char_to_strip in o.name:
            print ("Before: " + o.name)
            o.name = o.name.replace(char_to_strip, "")
            print ("After: " + o.name)
            o.save()


def fix_profile_images(actors):
    for actor in actors:
        path_to_check = os.path.join(os.path.abspath("E:\\djangoProject\\YAPO\\videos\\static\\images\\actor"),
                                     actor.name, "profile\\profile.jpg")
        print (path_to_check)
        if os.path.isfile(path_to_check):
            rel_path = os.path.relpath(path_to_check, "E:\\djangoProject\\YAPO\\videos\\")
            print (rel_path)
            rel_path = rel_path.replace("\\", "/")
            print (rel_path)
            actor.thumbnail = rel_path
            actor.save()
        else:
            print ("No Image")
            actor.thumbnail = const.UNKNOWN_PERSON_IMAGE_PATH
            actor.save()


def main():
    print ("hello")
    #
    # actor_tags = ActorTag.objects.all()
    # strip_char(actor_tags, )
    actors = Actor.objects.all()

    fix_profile_images(actors)


if __name__ == "__main__":
    # clean_taling_spaces()
    main()
