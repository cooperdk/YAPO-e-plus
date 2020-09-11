# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import django
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

def onlyChars(toClean):
    valids = "".join(char for char in toClean if char.isalpha())
    return valids
    

def matcher(text):
    site=site_facialfest(text)
    if site!=("Unknown"):
        return(site) #Go back to parser

    else:
        return("Unknown")

def site_facialfest(text):
    if "facialfest" in text.lower().replace(" ",""): return("RENAME|Facial Fest")
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
