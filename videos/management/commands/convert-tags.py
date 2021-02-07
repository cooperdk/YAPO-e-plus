from django.core.management.base import BaseCommand
from django.utils import timezone
import os
from os import path
import sys
import shutil
import requests
import platform
import videos.aux_functions as aux
from configuration import Config
from utils import Constants
from utils.printing import Logger
from videos.models import Scene, Actor, ActorTag, SceneTag
log = Logger()

class Command(BaseCommand):
    help = 'Get all TpDB tracking tags from scenes and convert them to database fields (time consuming)'


    def handle(self, *args, **kwargs):
        log.sinfo(f'Converting old TpDB tags to database fields...')
        scenes = Scene.objects.order_by("id")
        row = Scene.objects.raw(
            "SELECT COUNT(*) AS total, id FROM videos_scene"
        )  # cursor.fetchone()
        if row[0].total is not None:
            scenetotal = str(row[0].total)
        print("")
        number = 0
        for scene in scenes:
            changed = False
            print(f"\rScanning and converting tags to database fields - scene {number} of {scenetotal}... ", end="")

            for scene_tag in scene.scene_tags.all():
                try:
                    scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Scanned"))
                except:
                    pass

                if scene_tag.name == "TpDB: Match: None":
                    scene.tpdb_scanned = True
                    scene.tpdb_scanned_match = False
                    scene.tpdb_scanned_unsure = False
                    changed = True
                    try:
                        scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Match: None"))
                        print(f'S ', end="")
                    except:
                        pass

                if scene_tag.name == "TpDB: Match: Questionable":
                    scene.tpdb_scanned = True
                    scene.tpdb_scanned_match = True
                    scene.tpdb_scanned_unsure = True
                    changed = True
                    try:
                        scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Match: Questionable"))
                        print(f'M ', end="")
                    except:
                        pass

                if scene_tag.name == "TpDB: Match: Good":
                    scene.tpdb_scanned = True
                    scene.tpdb_scanned_match = True
                    scene.tpdb_scanned_unsure = False
                    changed = True
                    try:
                        scene.scene_tags.remove(SceneTag.objects.get(name="TpDB: Match: Good"))
                        print(f'U ', end="")
                    except:
                        pass

            if changed:
                scene.save()
                print(f'(SAVE) ', end="")
            number += 1
        print("\nDone.")
