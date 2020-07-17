from datetime import datetime
from configuration import Config
from utils import Singleton


class Logger(metaclass=Singleton):

  def warn(self, message: str):
    timeprint(message)

  def debug(self, message: str):
    timeprint(f"[DEBUG] {message}")

  def info(self, message: str):
    timeprint(f"[INFO ] {message}")

  def error(self, message: str):
    timeprint(f"[ERROR] {message}")

def timeprint(message: str):
  print(f"{datetime.now().strftime(Config().timeprint_format)}-> {message}")
