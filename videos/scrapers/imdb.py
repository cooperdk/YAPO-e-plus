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
#import videos.const as const
from django.utils import timezone

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

django.setup()

from videos.models import Actor, ActorAlias, ActorTag
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

def search_imdb(actor_to_search, alias, force):
    #return None
    success = False
    if Actor.objects.get(name=actor_to_search.name):
        actor_to_search = Actor.objects.get(name=actor_to_search.name)
    name = actor_to_search.name

    # https://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=isis+love
    if alias:
        name_with_plus = alias.name.replace(' ', '+')
        print(f"Searching IMDB for: {actor_to_search.name} alias: {alias.name}")
        name = alias.name
    else:
        name_with_plus = name.replace(' ', '+')
        print(f"Searching IMDB for: {actor_to_search.name}")
        print(f"({name_with_plus})")
    r = requests.get(f"https://www.imdb.com/search/name?name={name_with_plus}&adult=include", verify=False)
    print(f"https://www.imdb.com/search/name?name={name_with_plus}&adult=include")
    soup = BeautifulSoup(r.content, "html5lib")
    # link = soup.find_all("a", {"text": "Isis Love"})
    for soup_links in soup.find_all("h3", attrs={'class': 'lister-item-header'}):	#, class_="lister-item-header")

        link = soup_links.find('a')['href']
        #link.replace("nm","")
        match = soup_links.find('a').contents[0]
        match = strip_bad_chars(match).lstrip()
        match = match.rstrip()
        #print("Link is: " + link + ", match name: " + match)
    #print("SOUP: " + str(soup_links))
        href_found = match_text_in_link_to_query(match, name, link) # was soup_links

        if href_found:
            success = True
            found_lnk = urllib_parse.urljoin("https://www.imdb.com/",href_found)
            bio_page = f"{found_lnk}/bio?ref_=nm_ov_bio_sm"
            imdb_id = href_found.replace("/name/","").replace("/","")
            print(f"{actor_to_search.name} was found on IMDB!")# + href_found + "ID " + imdb_id)
            actor_to_search.imdb_id = imdb_id
            print(f"Scraping biography from {bio_page}")
            r = requests.get(bio_page, verify=False)
            soup = BeautifulSoup(r.content, "html5lib")
            soup_bio = soup.find("div", attrs={'class': 'soda'})
            if soup_bio is not None:
                bio = soup_bio.find('p').contents[0]
                print("Bio found, checking if it should be inserted")
            #bio=str(soup_bio) #soup_bio.contents[0]
            #print(bio)
                if not (actor_to_search.description) or (len(actor_to_search.description)<48):
                    actor_to_search.description = bio
                    print("There's no description or it's too short, so added it from IMDB.")
                else:
                    print("Skipping, there's already a bio.")

            actor_to_search.last_lookup = datetime.datetime.now()
            actor_to_search.save()

        else:
            #actor_to_search.last_lookup = datetime.datetime.now()
           #actor_to_search.save()
            print(f"{actor_to_search.name} was not found on IMDB.")
		
        return success

def strip_bad_chars(name):
    bad_chars = {" "}
    for char in bad_chars:
        if char in name:
            #print("Before: " + name)
            name = name.replace(char, "")
            print(f"Adding Data: {name}")
    return name

def insert_aliases(actor_to_insert, aliases):
    for alias in aliases.split(','):
        alias = alias.lstrip()
        alias = alias.rstrip()
        if not actor_to_insert.actor_aliases.filter(name=alias):
            alias_to_insert = ActorAlias()
            alias_to_insert.name = alias.encode('utf-8')
            # alias_to_insert.actor = actor_to_insert
            try:
                alias_to_insert.save()
                actor_to_insert.actor_aliases.add(alias_to_insert)
            except django.db.IntegrityError as e:
                print(e)


def match_text_in_link_to_query(soup, text, href):
    ans = None
    #for link in soup_links:
    #print("Checking " + text + " against " + soup)
    if text.lower() == soup.lower():
        #print("Match -->" + href)
        ans = href
    #    break
    return ans

def search_imdb_with_force_flag(actor_to_search, force):
    success = False
    if force:
        success = search_imdb(actor_to_search, None, force)

        if not success:
            for alias in actor_to_search.actor_aliases.all():
                if alias.name.count(' ') > 0 or alias.is_exempt_from_one_word_search:
                    success = search_imdb(actor_to_search, alias, force)
                    if success:
                        break

    elif not actor_to_search.last_lookup:
        success = search_imdb(actor_to_search, None, force)
    return success

def search_imdb_alias(actor_to_search, alias, force):
    success = False

    if force:
        success = search_imdb(actor_to_search, alias, force)
    elif not actor_to_search.last_lookup:
        success = search_imdb(actor_to_search, alias, force)

    return success

def main():
    print("test")
    for actor in Actor.objects.all():

        print(f"Fetching info for: {actor.name}")
        time.sleep(10)
        sucess = search_imdb_with_force_flag(actor, True)
        if not sucess:
            for alias in actor.actor_aliases.all():
                sucess = search_imdb_alias(actor, alias, True)
                if sucess:
                    break

    print("Done!")

        # actor = Actor()
        # actor.name = "Daisy Marie"
        # search_freeones(actor)


if __name__ == "__main__":
    main()
