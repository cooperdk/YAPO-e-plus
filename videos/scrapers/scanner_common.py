import datetime
import os
import time

import requests
from videos.models import SceneTag, ActorTag, Actor
import logging

from videos.scrapers.webAccess import webAccess

log = logging.getLogger(__name__)

class scanner_common:
    web: webAccess

    def __init__(self):
        self.web = webAccess()

    @staticmethod
    def createForSite(siteName : str):
        siteName = siteName.lower()
        if siteName == "tmdb":
            from videos.scrapers.tmdb import scanner_tmdb
            return scanner_tmdb()
        elif siteName == "tpdb":
            from videos.scrapers.scanner_tpdb import scanner_tpdb
            return scanner_tpdb()
        elif siteName == "freeones":
            from videos.scrapers.freeones import scanner_freeones
            return scanner_freeones()
        elif siteName == "imdb":
            from videos.scrapers.imdb import scanner_imdb
            return scanner_imdb()
        else:
            return None

    def save_actor_profile_image_from_web(self, image_link : str, actor : Actor, force : bool):
        if not force and actor.has_thumbnail_image():
            log.info(f"Skipping download, we already have a usable photo of {actor.name}.")
            return
        if not webAccess.download_image(image_link, actor.generateThumbnailPath()):
            log.warning(f"Error downloading photo for {actor.name} ({image_link}).")
            return

        actor.thumbnail = actor.getThumbnailPathURL()

    def strip_bad_chars(self, name):
        bad_chars = {" "}
        for char in bad_chars:
            if char in name:
                name = name.replace(char, "")
        return name

    def onlyChars(self, toClean):
        valids = "".join(char for char in toClean if char.isalpha())
        return valids

    def remove_text_inside_brackets(self, text, brackets="()[]"):
        count = [0] * (len(brackets) // 2)  # count open/close brackets
        saved_chars = []
        for character in text:
            for i, b in enumerate(brackets):
                if character == b:  # found bracket
                    kind, is_close = divmod(i, 2)
                    count[kind] += (-1) ** is_close  # `+1`: open, `-1`: close
                    if count[kind] < 0:  # unbalanced bracket
                        count[kind] = 0  # keep it
                    else:  # found bracket to remove
                        break
            else:  # character is not a [balanced] bracket
                if not any(count):  # outside brackets
                    saved_chars.append(character)
        return ''.join(saved_chars)

    def addactor(self, current_scene, actor_to_add):
        if not current_scene.actors.filter(name=actor_to_add):
            current_scene.actors.add(actor_to_add)
            log.info(f"Added Actor '{actor_to_add.name}' to scene '{current_scene.name}'")
        else:
            log.info(f"Actor {actor_to_add.name} already in scene.")

        if actor_to_add.actor_tags.count() > 0:
            for actor_tag in actor_to_add.actor_tags.all():
                if not current_scene.scene_tags.filter(name=actor_tag.name):
                    current_scene.scene_tags.add(
                        actor_tag.scene_tags.first()
                    )
                    log.info(f"Added Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{current_scene.name}'")

        current_scene.save()

    def insert_aliases_from_CSV(self, actor_to_insert: Actor, aliases : str):
        for alias in aliases.split(','):
            actor_to_insert.createOrAddAlias(alias.strip())

    def insert_scene_tag(self, current_scene, tagname):
        if not SceneTag.objects.filter(name=tagname):
            SceneTag.objects.create(name=tagname)

        scene_tag_to_add = SceneTag.objects.get(name=tagname)
        current_scene.scene_tags.add(scene_tag_to_add)

    def insert_actor_tag(self, actor_to_insert, actor_tag_name):
        actor_tag_name = self.strip_bad_chars(actor_tag_name)

        if not ActorTag.objects.filter(name=actor_tag_name):
            actor_tag = ActorTag()
            actor_tag.name = actor_tag_name

            actor_tag.save()
            actor_to_insert.actor_tags.add(actor_tag)
        else:
            actor_tag = ActorTag.objects.get(name=actor_tag_name)
            actor_to_insert.actor_tags.add(actor_tag)
            actor_tag.save()

    def send_piercings_to_actortag(self, actor):
        for tagName in self.parsePiercingsToTags(actor.piercings):
            self.insert_actor_tag(actor, tagName)

    def parsePiercingsToTags(self, toParse : str):
        piercingNames = {
            'Pierced navel' : [ "navel", "belly button", "bellybutton" ],
            "Pierced clitoris" : ["clit", "clitoris" ],
            "Pierced nipples" : ["nipples", "nipple rings" ],
            "Pierced single nipple": ["nipple", "nipple ring" ],
            "Pierced septum": [ "septum" ] ,
            "Pierced nose": [ "nose" ] ,
            "Pierced nostril": [ "nostril" ],
            "Pierced tongue": [ "tongue" ] ,
            "Pierced tragus":[ "tragus" ] ,
            "Pierced helix":[ "helix" ] ,
            "Pierced ear lobe": ["earlobe", "ear lobe"],
            "Pierced lower lip": [ "lower lip" ],
            "Pierced upper lip": [ "upper lip" ],
            "Pierced Monroe": [ "monroe" ],
            "Pierced dermal":["dermal", "surface"],
            "Pierced wrists": [ "wrists" ] ,
            "Pierced single wrist": [ "wrist" ],
            "Pierced hip": [ "hip" ] ,
            "Pierced hips": [ "hips" ],
            "Pierced labia": [ "labia" ],
            "Pierced back dimples": [ "back dimples" ],
            "Pierced right eyebrow": ["right brow", "right eyebrow"],
            "Pierced left eyebrow": ["left brow", "left eyebrow"] ,
            "Pierced eyebrow": [ "brow" ] ,
            "Pierced ears": [ "ears" ] ,
            "Pierced left ear": [ "left ear" ],
            "Pierced right ear": [ "right ear" ],
            "Pierced dermal on chest": [ "chest" ],
            "No piercings": ["none", "no", "no piercings"]
        }

        toRet = []
        for piercingName in toParse.lower().split(" "):
            toRet.extend(x for x in piercingNames.keys() if piercingNames[x] == piercingName )
        return toRet

    def addCupSize(self, actor: Actor, sizeString: str):
        cupSize = self.onlyChars(sizeString)
        if len(cupSize) == 0:
            return

        self.insert_actor_tag(actor, cupSize + " Cup")

        accepted_strings = {
            'Tiny tits' : {'A'},
            'Small tits' : {'B'},
            'Medium tits' : {'C'},
            'Big tits': {'D', 'E', 'F'},
            'Very big tits': {'G', 'H', 'I'},
            'Huge tits': {'J', 'K', 'L', 'M'},
            'Massively huge tits': {'N', 'O', 'P', 'Q', 'R', 'S'},
            'Extremely huge tits': {'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
        }

        for tagName in accepted_strings.keys():
            if cupSize in accepted_strings[tagName]:
                self.insert_actor_tag(actor, tagName)
                break

    def namecheck(self, actor: str):

        newActor = actor.strip()

        if newActor == "Abby Lee":
            newActor = "Abby Lee Brazil"
        if newActor == "Abby Rains":
            newActor = "Abbey Rain"
        if newActor == "Ms Addie Juniper":
            newActor = "Addie Juniper"
        if newActor == "Adrianna Chechik" or newActor == "Adriana Chechick":
            newActor = "Adriana Chechik"
        if newActor == "Alex D":
            newActor = "Alex D."
        if newActor == "Alura Tnt Jenson" or newActor == "Alura 'Tnt' Jenson":
            newActor = "Alura Jenson"
        if newActor == "Amia Moretti":
            newActor = "Amia Miley"
        if newActor == "Amy Reid":
            newActor = "Amy Ried"
        if newActor == "Ana Fox" or newActor == "Ana Foxx":
            newActor = "Ana Foxxx"
        if newActor == "Andreina De Lux" or newActor == "Andreina De Luxe" or newActor == "Andreina Dlux":
            newActor = "Andreina Deluxe"
        if newActor == "Angela Piaf" or newActor == "Angel Piaf":
            newActor = "Angel Piaff"
        if newActor == "Ani Black Fox" or newActor == "Ani Black":
            newActor = "Ani Blackfox"
        if newActor == "Anikka Albrite":
            newActor = "Annika Albrite"
        if newActor == "Anita Bellini":
            newActor = "Anita Bellini Berlusconi"
        if newActor == "Anjelica" or newActor == "Ebbi" or newActor == "Abby H" or newActor == "Katherine A":
            newActor = "Krystal Boyd"
        if newActor == "Anna Morna":
            newActor = "Anastasia Morna"
        if newActor == "April ONeil" or newActor == "April Oneil" or newActor == "April O'neil":
            newActor = "April O'Neil"
        if newActor == "Ashley Graham":
            newActor = "Ashlee Graham"
        if newActor == "Bella Danger":
            newActor = "Abella Danger"
        if newActor == "Bibi Jones" or newActor == "Bibi Jones™":
            newActor = "Britney Beth"
        if newActor == "Bridgette B.":
            newActor = "Bridgette B"
        if newActor == "Capri Cavalli":
            newActor = "Capri Cavanni"
        if newActor == "Ce Ce Capella":
            newActor = "CeCe Capella"
        if newActor == "Charli Red":
            newActor = "Charlie Red"
        if newActor == "Charlotte Lee":
            newActor = "Jaye Summers"
        if newActor == "Chloe Cherry":
            newActor = "Chloe Couture"
        if newActor == "Criss Strokes":
            newActor = "Chris Strokes"
        if newActor == "Christy Charming":
            newActor = "Paula Shy"
        if newActor == "CléA Gaultier":
            newActor = "Clea Gaultier"
        if newActor == "Crissy Kay" or newActor == "Emma Hicks" or newActor == "Emma Hixx":
            newActor = "Emma Hix"
        if newActor == "Crystal Rae":
            newActor = "Cyrstal Rae"
        if newActor == "Doris Ivy":
            newActor = "Gina Gerson"
        if newActor == "Eden Sin":
            newActor = "Eden Sinclair"
        if newActor == "Elsa Dream":
            newActor = "Elsa Jean"
        if newActor == "Eve Lawrence":
            newActor = "Eve Laurence"
        if newActor == "Francesca Di Caprio" or newActor == "Francesca Dicaprio":
            newActor = "Francesca DiCaprio"
        if newActor == "Guiliana Alexis":
            newActor = "Gulliana Alexis"
        if newActor == "Grace Hartley":
            newActor = "Pinky June"
        if newActor == "Hailey Reed":
            newActor = "Haley Reed"
        if newActor == "Josephina Jackson":
            newActor = "Josephine Jackson"
        if newActor == "Jane Doux":
            newActor = "Pristine Edge"
        if newActor == "Jade Indica":
            newActor = "Miss Jade Indica"
        if newActor == "Jassie Gold" or newActor == "Jaggie Gold":
            newActor = "Jessi Gold"
        if newActor == "Jenna J Ross" or newActor == "Jenna J. Ross":
            newActor = "Jenna Ross"
        if newActor == "Jenny Ferri":
            newActor = "Jenny Fer"
        if newActor == "Jessica Blue" or newActor == "Jessica Cute":
            newActor = "Jessica Foxx"
        if newActor == "Jo Jo Kiss":
            newActor = "Jojo Kiss"
        if newActor == "Josephine" or newActor == "Conny" or newActor == "Conny Carter" or newActor == "Connie":
            newActor = "Connie Carter"
        if newActor == "Kagney Lynn Karter":
            newActor = "Kagney Linn Karter"
        if newActor == "Kari Sweets":
            newActor = "Kari Sweet"
        if newActor == "Katarina":
            newActor = "Katerina Hartlova"
        if newActor == "Kendra May Lust":
            newActor = "Kendra Lust"
        if newActor == "Khloe Capri" or newActor == "Chloe Capri":
            newActor = "Khloe Kapri"
        if newActor == "Lara Craft":
            newActor = "Lora Craft"
        if newActor == "Lilly LaBeau" or newActor == "Lilly Labuea" or newActor == "Lily La Beau" or \
                newActor == "Lily Lebeau" or newActor == "Lily Luvs":
            newActor = "Lily Labeau"
        if newActor == "Lilly Lit":
            newActor = "Lilly Ford"
        if newActor == "Maddy OReilly" or newActor == "Maddy Oreilly" or newActor == "Maddy O'reilly":
            newActor = "Maddy O'Reilly"
        if newActor == "Maria Rya" or newActor == "Melena Maria":
            newActor = "Melena Maria Rya"
        if newActor == "Moe The Monster Johnson":
            newActor = "Moe Johnson"
        if newActor == "Nadya Nabakova" or newActor == "Nadya Nabokova":
            newActor = "Bunny Colby"
        if newActor == "Nancy A." or newActor == "Nancy A":
            newActor = "Nancy Ace"
        if newActor == "Nathaly" or newActor == "Nathalie Cherie" or newActor == "Natalie Cherie" or newActor == "Nathaly Cherie":
            newActor = "Nathaly Heaven"
        if newActor == "Nika Noir":
            newActor = "Nika Noire"
        if newActor == "Noe Milk" or newActor == "Noemiek":
            newActor = "Noemilk"
        if newActor == "Rebel Lynn (Contract Star)":
            newActor = "Rebel Lynn"
        if newActor == "Remy La Croix":
            newActor = "Remy Lacroix"
        if newActor == "Riley Jenson" or newActor == "Riley Anne" or newActor == "Rilee Jensen":
            newActor = "Riley Jensen"
        if newActor == "Sara Luv":
            newActor = "Sara Luvv"
        if newActor == "Dylann Vox" or newActor == "Dylan Vox":
            newActor = "Skylar Vox"
        if newActor == "Sedona" or newActor == "Stefanie Renee":
            newActor = "Stephanie Renee"
        if newActor == "Stella Bankxxx" or newActor == "Stella Ferrari":
            newActor = "Stella Banxxx"
        if newActor == "Steven St.Croix":
            newActor = "Steven St. Croix"
        if newActor == "Sybil Kailena" or newActor == "Sybil":
            newActor = "Sybil A"
        if newActor == "Tiny Teen" or newActor == "Tieny Mieny" or newActor == "Lady Jay" \
                or newActor == "Tiny Teen / Eva Elfie":
            newActor = "Eva Elfie"
        if newActor == "Veronica Vega":
            newActor = "Veronica Valentine"

        return newActor
