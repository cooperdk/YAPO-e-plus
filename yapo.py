#!/usr/bin/env python

from utils import dbcheck
dbcheck.boot()

from waitress import serve
from configuration import Config
from YAPO.wsgi import application

#import migrater
from videos import startup
a = 0
if __name__ == '__main__' and a == 0:
    startup.startup_sequence()
    config = Config().yapo_url
    print(f'YAPO configured URL: "{config}"')
    if config == None:
        print("Using default host/port until one is properly configured.")
        config == "127.0.0.1:8000"
    a += 1
    serve(application, listen=str(Config().yapo_url), threads=10, ident="YAPO", log_socket_errors=False)
