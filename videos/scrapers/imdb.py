# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import time
import urllib.parse as urllib_parse

import django
import requests.packages.urllib3
from bs4 import BeautifulSoup

from videos.scrapers.scanner_common import scanner_common

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

django.setup()
import logging
log = logging.getLogger(__name__)

from videos.models import Actor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

class scanner_imdb(scanner_common):

    def search_imdb_with_force_flag(self, actor_to_search, force):
        success = False
        if force:
            success = self.search_imdb(actor_to_search, None, force)

            if not success:
                for alias in actor_to_search.actor_aliases.all():
                    if alias.name.count(' ') > 0 or alias.is_exempt_from_one_word_search:
                        success = self.search_imdb(actor_to_search, alias, force)
                        if success:
                            break

        elif not actor_to_search.last_lookup:
            success = self.search_imdb(actor_to_search, None, force)
        return success

    def search_imdb_alias(self, actor_to_search, alias, force):
        success = False

        if force:
            success = self.search_imdb(actor_to_search, alias, force)
        elif not actor_to_search.last_lookup:
            success = self.search_imdb(actor_to_search, alias, force)

        return success

    def search_imdb(self, actor_to_search, alias, force):
        success = False
        if Actor.objects.get(name=actor_to_search.name):
            actor_to_search = Actor.objects.get(name=actor_to_search.name)
        name = actor_to_search.name

        # https://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=isis+love
        if alias:
            name_with_plus = alias.name.replace(' ', '+')
            log.info(f"Searching IMDB for: {actor_to_search.name} alias: {alias.name}")
            name = alias.name
        else:
            name_with_plus = name.replace(' ', '+')
            log.info(f"Searching IMDB for: {actor_to_search.name}")
            log.info(f"({name_with_plus})")
        r = self.web.get_with_retry(f"https://www.imdb.com/search/name?name={name_with_plus}&adult=include")
        log.info(f"https://www.imdb.com/search/name?name={name_with_plus}&adult=include")
        soup = BeautifulSoup(r.content, "html5lib")
        # link = soup.find_all("a", {"text": "Isis Love"})
        for soup_links in soup.find_all("h3", attrs={'class': 'lister-item-header'}):	#, class_="lister-item-header")

            link = soup_links.find('a')['href']
            #link.replace("nm","")
            match = soup_links.find('a').contents[0]
            match = self.strip_bad_chars(match).lstrip()
            match = match.rstrip()
            href_found = self.match_text_in_link_to_query(match, name, link) # was soup_links

            if href_found:
                success = True
                found_lnk = urllib_parse.urljoin("https://www.imdb.com/",href_found)
                bio_page = f"{found_lnk}/bio?ref_=nm_ov_bio_sm"
                imdb_id = href_found.replace("/name/","").replace("/","")
                log.info(f"{actor_to_search.name} was found on IMDB!")
                actor_to_search.imdb_id = imdb_id
                log.info(f"Scraping biography from {bio_page}")
                r = self.web.get_with_retry(bio_page)
                soup = BeautifulSoup(r.content, "html5lib")
                soup_bio = soup.find("div", attrs={'class': 'soda'})
                if soup_bio is not None:
                    bio = soup_bio.find('p').contents[0]
                    log.info("Bio found, checking if it should be inserted")
                    if not actor_to_search.description or (len(actor_to_search.description) < 48):
                        actor_to_search.description = bio
                        log.info("There's no description or it's too short, so added it from IMDB.")
                    else:
                        log.info("Skipping, there's already a bio.")

                actor_to_search.last_lookup = datetime.datetime.now()
                actor_to_search.save()

            else:
                log.info(f"{actor_to_search.name} was not found on IMDB.")

            return success

    def match_text_in_link_to_query(self, soup, text, href):
        ans = None
        if text.lower() == soup.lower():
            ans = href
        return ans
