# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import re
import time

import urllib.parse as urllib_parse

import urllib.request as urllib_req
import django
import requests
import videos.aux_functions as aux
from bs4 import BeautifulSoup
from dateutil.parser import parse
import videos.const as const
from django.utils import timezone

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
django.setup()

from videos.models import Actor, ActorAlias, ActorTag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

# MEDIA_PATH = "videos\\media"


def sendAllPiercings():
    actors = Actor.objects.all()
    for actor in actors:
        aux.send_piercings_to_actortag(actor)

