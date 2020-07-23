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
from bs4 import BeautifulSoup
from dateutil.parser import parse
import videos.const as const
from django.utils import timezone
from utils.printing import Logger
log = Logger()

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

django.setup()

from videos.models import Actor, ActorAlias, ActorTag


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

# MEDIA_PATH = "videos\\media"

def onlyChars(input):
    valids = "".join(char for char in input if char.isalpha())
    return valids

def inchtocm(input):
    if cm.isdigit(): cm=int(cm)*2.54
    return cm

def sendAllPiercings():
    actors = Actor.objects.all()
    for actor in actors:
        aux.send_piercings_to_actortag(actor)

def search_freeones(actor_to_search, alias, force):
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
        print(f"Searching Freeones for: {actor_to_search.name}... ",end="")
    r = requests.get(f"https://www.freeones.com/babes?q={name_with_dash}", verify=False)

    soup = BeautifulSoup(r.content, "html5lib")

    soup_links = soup.find_all("a")

    href_found = match_link_to_query(soup_links, name_with_dash)


    if href_found:
    
        success = True
        print("\r")
        aux.progress(1,27,f"Found {actor_to_search.name}, parsing...")
        #print("\nI found " + actor_to_search.name + ", so I am looking for information on her profile page.")
        actor_to_search.gender = 'F'
        actor_to_search.save()
        actor_page = urllib_parse.urljoin("https://www.freeones.com/", href_found)
        r = requests.get(actor_page, verify=False)

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
        #print ("Bio: " + biography_page)
        if has_image:
            images_page = href

            if ("freeones.com" in images_page.lower()):
                r = requests.get(images_page, verify=False)
                #print("There is at least one picture reference.\nURL: " + images_page + ".")
                soup = BeautifulSoup(r.content, "html5lib")

            if actor_to_search.thumbnail == const.UNKNOWN_PERSON_IMAGE_PATH or force:
                if not("freeones.com" in images_page.lower()):
                    aux.progress(3,27,"Searching for Photo")
                elif soup.find("section", {'id': 'fxgp-gallery'}):
                    aux.progress(3,27,"Searching for Photo")
                    picture_list = soup.find("section", {'id': 'fxgp-gallery'})

                    if picture_list.find("a"):
                        first_picture = picture_list.find("a")
                        #print("Saving... ", end="")
                        save_path = os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor_to_search.id), 'profile')
                        #print("Profile pic path: " + save_path)
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
                                   

        r = requests.get(biography_page, verify=False)
        soup = BeautifulSoup(r.content, "html5lib")
        soup_links = soup.find_all("p", {'class': ['heading', "text-center", "pt-1"]}) # {'class': ['heading', 'mb1']})    ("p", {'class': ['profile-meta-item']})
        #print (soup_links)

        aux.progress(5,29,"Parsing info")
        for link in soup_links:
            #print (link)
            next_td_tag = link.findNext('p')
            link_text = link.text.strip("',/\n/\t")  #link.get_text(strip=True)  #.strip("',/\r\n/\t")   #link.text.strip("',/\n/\t") get_text()

            num+=1
            #if num==1: print (str(num) + ": " + link_text)
            if link_text.strip().lower() == 'personal information':
           

                if not actor_to_search.date_of_birth:
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
                                aux.progress(6,29,"Birthday")
                                
            elif link_text.lower() == 'ethnicity':
                if not actor_to_search.ethnicity:
                    #print("E: ",end="")
                    next_td_tag = link.findNext('p')
                    next_td_tag = link.findNext('p')
                    ethnicity = next_td_tag.get_text(strip=True)  #next_td_tag.text.strip("',/\n/\t")
                    #print(ethnicity)
                    actor_to_search.ethnicity = ethnicity
                    aux.progress(7,29,"Ethnicity")
                #else:
                    #ethnicity = actor_to_search.ethnicity 

                    
            elif link_text.lower()=="official website":
                official = link.findNext('div')  # ul id="socialmedia
                all_official = official.find_all("a") #was: li
                actor_to_search.official_pages = ""            
                for official_link in all_official:
                    try:
                        href = official_link['href']
                        if href not in actor_to_search.official_pages:
                            actor_to_search.official_pages += f"{official_link['href']},"  
                            #print ("Official Website added: " + official_link['href'])
                    except:
                        #print("Actor apparently has no official website")
                        pass
                aux.progress(8,29,"Official WWW")

            elif link_text.lower() == 'aliases':
                try:
                    actor_aliases = next_td_tag.text.strip("'/\n/\t")
                    if not("Unknown" in actor_aliases):
                        actor_aliases = actor_aliases.replace(", ", ",")
                        insert_aliases(actor_to_search, actor_aliases)
                except:
                    pass
                aux.progress(9,29,"Aliases")

            elif link_text.lower() == 'follow on':

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
                            insert_actor_tag(actor_to_search, eye_color)
                        aux.progress(12,29,"Eye color")

                    elif link2_text.lower().strip() == 'hair color':
                        next_td_tag1 = link2.find_next('span').find_next('span').find_next('span')
                        hair_color = next_td_tag1.get_text(strip=True) #text.strip("',/\n/\t")
                        hair_color = hair_color.title() + ' hair'
                        if hair_color and len(hair_color)>7:
                            insert_actor_tag(actor_to_search, hair_color)
                        aux.progress(13,29,"Hair color")

                    elif link2_text.lower().strip() == 'height':
                        next_td_tag1 = link2.find_next('span').find_next('span')
                        if not actor_to_search.height:
                            height = next_td_tag1.get_text(strip=True)  #tag.text.strip("'/\n/\t")
                            if len(height)<1 or height=="Unknown": height="0"
                            #print("Height: " + str(height))
                            height=re.findall(r'[\d]+', height)
                            height=int(height[0])
                            #print("Truncated: "+str(height))
                            #height = re.search(r'heightcm = \"(\d+)\"', height)
                            #height = height.group(1)
                            actor_to_search.height = height
                        height=int(actor_to_search.height)
                        aux.progress(14,29,"Height")
                        doneX=False
                        if not doneX and height is not None:
                            if height > 100:
                                if  height < 148:
                                    insert_actor_tag(actor_to_search, "Extremely tiny")
                                    #print("Added tag: Extremely tiny")
                                    doneX=True
                                if 148 < height < 152:
                                    insert_actor_tag(actor_to_search, "Tiny")
                                    #print("Added tag: Tiny")
                                    doneX=True
                                if 152 < height < 161:
                                    insert_actor_tag(actor_to_search, "Petite")
                                    #print("Added tag: Petite")
                                    doneX=True
                                if 178 < height < 186:
                                    insert_actor_tag(actor_to_search, "Tall")
                                    #print("Added tag: Tall")
                                    doneX=True
                                if 186 < height < 220:
                                    insert_actor_tag(actor_to_search, "Extremely tall")
                                    #print("Added tag: Extremely tall")
                                    doneX=True
                                aux.progress(15,29,"Height [Group tag]")
                        
                    elif link2_text.lower().strip() == 'weight':
                        next_td_tag1 = link2.find_next('span').find_next('span')
                        if not actor_to_search.weight:

                            weight = next_td_tag1.get_text(strip=True)  #tag.text.strip("'/\n/\t")
                            if len(weight)<1 or weight=="Unknown": weight="0"
                            weight = re.findall(r'[\d]+', weight)
                            weight = int(weight[0])
                            actor_to_search.weight = weight
                            aux.progress(16,29,"Weight")

                    elif link2_text.lower().strip() == 'measurements':
                            #next_td_tag1 = link2.find_next('a')
                        cupSize = ""
                        if not actor_to_search.measurements or actor_to_search.measurements=="":
                            try:
                                mea = link2.find_next('span').find_next('span').get_text(strip=True)
                                #print(mea)
                                meas=mea.split("-")
                                measlen = len(meas)
                                if measlen == 2 and meas[1] == "": measlen = 1
                                if measlen == 3 and meas[2] == "": measlen = 2

                                #print("\n\n\n" + str(measlen) + "\n\n\n")
                                #print ("\n\n" + che + "\n\n")
                                che = meas[0]
                                #print ("CHE " + str(che))
                                if measlen > 1:
                                    wai = meas[1]
                                else:
                                    wai = "??"
                                #print ("WAI " + str(wai))
                                if measlen > 2:
                                    hip = meas[2]
                                else:
                                    hip = "??"
                                #print("HIP " + str(hip))
                                #if not che: che="??"
                                #if not wai: wai="??"
                                #if not hip: hip="??"
                                #if not(isinstance(wai, int)): wai = "??"
                                #if not(isinstance(hip, int)): hip = "??"
                                measure = str(che) + "-" + str(wai) + "-" + str(hip)
                            except:
                                pass
                            actor_to_search.measurements = measure            #next_td_tag1.get_text(strip=True)  #text.strip("'/\n/\t")
                            aux.progress(17,29,"Measurements")
                            #if actor_to_search.measurements[-1]=="-": actor_to_search.measurements=actor_to_search.measurements[:-1]
                            if len(actor_to_search.measurements)>8  or len(actor_to_search.measurements)==3:
                                try:
                                    measure=re.findall(r'[\d]+', actor_to_search.measurements)
                                    che=int(measure[0])
                                    wai=int(measure[1])
                                    hip=int(measure[2])
                                    #che=int(che*2.54)
                                    #wai=int(wai*2.54)
                                    #hip=int(hip*2.54)
                                    cupSize = onlyChars(actor_to_search.measurements)
                                    if len(actor_to_search.measurements)==3:
                                        actor_to_search.measurements=str(che)+cupSize
                                    else:
                                        actor_to_search.measurements=str(che)+cupSize+"-"+str(wai)+"-"+str(hip)
                                except: pass    
                            else:
                                actor_to_search.measurements="??-??-??"
                        cupSize = onlyChars(actor_to_search.measurements)
                        
                        if len(cupSize)>0:
                            insert_actor_tag(actor_to_search, cupSize + " Cup")
                            aux.progress(18,29,"Measurements [Cup size]")
            
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
                                aux.progress(19,29,"Measurements [Tits size]")
                            except: pass

                    elif link2_text.lower().strip() == 'boobs':
                       
                        next_td_tag1 = link2.find_next('span')
                        boobs = next_td_tag1.get_text(strip=True) #.strip("',/\n/\t")
                        if "fake" in boobs.lower():
                            insert_actor_tag(actor_to_search, "Fake tits")
                            #print("Her tits are fake, added that tag")
                        else:
                            insert_actor_tag(actor_to_search, "Natural tits")
                            #print("Her tits are natural, added that tag")
                        aux.progress(20,29,"Tits fake/natural")

                    elif link2_text.lower().strip() == 'tattoos':
                        next_td_tag1 = link2.find_next('span').find_next('span').find_next('span')

                        if not actor_to_search.tattoos or actor_to_search.tattoos=="":
                            tattoos = next_td_tag1.get_text(strip=True) #text.strip("'/\n/\t")
                            actor_to_search.tattoos = tattoos.capitalize()
                            aux.progress(21,29,"Tattoos")
                            #print ("Tattoos: " + actor_to_search.tattoos)

                            tattoos = str(actor_to_search.tattoos).strip()
                            tattoos1 = tattoos.replace(";", ",")
                            tattoos1 = tattoos1.replace(" and ", ",")
                            tattoos1 = tattoos1.replace("-", ",")
                            tattoos1 = tattoos1.replace(":", ",")

                            tattoos = tattoos1.split(",")

                            numTattoos = len(tattoos)
                            #print(f"Actor: {actor_to_search.name} - {str(numTattoos)} tattoos", end="")

                            if (numTattoos == 0 or numTattoos is None) or (
                                    tattoos1.lower().strip() == "none"
                                    or tattoos1.lower().strip() == "no tattoos"
                                    or tattoos[0].lower().strip() == "none"
                                    or tattoos[0].lower().strip() == "no tattoos"
                                    or tattoos[0].lower().strip() == "n/a"
                            ):
                                aux.insert_actor_tag(actor_to_search, "No tattoos")

                            if numTattoos == 1 and (
                                    tattoos[0].lower().strip() == "none"
                                    or tattoos1.lower().strip() == "none"
                                    or tattoos1.lower().strip() == "no tattoos"
                                    or tattoos[0].lower().strip() == "no tattoos"
                                    or tattoos[0].lower().strip() == "n/a"
                                    or tattoos1.lower().strip() == "n/a"
                            ):
                                aux.insert_actor_tag(actor_to_search, "No tattoos")

                            if numTattoos == 1 and (
                                    tattoos1.lower().strip() == "various" or tattoos[0].lower().strip() == "various"
                            ):
                                aux.insert_actor_tag(actor_to_search, "Some tattoos")

                            elif numTattoos == 1 and (
                                    tattoos1.lower().strip() != "various"
                                    and tattoos[0].lower().strip() != "various"
                                    and tattoos[0].lower().strip() != "none"
                                    and tattoos[0].lower().strip() != "none"
                                    and tattoos[0].lower().strip() != "unknown"
                                    and tattoos[0].lower().strip() != "no tattoos"
                                    and tattoos[0].lower().strip() != "n/a"
                            ):
                                aux.insert_actor_tag(actor_to_search, "One tattoo")

                            if numTattoos >= 2 and numTattoos <= 4:
                                aux.insert_actor_tag(actor_to_search, "Few tattoos")

                            if numTattoos > 4 and numTattoos <= 6:
                                aux.insert_actor_tag(actor_to_search, "Some tattoos")

                            if numTattoos > 6 and numTattoos <= 8:
                                aux.insert_actor_tag(actor_to_search, "Lots of tattoos")

                            if numTattoos > 8:
                                aux.insert_actor_tag(actor_to_search, "Massive amount of tattoos")

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
                            #print ("Piercings: " + piercings)
                            aux.progress(23,29,"Piercings")
 
            elif link_text == 'Additional Information':
                if not actor_to_search.extra_text:
                    actor_to_search.extra_text = next_td_tag.get_text(strip=True)   #text.strip("'/\n/\t")
                    aux.progress(24,29,"Additional info")

        if not (actor_to_search.description) or (len(actor_to_search.description)<72):
            actor_to_search.description = free_ones_biography
            aux.progress(25,29,"Biography")
            

        
        try:
            if ethnicity is not None:
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
            aux.progress(26,29,"Ethnicity")
        except:
            pass
            

        aux.send_piercings_to_actortag(actor_to_search)
        aux.progress(27,29,"Sending piercings to tags")
    #    sendAllPiercings()
    #    use the above whenever you want to update all piercings in db

        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()
        aux.progress(28,29,"Saving to database")

    else:
        actor_to_search.last_lookup = datetime.datetime.now()
        actor_to_search.save()
        print(" Not Found")
        fail = True
        aux.progress_end()
        print("")
#    try:
    if success:
        aux.progress(29,29,f"{num} tags parsed for {actor_to_search.name}.")
        aux.progress_end()
        print("")
        log.info(f"Actor scraped: {actor_to_search.name}")
#    except:
#        pass
        #aux.progress(29,29,str(num) + " tags parsed for " + actor_to_search.name + ".")
        #aux.progress_end()
        #print("")
    return success

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
                print(e)


def match_link_to_query(soup_links, text_to_find):
    ans = None
    for link in soup_links:
        try:
            if link.get("href").replace('/', '').lower() == text_to_find.lower():
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

    if force:
        success = search_freeones(actor_to_search, alias, force)
    elif not actor_to_search.last_lookup:
        success = search_freeones(actor_to_search, alias, force)

    return success


def main():
    #print("test")
    for actor in Actor.objects.all():

        #print("Fetching info for: " + actor.name)
        if not actor.gender == 'M':
            time.sleep(10)
            sucess = search_freeones_with_force_flag(actor, True)
            if not sucess:
                for alias in actor.actor_aliases.all():
                    sucess = search_freeones_alias(actor, alias, True)
                    if sucess:
                        break

        #print("Done!")

        # actor = Actor()
        # actor.name = "Daisy Marie"
        # search_freeones(actor)



if __name__ == "__main__":
    main()
