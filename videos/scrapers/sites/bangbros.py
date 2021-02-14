import re

import requests
import requests.packages.urllib3
from bs4 import BeautifulSoup
from lxml import etree

from datetime import datetime
from utils.printing import Logger

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
log = Logger()


def getinfo (scene_id: int, search: str = ""):  # returns ID, site, title and rlsdate as a list

    if search == "":
        return False
    title = ""
    site = ""
    dt = ""

    search2 = match(search)

    if not re.search('^[a-zA-Z]+[0-9]+$', search2):
        # print(f'EXIT: ({search2}): Scene does not follow the Bangbros naming convention.')
        return False
    bangbros = get_sites(search2)
    if bangbros is not None:
        print(f"The scene is likely from the Bangbros site {bangbros}.")
        print(f'Expecting scene release ID name to be "{search2}", so searching bangbros.com for that...')
        x = scrape(search2)
        if not x:
            log.swarn(f'BANGBROS: No match for scene ID {scene_id}> BBID: {search2}')
            return False

    id = x[0]
    site = x[1]
    title = x[2]
    dt = x[3]

    if title is not None:
        # print(f'Found the scene:\nID   : {scene_id}\nRLSID: {id}\nSite : {site}\nTitle: {title}\nDate : {dt}')
        log.sinfo(f'BANGBROS: Match scene ID {scene_id}: (BBID: {id}) > {title} ({dt})')
        return id, site, title, dt
    else:
        return False


def scrape (scene: str = ""):
    title = None
    rlsdate = None
    site = None

    url = f"https://bangbros.com/search/{scene}"
    # print(url)
    response = requests.get(url, verify=False, timeout=10)
    response.raw.decode_content = True
    soup = BeautifulSoup(response.content, 'html.parser')

    if "Nothing matched" in str(soup):
        # print("No match on bangbros.com")
        return False

    dom = etree.HTML(str(soup))

    scrape = dom.xpath('//a[contains(@class, "thmb_lnk")]/@id')
    try:
        if scrape[0] and scene in scrape[0]:
            bbid = scene

    except:
        pass

    scrape = dom.xpath('//span[contains(@class, "faTxt")]/text()')
    try:
        if scrape[0]:
            site = scrape[0].strip()
        if scrape[1]:
            rlsdate = scrape[1].strip()

    except:
        pass
    if rlsdate:
        rlsdate = datetime.strptime(rlsdate, "%b %d, %Y").strftime("%Y-%m-%d")

    scrape = dom.xpath('//span[contains(@class, "thmb_ttl")]/text()')
    try:
        if scrape[0]:
            title = scrape[0]
    except:
        pass

    return scene, site, title, rlsdate


def match (match1: str = ""):
    match1 = match1.split(" ")[0].split(".")[0].split("-")[0]
    match1 = str(match1).replace("_2", "").replace("_", "").replace("-", "").replace(" ", "")
    endlist = ["3000k", "1500k", "800k", "500k", "3000", "1500", "800", "500", "4k"]
    for endstr in endlist:
        if match1.endswith(endstr) and len(match1) - len(endstr) > 4:
            match1 = match1[:len(match1) - len(endstr)]
            break
    return match1


def get_sites (search: str):
    sites = [("Bang Bus", "bb"), ("Ass Parade", "ap"), ("Monsters of Cock", "mc"), ("Big Tits, Round Asses", "btra"), \
             ("Big Mouthfuls", "bmf"), ("Tugjobs", "hj"), ("Big Tit Cream Pie", "btcp"), ("Brown Bunnies", "bkb"), \
             ("BangBros Remastered", "rm"), ("MILF Lessons", "ml"), ("Milf Soup", "ms"), ("Bangbros Clips", "bbc"), \
             ("BlowJob Fridays", "bj"), ("BangBros 18", "bbe"), ("Facial Fest", "ff"), ("Magical Feet", "fj"), \
             ("Ball Honeys", "es"), ("Mr. Anal", "ma"), ("Fuck Team Five", "bbw"), ("Back Room Facials", "brf"), \
             ("Bang POV", "bpov"), ("Pawg", "pwg"), ("My Dirty Maid", "mda"), ("Porn Star Spa", "pos"), \
             ("Party of 3", "ls"), ("Latina Rampage", "lrp"), ("Backroom MILF", "mf"), ("Can He Score?", "bd"), \
             ("MomIsHorny", "mih"), ("Public Bang", "pb"), ("Colombia Fuck Fest", "cff"), ("Newbie Black", "blkg"), \
             ("Bang Casting", "hih"), ("Glory Hole Loads", "ghl"), ("Blowjob Ninjas", "aa"), ("Street Ranger", "sg"), \
             ("Chongas", "ch"), ("Stepmom Videos", "smv"), ("Mr CamelToe", "ct"), ("Power Munch", "pm"), \
             ("Boob Squad", "bs"), ("Dorm Invasion", "di"), ("Dirty World Tour", "bf"), ("Living With Anna", "lr"), \
             ("My Life In Brazil", "mb"), ("Working Latinas", "lw"), ("Casting", "ca"), ("BangBros Angels", "bng"), \
             ("Penny Show", "ps"), ("Bangbros Vault", "bv"), ("Bang Tryouts", "bto"), ("Slutty White Girls", "swg"), \
             ("AvaSpice", "av")]

    for site in sites:
        if site[1] in search:
            return site[0]
    return None
