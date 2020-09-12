import os

from django.test import TestCase
import videos.models
from configuration import Config
from videos import views


class Test_views(TestCase):
    def test_clean_dir_actors_removes_deleted_actor(self):
        # Make an actor, thus creating files on the filesystem. Then, delete the actor, run a clean_dir, and ensure that
        # the files are cleaned up from the filesystem.
        actor = videos.models.Actor(name='foo', id = 123)
        actor.save()
        mediapath = actor.get_media_path(createIfNotExisting=True)
        self.assertTrue(os.path.exists(mediapath), "actor media was not created before test")

        actor.delete()
        views.clean_dir(videos.models.Actor)
        self.assertFalse(os.path.exists(mediapath), "actor media was not deleted")

    def test_clean_dir_actors_does_not_remove_not_deleted_actor(self):
        actor = videos.models.Actor(name='foo', id = 123)
        actor.save()
        mediapath = actor.get_media_path(createIfNotExisting=True)
        self.assertTrue(os.path.exists(mediapath), "actor media was not created before test")
        views.clean_dir(videos.models.Actor)
        self.assertTrue(os.path.exists(mediapath), "actor media was deleted but should not have been")
