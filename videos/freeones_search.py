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

from videos.models import Actor, ActorAlias, ActorTag


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

# MEDIA_PATH = "videos\\media"

def onlyChars(input):
    valids = ""
    for character in input:
        if character.isalpha():
            valids += character
    return valids

def search_freeones(actor_to_search, alias, force):
    success = False
    if Actor.objects.get(name=actor_to_search.name):
        actor_to_search = Actor.objects.get(name=actor_to_search.name)
    name = actor_to_search.name
    

#    actor_to_search.last_lookup = datetime.datetime.now()
#    actor_to_search.save()
#    save_path = os.path.join(videos.const.MEDIA_PATH, 'actor/' + str(actor_to_search.id) + '/profile/')
#    save_file_name = os.path.join(save_path, 'profile.jpg')
#    print(save_file_name)
#    if os.path.isfile(save_file_name):
#        print("Skipping, as there's already a photo for the profile.")
#        return

    # https://www.iafd.com/results.asp?searchtype=comprehensive&searchstring=isis+love
    if alias:
        name_with_plus = alias.name.replace(' ', '+')
        print("Searching Freeones for: " + actor_to_search.name + " alias: " + alias.name)
        name = alias.name
    else:
        name_with_plus = name.replace(' ', '+')
        print("Searching Freeones for: " + actor_to_search.name)
    r = requests.get("https://www.freeones.com/search/?t=1&q=" + name_with_plus, verify=False)
    soup = BeautifulSoup(r.content, "html5lib")


    # link = soup.find_all("a", {"text": "Isis Love"})

    soup_links = soup.find_all("a")

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
        print(actor_to_search.name + " was found on Freeones!")
        actor_to_search.gender = 'F'
        actor_to_search.save()
        actor_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
        r = requests.get(actor_page, verify=False)

        soup = BeautifulSoup(r.content, "html5lib")
        soup_links = soup.find_all("a")
        href_found = match_text_in_link_to_query(soup_links, "Biography")

        free_ones_bio_search = soup.findAll("p", {"class": "dashboard-bio-description"})
        free_ones_career_status_search = soup.findAll("p", {"class": "dashboard-bio-career-status-text"})

        free_ones_biography = "From freeones.com: " + free_ones_bio_search[0].text
        # free_ones_career_status = "From freeones.com: " + free_ones_career_status_search[0].text

        # print (free_ones_biography, free_ones_career_status)
        # img class="middle bordered babeinfoblock-thumb"
        try:
            profile_thumb = soup.find("img", {'class': 'middle bordered babeinfoblock-thumb'})
            profile_thumb_parent = profile_thumb.parent

        #print(profile_thumb_parent)
            has_image = False

        
            #print(profile_thumb_parent['href'])
            if len(profile_thumb_parent['href'])>3:     
                has_image = True
        except:
            print("Parsing Error - not getting any image.")
            pass
        
 #       except RequestException:
 #           print("No image fetched from Freeones!")      
 #       except KeyError:
 #           print("No image fetched from Freeones!")
 #       except ConnectionError:
 #           print("No image fetched from Freeones (Connection error in BeautifulSoup module)")
 #       except BaseException:
 #           print("No image fetched from Freeones  - Exception error in BeautifulSoup module")
 #       except StandardError:
 #           print("No image fetched from Freeones  - Standard error in BeautifulSoup module")
 #       except IOError:
 #           print("No image fetched from Freeones - I/O Error")
 #       except EnvironmentError:
 #           print("No image fetched from Freeones  - Environment error in BeautifulSoup module")


        biography_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)

        if has_image:
            images_page = profile_thumb_parent['href']

            r = requests.get(images_page, verify=False)
            #print("images page is " + images_page + "\n ^ That is all.")
            soup = BeautifulSoup(r.content, "html5lib")

            if actor_to_search.thumbnail == const.UNKNOWN_PERSON_IMAGE_PATH or force:
                if soup.find("div", {'id': 'PictureList'}):

                    picture_list = soup.find("div", {'id': 'PictureList'})

                    if picture_list.find("a"):
                        first_picture = picture_list.find("a")
                        #print(str(picture_list) + "is first_picture")
                        save_path = os.path.join(videos.const.MEDIA_PATH, 'actor/' + str(actor_to_search.id) + '/profile/')
                        print("Profile pic path: " + save_path)
                        save_file_name = os.path.join(save_path, 'profile.jpg')
                        if not os.path.isfile(save_file_name):
#        print("Skipping, as there's already a photo for the profile.")
                        #if not os.path.isfile(save_path):
                            if first_picture['href']:
                                if re.match(r'^\/\/', first_picture['href']):
                                        first_picture_link = "https:" + first_picture['href']
                                        print(first_picture_link)
                                        aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search,force)
                                        print("Image Saved!")
                                elif re.match(r'^.*jpg$', first_picture['href']):
                                        first_picture_link = first_picture['href']
                                        print(first_picture_link)
                                        aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search,force)
                                        print("Image Saved!")
                                else:
                                        print("No picture found!")
                        else:
                            print("Skipping photo download, as there's already a photo for the profile.\nIt's probably from TMDB, therefore a better one.")
        #remember to remark:
        #actor_to_search.last_lookup = datetime.datetime.now()
        #actor_to_search.save()
        #return success
                                   

        r = requests.get(biography_page, verify=False)

        soup = BeautifulSoup(r.content, "html5lib")

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
                if str(actor_to_search.measurements) != "None":
                    cupSize = onlyChars(actor_to_search.measurements)
                    print("Measurements added: " + actor_to_search.measurements)
                else:
                    cupSize = ""
                if len(cupSize)>0:
                    insert_actor_tag(actor_to_search, cupSize + " Cup")
                    print("Stripped measurements for cup size - this actor has a "+cupSize+" cup.")                
                    accepted_stringsTiny = {'A'}
                    accepted_stringsSmall = {'B'}
                    accepted_stringsReg = {'C'}       
                    accepted_stringsBig = {'D', 'E', 'F'}
                    accepted_stringsVBig = {'G', 'H', 'I'}
                    accepted_stringsHuge = {'J', 'K', 'L', 'M'}
                    accepted_stringsMassive = {'N', 'O', 'P', 'Q', 'R', 'S'}
                    accepted_stringsExtreme = {'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
                    cupSizePart=[cupSize]
        
                    try:
                        success=True
                        done=False
                        actor_to_search.last_lookup = datetime.datetime.now()
                        while not done:
                            for cupSizePart in cupSize:
                                if (cupSizePart in accepted_stringsTiny):
                                    insert_actor_tag(actor_to_search, "Tiny tits")
                                    print("Added tag: Tiny tits")
                                    done=True

                                if (cupSizePart in accepted_stringsSmall):
                                    insert_actor_tag(actor_to_search, "Small tits")
                                    print("Added tag: Small tits")
                                    done=True

                                if (cupSizePart in accepted_stringsReg):
                                    insert_actor_tag(actor_to_search, "Medium tits")
                                    print("Added tag: Medium tits")
                                    done=True
                        
                                elif (cupSizePart in accepted_stringsBig):
                                    insert_actor_tag(actor_to_search, "Big tits")
                                    print("Added tag: Big tits")
                                    done=True

                                elif (cupSizePart in accepted_stringsVBig):
                                    insert_actor_tag(actor_to_search, "Very big tits")                  
                                    print("Added tag: Very big tits")
                                    done=True

                                elif (cupSizePart in accepted_stringsHuge):
                                    insert_actor_tag(actor_to_search, "Huge tits")    
                                    print("Added tag: Huge tits")
                                    done=True

                                elif (cupSizePart in accepted_stringsMassive):
                                    insert_actor_tag(actor_to_search, "Massively huge tits")     
                                    print("Added tag: Massively huge tits")
                                    done=True

                                elif (cupSizePart in accepted_stringsExtreme):
                                    insert_actor_tag(actor_to_search, "Extremely huge tits")                            
                                    print("Added tag: Extremely huge tits")
                                    done=True
                    
                                if done: break
                            if done: break
                    except: pass

            elif link_text == 'Tattoos:':
                if not actor_to_search.tattoos:
                    tattoos = next_td_tag.text.strip("'/\n/\t")
                    actor_to_search.tattoos = tattoos
                    print ("Tattoos: " + tattoos)
            elif link_text == 'Piercings:':
                if not actor_to_search.piercings:
                    piercings = next_td_tag.text.strip("'/\n/\t")
                    actor_to_search.piercings = piercings
                    print ("Piercings: " + piercings)
            elif link_text == 'Extra text:':
                if not actor_to_search.extra_text:
                    actor_to_search.extra_text = next_td_tag.text.strip("'/\n/\t")
            elif link_text == 'Fake boobs:':
                fake_boobs = next_td_tag.text.strip("',/\n/\t")
                if "Yes" in fake_boobs:
                    insert_actor_tag(actor_to_search, "Fake tits")
                    print("Her tits are fake, added that tag")
                else:
                    insert_actor_tag(actor_to_search, "Natural tits")
                    print("Her tits are natural, added that tag")
            elif link_text == 'Eye Color:':
                eye_color = next_td_tag.text.strip("',/\n/\t")
                eye_color = eye_color.title() + " eyes"


                if eye_color:
                    insert_actor_tag(actor_to_search, eye_color)
            elif link_text == 'Hair Color:':
                hair_color = next_td_tag.text.strip("',/\n/\t")
                hair_color = hair_color.title() + ' hair'
                if hair_color:
                    insert_actor_tag(actor_to_search, hair_color)
            elif link_text == 'Social Network Links:':
                social = next_td_tag  # ul id="socialmedia
                all_social = social.find_all("a") #was: li
                actor_to_search.official_pages = ""
                for social_link in all_social:
                    try:
                        href = social_link['href']
                        if href not in actor_to_search.official_pages:
                            actor_to_search.official_pages = actor_to_search.official_pages + social_link['href'] + ","  
                            print ("Social Network Link added: " + social_link['href'])
                    except:
                        pass

        if not (actor_to_search.description) or (len(actor_to_search.description)<72):
            actor_to_search.description = free_ones_biography
            print("There's no description or it's too short, so it's added from Freeones.")

        if "Black" in ethnicity:
            insert_actor_tag(actor_to_search, "Black")
            print ("Adding Ethnicity: Black")
        elif "Asian" in ethnicity:
            insert_actor_tag(actor_to_search, "Asian")
            print ("Adding Ethnicity: Asian")
        elif "Latin" in ethnicity:
            insert_actor_tag(actor_to_search, "Latin")
            print ("Adding Ethnicity: Latin")
        elif "Caucasian" in ethnicity:
            insert_actor_tag(actor_to_search, "Caucasian")
            print ("Adding Ethnicity: Caucasian")
        elif "Middle Eastern" in ethnicity:
            insert_actor_tag(actor_to_search, "Middle Eastern")
            print ("Adding Ethnicity: Middle Eastern")
        elif "Arabic" in ethnicity:
            insert_actor_tag(actor_to_search, "Arabic")
            print ("Adding Ethnicity: Arabic")
        elif "Inuit" in ethnicity:
            insert_actor_tag(actor_to_search, "Inuit")
            print ("Adding Ethnicity: Inuit")

        aux.send_piercings_to_actortag(actor_to_search)
    #    updatepiercings.sendAllPiercings()
    #    use the above whenever you want to update all piercings in db

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
            #print("Before: " + name)
            name = name.replace(char, "")
            print("Adding Data: " + name)
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
            #print(link.text, link.get("href"))
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

    if force:
        success = search_freeones(actor_to_search, alias, force)
    elif not actor_to_search.last_lookup:
        success = search_freeones(actor_to_search, alias, force)

    return success


def main():
    print("test")
    for actor in Actor.objects.all():

        print("Fetching info for: " + actor.name)
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
