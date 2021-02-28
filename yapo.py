#!/usr/bin/env python

import sys
import os
import shutil
from configuration import Config, Constants
from utils import dbcheck
from utils.printing import Logger
log = Logger()

#if os.path.exists(os.path.join(self.root_path,))
sitemediaold = os.path.join(Config().site_path, Constants().site_media_subdir)
if os.path.exists(sitemediaold): #)(Config().site_media_path):
    log.sinfo(f"Media dir is currently {sitemediaold} (old configuration)")
    newmedia = os.path.join(Config().root_path,Config().data_path,Constants().site_media_subdir)
    newmedianosub = os.path.join(Config().root_path,Config().data_path)
    if not os.path.exists(newmedia):
        log.info(f'Media moves to {newmedia}...')
        print(f"Source: {sitemediaold}")
        print(f"Destination: {newmedianosub}")
        try:
            shutil.move(sitemediaold, newmedianosub)
        except OSError as exp:
            log.error(f"Error when moving media: {exp}")
            print("Please move the media directory (within /videos) yourself to the /data directory,"
                  "then restart YAPO.")
            Config().site_media_path = newmedia
            Config().save()
            sys.exit(0)
        Config().site_media_path = newmedia
        Config().save()
        print(f"Configuration saved...")
    else:
        log.error('New media location {newmedia} already exists! Move the files manually.')

if not os.path.exists(Config().config_path):
    os.makedirs(Config().config_path)

if not os.path.isfile(Config().configfile_path):
    Config().save()

if not os.path.exists(Config().temp_path):
    os.makedirs(Config().temp_path)

if not os.path.exists(os.path.join(Config().site_media_path,"logos")):
    os.makedirs(os.path.join(Config().site_media_path,"logos"))

if not os.path.exists(os.path.join(Config().site_media_path,"scenes")):
    os.makedirs(os.path.join(Config().site_media_path,"scenes"))

if not os.path.exists(os.path.join(Config().site_media_path,"tags")):
    os.makedirs(os.path.join(Config().site_media_path,"tags"))

if not os.path.exists(os.path.join(Config().site_media_path,"websites")):
    os.makedirs(os.path.join(Config().site_media_path,"websites"))

if not os.path.exists(Config().database_dir):
    os.makedirs(Config().database_dir)

dbcheck.boot()

from waitress import serve
from YAPO.wsgi import application

#import migrater
from videos import startup
a = 0
if __name__ == '__main__' and a == 0:
    startup.startup_sequence()
    config = Config().yapo_url
    print(f'YAPO configured URL: "{config}"')
    if config is None:
        print("Using default host/port until one is properly configured.")
        config = "127.0.0.1:8000"
    a += 1
    serve(application, listen=str(Config().yapo_url), threads=10, ident="YAPO", log_socket_errors=False)
