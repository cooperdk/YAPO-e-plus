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

def inchtocm(input):
    if cm.isdigit(): cm=int(cm)*2.54
    return cm

def search_freeones(actor_to_search, alias, force):
    success = False
    if Actor.objects.get(name=actor_to_search.name):
        actor_to_search = Actor.objects.get(name=actor_to_search.name)
    name = actor_to_search.name
    
#    actor_to_search.last_lookup = datetime.datetime.now()
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
        name_with_dash = alias.name.replace(' ', '-')        
        print("Searching Freeones for: " + actor_to_search.name + " alias: " + alias.name+"...",end="")
        name = alias.name
    else:
        name_with_plus = name.replace(' ', '+')
        name_with_dash = name.replace(' ', '-')
        print("Searching Freeones for: " + actor_to_search.name + " as " + name+"...",end="")
    r = requests.get("https://www.freeones.com/babes?q=" + name_with_dash, verify=False)
    #print("Working with " + "https://www.freeones.com/babes?q=" + name_with_dash + "...")
    soup = BeautifulSoup(r.content, "html5lib")


    # link = soup.find_all("a", {"text": "Isis Love"})

    soup_links = soup.find_all("a")
    #print (soup_links)
    href_found = match_link_to_query(soup_links, name_with_dash)
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
        print("Found.")
        actor_to_search.gender = 'F'
        actor_to_search.save()
        actor_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
        r = requests.get(actor_page, verify=False)
        #print (actor_page)
        soup = BeautifulSoup(r.content, "html5lib")
        soup_links = soup.find_all("a")
        #print(soup_links)
        href_found = "/"+name_with_dash + "/profile" #match_text_in_link_to_query(soup_links, "Profile")
        #print("Found Profile text: " + href_found)
        free_ones_bio_search = soup.find_all("div", {"class": "js-read-more-text read-more-text-ellipsis"})
        #print(free_ones_bio_search)
        free_ones_career_status_search = soup.find_all("p", {"class": "dashboard-bio-career-status-text"})
        free_ones_biography = free_ones_bio_search[0].text.strip()
        free_ones_country_search = soup.find_all("p", {"class": "color-text-dark font-size-xs font-weight-bold mb-1"})
        for link in free_ones_country_search:
            next_td_tag = link.findNext('p')
            link_text = link.text.strip("',/\n/\t")
            if link_text == "Country":
                title=link.findNext('a')
                free_ones_country=title.get('title')
                print("10%",end="\r",flush=True)
                actor_to_search.country_of_origin = free_ones_country
        #if len(free_ones_biography)>10: print("Biography saved.")
        #print("Bio: " + free_ones_biography)
        #print("Looking for a profile image... ", end = "")
        has_image=False
        try:
            #print("Scanning...")
            profile_thumb = soup.find("img", {'class': 'img-fluid'})
            #print("Find it...")
            profile_thumb_parent = profile_thumb.parent
            #print("Getting parent...")
            href=profile_thumb_parent['href']
            if href[0]=="/": href = "https://www.freeones.com" + href
            #print(href)
            has_image = False
            if len(href)>3:     
                has_image = True
        except:
            #print("Parse Error - not getting any image.")
            pass
        

        biography_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
        #print ("Bio: " + biography_page)
        if has_image:
            images_page = href

            if ("freeones.com" in images_page.lower()):
                r = requests.get(images_page, verify=False)
                #print("There is at least one picture reference.\nURL: " + images_page + ".")
                soup = BeautifulSoup(r.content, "html5lib")

            if actor_to_search.thumbnail == const.UNKNOWN_PERSON_IMAGE_PATH or force:
                if not("freeones.com" in images_page.lower()):
                    print("15%",end="\r",flush=True)
                elif soup.find("section", {'id': 'fxgp-gallery'}):
                    print("15%",end="\r",flush=True)
                    picture_list = soup.find("section", {'id': 'fxgp-gallery'})

                    if picture_list.find("a"):
                        first_picture = picture_list.find("a")
                        #print("Saving... ", end="")
                        save_path = os.path.join(videos.const.MEDIA_PATH, 'actor/' + str(actor_to_search.id) + '/profile/')
                        #print("Profile pic path: " + save_path)
                        save_file_name = os.path.join(save_path, 'profile.jpg')
                        if not os.path.isfile(save_file_name):
#        print("Skipping, as there's already a photo for the profile.")
                        #if not os.path.isfile(save_path):
                            if first_picture['href']:
                                if re.match(r'^\/\/', first_picture['href']):
                                        first_picture_link = "https:" + first_picture['href']
                                        aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search,force)
                                        print("20%",end="\r",flush=True)
                                elif re.match(r'^.*jpg$', first_picture['href']):
                                        first_picture_link = first_picture['href']
                                        aux.save_actor_profile_image_from_web(first_picture_link, actor_to_search,force)
                                        print("20%",end="\r",flush=True)
                                else:
                                        print("20%",end="\r",flush=True)
                        #else:
                            #print("Skipping photo, as there's already a photo for the profile.")

        #remember to remark:
        #actor_to_search.last_lookup = datetime.datetime.now()
        #actor_to_search.save()
        #return success
                                   

        r = requests.get(biography_page, verify=False)

        soup = BeautifulSoup(r.content, "html5lib")

        soup_links = soup.find_all("p", {'class': ['heading', 'mb1']})
        #print (soup_links)
        num = 1
        for link in soup_links:
            #print (link)
            next_td_tag = link.findNext('p')
            link_text = link.text.strip("',/\n/\t")  #link.get_text(strip=True)  #.strip("',/\r\n/\t")   #link.text.strip("',/\n/\t") get_text()
            #print (str(num) + ": " + link_text)
            num=+1
            if link_text == 'Ethnicity':
                print("60%",end="\r",flush=True)
                #print("E: ",end="")
                next_td_tag = link.findNext('p')
                next_td_tag = link.findNext('p')
                ethnicity = next_td_tag.get_text(strip=True)  #next_td_tag.text.strip("',/\n/\t")
                #print(ethnicity)
                if not actor_to_search.ethnicity:
                    actor_to_search.ethnicity = ethnicity
            elif link_text == 'Personal Information':
                print("40%",end="\r",flush=True)
                #print(next_td_tag.text)
                if next_td_tag.text.strip("',/\n/\t"):
                    
                    free_ones_date_of_birth = next_td_tag.get_text(strip=True) #.strip("',/\n/\t")
                    free_ones_date_of_birth = free_ones_date_of_birth.replace("Born On ", "")
                    #print("DOB - " + free_ones_date_of_birth )
                    if re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth):
                        parse_date_time = re.search(r'(\w+ \d{1,2}, \d{4})', free_ones_date_of_birth)
                        if parse_date_time.group(0):
                            parse_date_time = parse_date_time.group(0)
                            parse_date_time = parse(parse_date_time.encode('utf-8'), fuzzy=True, ignoretz=True)
                            actor_to_search.date_of_birth = parse_date_time
                            print("45%",end="\r",flush=True)


            elif link_text == 'Aliases':
                print("50%",end="\r",flush=True)
                try:
                    actor_aliases = next_td_tag.text.strip("'/\n/\t")
                    actor_aliases = actor_aliases.replace(", ", ",")
                    insert_aliases(actor_to_search, actor_aliases)
                except:
                    pass
            elif link_text == 'Height':
                print("75%",end="\r",flush=True)
                if not actor_to_search.height:
                    height = next_td_tag.get_text(strip=True)  #tag.text.strip("'/\n/\t")
                    if len(height)<1 or height=="Unknown": height="0"
                    #print("Height: " + str(height))
                    height=re.findall(r'[\d]+', height)
                    height=int(height[0])
                    #print("Truncated: "+str(height))
                    #height = re.search(r'heightcm = \"(\d+)\"', height)
                    #height = height.group(1)
                    actor_to_search.height = height
                height=int(actor_to_search.height)
                doneX=False
                if not doneX and height is not None:
                    if height > 110:
                        if  height < 148:
                            insert_actor_tag(actor_to_search, "Extremely tiny actor")
                            #print("Added tag: Extremely tiny actor")
                            doneX=True
                        if 148 < height < 152:
                            insert_actor_tag(actor_to_search, "Tiny actor")
                            #print("Added tag: Tiny actor")
                            doneX=True
                        if 152 < height < 161:
                            insert_actor_tag(actor_to_search, "Petite actor")
                            #print("Added tag: Petite actor")
                            doneX=True
                        if 178 < height < 186:
                            insert_actor_tag(actor_to_search, "Tall actor")
                            #print("Added tag: Tall actor")
                            doneX=True
                        if 186 < height < 220:
                            insert_actor_tag(actor_to_search, "Extremely tall actor")
                            #print("Added tag: Extremely tall actor")
                            doneX=True
                        print("77%",end="\r",flush=True)
                
            elif link_text == 'Weight':
                print("80%",end="\r",flush=True)
                if not actor_to_search.weight:

                    weight = next_td_tag.get_text(strip=True)  #tag.text.strip("'/\n/\t")
                    if len(weight)<1 or weight=="Unknown": weight="0"
                    #print("Weight: "+str(weight))
                    weight = re.findall(r'[\d]+', weight)
                    weight = int(weight[0])
                    actor_to_search.weight = weight
                    #print("Truncated: "+str(weight))


                    
            elif link_text == 'Measurements':
                print("85%",end="\r",flush=True)
                cupSize = ""
                if not actor_to_search.measurements:
                    #print("There are no measurements...")
                    actor_to_search.measurements = next_td_tag.get_text(strip=True)  #text.strip("'/\n/\t")
                    if len(actor_to_search.measurements)>8:
                        try:
                            measure=re.findall(r'[\d]+', actor_to_search.measurements)
                            che=int(measure[0])
                            wai=int(measure[1])
                            hip=int(measure[2])
                            #che=int(che*2.54)
                            #wai=int(wai*2.54)
                            #hip=int(hip*2.54)
                            cupSize = onlyChars(actor_to_search.measurements)
                            actor_to_search.measurements=str(che)+cupSize+"-"+str(wai)+"-"+str(hip)
                        except: pass    
                        #print("Measurements: " + actor_to_search.measurements)
                    else:
                        actor_to_search.measurements="??-??-??"
                cupSize = onlyChars(actor_to_search.measurements)
                
                if len(cupSize)>0:
                    insert_actor_tag(actor_to_search, cupSize + " Cup")
                    #print("This actor has a "+cupSize+" cup.")                
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
                        doneY=False
                        #actor_to_search.last_lookup = datetime.datetime.now()
                        print("90%",end="\r",flush=True)
                        while not doneY:
                            for cupSizePart in cupSize:
                                if (cupSizePart in accepted_stringsTiny):
                                    insert_actor_tag(actor_to_search, "Tiny tits")
                                    #print("Added tag: Tiny tits")
                                    doneY=True

                                if (cupSizePart in accepted_stringsSmall):
                                    insert_actor_tag(actor_to_search, "Small tits")
                                    #print("Added tag: Small tits")
                                    doneY=True

                                if (cupSizePart in accepted_stringsReg):
                                    insert_actor_tag(actor_to_search, "Medium tits")
                                    #print("Added tag: Medium tits")
                                    doneY=True
                        
                                elif (cupSizePart in accepted_stringsBig):
                                    insert_actor_tag(actor_to_search, "Big tits")
                                    #print("Added tag: Big tits")
                                    doneY=True

                                elif (cupSizePart in accepted_stringsVBig):
                                    insert_actor_tag(actor_to_search, "Very big tits")                  
                                    #print("Added tag: Very big tits")
                                    doneY=True

                                elif (cupSizePart in accepted_stringsHuge):
                                    insert_actor_tag(actor_to_search, "Huge tits")    
                                    #print("Added tag: Huge tits")
                                    doneY=True

                                elif (cupSizePart in accepted_stringsMassive):
                                    insert_actor_tag(actor_to_search, "Massively huge tits")     
                                    #print("Added tag: Massively huge tits")
                                    doneY=True

                                elif (cupSizePart in accepted_stringsExtreme):
                                    insert_actor_tag(actor_to_search, "Extremely huge tits")                            
                                    #print("Added tag: Extremely huge tits")
                                    doneY=True
                    
                                if done: break
                            if done: break
                    except: pass

            elif link_text == 'Tattoos':
                print("95%",end="\r",flush=True)
                if not actor_to_search.tattoos:
                    tattoos = next_td_tag.get_text(strip=True) #text.strip("'/\n/\t")
                    actor_to_search.tattoos = tattoos.capitalize()
                    #print ("Tattoos: " + actor_to_search.tattoos)

            elif link_text == 'Piercings':
                print("97%",end="\r",flush=True)
                if not actor_to_search.piercings:    
                    piercings = next_td_tag.get_text(strip=True)  #text.strip("'/\n/\t")
                    actor_to_search.piercings = piercings
                    #print ("Piercings: " + piercings)
            elif link_text == 'Additional Information':

                if not actor_to_search.extra_text:
                    actor_to_search.extra_text = next_td_tag.get_text(strip=True)   #text.strip("'/\n/\t")
                    #print("Additional information saved.")
            elif link_text == 'Fake Boobs':
                print("98%",end="\r",flush=True)
                fake_boobs = next_td_tag.get_text(strip=True) #.strip("',/\n/\t")
                if "Yes" in fake_boobs:
                    insert_actor_tag(actor_to_search, "Fake tits")
                    #print("Her tits are fake, added that tag")
                else:
                    insert_actor_tag(actor_to_search, "Natural tits")
                    #print("Her tits are natural, added that tag")
            elif link_text == 'Eye Color':
                print("70%",end="\r",flush=True)
                eye_color = next_td_tag.get_text(strip=True) #text.strip("',/\n/\t")
                eye_color = eye_color.title() + " eyes"
                if eye_color:
                    insert_actor_tag(actor_to_search, eye_color)
                    #print (eye_color)
            elif link_text == 'Hair Color':
                print("72%",end="\r",flush=True)
                hair_color = next_td_tag.get_text(strip=True) #text.strip("',/\n/\t")
                hair_color = hair_color.title() + ' hair'
                if hair_color:
                    insert_actor_tag(actor_to_search, hair_color)
                    #print (hair_color)
                    
            elif link_text=="Official website":
                print("60%",end="\r",flush=True)
                official = link.findNext('div')  # ul id="socialmedia
                all_official = official.find_all("a") #was: li
                actor_to_search.official_pages = ""            
                for official_link in all_official:
                    try:
                        href = official_link['href']
                        if href not in actor_to_search.official_pages:
                            actor_to_search.official_pages = actor_to_search.official_pages + official_link['href'] + ","  
                            #print ("Official Website added: " + official_link['href'])
                    except:
                        #print("Actor apparently has no official website")
                        pass
                        
            elif link_text == 'Follow On':
                #print("Social links...")
                print("65%",end="\r",flush=True)
                social = link.findNext('div')  # ul id="socialmedia
                all_social = social.find_all("a") #was: li
                #actor_to_search.official_pages = ""
                for social_link in all_social:
                    try:
                        href = social_link['href']
                        #print("Social link: " + href)
                        if href not in actor_to_search.official_pages:
                            actor_to_search.official_pages = actor_to_search.official_pages + social_link['href'] + ","  
                            #print ("Social Network Link added: " + social_link['href'])
                    except:
                        #print("Actor apparently has no social links")
                        pass

        if not (actor_to_search.description) or (len(actor_to_search.description)<72):
            actor_to_search.description = free_ones_biography
            #print("There's no description or it's too short, so it's added from Freeones.")
        print("99%",end="\r",flush=True)
        if "Black" in ethnicity:
            insert_actor_tag(actor_to_search, "Black")
            #print ("Adding Ethnicity: Black")
        elif "Asian" in ethnicity:
            insert_actor_tag(actor_to_search, "Asian")
            #print ("Adding Ethnicity: Asian")
        elif "Latin" in ethnicity:
            insert_actor_tag(actor_to_search, "Latin")
            #print ("Adding Ethnicity: Latin")
        elif "Caucasian" in ethnicity:
            insert_actor_tag(actor_to_search, "Caucasian")
            #print ("Adding Ethnicity: Caucasian")
        elif "Middle Eastern" in ethnicity:
            insert_actor_tag(actor_to_search, "Middle Eastern")
            #print ("Adding Ethnicity: Middle Eastern")
        elif "Arabic" in ethnicity:
            insert_actor_tag(actor_to_search, "Arabic")
            #print ("Adding Ethnicity: Arabic")
        elif "Inuit" in ethnicity:
            insert_actor_tag(actor_to_search, "Inuit")
            #print ("Adding Ethnicity: Inuit")

        print("100%",end="\r",flush=True)
        aux.send_piercings_to_actortag(actor_to_search)
    #    updatepiercings.sendAllPiercings()
    #    use the above whenever you want to update all piercings in db

        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()

    else:
        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()

    #try:
        #print("Inserted extra additional information:")
        #if ethnicity is not None: print("Ethnicity: " + ethnicity)
        #if ctry is not None: print("Country: " + ctry)
        #if parse_date_time is not None: print("DOB: " + str(parse_date_time))
        #if actor_aliases is not None: print("Aliases: " + actor_aliases)
        #if height is not None: print("Height: " + str(height))
        #if weight is not None: print("Weight: " + str(weight))
        #if eye_color is not None: print("Eye color: " + eye_color)
        #if hair_color is not None: print("Hair color: " + hair_color)
    #except: pass
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


def match_link_to_query(soup_links, text_to_find):
    ans = None
    for link in soup_links:
        try:
            if link.get("href").replace('/', '').lower() == text_to_find.lower():
                print(link.get("href"))
                ans = link.get("href")
                break
        except: print("Error")
    return ans

def match_text_in_link_to_query(soup_links, text_to_find):
    ans = None
    ct = 0
    for link in soup_links:
        if ct < 2: print (link.text.lower().strip())
        ct=+1
        if link.text.lower() == text_to_find.lower():
            print(link.text, link.get("href"))
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
