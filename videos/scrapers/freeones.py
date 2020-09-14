# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import re
import urllib.parse as urllib_parse

import django
from bs4 import BeautifulSoup
from dateutil.parser import parse

import videos.aux_functions as aux
import logging

from videos.scrapers.scanner_common import scanner_common

log = logging.getLogger(__name__)

from configuration import Config, Constants

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
#urllib3.disable_warnings()

django.setup()

from videos.models import Actor, ActorTag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

class scanner_freeones(scanner_common):

    def search_freeones_with_force_flag(self, actor_to_search : Actor, force : bool):
        success = False
        if force:
            success = self.search_freeones(actor_to_search, None, force)

            if not success:
                for alias in actor_to_search.actor_aliases.all():
                    if alias.name.count(' ') > 0 or alias.is_exempt_from_one_word_search:
                        success = self.search_freeones(actor_to_search, alias, force)
                        if success:
                            break
        elif not actor_to_search.last_lookup:
            success = self.search_freeones(actor_to_search, None, force)
        return success


    def search_freeones_alias(self, actor_to_search : Actor, alias : bool, force : bool):
        success = False

        if force:
            success = self.search_freeones(actor_to_search, alias, force)
        elif not actor_to_search.last_lookup:
            success = self.search_freeones(actor_to_search, alias, force)

        return success

    def search_freeones(self, actor_to_search, alias, force):
        num = 0
        name = actor_to_search.name

        if alias:
            log.info(f"searching AKA: {alias.name}... ")
            name = alias.name
        else:
            log.info(f"Searching Freeones for: {actor_to_search.name}... ")

        # FIXME: is this an error?! Why do we add pluses and not use it?
        name_with_plus = name.replace(' ', '+')
        name_with_dash = name.replace(' ', '-')

        r = self.web.get_with_retry(f"https://www.freeones.com/babes?q={name_with_dash}", {}, {})

        soup = BeautifulSoup(r.content, "html5lib")

        soup_links = soup.find_all("a")

        href_found = self.match_link_to_query(soup_links, name_with_dash)


        if href_found:
            success = True
            aux.progress(1,27,f"Found {actor_to_search.name}, parsing...")
            actor_to_search.gender = 'F'
            actor_to_search.save()
            actor_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
            r = self.web.get_with_retry(actor_page)

            soup = BeautifulSoup(r.content, "html5lib")
            soup_links = soup.find_all("a")
            href_found = f"/{name_with_dash}/profile" #match_text_in_link_to_query(soup_links, "Profile")
            free_ones_bio_search = soup.find_all("div", {"class": "js-read-more-text read-more-text-ellipsis"})
            free_ones_career_status_search = soup.find_all("div", {"class": "timeline-horisontal"})
            free_ones_biography = free_ones_bio_search[0].get_text(strip=True)
            free_ones_country_search = soup.find_all("p", {"class": "color-text-dark font-size-xs font-weight-bold mb-1"})
            for link in free_ones_country_search:
                next_td_tag = link.findNext('p')
                link_text = link.text.strip("',/\n/\t")
                if link_text.lower() == "country":
                    title=link.findNext('a')
                    free_ones_country=title.get('title')
                    actor_to_search.country_of_origin = free_ones_country
                    aux.progress(2,27,"Country")
            has_image=False
            try:
                profile_thumb = soup.find("img", {'class': 'img-fluid'})
                profile_thumb_parent = profile_thumb.parent
                href=profile_thumb_parent['href']
                if href[0]=="/":
                    href = f"https://www.freeones.com{href}"
                has_image = False
                if len(href)>3:
                    has_image = True
            except Exception as e:
                log.error(f"Parse Error {e} - not getting any image.")
                pass

            biography_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
            if has_image:
                images_page = href

                if "freeones.com" in images_page.lower():
                    r = self.web.get_with_retry(images_page)
                    soup = BeautifulSoup(r.content, "html5lib")

                if actor_to_search.thumbnail == Constants().unknown_person_image_path or force:
                    if not("freeones.com" in images_page.lower()):
                        aux.progress(3,27,"Searching for Photo")
                    elif soup.find("section", {'id': 'fxgp-gallery'}):
                        aux.progress(3,27,"Searching for Photo")
                        picture_list = soup.find("section", {'id': 'fxgp-gallery'})

                        if picture_list.find("a"):
                            first_picture = picture_list.find("a")
                            save_path = os.path.join(Config().site_media_path, 'actor', str(actor_to_search.id), 'profile')
                            save_file_name = os.path.join(save_path, 'profile.jpg')
                            if not os.path.isfile(save_file_name):
                                if first_picture['href']:
                                    # FIXME/TODO: wtf is this regex
                                    if re.match(r'^\/\/', first_picture['href']):
                                            first_picture_link = f"https:{first_picture['href']}"
                                            aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search,force)
                                            aux.progress(4,27,"Storing photo")
                                    elif re.match(r'^.*jpg$', first_picture['href']):
                                            first_picture_link = first_picture['href']
                                            aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search,force)
                                            aux.progress(4,27,"Storing photo")
                            else:
                                aux.progress(4,29,"Not saving photo, one exists")

            r = self.web.get_with_retry(biography_page)
            soup = BeautifulSoup(r.content, "html5lib")
            soup_links = soup.find_all("p", {'class': ['heading', "text-center", "pt-1"]}) # {'class': ['heading', 'mb1']})    ("p", {'class': ['profile-meta-item']})

            aux.progress(5,29,"Parsing info")
            ethnicity = None
            for link in soup_links:
                next_td_tag = link.findNext('p')
                link_text = link.text.strip("',/\n/\t")  #link.get_text(strip=True)  #.strip("',/\r\n/\t")   #link.text.strip("',/\n/\t") get_text()

                num+=1
                if link_text.strip().lower() == 'personal information':
                    if not actor_to_search.date_of_birth:
                        if next_td_tag.text.strip("',/\n/\t"):
                            free_ones_date_of_birth = next_td_tag.get_text(strip=True) #.strip("',/\n/\t")
                            free_ones_date_of_birth = free_ones_date_of_birth.replace("Born On ", "")
                            if re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth):
                                parse_date_time = re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth)
                                if parse_date_time.group(0):
                                    parse_date_time = parse_date_time.group(0)
                                    parse_date_time = parse(parse_date_time.encode('utf-8'), fuzzy=True, ignoretz=True)
                                    actor_to_search.date_of_birth = parse_date_time
                                    aux.progress(6,29,"Birthday")

                elif link_text.lower() == 'ethnicity':
                    if not actor_to_search.ethnicity:
                        next_td_tag = link.findNext('p')
                        next_td_tag = link.findNext('p')
                        ethnicity = next_td_tag.get_text(strip=True)  #next_td_tag.text.strip("',/\n/\t")
                        actor_to_search.ethnicity = ethnicity
                        aux.progress(7,29,"Ethnicity")

                elif link_text.lower()=="official website":
                    official = link.findNext('div')  # ul id="socialmedia
                    all_official = official.find_all("a") #was: li
                    actor_to_search.official_pages = ""
                    for official_link in all_official:
                        try:
                            href = official_link['href']
                            if href not in actor_to_search.official_pages:
                                actor_to_search.official_pages += f"{official_link['href']},"
                        except Exception as e:
                            log.error(f"Cannot get official website for actor {actor_to_search.name}: {e}")
                            pass
                    aux.progress(8,29,"Official WWW")

                elif link_text.lower() == 'aliases':
                    try:
                        actor_aliases = next_td_tag.text.strip("'/\n/\t")
                        if not("Unknown" in actor_aliases):
                            actor_aliases = actor_aliases.replace(", ", ",")
                            self.insert_aliases(actor_to_search, actor_aliases)
                    except Exception as e:
                        log.error(f"Cannot get aliases for actor {actor_to_search.name}: {e}")
                        pass
                    aux.progress(9,29,"Aliases")

                elif link_text.lower() == 'follow on':
                    social = link.findNext('div')  # ul id="socialmedia
                    all_social = social.find_all("a") #was: li
                    for social_link in all_social:
                        try:
                            href = social_link['href']
                            if href not in actor_to_search.official_pages:
                                actor_to_search.official_pages = actor_to_search.official_pages + social_link['href'] + ","
                        except Exception as e:
                            log.error(f"Cannot get social media for actor {actor_to_search.name}: {e}")
                            pass
                    aux.progress(10,29,"Social links")

                elif link_text.lower() == 'appearance':
                    aux.progress(11,29,"Parsing appearance")
                    soup2 = BeautifulSoup(r.content, "html5lib")
                    soup2_links = soup.find_all("li") #, {'class': ['profile-meta-list']}) #("dt") #("p", {'class': ['heading', 'mb-0']})
                    for link2 in soup2_links:
                        next_td_tag1 = link2.find_next('span')

                        if next_td_tag1 is not None:
                            link2_text = next_td_tag1.get_text() #link2.get_text()
                        else:
                            continue
                        #link2_text = link2.text.strip("',/\n/\t")
                        num+=1
                        if  link2_text.lower().strip() == 'eye color': #'eye color' in link2_text.lower().strip():
                            next_td_tag1 = link2.find_next('span').find_next('span').find_next('span')
                            eye_color = next_td_tag1.get_text(strip=True) #text.strip("',/\n/\t")
                            eye_color = eye_color.title() + " eyes"
                            if eye_color and len(eye_color)>7:
                                self.insert_actor_tag(actor_to_search, eye_color)
                            aux.progress(12,29,"Eye color")

                        elif link2_text.lower().strip() == 'hair color':
                            next_td_tag1 = link2.find_next('span').find_next('span').find_next('span')
                            hair_color = next_td_tag1.get_text(strip=True) #text.strip("',/\n/\t")
                            hair_color = hair_color.title() + ' hair'
                            if hair_color and len(hair_color)>7:
                                self.insert_actor_tag(actor_to_search, hair_color)
                            aux.progress(13,29,"Hair color")

                        elif link2_text.lower().strip() == 'height':
                            next_td_tag1 = link2.find_next('span').find_next('span')
                            if not actor_to_search.height:
                                height = next_td_tag1.get_text(strip=True)  #tag.text.strip("'/\n/\t")
                                if len(height)<1 or height=="Unknown": height="0"
                                height=re.findall(r'[\d]+', height)
                                height=int(height[0])
                                actor_to_search.height = height
                            height=int(actor_to_search.height)
                            if height > 100:
                                heightStr = aux.heightcmToTagString(height)
                                self.insert_actor_tag(actor_to_search, heightStr)

                        elif link2_text.lower().strip() == 'weight':
                            next_td_tag1 = link2.find_next('span').find_next('span')
                            if not actor_to_search.weight:
                                weight = next_td_tag1.get_text(strip=True)  #tag.text.strip("'/\n/\t")
                                if len(weight)<1 or weight=="Unknown":
                                    weight="0"
                                weight = re.findall(r'[\d]+', weight)
                                weight = int(weight[0])
                                actor_to_search.weight = weight
                                aux.progress(16,29,"Weight")

                        elif link2_text.lower().strip() == 'measurements':
                            cupSize = ""
                            if not actor_to_search.measurements or actor_to_search.measurements=="":
                                try:
                                    mea = link2.find_next('span').find_next('span').get_text(strip=True)
                                    meas=mea.split("-")
                                    measlen = len(meas)
                                    if measlen == 2 and meas[1] == "":
                                        measlen = 1
                                    if measlen == 3 and meas[2] == "":
                                        measlen = 2

                                    che = meas[0]
                                    if measlen > 1:
                                        wai = meas[1]
                                    else:
                                        wai = "??"
                                    if measlen > 2:
                                        hip = meas[2]
                                    else:
                                        hip = "??"
                                    measure = str(che) + "-" + str(wai) + "-" + str(hip)
                                except Exception as e:
                                    log.error(f"While parsing measurements: {e}")
                                    pass
                                actor_to_search.measurements = measure            #next_td_tag1.get_text(strip=True)  #text.strip("'/\n/\t")
                                aux.progress(17,29,"Measurements")
                                if len(actor_to_search.measurements)>8  or len(actor_to_search.measurements)==3:
                                    try:
                                        measure=re.findall(r'[\d]+', actor_to_search.measurements)
                                        che=int(measure[0])
                                        wai=int(measure[1])
                                        hip=int(measure[2])
                                        cupSize = self.onlyChars(actor_to_search.measurements)
                                        if len(actor_to_search.measurements)==3:
                                            actor_to_search.measurements=str(che)+cupSize
                                        else:
                                            actor_to_search.measurements=str(che)+cupSize+"-"+str(wai)+"-"+str(hip)
                                    except Exception as e:
                                        log.error(f"While parsing measurements: {e}")
                                else:
                                    actor_to_search.measurements="??-??-??"

                            self.addCupSize(actor_to_search, cupSize)

                        elif link2_text.lower().strip() == 'boobs':

                            next_td_tag1 = link2.find_next('span')
                            boobs = next_td_tag1.get_text(strip=True) #.strip("',/\n/\t")
                            if "fake" in boobs.lower():
                                self.insert_actor_tag(actor_to_search, "Fake tits")
                            else:
                                self.insert_actor_tag(actor_to_search, "Natural tits")
                            aux.progress(20,29,"Tits fake/natural")

                        elif link2_text.lower().strip() == 'tattoos':
                            next_td_tag1 = link2.find_next('span').find_next('span').find_next('span')

                            if not actor_to_search.tattoos or actor_to_search.tattoos=="":
                                tattoos = next_td_tag1.get_text(strip=True) #text.strip("'/\n/\t")
                                actor_to_search.tattoos = tattoos.capitalize()
                                aux.progress(21,29,"Tattoos")

                                tattoos = str(actor_to_search.tattoos).strip()
                                tattoos1 = tattoos.replace(";", ",")
                                tattoos1 = tattoos1.replace(" and ", ",")
                                tattoos1 = tattoos1.replace("-", ",")
                                tattoos1 = tattoos1.replace(":", ",")

                                tattoos = tattoos1.split(",")

                                numTattoos = len(tattoos)

                                noTattooStrings = ( "none", "no tattoos", "n/a")

                                if tattoos1.lower().strip() in noTattooStrings or tattoos[0].lower().strip() in noTattooStrings:
                                    if numTattoos == 0 or numTattoos == 1 or numTattoos is None:
                                        self.insert_actor_tag(actor_to_search, "No tattoos")

                                if numTattoos == 1:
                                    if tattoos1.lower().strip() == "various" or tattoos[0].lower().strip() == "various":
                                        self.insert_actor_tag(actor_to_search, "Some tattoos")
                                    else:
                                        if      tattoos1.lower().strip() != "unknown" and \
                                                tattoos[0].lower().strip() != "unknown" and \
                                                tattoos[0].lower().strip() not in noTattooStrings:
                                            self.insert_actor_tag(actor_to_search, "One tattoo")

                                if numTattoos >= 2 and numTattoos <= 4:
                                    self.insert_actor_tag(actor_to_search, "Few tattoos")

                                if numTattoos > 4 and numTattoos <= 6:
                                    self.insert_actor_tag(actor_to_search, "Some tattoos")

                                if numTattoos > 6 and numTattoos <= 8:
                                    self.insert_actor_tag(actor_to_search, "Lots of tattoos")

                                if numTattoos > 8:
                                    self.insert_actor_tag(actor_to_search, "Massive amount of tattoos")

                                if (actor_to_search.tattoos and tattoos1) and actor_to_search.tattoos.lower() != tattoos1.lower():
                                    actor_to_search.tattoos = tattoos1

                                aux.progress(22,29,"Tattoos [Amount]")


                        elif link2_text.lower().strip() == 'piercings':
                            next_td_tag1 = link2.find_next('span').find_next('span').find_next('span')
                            if not actor_to_search.piercings or actor_to_search.piercings=="":
                                piercings = next_td_tag1.get_text(strip=True)  #text.strip("'/\n/\t")

                                piercings = str(piercings).strip()
                                piercings = piercings.replace(";", ",")
                                piercings = piercings.replace(" and ", ",")
                                if any([piercings.lower() == "none", piercings.lower() == "no piercings", piercings.lower() == "no"]):
                                    piercings="No piercings"
                                actor_to_search.piercings = piercings
                                aux.progress(23,29,"Piercings")

                elif link_text == 'Additional Information':
                    if not actor_to_search.extra_text:
                        actor_to_search.extra_text = next_td_tag.get_text(strip=True)   #text.strip("'/\n/\t")
                        aux.progress(24,29,"Additional info")

            if not actor_to_search.description or (len(actor_to_search.description) < 72):
                actor_to_search.description = free_ones_biography
                aux.progress(25,29,"Biography")

            valid_ethnicities = ("Black", "Asian", "Latin", "Caucasian", "Middle Eastern", "Arabic", "Inuit")
            if ethnicity is not None and ethnicity in valid_ethnicities:
                self.insert_actor_tag(actor_to_search, ethnicity)
            aux.progress(26,29,"Ethnicity")

            self.send_piercings_to_actortag(actor_to_search)
            aux.progress(27,29,"Sending piercings to tags")

            actor_to_search.last_lookup = datetime.datetime.now()
            actor_to_search.save()
            aux.progress(28,29,"Saving to database")

        else:
            actor_to_search.last_lookup = datetime.datetime.now()
            actor_to_search.save()
            log.info("Not Found")
            success = False
            aux.progress_end()

        if success:
            aux.progress(29,29,f"{num} tags parsed for {actor_to_search.name}.")
            aux.progress_end()
            log.info(f"Actor scraped: {actor_to_search.name}")

        return success

    def match_link_to_query(self, soup_links, text_to_find):
        ans = None
        for link in soup_links:
            try:
                if link.get("href").replace('/', '').lower() == text_to_find.lower():
                    ans = link.get("href")
                    break
            except Exception as e:
                log.error(f"While maching link to query: {e}")
        return ans

    def match_text_in_link_to_query(self, soup_links, text_to_find):
        ans = None
        ct = 0
        for link in soup_links:
            if ct < 2:
                log.info(link.text.lower().strip())
            ct+=1
            if link.text.lower() == text_to_find.lower():
                ans = link.get("href")
                break
        return ans


