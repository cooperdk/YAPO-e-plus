from datetime import datetime
from configuration import Config
from utils import Singleton
import re
import os
from os import path
class Logger(metaclass=Singleton):

    def warn(self, message: str):
      timeprint(f"[\033[31mWARN!\033[39m] {message}")
      logsave(f"[WARN!] {message}")

    def swarn(self, message: str):
      timeprint(f"[\033[31mWARN!\033[39m] {message}")

    def debug(self, message: str):
      if Config().debug == 'true':
        timeprint(f"[\033[34mDEBUG\033[39m] {message}")
        dbgsave(f"[DEBUG] {message}")

    def info(self, message: str):
      timeprint(f"[\033[33mINFO\033[39m ] {message}")
      logsave(f"[INFO ] {message}")

    def sinfo(self, message: str):
      timeprint(f"[\033[33mINFO\033[39m ] {message}")

    def error(self, message: str):
      timeprint(f"\033[31m[ERROR]\033[39m {message}")
      logsave(f"[ERROR] {message}")


def timeprint(message: str):
    print(f"{datetime.now().strftime('%H:%M:%S')} {message}")

def logsave(message: str):
    logfile = open(os.path.join(Config().data_path,'yapo-eplus_' + datetime.now().strftime("%Y-%m-%d") +'.log'), 'a+')
    logfile.write(f"{datetime.now().strftime(Config().timeprint_format)} {message}\n")
    logfile.close()

def dbgsave(message: str):
    logfile = open(os.path.join(Config().data_path,'yapo-eplus-debug_' + datetime.now().strftime("%Y-%m-%d") +'.log'), 'a+')
    logfile.write(f"{datetime.now().strftime(Config().timeprint_format)} {message}\n")
    logfile.close()
