import http.client
import sys
import urllib.request

from videos.models import *

import datetime
import socket
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
    cpuinfo = psutil.cpu_freq()
    # On some systems, 'max' will be 0.0. In this case, use the current speed.
    if cpuinfo.max == 0.0:
        cpufreqMhz = cpuinfo.current
    else:
        cpufreqMhz = cpuinfo.max

    cpufreqGhz = round(cpufreqMhz / 1000, 1)
    return cpufreqGhz


def getCPUCount():
    import psutil
    return psutil.cpu_count(logical=False)  # set Logical to true if treads are to be included







def strip_html (s):
    return str(html.fromstring(s).text_content())


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
                log.info(f"A scene was added to {ws.name}: {scene.name}")
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

    web = webAccess()
    if not web.download_image(image_link, save_file_name):
        log.error(f"DOWNLOAD ERROR: Logo: ({ws.name}): {image_link}")
        return

    ws = Website.objects.get(name=website)
    log.info("OK")
    as_uri = webAccess.pathname2url(save_file_name)
    ws.thumbnail = as_uri
    log.info(f"Saved {as_uri} to DB ({save_file_name})")
    ws.modified_date = datetime.datetime.now()
    ws.save()



def actor_folder_from_name_to_id ():
    actors = Actor.objects.all()

    for actor in actors:
        abs_path = actor.generateThumbnailPath()
        as_uri = actor.getThumbnailPathURL()
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

def heightcmToTagString(height):
    if height < 148:
        return "Extremely tiny"
    if height < 152:
        return "Tiny"
    if height < 161:
        return "Petite"
    if height < 178:
        return "Average"
    if height < 186:
        return "Tall"
    if height < 220:
        return "Extremely tall"

    raise Exception(f"Failed to parse height string {height}")
