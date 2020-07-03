from datetime import datetime
from YAPO.config import Config


class Singleton(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]


class Constants(metaclass=Singleton):
  def __init__(self):
    self.code_subdir = 'YAPO'
    self.data_subdir = 'data'
    self.site_subdir = 'videos'
    self.config_subdir = 'config'
    self.db_filename = 'db.sqlite3'
    self.db_subdir = 'database'
    self.site_static_subdir = 'static'
    self.site_media_subdir = 'media'
    self.default_timeprint_format = '%Y-%m-%d, %H:%M:%S'


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
  print(f"{datetime.now().strftime(Config().timeprint_format)}> {message}"
