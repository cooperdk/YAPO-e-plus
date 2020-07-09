import os
from datetime import datetime
from typing import Dict, Optional

import yaml
import json
from utils import Singleton
from utils import Constants

__yaml_root_element__ = "YAMLConfig"
__settings_datetime_format__ = "%Y-%m-%d %H:%M:%S"
__settings_keyword_none__ = "None"


class Config(metaclass=Singleton):
  last_all_scene_tag: Optional[datetime]
  root_path: str
  yapo_path: str
  site_path: str
  data_path: str
  config_path: str
  database_dir: str
  database_path: str
  site_static_path: str
  site_media_path: str
  timeprint_format: str
  configfile_path: str
  vlc_path: Optional[str]
  current_setting_version: int

  def __init__(self):
    self.root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
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
    self.current_setting_version = 3
    self.vlc_path = None
    self.last_all_scene_tag = None
    self.__update_config_from_file__()

  def __log__(self, message: str) -> None:  # should be utils.printing, but that leads to circular dependency
    print(f"{datetime.now().strftime(self.timeprint_format)}> {message}")

  def __update_config_from_file__(self) -> None:
    if os.path.isfile(self.configfile_path):
      self.__load_settings__(self.configfile_path)
    else:
      json_settings_path = os.path.join(self.config_path, Constants().default_json_settings_filename)
      if os.path.isfile(json_settings_path):
        self.__load_settings__(json_settings_path)

  def __load_settings__(self, settings_path: str) -> None:
    if os.path.splitext(settings_path)[-1] == '.yml':
      with open(settings_path, 'r') as file:
        settings_dict = yaml.safe_load(file)
        self.__update_settings__(settings_dict)
      return
    if os.path.splitext(settings_path)[-1] == '.json':
      with open(settings_path, 'r') as file:
        settings_dict = json.loads(file.read())
        self.__update_settings__({__yaml_root_element__: settings_dict})
      self.__log__("Converting old json format configuration file to yaml...")
      self.save()
      os.remove(settings_path)
      self.__log__("Finished, deleted old json format configuration file.")
      return
    raise Exception(f'{settings_path} is no known config format. Only .yml or .json are allowed.')

  def __update_settings__(self, settings_dict: Optional[Dict[str, Dict[str, str]]]) -> None:
    if settings_dict and settings_dict.get(__yaml_root_element__):
      self.data_path = settings_dict[__yaml_root_element__].get("data_path") or self.data_path
      self.config_path = settings_dict[__yaml_root_element__].get("config_path") or self.config_path
      self.database_dir = settings_dict[__yaml_root_element__].get("db_dir") or self.database_dir
      self.timeprint_format = settings_dict[__yaml_root_element__].get("log_timeformat") or self.timeprint_format
      self.last_all_scene_tag = __string_to_nullable_time__(settings_dict[__yaml_root_element__].get("last_all_scene_tag")) or self.last_all_scene_tag
      self.site_media_path = settings_dict[__yaml_root_element__].get("site_media_path") or self.site_media_path
      self.vlc_path = settings_dict[__yaml_root_element__].get("vlc_path") or self.vlc_path
      self.current_setting_version = __string_to_nullable_int__(settings_dict[__yaml_root_element__].get("current_setting_version")) or self.current_setting_version

  def __settings_to_dict__(self):
    return {
      __yaml_root_element__: {
        "data_path": self.data_path,
        "config_path": self.config_path,
        "db_dir": self.database_dir,
        "log_timeformat": self.timeprint_format,
        "last_all_scene_tag": __nullable_time_to_string__(self.last_all_scene_tag),
        "site_media_path": self.site_media_path,
        "vlc_path": self.vlc_path,
        "current_setting_version": __nullable_int_to_string__(self.current_setting_version)
      }
    }

  def save(self) -> None:
    with open(self.configfile_path, 'w+') as file:
      yaml.dump(self.__settings_to_dict__(), stream=file, default_flow_style=False)

  def get_old_settings_as_json(self):
    # return f'{{"settings_version": 3, "vlc_path": "{os.path.normpath(self.vlc_path)}", "last_all_scene_tag": "{__nullable_time_to_string__(self.last_all_scene_tag)}"}}'
    # the given vlc_path somehow leads to a json error, it thinks the ':' should be escaped? Unclear, because a colon should just work fine
    return f'{{"settings_version": 3, "vlc_path": "", "last_all_scene_tag": "{__nullable_time_to_string__(self.last_all_scene_tag)}"}}'


def __nullable_time_to_string__(time: Optional[datetime]) -> str:
  if time:
    return time.strftime(__settings_datetime_format__)
  return __settings_keyword_none__


def __string_to_nullable_time__(timestring: str) -> Optional[datetime]:
  if not timestring or timestring == __settings_keyword_none__:
    return None
  return datetime.strptime(timestring, __settings_datetime_format__)


def __nullable_int_to_string__(number: Optional[int]) -> str:
  if number:
    return str(number)
  return __settings_keyword_none__


def __string_to_nullable_int__(intstring: str) -> Optional[int]:
  if not intstring or intstring == __settings_keyword_none__:
    return None
  return int(intstring)



