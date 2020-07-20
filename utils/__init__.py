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
    self.videoprocessing = True
    self.default_json_settings_filename = 'settings.json'
    self.default_yaml_settings_filename = 'settings.yml'
    self.unknown_person_image_path = "media/images/actor/Unknown/profile/profile.jpg"
    self.sheet_width = 1024
    self.sheet_grid = "4x4"
    self.vlc_path = "c:/program files/videolan/vlc/vlc.exe"
