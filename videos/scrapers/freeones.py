# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import re
import time
import urllib.parse as urllib_parse
from lxml import etree
import django
import requests
import videos.aux_functions as aux
from bs4 import BeautifulSoup
from dateutil.parser import parse
#import videos.const as const
from django.utils import timezone
from utils.printing import Logger
log = Logger()

django.setup()
from configuration import Config, Constants
from videos.models import Actor, ActorAlias, ActorTag


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

# MEDIA_PATH = "videos\\media"

def onlychars(chars):
    return "".join(char for char in chars if char.isalpha())

def inchtocm(inch):
    if inch.isdigit(): cm=int(inch)*2.54
    return cm

def sendallpiercings():
    actors = Actor.objects.all()
    for actor in actors:
        aux.send_piercings_to_actortag(actor)

def search_freeones(actor_to_search: object, alias: object, force: bool = False):
    num = 0
    success = False
    if Actor.objects.get(name=actor_to_search.name):
        actor_to_search = Actor.objects.get(name=actor_to_search.name)
    name = actor_to_search.name

    if alias:
        name_with_plus = alias.name.replace(' ', '+')
        name_with_dash = alias.name.replace(' ', '-')
        print(f"searching AKA: {alias.name}... ",end="")
        name = alias.name
    else:
        name_with_plus = name.replace(' ', '+')
        name_with_dash = name.replace(' ', '-')
        print(f"Searching Freeones for {actor_to_search.name}... ")
    r = requests.get(f"https://www.freeones.com/babes?q={name_with_dash}")

    soup = BeautifulSoup(r.content, "html5lib")

    soup_links = soup.find_all("a")

    href_found = match_link_to_query(soup_links, name_with_dash)


    if href_found:

        success = True
        aux.progress(1,27,f"Found {actor_to_search.name}, parsing...")
        #print("\nI found " + actor_to_search.name + ", so I am looking for information on her profile page.")
        actor_to_search.gender = 'F'
        actor_to_search.save()
        actor_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
        r = requests.get(actor_page)

        soup = BeautifulSoup(r.content, "html5lib")
        content = BeautifulSoup(r.content, "html.parser")
        dom = etree.HTML(str(content))
        soup_links = soup.find_all("a")
        href_found = f"/{name_with_dash}/profile" #match_text_in_link_to_query(soup_links, "Profile")

        #if len(free_ones_biography)>10: print("Biography saved.")
        #print("Bio: " + free_ones_biography)
        #print("Looking for a profile image... ", end = "")
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
        except:
            #print("Parse Error - not getting any image.")
            pass


        biography_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
        if has_image:
            images_page = href

            if "freeones.com" in images_page.lower():
                r = requests.get(images_page)
                soup = BeautifulSoup(r.content, "html5lib")

            if actor_to_search.thumbnail == Constants().unknown_person_image_path:
                if not "freeones.com" in images_page.lower():
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

        #remember to remark:
        #actor_to_search.last_lookup = datetime.datetime.now()
        #actor_to_search.save()
        #return success


        r = requests.get(biography_page)
        soup = BeautifulSoup(r.content, "html5lib")
        soup_links = soup.find_all("p", {'class': ['heading', "text-center", "pt-1"]}) # {'class': ['heading', 'mb1']})    ("p", {'class': ['profile-meta-item']})
        content = BeautifulSoup(r.content, "html.parser")
        dom = etree.HTML(str(content))

        aux.progress(5,29,"Parsing info")

        if not actor_to_search.description:
            x = dom.xpath("//div[@data-test='biography']/text()")
            if len(x)>0 and x is not None:
                free_ones_bio_search = x[0].strip()
                actor_to_search.description = free_ones_bio_search
                num += 1

        if not actor_to_search.country_of_origin:
            x = dom.xpath("//a[@data-test='link-country']//span/text()")
            if len(x)>0 and x is not None:
                free_ones_country = x[0].strip()
                actor_to_search.country_of_origin = free_ones_country
                num += 1

        if not actor_to_search.date_of_birth:
            x = dom.xpath("//a[contains(@href,'babes?f%5BdateOfBirth')]//span/text()")
            if len(x)>0 and x is not None:
                free_ones_date_of_birth = x[0].replace("Born On ", "").strip()
                if re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth):
                    parse_date_time = re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth)
                    if parse_date_time.group(0):
                        parse_date_time = parse_date_time.group(0)
                        parse_date_time = parse(parse_date_time.encode('utf-8'), fuzzy=True, ignoretz=True)
                        actor_to_search.date_of_birth = parse_date_time
                        aux.progress(6,29,"Birthday")
                        num += 1


        if not actor_to_search.ethnicity:
            x = dom.xpath("//p[contains(text(),'Ethnicity')]//following::p[1]//span/text()")
            if len(x)>0 and x is not None:
                ethnicity = x[0].strip()
                actor_to_search.ethnicity = str(ethnicity)
                aux.progress(7,29,"Ethnicity")
                num += 1


        if  not actor_to_search.official_pages:
            actor_to_search.official_pages = ""
            official_link = dom.xpath("//p[contains(text(),'Official website')]//following::p[1]/a/@href")
            if len(official_link)>0:
                if official_link[0].lower():
                    actor_to_search.official_pages = official_link[0]
                    num += 1

            aux.progress(8,29,"Official WWW")

        try:
            x = dom.xpath("//p[contains(text(),'Aliases')]//following::p[1]/text()")
            if len(x)>0 and x is not None:
                actor_aliases = [0].strip()
                if not "unknown" in actor_aliases.lower():
                    actor_aliases = actor_aliases.replace(", ", ",")
                    insert_aliases(actor_to_search, actor_aliases)
                    num += 1

        except:
            pass
        aux.progress(9,29,"Aliases")


        social = dom.xpath("//p[contains(text(),'Follow On')]//following::div[1]//a/@href")
        if len(actor_to_search.official_pages) > 8: actor_to_search.official_pages += ","
        for social_link in social:
            href = social_link
            if href not in actor_to_search.official_pages:
                actor_to_search.official_pages += href + ","
                num += 1

        aux.progress(10,29,"Social links")

        x = dom.xpath("//span[contains(text(),'Eye Color')]//following::span[2]/text()")
        if len(x)>0 and x is not None:
            eyes = x[0].strip()
            eye_color = eyes + ' eyes'
            if eye_color and len(eye_color)>7 and not "unknown" in eye_color.lower() and not actor_to_search.actor_tags.filter(name=eye_color):
                insert_actor_tag(actor_to_search, eye_color)
                num += 1

        aux.progress(12,29,"Eye color")

        hair = dom.xpath("//span[contains(text(),'Hair Color')]//following::span[2]/text()")[0].strip()
        hair_color = hair + ' hair'
        if hair_color and len(hair_color)>7 and not "unknown" in hair_color.lower() and not actor_to_search.actor_tags.filter(name=hair_color):
            insert_actor_tag(actor_to_search, hair_color)
            num += 1

        aux.progress(13,29,"Hair color")



        if not actor_to_search.height:
            x = dom.xpath("//span[contains(text(),'Height')]//following::span[2]/text()")
            if len(x)>0 and x is not None:
                height = x[0].strip()
                if len(height)<1 or height.lower()=="unknown" or height is None: height="0"

                height=re.findall(r'^[0-9]+', height)
                height=int(height[0])
                num += 1
            else: height = 0
            actor_to_search.height = int(height)
            height=int(actor_to_search.height)
            aux.progress(14,29,"Height")
            if height is not None:
                if height > 100:
                    if  height < 148 and not actor_to_search.actor_tags.filter(name="Extremely tiny"):
                        insert_actor_tag(actor_to_search, "Extremely tiny")
                        num += 1

                    if 148 < height < 152 and not actor_to_search.actor_tags.filter(name="Tiny"):
                        insert_actor_tag(actor_to_search, "Tiny")
                        num += 1

                    if 152 < height < 161 and not actor_to_search.actor_tags.filter(name="Petite"):
                        insert_actor_tag(actor_to_search, "Petite")
                        num += 1

                    if 178 < height < 186 and not actor_to_search.actor_tags.filter(name="Tall"):
                        insert_actor_tag(actor_to_search, "Tall")
                        num += 1

                    if 186 < height < 220 and not actor_to_search.actor_tags.filter(name="Extremely tall"):
                        insert_actor_tag(actor_to_search, "Extremely tall")
                        num += 1

                aux.progress(15,29,"Height [Group tag]")

        if not actor_to_search.weight:
            x = dom.xpath("//span[contains(text(),'Weight')]//following::span[2]/text()")
            if len(x)>0 and x is not None:
                weight = x[0].strip()
            else: weight = "0"
            if len(weight)<1 or weight.lower()=="unknown" or weight is None: weight="0"
            weight = re.findall(r'^[0-9]+', weight)
            weight = int(weight[0])
            actor_to_search.weight = weight
            num += 1
            aux.progress(16,29,"Weight")

        cupsize = ""
        #os.system('cls')
        if not actor_to_search.measurements or actor_to_search.measurements == "":
            mea = []
            measurements = []
            #print("Testing measurements")
            mea = dom.xpath("//span[contains(text(),'Measurements')]//following::span[2]//a//span/text()")
            measlen = 0
            measure = "???-??-??"
            #print(f"\n\n\nMEAS RAW: {mea[0]} -- {len(mea)}\n\n")
            if len(mea)>0:
                if mea[0].lower()!="unknown":
                    try:
                        measlen = len(mea)
                        if measlen == 1: measlen = 1
                        if measlen == 2 and mea[1].strip() == "": measlen = 1
                        if measlen == 3 and mea[2].strip() == "": measlen = 2
                        if mea[0]:
                            che = mea[0].strip()
                        if che.lower() == "unknown" or che == "?" or che == "??" or che == "":
                            che = "???"
                        if measlen > 1:
                            wai = mea[1]
                        else:
                            wai = "??"
                        if measlen > 2:
                            hip = mea[2]
                        else:
                            hip = "??"
                        measure = str(che) + "-" + str(wai) + "-" + str(hip)
                        #print(measure)
                    except Exception as e:
                        log.error(f'FO: MEA: {e}')
                    measurements = measure            #next_td_tag1.get_text(strip=True)  #text.strip("'/\n/\t")
                    actor_to_search.measurements = measurements
                else:
                    measurements = "???-??-??"
                aux.progress(17,29,"Measurements")

            if len(measurements)>8  or len(measurements)==3:
                #print(f"CONV > {measurements}")
                che=""
                wai=""
                hip=""
                try:
                    measure=re.findall(r'[\d]+', measurements)
                    if len(measure) >= 1:
                        che=int(measure[0])
                    else:
                        che = "???"
                    if len(measure) >= 2:
                        wai=int(measure[1])
                    else:
                        wai = ""
                    if len(measure) >= 3:
                        hip=int(measure[2])
                    else:
                        hip = ""
                    #print(che)
                    #print(wai)
                    #print(hip)
                    #che=int(che*2.54)
                    #wai=int(wai*2.54)
                    #hip=int(hip*2.54)
                    if not "un" in measurements[0:1] and not "?" in measurements[0:3]:
                        cupsize = onlychars(measurements)
                    #print(f"\n\n{cupsize} - {len(measure)} - {len(measurements)}  - {measurements}")

                    if len(measure)==1:
                        actor_to_search.measurements=str(che)+cupsize
                    else:
                        actor_to_search.measurements=str(che)+cupsize+"-"+str(wai)+"-"+str(hip)
                    num += 1
                except Exception as e:
                    log.error(f'FO: MEA: {e}')
            else:
                actor_to_search.measurements="???-??-??"
            actor_to_search.save()

            if len(measurements) > 8 or len(measurements) == 3:

                cupsize = onlychars(actor_to_search.measurements).upper().strip()
                if len(cupsize)>0 and not actor_to_search.actor_tags.filter(name=cupsize + " Cup"):
                    insert_actor_tag(actor_to_search, cupsize + " Cup")
                    num += 1
                    aux.progress(18,29,f"Measurements ({cupsize} Cup)")
                    try:
                        if cupsize[0] in 'A' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Tiny tits"):
                            insert_actor_tag(actor_to_search, "Tiny tits")
                            num += 1
                        if cupsize[0] in 'B' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Small tits"):
                            insert_actor_tag(actor_to_search, "Small tits")
                            num += 1
                        if cupsize[0] in 'C' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Medium tits"):
                            insert_actor_tag(actor_to_search, "Medium tits")
                            num += 1
                        elif cupsize[0] in 'DEF' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Big tits"):
                            insert_actor_tag(actor_to_search, "Big tits")
                            num += 1
                        elif cupsize[0] in 'GHI' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Very big tits"):
                            insert_actor_tag(actor_to_search, "Very big tits")
                            num += 1
                        elif cupsize[0] in 'JKLM' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Huge tits"):
                            insert_actor_tag(actor_to_search, "Huge tits")
                            num += 1
                        elif cupsize[0] in 'NOPQRS' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Extremely huge tits"):
                            insert_actor_tag(actor_to_search, "Extremely huge tits")
                            num += 1
                        elif cupsize[0] in 'TUVWXYZ' and len(cupsize) < 5 and not actor_to_search.actor_tags.filter(name="Gigantic tits"):
                            insert_actor_tag(actor_to_search, "Gigantic tits")
                            num += 1

                    except Exception as e:
                        log.error(f'FO: CUPS: {e}')
                aux.progress(19, 29, "Measurements [Tits description]")

        if not actor_to_search.actor_tags.filter(name="Natural tits") or not actor_to_search.actor_tags.filter(name="Fake tits"):
            x = dom.xpath("//span[@data-test='link_span_boobs']/text()")
            if len(x)>0 and x is not None:
                boobs=x[0]
                if "fake" in boobs.lower():
                    insert_actor_tag(actor_to_search, "Fake tits")
                    num += 1
                elif "natural" in boobs.lower():
                    insert_actor_tag(actor_to_search, "Natural tits")
                    num += 1
        aux.progress(20,29,"Fake or natural tits")


        if not actor_to_search.tattoos or actor_to_search.tattoos=="":
            x = dom.xpath("//span[contains(text(),'Tattoos')]//following::span[2]/text()")
            if len(x)>0 and x is not None:
                tattoos = x[0].strip()
                actor_to_search.tattoos = tattoos.capitalize()
                num += 1
            tattoos = str(actor_to_search.tattoos).strip()
            tattoos1 = tattoos.replace(";", ",")
            tattoos1 = tattoos1.replace(" and ", ",")
            tattoos1 = tattoos1.replace("-", ",")
            tattoos1 = tattoos1.replace(":", ",")
            tattoos = tattoos1.split(",")
            numTattoos = len(tattoos)
            aux.progress(21, 29, f"Tattoos: {str(numTattoos)}")

            if (numTattoos == 0 or numTattoos is None) or (
                    tattoos1.lower().strip() == "none"
                    or tattoos1.lower().strip() == "no tattoos"
                    or tattoos[0].lower().strip() == "none"
                    or tattoos[0].lower().strip() == "no tattoos"
                    or tattoos[0].lower().strip() == "n/a"
            ) and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "No tattoos")
                num += 1

            if numTattoos == 1 and (
                    tattoos[0].lower().strip() == "none"
                    or tattoos1.lower().strip() == "none"
                    or tattoos1.lower().strip() == "no tattoos"
                    or tattoos[0].lower().strip() == "no tattoos"
                    or tattoos[0].lower().strip() == "n/a"
                    or tattoos1.lower().strip() == "n/a"
                    or tattoos1.lower().strip() == "no"
            ) and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "No tattoos")
                num += 1

            if numTattoos == 1 and (
                    tattoos1.lower().strip() == "yes" or tattoos[0].lower().strip() == "yes"
            ) and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "Has tattoos")
                num += 1

            if numTattoos == 1 and (
                    tattoos1.lower().strip() == "various" or tattoos[0].lower().strip() == "various"
            ) and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "Some tattoos")
                num += 1

            elif numTattoos == 1 and (
                    tattoos1.lower().strip() != "various"
                    and tattoos[0].lower().strip() != "various"
                    and tattoos[0].lower().strip() != "none"
                    and tattoos[0].lower().strip() != "none"
                    and tattoos[0].lower().strip() != "unknown"
                    and tattoos[0].lower().strip() != "no tattoos"
                    and tattoos[0].lower().strip() != "n/a"
                    and tattoos[0].lower().strip() != "yes"
                    and tattoos[0].lower().strip() != "no"
            ) and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "One tattoo")
                num += 1

            if numTattoos >= 2 and numTattoos <= 4 and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "Few tattoos")
                num += 1

            if numTattoos > 4 and numTattoos <= 6 and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "Some tattoos")
                num += 1

            if numTattoos > 6 and numTattoos <= 8 and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "Lots of tattoos")
                num += 1

            if numTattoos > 8 and not actor_to_search.actor_tags.filter(name__contains="tattoo"):
                aux.insert_actor_tag(actor_to_search, "Massive amount of tattoos")
                num += 1

            if (actor_to_search.tattoos and tattoos1) and actor_to_search.tattoos.lower() != tattoos1.lower():
                actor_to_search.tattoos = tattoos1
                num += 1

            aux.progress(22,29,f"Tattoos ({numTattoos})")

        if not actor_to_search.piercings or actor_to_search.piercings=="":
            x = dom.xpath("//span[contains(text(),'Piercings')]//following::span[2]/text()")
            if len(x)>0 and x is not None:
                piercings = x[0].strip()
                if any([piercings.lower() == "n/a", piercings.lower() == "none", \
                        piercings.lower() == "no piercings", piercings.lower() == "no"]):
                    piercings="No piercings"
                piercings = piercings.strip()
                piercings = piercings.replace(";", ",")
                piercings = piercings.replace(" and ", ",")
                actor_to_search.piercings = piercings
                num += 1
            aux.progress(23,29,"Piercings")

            if not actor_to_search.extra_text:
                x = dom.xpath( \
                    "//div[@data-test='section-additional-info']//div//div//p/text()")
                if len(x)>0 and x is not None:
                    extra_text = x[0]
                aux.progress(24,29,"Additional info")
                if not actor_to_search.extra_text == "Unknown" and len(extra_text) > 5 \
                and actor_to_search.extra_text != None:
                    actor_to_search.extra_text = extra_text.strip()
                    num += 1
                else:
                    actor_to_search.extra_text = None


            try:
                if actor_to_search.ethnicity is not None:
                    if "black" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Black"):
                        insert_actor_tag(actor_to_search, "Black")
                        num += 1
                    elif "asian" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Asian"):
                        insert_actor_tag(actor_to_search, "Asian")
                        num += 1
                    elif "latin" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Latin"):
                        insert_actor_tag(actor_to_search, "Latin")
                        num += 1
                    elif "caucasian" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Caucasian"):
                        insert_actor_tag(actor_to_search, "Caucasian")
                        num += 1
                    elif "middle eastern" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Middle Eastern"):
                        insert_actor_tag(actor_to_search, "Middle Eastern")
                        num += 1
                    elif "arabic" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Arabic"):
                        insert_actor_tag(actor_to_search, "Arabic")
                        num += 1
                    elif "inuit" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Inuit"):
                        insert_actor_tag(actor_to_search, "Inuit")
                        num += 1
                    elif "native american" in ethnicity.lower() and not actor_to_search.actor_tags.filter(name="Native American"):
                        insert_actor_tag(actor_to_search, "Native American")
                        num += 1

                aux.progress(26,29,"Ethnicity")
            except:
                pass

            result = aux.send_piercings_to_actortag(actor_to_search)
            num += result
            aux.progress(27,29,"Sending piercings to tags")
            #    sendallpiercings() #    use this whenever you want to update all piercings in db


            actor_to_search.last_lookup = datetime.datetime.now()
            actor_to_search.save()
            aux.progress(28,29,"Saving to database")

    else:
        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()
        fail = True
        aux.progress_end()
        log.info(f"FO: {actor_to_search.name} was not found.")

    if success:
        aux.progress(29,29,"Done.")
        aux.progress(29,29,f"{num} items added for {actor_to_search.name}.")
        aux.progress_end()
        log.info(f"SCRAPER: FO: {num} items added to {actor_to_search.name}")
        print("")
        return success

    return False

def strip_bad_chars(name):
    bad_chars = {" "}
    for char in bad_chars:
        if char in name:
            #print("Before: " + name)
            name = name.replace(char, "")
            #print("Adding Data: " + name)
    return name


def insert_actor_tag(actor_to_insert, actor_tag_name):
    actor_tag_name = strip_bad_chars(actor_tag_name)

    if not ActorTag.objects.filter(name=actor_tag_name):
        actor_tag = ActorTag()
        actor_tag.name = actor_tag_name

        actor_tag.save()
        actor_to_insert.actor_tags.add(actor_tag)

    else:
        actor_tag = ActorTag.objects.get(name=actor_tag_name)
        actor_to_insert.actor_tags.add(actor_tag)
        actor_tag.save()


def insert_aliases(actor_to_insert, aliases):
    for alias in aliases.split(','):
        alias = alias.lstrip()
        alias = alias.rstrip()
        if not actor_to_insert.actor_aliases.filter(name=alias):
            alias_to_insert = ActorAlias()
            alias_to_insert.name = alias  #.decode('utf-8')    # Encode gives an error in Py 8
            # alias_to_insert.actor = actor_to_insert
            try:
                alias_to_insert.save()
                actor_to_insert.actor_aliases.add(alias_to_insert)
            except django.db.IntegrityError as e:
                log.error(f"SCRAPER: FO: {e}")


def match_link_to_query(soup_links, text_to_find):
    ans = None
    for link in soup_links:
        try:
            if link.get("href").replace('/feed','').replace('/', '').lower() == text_to_find.lower():
            #    print(link.get("href"))
                ans = link.get("href")
                break
        except:
            pass #print("Error")
    return ans

def match_text_in_link_to_query(soup_links, text_to_find):
    ans = None
    ct = 0
    for link in soup_links:
        if ct < 2: print (link.text.lower().strip())
        ct+=1
        if link.text.lower() == text_to_find.lower():
        #    print(link.text, link.get("href"))
            ans = link.get("href")
            break
    return ans

def search_freeones_with_force_flag(actor_to_search, force):
    success = False
    if force:
        success = search_freeones(actor_to_search, None, force)

        if not success:
            for alias in actor_to_search.actor_aliases.all():
                if alias.name.count(' ') > 0 or alias.is_exempt_from_one_word_search:
                    success = search_freeones(actor_to_search, alias, force)
                    if success:
                        break

    elif not actor_to_search.last_lookup:
        success = search_freeones(actor_to_search, None, force)
    return success


def search_freeones_alias(actor_to_search, alias, force):
    success = False

    if force or not actor_to_search.last_lookup:
        success = search_freeones(actor_to_search, alias, force)
    return success


def main():
    #print("test")
    for actor in Actor.objects.all():

        #print("Fetching info for: " + actor.name)
        if actor.gender != 'M':
            time.sleep(10)
            sucess = search_freeones_with_force_flag(actor, True)
            if not sucess:
                for alias in actor.actor_aliases.all():
                    sucess = search_freeones_alias(actor, alias, True)
                    if sucess:
                        break



if __name__ == "__main__":
    main()
