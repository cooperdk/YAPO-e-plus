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
django.setup()

from videos.models import Actor, ActorAlias, ActorTag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

MEDIA_PATH = "videos\\media"


def search_freeones(actor_to_search, alias):
    success = False
    if Actor.objects.get(name=actor_to_search.name):
        actor_to_search = Actor.objects.get(name=actor_to_search.name)
    name = actor_to_search.name

    # http://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=isis+love
    if alias:
        name_with_plus = alias.name.replace(' ', '+')
        print("Searching freeones for " + actor_to_search.name + " alias: " + alias.name)
    else:
        name_with_plus = name.replace(' ', '+')
        print("Searching freeones for " + actor_to_search.name)
    r = requests.get("http://www.freeones.com/search/?t=1&q=" + name_with_plus + "sq=")
    soup = BeautifulSoup(r.content, "html.parser")

    # link = soup.find_all("a", {"text": "Isis Love"})

    soup_links = soup.find_all("a")
    soup_all_tr = soup.find_all("tr", )
    actor_page = ""

    href_found = match_text_in_link_to_query(soup_links, name)
    # if not href_found:
    #     table = soup.find("div", {"class": "ContentBlockBody Block3"})
    #     tr_list = table.find_all("tr")
    #     first_line = tr_list[1]
    #     for tr in tr_list:
    #         td_list = tr.find_all("td")
    #         for td in td_list:
    #             if "100%" in td.text:
    #                 correct_td = td
    #                 print (correct_td)
    #
    #                 tr_links = tr.find_all("a")
    #                 for tr_link in tr_links:
    #                     if tr_link.has_attr('onmouseover'):
    #                         print (tr_link['href'])
    #
    #     relevance = first_line("td", {"class": "right top"})
    #     if relevance.text.strip("',/\n/\t") == "100%":
    #         tr_in_first_line = first_line.find_all("tr")
    #         temp = tr_in_first_line[4]
    #         link_in_first_line = temp.find("a")
    #         actual_link = link_in_first_line['href']
    #         href_found = actual_link

    if href_found:
        success = True
        print(actor_to_search.name + "Was found on freeones!")
        actor_to_search.gender = 'F'
        actor_to_search.save()
        actor_page = urllib_parse.urljoin("http://www.freeones.com/", href_found)
        r = requests.get(actor_page)

        soup = BeautifulSoup(r.content)
        soup_links = soup.find_all("a")
        href_found = match_text_in_link_to_query(soup_links, "Biography")

        free_ones_bio_search = soup.findAll("p", {"class": "dashboard-bio-description"})
        free_ones_career_status_search = soup.findAll("p", {"class": "dashboard-bio-career-status-text"})

        free_ones_biography = "From freeones.com: " + free_ones_bio_search[0].text
        # free_ones_career_status = "From freeones.com: " + free_ones_career_status_search[0].text

        # print (free_ones_biography, free_ones_career_status)
        # img class="middle bordered babeinfoblock-thumb"
        profile_thumb = soup.find("img", {'class': 'middle bordered babeinfoblock-thumb'})
        profile_thumb_perent = profile_thumb.parent

        print(profile_thumb_perent)
        print(profile_thumb_perent['href'])

        biography_page = urllib_parse.urljoin("http://www.freeones.com/", href_found)

        images_page = profile_thumb_perent['href']

        r = requests.get(images_page)
        soup = BeautifulSoup(r.content)

        if actor_to_search.thumbnail == const.UNKNOWN_PERSON_IMAGE_PATH:
            if soup.find("div", {'id': 'PictureList'}):

                picture_list = soup.find("div", {'id': 'PictureList'})

                if picture_list.find("a"):
                    first_picture = picture_list.find("a")

                    if first_picture['href']:
                        first_picture_link = first_picture['href']

                        print(first_picture_link)
                        aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search)

        r = requests.get(biography_page)

        soup = BeautifulSoup(r.content)

        soup_links = soup.find_all("td", {'class': 'paramname'})
        for link in soup_links:
            next_td_tag = link.findNext('td')

            next_td_tag_text = next_td_tag.text.strip("',/\n/\t")
            link_text = link.text.strip("',/\n/\t")

            if link_text == 'Ethnicity:':
                ethnicity = next_td_tag.text.strip("',/\n/\t")
                if not actor_to_search.ethnicity:
                    actor_to_search.ethnicity = ethnicity
            elif link_text == 'Country of Origin:':
                if not actor_to_search.country_of_origin:
                    actor_to_search.country_of_origin = next_td_tag.text.strip("',/\n/\t")
            elif link_text == 'Date of Birth:':
                if not actor_to_search.date_of_birth:
                    if next_td_tag.text.strip("',/\n/\t"):
                        free_ones_date_of_birth = next_td_tag.text.strip("',/\n/\t")

                        if re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth):
                            parse_date_time = re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth)
                            if parse_date_time.group(0):
                                parse_date_time = parse_date_time.group(0)
                                parse_date_time = parse(parse_date_time.encode('utf-8'), fuzzy=True, ignoretz=True)
                                actor_to_search.date_of_birth = parse_date_time
            elif link_text == 'Aliases:':
                actor_aliases = next_td_tag.text.strip("'/\n/\t")
                actor_aliases = actor_aliases.replace(", ", ",")
                insert_aliases(actor_to_search, actor_aliases)
            elif link_text == 'Height:':
                if not actor_to_search.height:
                    height = next_td_tag.text.strip("'/\n/\t")
                    height = re.search(r'heightcm = \"(\d+)\"', height)
                    height = height.group(1)
                    actor_to_search.height = height

            elif link_text == 'Weight:':
                if not actor_to_search.weight:
                    weight = next_td_tag.text.strip("'/\n/\t")
                    weight = re.search(r'weightkg = \"(\d+)\"', weight)
                    weight = weight.group(1)
                    actor_to_search.weight = weight
            elif link_text == 'Measurements:':
                if not actor_to_search.measurements:
                    actor_to_search.measurements = next_td_tag.text.strip("'/\n/\t")
            elif link_text == 'Tattoos:':
                if not actor_to_search.tattoos:
                    actor_to_search.tattoos = next_td_tag.text.strip("'/\n/\t")
            elif link_text == 'Extra text:':
                if not actor_to_search.extra_text:
                    actor_to_search.extra_text = next_td_tag.text.strip("'/\n/\t")
            elif link_text == 'Fake boobs:':
                fake_boobs = next_td_tag.text.strip("',/\n/\t")
                if "Yes" in fake_boobs:
                    insert_actor_tag(actor_to_search, "Fake.Breasts")
                else:
                    insert_actor_tag(actor_to_search, "Natural.Breasts")
            elif link_text == 'Eye Color:':
                eye_color = next_td_tag.text.strip("',/\n/\t")
                eye_color = "Eye.Color." + eye_color.title()

                insert_actor_tag(actor_to_search, eye_color)
            elif link_text == 'Hair Color:':
                hair_color = next_td_tag.text.strip("',/\n/\t")
                hair_color = "Hair.Color." + hair_color.title()
                insert_actor_tag(actor_to_search, hair_color)
            elif link_text == 'Social Network Links:':
                social = next_td_tag  # ul id="socialmedia
                all_social = social.find_all("li")

                for social_link in all_social:
                    try:
                        href = social_link['href']
                        if href not in actor_to_search.official_pages:
                            actor_to_search.official_pages = actor_to_search.official_pages + "," + social_link['href']
                    except:
                        pass

        if not actor_to_search.description:
            actor_to_search.description = free_ones_biography

        if "Black" in ethnicity:
            insert_actor_tag(actor_to_search, "Black.Female")
        elif "Asian" in ethnicity:
            insert_actor_tag(actor_to_search, "Asian.Female")
        elif "Latin" in ethnicity:
            insert_actor_tag(actor_to_search, "Latin.Female")

        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()

    else:
        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()

    return success


def strip_bad_chars(name):
    bad_chars = {" "}
    for char in bad_chars:
        if char in name:
            print("Before: " + name)
            name = name.replace(char, "")
            print("After: " + name)
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
            alias_to_insert.name = alias.encode('utf-8')
            # alias_to_insert.actor = actor_to_insert
            try:
                alias_to_insert.save()
                actor_to_insert.actor_aliases.add(alias_to_insert)
            except django.db.IntegrityError as e:
                print(e)


def match_text_in_link_to_query(soup_links, text_to_find):
    ans = None
    for link in soup_links:
        if link.text.lower() == text_to_find.lower():
            print(link.text, link.get("href"))
            ans = link.get("href")
            break
    return ans


def search_freeones_with_force_flag(actor_to_search, force):
    success = False
    if force:
        success = search_freeones(actor_to_search, None)
    elif not actor_to_search.last_lookup:
        success = search_freeones(actor_to_search, None)
    return success


def search_freeones_alias(actor_to_search, alias, force):
    success = False

    if force:
        success = search_freeones(actor_to_search, alias)
    elif not actor_to_search.last_lookup:
        success = search_freeones(actor_to_search, alias)

    return success


def main():
    print("test")
    for actor in Actor.objects.all():

        print("Fetching info for " + actor.name)
        if not actor.gender == 'M':
            time.sleep(10)
            sucess = search_freeones_with_force_flag(actor, True)
            if not sucess:
                for alias in actor.actor_aliases.all():
                    sucess = search_freeones_alias(actor, alias, True)
                    if sucess:
                        break

        print("Done!")

        # actor = Actor()
        # actor.name = "Daisy Marie"
        # search_freeones(actor)


if __name__ == "__main__":
    main()
