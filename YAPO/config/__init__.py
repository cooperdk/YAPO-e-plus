import os
from YAPO.utils import Singleton
from YAPO.utils import Constants


class Config(metaclass=Singleton):
  def __init__(self):
    self.root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    self.yapo_path = os.path.join(self.root_path, Constants().code_subdir)
    self.site_path = os.path.join(self.root_path, Constants().site_subdir)
    self.data_path = os.path.join(self.root_path, Constants().data_subdir)
    self.config_path = os.path.join(self.root_path, Constants().config_subdir)
    self.database_dir = os.path.join(self.root_path, Constants().db_subdir)
    self.database_path = os.path.join(self.database_dir, Constants().db_filename)
    self.site_static_path = os.path.join(self.site_path, Constants().site_static_subdir)
    self.site_media_path = os.path.join(self.site_path, Constants().site_media_subdir)
    self.timeprint_format = Constants().default_timeprint_format
