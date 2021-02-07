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
    help = 'Scan the database for scenes with a TpDB ID and mark them as scanned'


    def handle(self, *args, **kwargs):

        from utils import titleparser as tp
        print(f'Updating successfully scanned TpDB scenes...')
        scenes = Scene.objects.order_by("id")
        row = Scene.objects.raw(
            "SELECT COUNT(*) AS total, id FROM videos_scene"
        )  # cursor.fetchone()
        if row[0].total is not None:
            scenetotal = str(row[0].total)
        print("")
        number = 0

        for scene in scenes:
            print(f"\rMarking scenes found by TpDB - scene {number} of {scenetotal}...", end="")
            if not scene.tpdb_scanned and scene.tpdb_id:
                scene.tpdb_scanned = True
                scene.save(force_update=True)
            number += 1
        print("\nDone.")
