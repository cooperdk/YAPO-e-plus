# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import re
import time

import urllib.parse as urllib_parse
import videos.const
import urllib.request as urllib_req
import django
import requests
import videos.aux_functions as aux
import videos.updatepiercings as updatepiercings
from bs4 import BeautifulSoup
from dateutil.parser import parse
import videos.const as const
from django.utils import timezone


import requests.packages.urllib3
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

django.setup()

from videos.models import Actor, Scene, ActorAlias, SceneTag, Website

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

# MEDIA_PATH = "videos\\media"

def onlyChars(input):
    valids = ""
    for character in input:
        if character.isalpha():
            valids += character
    return valids
    
def parse(scene):

#    scene_path = scene.path
    site = matcher(scene)
    
    
def matcher(text):
    site=site_facialfest(text)
    if site!=("Unknown"):
        return(site) #Go back to parser

    else:
        return("Unknown")

def site_facialfest(text):
    if "facialfest" in text.lower() or "facial fest" in text.lower(): return("RENAME|Facial Fest")
    if len(text) < 6: return False
    if text[:2].lower() == "ff":
        site="FF"
#        print("FF yes")
    for i in range(2, 5):
        if text[i].isdecimal():
#            print("FF + 4 numbers yes")
            site="FF"
        elif not(text[i].isdecimal()):
            site="Unknown"
            break
    if site=="FF":
        return("ORIGNAME|Facial Fest")
            
    else: return("Unknown")    