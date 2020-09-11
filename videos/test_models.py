import os

from django.test import TestCase
import videos.models
from configuration import Config


class TestActor(TestCase):
    def test_media_paths(self):
        # Make an actor, with ID 123, and ensure that the media is placed into the actor/123 directory.
        actor = videos.models.Actor(name='foo', id = 123)
        expected = os.path.join(Config().site_media_path, "actor", "123", "test")
        self.assertEqual(actor.get_media_path('test'), expected)
