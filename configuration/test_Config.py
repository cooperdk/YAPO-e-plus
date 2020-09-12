import os

from django.test import TestCase

from configuration import Config

class Test_Config(TestCase):
    def test_config_loading(self):
        tempConfigFile = os.path.join( 'testdata', 'testsettings.yml')

        with open(tempConfigFile, 'w') as f:
            f.write("YAPOConfig:\n")
            f.write("  current_setting_version: 3\n")
            f.write("  data_path: /data/path/here\n")
            f.write("  yapo_url: myurl\n")
        Config().configfile_path = tempConfigFile
        Config().__update_config_from_file__()
        self.assertEqual('/data/path/here', Config().data_path)
        self.assertEqual('myurl', Config().yapo_url)

    def test_config_loading_database(self):
        tempConfigFile = os.path.join( 'testdata', 'testsettings.yml')

        with open(tempConfigFile, 'w') as f:
            f.write("YAPOConfig:\n")
            f.write("  current_setting_version: 3\n")
            f.write("  db_dir: /data/path/here\n")
        Config().configfile_path = tempConfigFile
        Config().__update_config_from_file__()
        self.assertEqual('/data/path/here', Config().database_dir)

    def test_config_setting_generated_property(self):
        tempConfigFile = os.path.join( 'testdata', 'testsettings.yml')

        with open(tempConfigFile, 'w') as f:
            f.write("YAPOConfig:\n")
            f.write("  current_setting_version: 3\n")
            f.write("  yapo_path: somepath\n")
        Config().configfile_path = tempConfigFile
        Config().__update_config_from_file__()
        self.assertEqual('somepath', Config().yapo_path)
        self.assertEqual('todo', Config().site_path)
