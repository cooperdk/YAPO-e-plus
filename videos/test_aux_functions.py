import os

from django.test import TestCase

import videos.models
import videos.scrapers.tmdb as scraper_tmdb
from configuration import Config
from utils import Constants
from videos.scrapers.scanner_tpdb import scanner_tpdb


class Test(TestCase):
    def setUp(self):
        pass

    def test_scan_actor_simple_id(self):
        uut = scanner_tpdb()
        newActor = videos.models.Actor(name = 'Ava Addams')
        uut.tpdb_scan_actor(newActor, False)
        actors = videos.models.Actor.objects.all()
        self.assertEqual(1, len(actors))
        self.assertEqual('Ava Addams', actors[0].name)
        self.assertEqual('9bc542ba-0dce-4765-835d-b4e1989bd8b4', actors[0].tpdb_id)
        self.assertTrue(len(actors[0].description) > 0)

    def test_scan_actor_simple(self):
        uut = scanner_tpdb()
        newActor = videos.models.Actor(name = 'Anna Song')
        uut.tpdb_scan_actor(newActor, False)
        actors = videos.models.Actor.objects.all()
        self.assertEqual(1, len(actors))
        self.assertEqual('Anna Song', actors[0].name)
        self.assertTrue(len(actors[0].description) > 0)

    def test_scan_actor_tmdb(self):
        uut = scraper_tmdb.scanner_tmdb()
        newActor = videos.models.Actor(name = 'Anna Song')
        uut.search_person_with_force_flag(newActor, False)
        newActor = videos.models.Actor(name = 'Ava Addams', thumbnail = Constants().unknown_person_image_path)
        newActor.save()
        uut.search_person_with_force_flag(newActor, True)
        actors = videos.models.Actor.objects.all()
        self.assertEqual(1, len(actors))
        self.assertEqual('Ava Addams', actors[0].name)
        self.assertEqual('F', actors[0].gender)
        self.assertEqual(1981, actors[0].date_of_birth.year)
        self.assertEqual(9, actors[0].date_of_birth.month)
        self.assertEqual(16, actors[0].date_of_birth.day)
        self.assertTrue(len(actors[0].description) > 0)
        aliases = actors[0].actor_aliases.all()
        self.assertEqual(4, len(aliases))
        self.assertEqual(1, len([x for x in aliases if x.name == 'Alexia Roy']))
        self.assertEqual(1, len([x for x in aliases if x.name == 'Luna']))
        self.assertEqual(1, len([x for x in aliases if x.name == 'Avva']))
        self.assertEqual(1, len([x for x in aliases if x.name == 'Ava Adams']))

        self.assertEqual('media/actor/1/profile/profile.jpg', actors[0].thumbnail)
        self.assertTrue(os.path.isfile(os.path.join(Config().site_media_path, 'actor/1/profile/profile.jpg' )))