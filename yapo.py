#!/usr/bin/env python

from utils import dbcheck
dbcheck.boot()

from waitress import serve
from configuration import Config
from YAPO.wsgi import application

#import migrater
from videos import startup
if __name__ == '__main__':

    startup.startup_sequence()
    print(f'YAPO configured URL: "{Config().yapo_url}"')
    if Config().yapo_url and (Config().yapo_url != "no" or Config().yapo_url) != "":
        serve(application, listen=Config().yapo_url)
    else:
        print("Fallback: No configured host or port. Using fallback URL (localhost:8000)")
        serve(application, listen='localhost:8000')
