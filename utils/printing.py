import os
from datetime import datetime

from configuration import Config
from utils import Singleton

class Logger(metaclass=Singleton):

    def warn(self, message: str):
      timeprint(f"[\033[31mWARN!\033[39m] {message}")
      logsave(f"[WARN!] {message}")

    def swarn(self, message: str):
      timeprint(f"[\033[31mWARN!\033[39m] {message}")

    def debug(self, message: str):
      timeprint(f"[\033[34mDEBUG\033[39m] {message}")
      logsave(f"[DEBUG] {message}")

    def info(self, message: str):
      timeprint(f"[\033[33mINFO\033[39m ] {message}")
      logsave(f"[INFO ] {message}")

    def sinfo(self, message: str):
      timeprint(f"[\033[33mINFO\033[39m ] {message}")

    def error(self, message: str):
      timeprint(f"\033[31m[ERROR]\033[39m {message}")
      logsave(f"[ERROR] {message}")

def timeprint(message: str):
    print(f"{datetime.now().strftime('%H:%M:%S')}-> {message}")

def logsave(message: str):
    logfile = open(os.path.join(Config().data_path,'yapo-eplus.log'), 'a+')
    logfile.write(f"{datetime.now().strftime(Config().timeprint_format)}-> {message}\n")
    logfile.close()
