import base64
import os
from typing import Dict, Any

from django.test import TestCase
import videos.models
from videos import views, aux_functions
from configuration import Config


class Test_views(TestCase):
    def test_clean_dir_actors_removes_deleted_actor(self):
        # Make an actor, thus creating files on the filesystem. Then, delete the actor, run a clean_dir, and ensure that
        # the files are cleaned up from the filesystem.
        actor = videos.models.Actor(name='foo', id=123)
        actor.save()
        mediapath = actor.get_media_path(createIfNotExisting=True)
        self.assertTrue(os.path.exists(mediapath), "actor media was not created before test")

        actor.delete()
        views.clean_dir(videos.models.Actor)
        self.assertFalse(os.path.exists(mediapath), "actor media was not deleted")

    def test_clean_dir_actors_does_not_remove_not_deleted_actor(self):
        actor = videos.models.Actor(name='foo', id=123)
        actor.save()
        mediapath = actor.get_media_path(createIfNotExisting=True)
        self.assertTrue(os.path.exists(mediapath), "actor media was not created before test")
        views.clean_dir(videos.models.Actor)
        self.assertTrue(os.path.exists(mediapath), "actor media was deleted but should not have been")

class mockedRequest:
    data: Dict[Any, Any]

    def __init__(self, imageFilename = None):
        self.data = {}
        if imageFilename is not None:
            with open(imageFilename, 'rb') as f:
                base64data = base64.b64encode(f.read()).decode("utf-8")
            self.data["file"] = f"data:image/foo.jpg;base64,{base64data}"
            print(self.data["file"][:100])

class TestAssetAdd(TestCase):

    def test_post(self):
        testfilename = 'testdata/debian-logo.png'
        # Send a base64-encoded image the AssetAdd class, and ensure the specified actor is updated and the image saved
        # appropriately.
        actor = videos.models.Actor(name='foo', id = 10)
        actor.save()

        uut = views.AssetAdd()
        req = mockedRequest(testfilename)
        req.data["type"] = "Actor"
        req.data["id"] = actor.id
        uut.post(req)
        actor.refresh_from_db()
        thumbnail_filename = aux_functions.urlpath2pathname(actor.thumbnail)

        self.assertTrue(os.path.exists(thumbnail_filename))
        with open(thumbnail_filename, 'rb') as f:
            thumbnailBytes = f.read()
        with open(testfilename, 'rb') as f:
            testFilenameBytes = f.read()
        self.assertEqual(thumbnailBytes, testFilenameBytes)
