import os
import sys
from videos.models import *
from configuration import Config, Constants
#from dateutil.parser import parse
import datetime
import urllib.request
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError
from urllib.parse import quote
import http.client
from http.client import IncompleteRead, BadStatusLine
http.client._MAXHEADERS = 1000
from http.client import IncompleteRead, BadStatusLine
import argparse
import ssl
import datetime
import platform
import json
import re
http.client._MAXHEADERS = 1000
import socket
import requests
import shutil
from lxml import html
from utils.printing import Logger
log = Logger()


def progress(count: int, total: int, suffix=''):
    bar_len = 36
    filled_len = int(round(bar_len * count / float(total)))

    percents = int(round(100 * count / float(total), 1))
    bar = '\u2588' * filled_len + '\u2591' * (bar_len - filled_len)
    #bar = '█' * filled_len + '░' * (bar_len - filled_len)
    aaa=(f"\r{bar} ({percents}%) - {suffix}")
    b=len(aaa)
    c=79-b
    print(aaa,end="")  # was sys.stdout.write
    for _ in range(c):
        print(" ",end="")
        if count != total:
            print("\r",end="")


def progress_end():
    print("\n",end="")
    sys.stdout.flush()

def get_human_readable_size(num):
    exp_str = [ (0, 'B'), (10, 'KB'),(20, 'MB'),(30, 'GB'),(40, 'TB'), (50, 'PB'),]
    i = 0
    while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return f'{int(rounded_val)} {exp_str[i][1]}'

def getMemory():
    import psutil
    vmem = psutil.virtual_memory().total
    return vmem  # "{:.2}".format(vmem.total/100000000) #shold that be 102400000?


def getCPU():
    import psutil
    cpuinfo = psutil.cpu_freq()
    # On some systems, 'max' will be 0.0. In this case, use the current speed.
    cpufreqMhz = cpuinfo.current if cpuinfo.max == 0.0 else cpuinfo.max
    return round(cpufreqMhz / 1000, 1)


def getCPUCount():
    import psutil
    return psutil.cpu_count(logical=False)  # set Logical to true if treads are to be included


def sysclear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def restest(height:int):
    if not isinstance(height, int):
        return "???"
    if height < 240:
        res = "240p"
    if 240 < height <= 360:
        res = "360p"
    if 360 < height <= 480:
        res = "480p"
    if 480 < height <= 576:
        res = "576p"
    if 576 < height <= 720:
        res = "720p"
    if 720 < height <= 1080:
        res = "1080p"
    if 1080 < height <= 1440:
        res = "1440p"
    if 1440 < height <= 2160:
        res = "4K"
    if 2160 < height <= 4320:
        res = "8K"
    return res

def send_piercings_to_actortag (actor):
    cnt = 0
    piercings = actor.piercings
    if piercings:
        if ("navel" or "belly button" or "bellybutton") in piercings.lower():
            insert_actor_tag(actor, "Pierced navel")
            cnt += 1
        if "clit" in piercings.lower():
            insert_actor_tag(actor, "Pierced clitoris")
            cnt += 1
        if ("nipples" or "nipple rings") in piercings.lower():
            insert_actor_tag(actor, "Pierced nipples")
            cnt += 1
        elif "nipple" in piercings.lower():
            insert_actor_tag(actor, "Pierced single nipple")
            cnt += 1
        if "septum" in piercings.lower():
            insert_actor_tag(actor, "Pierced septum")
            cnt += 1
        if "nose" in piercings.lower():
            insert_actor_tag(actor, "Pierced nose")
            cnt += 1
        if "nostril" in piercings.lower():
            insert_actor_tag(actor, "Pierced nostril")
            cnt += 1
        if "tongue" in piercings.lower():
            insert_actor_tag(actor, "Pierced tongue")
            cnt += 1
        if "tragus" in piercings.lower():
            insert_actor_tag(actor, "Pierced tragus")
            cnt += 1
        if "helix" in piercings.lower():
            insert_actor_tag(actor, "Pierced helix")
            cnt += 1
        if ("earlobe" or "ear lobe") in piercings.lower():
            insert_actor_tag(actor, "Pierced ear lobe")
            cnt += 1
        if "lower lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced lower lip")
            cnt += 1
        if "upper lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced upper lip")
            cnt += 1
        if "monroe" in piercings.lower():
            insert_actor_tag(actor, "Pierced Monroe")
            cnt += 1
        if ("dermal" or "surface") in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal")
            cnt += 1
        if "wrists" in piercings.lower():
            insert_actor_tag(actor, "Pierced wrists")
            cnt += 1
        elif "wrist" in piercings.lower():
            insert_actor_tag(actor, "Pierced single wrist")
            cnt += 1
        if "hips" in piercings.lower():
            insert_actor_tag(actor, "Pierced hip dermals")
            cnt += 1
        elif "hip" in piercings.lower():
            insert_actor_tag(actor, "Pierced single hip dermal")
            cnt += 1
        if "labia" in piercings.lower():
            insert_actor_tag(actor, "Pierced labia")
            cnt += 1
        if "back dimples" in piercings.lower():
            insert_actor_tag(actor, "Pierced back dimples")
            cnt += 1
        if ("right brow" or "right eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced right eyebrow")
            cnt += 1
        elif ("left brow" or "left eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced left eyebrow")
            cnt += 1
        elif "brow" in piercings.lower():
            insert_actor_tag(actor, "Pierced eyebrow")
            cnt += 1
        if "ears" in piercings.lower():
            insert_actor_tag(actor, "Pierced ears")
            cnt += 1
        elif "left ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced left ear")
            cnt += 1
        elif "right ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced right ear")
            cnt += 1
        if "chest" in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal on chest")
            cnt += 1
        if any([piercings.lower() == "n/a", piercings.lower() == "none", piercings.lower() == "no piercings", piercings.lower() == "no"]):
            insert_actor_tag(actor, "No piercings")
            cnt += 1
        return cnt
    else:
        return 0

def addactor (current_scene, actor_to_add):

    if not current_scene.actors.filter(name=actor_to_add):
        current_scene.actors.add(actor_to_add)
        print(f"Added Actor '{actor_to_add.name}' to scene '{current_scene.name}'")

    if actor_to_add.actor_tags.count() > 0:
        for actor_tag in actor_to_add.actor_tags.all():
            if not current_scene.scene_tags.filter(name=actor_tag.name):
                current_scene.scene_tags.add(
                    actor_tag.scene_tags.first()
                )
                print(
                    f"Added Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{current_scene.name}'"
                )

    current_scene.save()


def insert_actor_tag (actor_to_insert, actor_tag_name):
    actor_tag_name = strip_bad_chars(actor_tag_name)

    if not ActorTag.objects.filter(name=actor_tag_name):
        actor_tag = ActorTag()
        actor_tag.name = actor_tag_name
        actor_tag.save()
        actor_to_insert.actor_tags.add(actor_tag)
    #        print("Added new tag: " + actor_tag_name + " for " + actor_to_insert.name)
    else:
        actor_tag = ActorTag.objects.get(name=actor_tag_name)
        actor_to_insert.actor_tags.add(actor_tag)
        #        print("Added tag: " + actor_tag_name + " for " + actor_to_insert.name)
        actor_tag.save()


def url_is_alive (url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


def remove_text_inside_brackets(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


def tpdb_formatter (name):
    trashTitle = (
        'RARBG', 'COM', '\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', '\d{2,4}K', '\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4',
        'KLEENEX', 'SD', 'H264', 'repack', '1500k', '500k', '1000k', 'rq', 'NEW', 'APT', '[TK]', 'TK', 'hd\d{3,4}p',
        '1500', '1000', 'SD', 'MP4-KT', 'MP4-KTR', 'SEXORS', 'MKV', 'DIVX', 'AVI', 'M4V', 'MP2', 'WEBM', 'MR4', 'GUSH',
        '[TK]', 'rq', ' Unknown -', 'Unknown', '\ss\s'
    )

    name = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', '', name)
    name = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', '', name)
    name = re.sub(r'\d{1,2}\.{0,1}\s{0,1}(January|February|March|April|May|June|July|August|September|October|November|December)\s{0,1}.\d{4}', '', name)
    name = re.sub(r'(\d+)[/\.-](\d+)[/\.-](\d+)', '', name)
    name = re.sub(r'\W', ' ', name)
    for trash in trashTitle:
        name = re.sub(r'\b%s\b' % trash, '', name, flags=re.IGNORECASE)
    name = ' '.join(name.split())

    name = name.replace("(", " ")
    name = name.replace(")", " ")
    name = name.replace("[", " ")
    name = name.replace("]", " ")
    name = name.replace("!", " ")
    name = name.replace("?", " ")
    name = name.replace("_", " ")
    name = remove_text_inside_brackets(name)
    name = re.sub(' +', ' ', name)

    #name = name.replace(" ","+")
    #name = name.replace(".","+")
    #print(f"New name to use for searching: {name}")
    return name

def strip_html (s):
    return str(html.fromstring(s).text_content())


def strip_bad_chars (name):
    bad_chars = { " " }
    for char in bad_chars:
        if char in name:
            # print("Before: " + name)
            name = name.replace(char, "")
            print(f"Adding Data: {name}")
    return name


def is_domain_reachable(host, timeout=5) -> bool:
    """ This function checks to see if a host name has a DNS entry by checking
        for socket info. If the website gets something in return,
        we know it's available to DNS.
    """
    result = True
    try:
        response=requests.head(host, timeout=timeout)
        #socket.gethostbyname(host)
    except Exception as e: #socket.gaierror:
        log.error(f"{host} did not answer within {timeout} seconds. Try again later.")
        result = False
        return result
    if response.status_code < 400:
        result =  True
    elif response.status_code < 500:
        result = False
        log.warn(f"{host} reported a response error {response.status_code}. Please report this to Team YAPO.")
    else:
        result = False
        log.warn(f"{host} reported a server error {response.status_code}.")

    return result


def checkTpDB():
    try:
        request = requests.get("http://api.metadataapi.net/scenes?parse=faye-reagan&limit=1", timeout = 3)
        if request.status_code == 200:
            result = True
        else:
            result = False
            log.warn(f"api.metadataapi.net returns an unexpected reply code: {request.status_code}")

    except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as e:
        log.warn(f"Cannot connect to api.metadataapi.net: {e}")
        result = False
    return result


def save_website_logo(image_link, website, force, *args):
    website = website.strip()

    try:
        ws = None
        print("Website scan, method 1...")
        ws = Website.objects.filter(name=website)

        if ws:
            #print("Found the website locally")
            ws = Website.objects.get(name=website)
            website = ws.name
        if not ws:
            #print("Method unsuccesful, trying method 2...")
            ws = Website.objects.filter(name__iexact=website.replace(" ",""))
            if ws:
                #print("Found 2")
                ws = Website.objects.get(name__iexact=website.replace(" ",""))
                website = ws.name
        if not ws and Config().tpdb_websites:
            print(f"Adding website: {website}")
            hasarg = 0
            for arg in args:
                hasarg += 1
                sceneid = arg
                if hasarg == 1:
                    break

            scene = Scene.objects.get(pk=sceneid)
            ws = Website()
            ws.name = website
            ws.website_alias = website.replace(" ","").lower()
            ws.date_added = datetime.datetime.now()
            ws.save()
            log.info(f"Auto-added website: {ws.name}")
            ws = Website.objects.get(name=website)
            if hasarg == 1:
                scene.websites.add(ws)
                scene.save()
                log.sinfo(f"A scene was added to {ws.name}: {scene.name}")
        if not ws and not Config().tpdb_websites:
                log.info(f"We could add the website {website}, but auto-adding is disabled.")
    except:
        pass


    if image_link:
        if image_link.lower() == "null" or image_link == "":
            print(f"No logo URL available for {website}.")
            success = False
            return
    else:
        print(f"No logo URL available for {website}.")
        success = False
        return



    if not Config().tpdb_website_logos:
        return
    if not ws and not Config().tpdb_websites:
        log.warn(f'LOGO: No website "{website}", and we cannot add it because you didn\'t allow it!')
        return

    ws = Website.objects.get(name=website)
    save_path = os.path.join(Config().site_media_path, "websites", str(ws.id))
    #print("Save path: " + save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Created website directory: {save_path}")
    if os.path.splitext(image_link)[1]:
        ext = os.path.splitext(image_link)[1]
    else:
        print("Error in logo filename!")
        success = False
        return

    save_file_name = os.path.join(save_path, "logo" + ext)
    if (not os.path.isfile(save_file_name) and Config().tpdb_website_logos) or force:

        #print("Saving to " + save_file_name)

        if download_image(image_link, save_file_name):
            ws = Website.objects.get(name=website)
            print("OK")
            rel_path = os.path.relpath(save_file_name, start="data")
            as_uri = urllib.request.pathname2url(rel_path)
            ws.thumbnail = as_uri
            print(f"Saved {as_uri} to DB ({rel_path})")
            ws.modified_date = datetime.datetime.now()
            ws.save()
            success = True

        else:
            log.swarn(f"DOWNLOAD ERROR: Logo: ({ws.name}): {image_link}")


    else:
        log.sinfo(f"LOGO: {ws.name}: Skipping download, because the website already has a logo.")


def populate_actors():
    actors = Actor.objects.order_by("name")  # name
    for actor in actors:
        photo = actor.thumbnail
        desc = actor.description
        url = 'https://metadataapi.net/api/performers'

        params = { 'q': actor.name }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'YAPO 0.7.6',
        }
        print(f"Contacting API for info about {actor.name}... ", end="")
        response = requests.request('GET', url, headers=headers, params=params)  # , params=params
        print("\n")
        try:
            response = response.json()
        except:
            pass

        pid = ""
        img = ""
        bio = ""
        desc = ""
        changed = False
        success = False
        photo = ""
        if all([response['data'], len(str(response['data'])) > 15]):
            # print("1")
            # try:
            if 'id' in response['data'][0].keys():
                pid = response['data'][0]['id']
                # print("id")
            if 'image' in response['data'][0].keys():
                img = response['data'][0]['image']
                # print("i")
            elif 'thumbnail' in response['data'][0].keys():
                img = response['data'][0]['thumbnail']
                # print("t")
            if 'bio' in response['data'][0].keys():
                desc = response['data'][0]['bio']

            if actor.thumbnail == Constants().unknown_person_image_path:
                # print(f"No image, downloading ({img}) - ", end="")
                save_path = os.path.join(Config().site_media_path, 'actor', str(actor.id), 'profile')
                # print("Profile pic path: " + save_path)
                save_file_name = os.path.join(save_path, 'profile.jpg')
                if img and not os.path.isfile(save_file_name):
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    if download_image(img, save_file_name):
                        rel_path = os.path.relpath(save_file_name, start="data")
                        as_uri = urllib.request.pathname2url(rel_path)
                        actor.thumbnail = as_uri
                        photo += " [ Photo ]"
                        success = True
                        changed = True
                    else:
                        log.swarn(f"DOWNLOAD ERROR: Photo ({actor.name}): {img}")

                    #save_actor_profile_image_from_web(img, actor, True)

            if any([not actor.description, len(actor.description) < 128,
                    "freeones" in actor.description.lower()]):
                # print("no good desc")
                if desc:
                    # print("chg desc")
                    if len(desc) > 72:
                        actor.description = strip_html(desc)
                        changed = True
                        success = True
                        photo += " [ Description ]"
            if pid:
                # print("id")
                if not actor.tpdb_id:
                    actor.tpdb_id = pid
                    photo += " [ TpDB ID ]"
                    changed = True
                    success = True

            if success:
                # print("yep, done")
                actor.last_lookup = datetime.datetime.now()
                actor.modified_date = datetime.datetime.now()
                actor.save()
                log.sinfo(f'Information about {actor.name} was successfully gathered from TpDB: {photo}.')

            else:

                save_path = os.path.join(Config().site_media_path, 'actor', str(actor.id), 'profile')
                save_file_name = os.path.join(save_path, 'profile.jpg')

                if (actor.tpdb_id == pid) and (len(actor.description) > 125 and (
                os.path.isfile(save_file_name))):
                    success = True
                    log.sinfo(
                        f'Your installation has good details about {actor.name}. You can force this operation.')

            #return success

        # except:
        # success = False
        # log.swarn(f'There was an error downloading a photo for and/or getting information about {actor.name}!')
        # return success

        else:
            log.swarn(f'It seems that TpDB might not know anything about {actor.name}!')
            logfile = open(os.path.join(Config().data_path, 'tpdb-missing-actors.log'), 'a+')
            logfile.write(f"{actor.name} - {str(actor.actor_aliases)}\n")
            logfile.close()
            success = False


def download_image(image_url, path):

    try:
        req = Request(image_url, headers={
            "User-Agent": "YAPO 0.7.6" })
        try:
            # timeout time to download an image
            timeout = 10
            response = urlopen(req, None, timeout)
            data = response.read()
            response.close()

            try:
                with open(path, 'wb') as output_file:
                    output_file.write(data)
            except OSError as e:
                download_status = 'fail'
                download_message = f"OSError on an image... Error: {e}"
                return_image_name = ''
                absolute_path = ''

            # return image name back to calling method to use it for thumbnail downloads
            log.sinfo(f'Image "{image_url}" downloaded to {path}')
            download_status = True



        except UnicodeEncodeError as e:
            download_status = 'fail'
            log.info(f"UnicodeEncodeError on an image...trying next one... Error: {e}")
            return_image_name = ''
            absolute_path = ''

        except URLError as e:
            download_status = 'fail'
            log.info(f"URLError on an image...trying next one... Error: {e}")
            return_image_name = ''
            absolute_path = ''

        except BadStatusLine as e:
            download_status = 'fail'
            log.info(f"BadStatusLine on an image...trying next one... Error: {e}")
            return_image_name = ''
            absolute_path = ''

        except HTTPError as e:  # If there is any HTTPError
            download_status = 'fail'
            log.info(f"HTTPError on an image...trying next one... Error: {e}")
            return_image_name = ''
            absolute_path = ''

        except ssl.CertificateError as e:
            download_status = 'fail'
            log.info(f"CertificateError on an image...trying next one... Error: {e}")
            return_image_name = ''
            absolute_path = ''

        except IOError as e:  # If there is any IOError
            download_status = 'fail'
            log.info(f"IOError on an image...trying next one... Error: {e}")
            return_image_name = ''
            absolute_path = ''

    except ssl.CertificateError as e:
        download_status = 'fail'
        log.info(f"CertificateError on an image...trying next one... Error: {e}")
        return_image_name = ''
        absolute_path = ''

    except IOError as e:  # If there is any IOError
        download_status = 'fail'
        log.info(f"IOError on an image...trying next one... Error: {e}")
        return_image_name = ''
        absolute_path = ''

    except IncompleteRead as e:
        download_status = 'fail'
        log.info(f"IncompleteReadError on an image...trying next one... Error: {e}")
        return_image_name = ''
        absolute_path = ''

    return download_status



def save_actor_profile_image_from_web (image_link, actor, force):
    save_path = os.path.join(
        Config().site_media_path, "actor", str(actor.id),"profile/"
    )

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_file_name = os.path.join(save_path, "profile.jpg")
    if not os.path.isfile(save_file_name) or force:

        if download_image(image_link, save_file_name):
            rel_path = os.path.relpath(save_file_name, start="data")
            as_uri = urllib.request.pathname2url(rel_path)
            actor.thumbnail = as_uri
        else:
            log.warn(f"Error downloading photo for {actor.name} ({image_link}).")

    else:
        log.sinfo(f"Skipping download, we already have a usable photo of {actor.name}.")



def actor_folder_from_name_to_id():
    actors = Actor.objects.all()

    for actor in actors:
        rel_path = os.path.relpath(
            os.path.join(
                Config().site_media_path,
                "actor",
                str(actor.id),
                "profile",
                "profile.jpg",
            ),
            start="videos",
        )

        as_uri = urllib.request.pathname2url(rel_path)

        print(
           f"Actor {actor.name} thumb path is: {actor.thumbnail} \n and it should be {as_uri}"
        )
        print(actor.thumbnail != as_uri)
        if actor.thumbnail not in [Config().unknown_person_image_path, as_uri]:
            try:
                os.rename(
                    os.path.join(Config().site_media_path, "actor", actor.name),
                    os.path.join(Config().site_media_path, "actor", str(actor.id)),
                )

                print(
                    "Renamed %s to %s"%(
                        os.path.join(Config().site_media_path, "actor", actor.name),
                        os.path.join(Config().site_media_path, "actor", str(actor.id)),
                    )
                )
            except FileNotFoundError:

                if os.path.isfile(
                        os.path.join(
                            Config().site_media_path,
                            "actor",
                            str(actor.id),
                            "profile",
                            "profile.jpg",
                        )
                ):

                    rel_path_changed = os.path.relpath(
                        os.path.join(
                            Config().site_media_path,
                            "actor",
                            str(actor.id),
                            "profile",
                            "profile.jpg",
                        ),
                        start="videos",
                    )
                    as_uri_changed = urllib.request.pathname2url(rel_path_changed)
                    actor.thumbnail = as_uri_changed
                    actor.save()
                    print(f"Changed {actor.name} thumb in database to {as_uri_changed}")
                else:
                    print("File %s not found!"%(
                            os.path.join(Config().site_media_path, "actor", actor.name)
                        )
                    )

            rel_path_changed = os.path.relpath(
                os.path.join(
                    Config().site_media_path,
                    "actor",
                    str(actor.id),
                    "profile",
                    "profile.jpg",
                ),
                start="videos",
            )
            as_uri_changed = urllib.request.pathname2url(rel_path_changed)
            actor.thumbnail = as_uri_changed
            actor.save()

            print(f"Changed {actor.name} thumb in database to {as_uri_changed}")

    return True


if __name__ == "__main__":
    print("this is main")
