from datetime import datetime
from configuration import Config
from utils import Singleton
import re
import os
from colorama import init
init()
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

    def timer(self, job: str, start: datetime, stop: datetime):
      time = result(start, stop)
      timeprint(f'[\033[36mTIMER\033[39m] Job "{job}" took {time}.')
      if Config().debug:
        dbgsave(f"[TIMER] Job {job} took {time}")


def timeprint(message: str):
    print(f"{datetime.now().strftime('%H:%M:%S')} {message}")


def logsave(message: str):
    with open(os.path.join(Config().data_path,'yapo-eplus_' + datetime.now().strftime("%Y-%m-%d") +'.log'), 'a+') as logfile:
        logfile.write(f"{datetime.now().strftime(Config().timeprint_format)} {message}\n")


def dbgsave(message: str):
    with open(os.path.join(Config().data_path,'yapo-eplus-debug_' + datetime.now().strftime("%Y-%m-%d") +'.log'), 'a+') as logfile:
        logfile.write(f"{datetime.now().strftime(Config().timeprint_format)} {message}\n")


def result(start: datetime, stop: datetime):
    import time
    from datetime import datetime
    delta = stop - start
    result = time.gmtime(delta.total_seconds())
    hr = "hour" if result.tm_hour == 1 else "hours"
    mn = "minute" if result.tm_min == 1 else "minutes"
    sc = "second" if result.tm_sec == 1 else "seconds"
    if result.tm_hour > 0:
        return f"{result.tm_hour} {hr}, {result.tm_min} {mn} and {result.tm_sec} {sc}"
    elif result.tm_min > 0:
        return f"{result.tm_min} {mn} and {result.tm_sec} {sc}"
    else:
        return f"{result.tm_sec} {sc}"
