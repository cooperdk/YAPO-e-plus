from datetime import datetime
from YAPO.config import Config
from YAPO.utils import Singleton


class Logger(metaclass=Singleton):
  def warn(self, message: str):
    timeprint(message)

  def debug(self, message: str):
    timeprint(message)

  def info(self, message: str):
    timeprint(message)

  def error(self, message: str):
    timeprint(message)


def timeprint(message: str):
  print(f"{datetime.now().strftime(Config().timeprint_format)}> {message}")