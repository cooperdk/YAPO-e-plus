import http.client
import sys
import time
import urllib.request
from urllib.request import Request, urlopen

from videos.models import *

http.client._MAXHEADERS = 1000
from http.client import IncompleteRead, BadStatusLine
import ssl
import datetime
import re
http.client._MAXHEADERS = 1000
import socket
import requests
from lxml import html

import logging
log = logging.getLogger(__name__)

def progress (count: int, total: int, suffix=''):
    bar_len = 42
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    #bar = '█' * filled_len + '░' * (bar_len - filled_len)
    sys.stdout.write(f"\r{bar} [{percents}%] - {suffix}                    \r")

def progress_end():
    sys.stdout.flush()

def getMemory():
    import psutil
    vmem = round(psutil.virtual_memory().total / 1000000000, 0)
    return vmem  # "{:.2}".format(vmem.total/100000000) #shold that be 102400000?


def getCPU():
    import psutil
    cpufreq = round(psutil.cpu_freq().max / 1000, 1)
    return cpufreq


def getCPUCount():
    import psutil
    return psutil.cpu_count(logical=False)  # set Logical to true if treads are to be included


def send_piercings_to_actortag (actor):
    piercings = actor.piercings
    if piercings:
        if ("navel" or "belly button" or "bellybutton") in piercings.lower():
            insert_actor_tag(actor, "Pierced navel")
        if "clit" in piercings.lower():
            insert_actor_tag(actor, "Pierced clitoris")
        if ("nipples" or "nipple rings") in piercings.lower():
            insert_actor_tag(actor, "Pierced nipples")
        elif "nipple" in piercings.lower():
            insert_actor_tag(actor, "Pierced single nipple")
        if "septum" in piercings.lower():
            insert_actor_tag(actor, "Pierced septum")
        if "nose" in piercings.lower():
            insert_actor_tag(actor, "Pierced nose")
        if "nostril" in piercings.lower():
            insert_actor_tag(actor, "Pierced nostril")
        if "tongue" in piercings.lower():
            insert_actor_tag(actor, "Pierced tongue")
        if "tragus" in piercings.lower():
            insert_actor_tag(actor, "Pierced tragus")
        if "helix" in piercings.lower():
            insert_actor_tag(actor, "Pierced helix")
        if ("earlobe" or "ear lobe") in piercings.lower():
            insert_actor_tag(actor, "Pierced ear lobe")
        if "lower lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced lower lip")
        if "upper lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced upper lip")
        if "monroe" in piercings.lower():
            insert_actor_tag(actor, "Pierced Monroe")
        if ("dermal" or "surface") in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal")
        if "wrists" in piercings.lower():
            insert_actor_tag(actor, "Pierced wrists")
        elif "wrist" in piercings.lower():
            insert_actor_tag(actor, "Pierced single wrist")
        if "hip" in piercings.lower():
            insert_actor_tag(actor, "Pierced hip")
        elif "hips" in piercings.lower():
            insert_actor_tag(actor, "Pierced hips")
        if "labia" in piercings.lower():
            insert_actor_tag(actor, "Pierced labia")
        if "back dimples" in piercings.lower():
            insert_actor_tag(actor, "Pierced back dimples")
        if ("right brow" or "right eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced right eyebrow")
        elif ("left brow" or "left eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced left eyebrow")
        elif "brow" in piercings.lower():
            insert_actor_tag(actor, "Pierced eyebrow")
        if "ears" in piercings.lower():
            insert_actor_tag(actor, "Pierced ears")
        elif "left ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced left ear")
        elif "right ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced right ear")
        if "chest" in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal on chest")
        if any([piercings.lower() == "none", piercings.lower() == "no piercings", piercings.lower() == "no"]):
            insert_actor_tag(actor, "No piercings")

def addactor (current_scene, actor_to_add):
    if not current_scene.actors.filter(name=actor_to_add):
        current_scene.actors.add(actor_to_add)
        log.info(f"Added Actor '{actor_to_add.name}' to scene '{current_scene.name}'")

    if actor_to_add.actor_tags.count() > 0:
        for actor_tag in actor_to_add.actor_tags.all():
            if not current_scene.scene_tags.filter(name=actor_tag.name):
                current_scene.scene_tags.add(
                    actor_tag.scene_tags.first()
                )
                log.info(f"Added Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{current_scene.name}'")

    current_scene.save()


def insert_actor_tag (actor_to_insert, actor_tag_name):
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
        '1500', '1000'
    )

    name = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', '', name)
    name = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', '', name)
    name = re.sub(r'\d{1,2}\.{0,1}\s{0,1}(January|February|March|April|May|June|July|August|September|October|November|December)\s{0,1}.\d{4}', '', name)
    name = re.sub(r'(\d+)[/.-](\d+)[/.-](\d+)', '', name)
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
    name = remove_text_inside_brackets(name)
    name = re.sub(' +', ' ', name)

    return name

def strip_html (s):
    return str(html.fromstring(s).text_content())

def strip_bad_chars (name):
    bad_chars = { " " }
    for char in bad_chars:
        if char in name:
            name = name.replace(char, "")
    return name

def onlyChars(toClean):
    valids = "".join(char for char in toClean if char.isalpha())
    return valids

def get_with_retry(url, headers, params):
    deadline = datetime.datetime.now() + datetime.timedelta(minutes=4)

    while True:
        try:
            response = requests.request('GET', url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except Exception as e:
            if datetime.datetime.now() > deadline:
                log.exception(f"Exception retrieving {url}: {e} ")

            log.warning(f"Exception retrieving {url}: {e}; will retry.")
            time.sleep(3)

def is_domain_reachable(host):
    """ This function checks to see if a host name has a DNS entry by checking
        for socket info. If the website gets something in return,
        we know it's available to DNS.
    """
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        result = False
    else:
        result =  True
    return result

def save_website_logo (image_link, website, force, *args):
    website = website.strip()

    ws = None
    try:
        hasarg = 0
        log.info("Website scan, method 1...")
        ws = Website.objects.filter(name=website)

        if ws:
            ws = Website.objects.get(name=website)
            website = ws.name
        if not ws:
            ws = Website.objects.filter(name__iexact=website.replace(" ",""))
            if ws:
                ws = Website.objects.get(name__iexact=website.replace(" ",""))
                website = ws.name
        if not ws and Config().tpdb_websites:
            log.info(f"Adding website: {website}")
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
            log.info(f"No logo URL available for {website}.")
            return
    else:
        log.info(f"No logo URL available for {website}.")
        return

    if not Config().tpdb_website_logos:
        return
    if not ws and not Config().tpdb_websites:
        log.warning(f'LOGO: No website "{website}", and we cannot add it because you didn\'t allow it!')
        return

    ws = Website.objects.get(name=website)
    save_path = scene.get_media_path()
    if os.path.splitext(image_link)[1]:
        ext = os.path.splitext(image_link)[1]
    else:
        log.error("Logo filename has no extension")
        return

    save_file_name = os.path.join(save_path, "logo" + ext)
    if os.path.isfile(save_file_name) and not force:
        log.info(f"LOGO: {ws.name}: Skipping download, because the website already has a logo.")
        return

    os.makedirs(save_file_name)

    if not download_image(image_link, save_file_name):
        log.error(f"DOWNLOAD ERROR: Logo: ({ws.name}): {image_link}")
        return

    ws = Website.objects.get(name=website)
    log.info("OK")
    as_uri = pathname2url(save_file_name)
    ws.thumbnail = as_uri
    log.info(f"Saved {as_uri} to DB ({save_file_name})")
    ws.modified_date = datetime.datetime.now()
    ws.save()


def download_image (image_url, path):

    try:
        req = Request(image_url, headers={
            "User-Agent": "YAPO e+ 0.71"
        })
        with urlopen(req, None, 10) as response:
            response.raise_for_status()
            data = response.read()

        with open(path, 'wb') as output_file:
            output_file.write(data)

        log.info(f'Image "{image_url}" downloaded to {path}')
        return True

    except Exception as e:
        log.warning(f"Failed to download {image_url}: {e}")
        return False

def save_actor_profile_image_from_web (image_link, actor, force):
    save_path = os.path.join(
        Config().site_media_path, "actor", str(actor.id),"profile/"
    )

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_file_name = os.path.join(save_path, "profile.jpg")
    if not force and os.path.isfile(save_file_name):
        log.sinfo(f"Skipping download, we already have a usable photo of {actor.name}.")
        return

    if not download_image(image_link, save_file_name):
        log.warn(f"Error downloading photo for {actor.name} ({image_link}).")
        return

    rel_path = os.path.relpath(save_file_name, start="videos")
    as_uri = pathname2url(save_file_name)
    actor.thumbnail = as_uri

def actor_folder_from_name_to_id ():
    actors = Actor.objects.all()

    for actor in actors:
        abs_path = actor.generateThumbnailPath()
        as_uri = pathname2url(abs_path)
        log.info(f"Actor {actor.name} thumb path is: {actor.thumbnail}, but it should be {as_uri}")

        if (actor.thumbnail != Config().unknown_person_image_path) and (
                actor.thumbnail != as_uri
        ):
            try:
                os.rename(
                    os.path.join(Config().site_media_path, "actor", actor.name),
                    os.path.join(Config().site_media_path, "actor", str(actor.id)),
                )

                log.info(
                    "Renamed %s to %s"%(
                        os.path.join(Config().site_media_path, "actor", actor.name),
                        os.path.join(Config().site_media_path, "actor", str(actor.id)),
                    )
                )
            except FileNotFoundError:
                if os.path.isfile(abs_path):
                    rel_path_changed = os.path.relpath(abs_path, start="videos")
                    as_uri_changed = urllib.request.pathname2url(rel_path_changed)
                    actor.thumbnail = as_uri_changed
                    actor.save()
                    log.info(f"Changed {actor.name} thumb in database to {as_uri_changed}")
                else:
                    log.warning("File %s not found!"%(os.path.join(Config().site_media_path, "actor", actor.name)))

            rel_path_changed = os.path.relpath(abs_path, start="videos")
            as_uri_changed = urllib.request.pathname2url(rel_path_changed)
            actor.thumbnail = as_uri_changed
            actor.save()
            log.info(f"Changed {actor.name} thumb in database to {as_uri_changed}")

    return True

def pathname2url(path):
    # Chop off the leading site media path
    if path.find(Config().site_media_path) is not 0:
        raise Exception(f"File {path} is not under the media path {Config().site_media_path}")
    path = path[len(Config().site_media_path):]

    # And turn into a URL.
    as_uri = urllib.request.pathname2url(path).strip('/')

    # It'll be under the media directory.
    mediaUrl = Config().site_media_url.strip('/')
    as_uri = "%s/%s" % (mediaUrl, as_uri)

    return as_uri

# Convert a filename mapping as returned from pathname2url back to a path name.
def urlpath2pathname(url):
    mediaUrl = Config().site_media_url.strip("/\\")
    if url.find(mediaUrl) is not 0:
        raise Exception(f"url {url} is not under the media path {mediaUrl}")
    url = url[len(mediaUrl):]
    url = url.strip('/\\')

    url = os.path.join(Config().site_media_path, url)
    return url

def heightcmToTagString(height):
    if height < 148:
        return "Extremely tiny"
    if 148 < height < 152:
        return "Tiny"
    if 152 < height < 161:
        return "Petite"
    if 178 < height < 186:
        return "Tall"
    if 186 < height < 220:
        return "Extremely tall"
