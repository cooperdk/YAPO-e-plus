from datetime import datetime
from configuration import Config
from utils import Singleton


class Logger(metaclass=Singleton):

  def warn(self, message: str):
    timeprint(message)

  def debug(self, message: str):
    timeprint(f"\033[34m[DEBUG]\033[39m {message}")

  def info(self, message: str):
    timeprint(f"\033[33m[INFO ]\033[39m {message}")

  def error(self, message: str):
    timeprint(f"\033[31m[ERROR]\033[39m {message}")

def timeprint(message: str):
  print(f"{datetime.now().strftime(Config().timeprint_format)}-> {message}")
