import os
import yaml
import json
from datetime import datetime
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
    self.configfile_path = os.path.join(self.config_path, Constants().default_yaml_settings_filename)
    self.last_all_scene_tag = None
    self.__update_config_from_file__()

  def __update_config_from_file__(self):
    if os.path.isfile(self.configfile_path):
      self.__load_settings__(self.configfile_path)
    else:
      json_settings_path = os.path.join(self.config_path, Constants().default_yaml_settings_filename)
      if os.path.isfile(json_settings_path):
        self.__load_settings__(json_settings_path)
      self.save()

  def __load_settings__(self, settings_path):
    if os.path.splitext(settings_path)[-1] == '.yml':
      with open(settings_path, 'r') as file:
        settings_dict = yaml.safe_load(file)
        self.__update_settings__(settings_dict)
      return
    if os.path.splitext(settings_path)[-1] == '.json':
      with open(settings_path, 'r') as file:
        settings_dict = json.loads(file.read())
        self.__update_settings__(settings_dict)
      return
    raise Exception(f'{settings_path} is no known config format. Only .yml or .json are allowed.')

  def save(self):
    pass

  def __update_settings__(self, settings_dict):
    pass
