from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from django.db.models import signals

import os

from configuration import Config

import abc

# Inherit from this if your model has files underneath the media dir, indexed by ID.
from utils import Constants


class ModelWithMediaContent:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_media_dir(self) -> str:
        return

    # Get the media path for this model. If createIfNotExisting is specified, ensure the path exists before returning.
    def get_media_path(self, filename : str = '', createIfNotExisting = True ) -> str:
        mediaDir = os.path.abspath(
            os.path.join(Config().site_media_path, self.get_media_dir(), str(self.id))
        )
        if createIfNotExisting:
            if not os.path.exists(mediaDir):
                os.makedirs(mediaDir)

        return os.path.join(mediaDir, filename)


class ActorAlias(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_exempt_from_one_word_search = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} "

class SceneTag(models.Model, ModelWithMediaContent):
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    play_count = models.IntegerField(default=0)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)
    scene_tag_alias = models.TextField(default="", blank=True)
    exclusions = models.TextField(default="", null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "

    def get_media_dir(self):
        return "tags"

class ActorTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    play_count = models.IntegerField(default=0)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)
    actor_tag_alias = models.TextField(default="", blank=True)
    exclusions = models.TextField(default="", null=True, blank=True)
    scene_tags = models.ManyToManyField(
        SceneTag, blank=True, related_name="actor_tags" # null=True, 
    )
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "


class Actor(models.Model, ModelWithMediaContent):
    MALE = "M"
    FEMALE = "F"
    TRANSGENDER = "T"

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (TRANSGENDER, "Transgender"),
    )

    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    play_count = models.IntegerField(default=0)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    description = models.TextField(default="", blank=True)
    thumbnail = models.CharField(max_length=640, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True)
    imdb_id = models.CharField(max_length=25, null=True, blank=True)
    tmdb_id = models.CharField(max_length=25, null=True, blank=True)
    tpdb_id = models.CharField(null=True, default="", max_length=48, blank=True)
    official_pages = models.TextField(default="", blank=True)
    actor_tags = models.ManyToManyField(
        ActorTag, blank=True, related_name="actors" # null=True, 
    )
    ethnicity = models.CharField(max_length=30, null=True, blank=True)
    weight = models.CharField(max_length=30, null=True, blank=True)
    country_of_origin = models.CharField(max_length=30, null=True, blank=True)
    tattoos = models.CharField(max_length=600, null=True, blank=True)
    piercings = models.CharField(max_length=600, null=True, blank=True)
    height = models.CharField(max_length=30, null=True, blank=True)
    measurements = models.CharField(max_length=30, null=True, blank=True)
    extra_text = models.TextField(default="", blank=True)
    last_lookup = models.DateTimeField(null=True, blank=True)
    is_exempt_from_one_word_search = models.BooleanField(default=False)
    actor_aliases = models.ManyToManyField(
        ActorAlias, blank=True, related_name="actors" # null=True, 
    )
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ""

    def get_media_dir(self):
        return "actor"

    def createOrAddAlias(self, aka):
        if not self.actor_aliases.filter(name=aka):
            newAlias = ActorAlias.objects.get_or_create(name=aka)
            newAlias[0].save()

            self.actor_aliases.add(newAlias[0])

    def generateThumbnailPath(self):
        thumnbail_dir = self.get_media_path('profile')
        if not os.path.exists(thumnbail_dir):
            os.makedirs(thumnbail_dir)
        return os.path.join(thumnbail_dir, 'profile.jpg')

    def has_thumbnail_image(self):
        if self.thumbnail == Constants().unknown_person_image_path:
            return False
        return os.path.isfile(self.generateThumbnailPath())

    def getThumbnailPathURL(self):
        # FIXME: will this work?
        self.thumbnail = web.pathname2url(save_file_name)

    def has_valid_date_of_birth(self):
        if self.date_of_birth is None or self.date_of_birth == "" or self.date_of_birth == "1970-01-01":
            return False
        return True

    def has_valid_ethnicity(self):
        if self.ethnicity is None or self.ethnicity == "":
            return False
        return True

    def has_valid_country_of_origin(self):
        if self.country_of_origin is None or self.country_of_origin == "":
            return False
        return True

    def has_valid_weight(self):
        if self.weight is None or self.weight == 0:
            return False
        return True

    def has_valid_height(self):
        if self.height is None or self.height == 0:
            return False
        return True


class Website(models.Model, ModelWithMediaContent):
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    play_count = models.IntegerField(default=0)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    thumbnail = models.CharField(max_length=640, null=True, blank=True)
    scene_tags = models.ManyToManyField(SceneTag, blank=True, related_name="websites") #null=True, 
    website_alias = models.TextField(default="", blank=True)
    exclusions = models.TextField(default="", null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    url = models.TextField(max_length=256, default="", null=True, blank=True)
    tpdb_id = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} "

    def get_media_dir(self):
        return "websites"

class Scene(models.Model, ModelWithMediaContent):
    name = models.CharField(max_length=500)
    tpdb_id = models.CharField(null=True, default="", max_length=48, blank=True)
    release_id = models.CharField(null=True, default="", max_length=64, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    hash = models.CharField(default="", max_length=32, blank=True)
    path_to_file = models.CharField(max_length=640, unique=True)
    path_to_dir = models.CharField(max_length=640)
    date_added = models.DateTimeField(auto_now_add=True)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_last_played = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    last_filename_tag_lookup = models.DateTimeField(null=True, blank=True)
    play_count = models.IntegerField(default=0)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    description = models.TextField(default="", blank=True)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)
    scene_tags = models.ManyToManyField(
        SceneTag, blank=True, related_name="scenes" # null=True, 
    )
    actors = models.ManyToManyField(Actor, blank=True, related_name="scenes") # null=True, 
    websites = models.ManyToManyField(
        Website, blank=True, related_name="scenes" # null=True, 
    )
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    bit_rate = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    codec_name = models.CharField(null=True, blank=True, max_length=20)
    framerate = models.FloatField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    orig_name = models.CharField(null=True, max_length=500)
    orig_path_to_file = models.CharField(null=True, default="", max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} "

    def get_media_dir(self):
        return "websites"

class Folder(MPTTModel):
    name = models.CharField(max_length=300, unique=True)
    last_folder_name_only = models.CharField(max_length=100, null=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", db_index=True, on_delete=models.PROTECT
    )
    scenes = models.ManyToManyField(Scene, related_name="folders_in_tree") # null=True, 
    path_with_ids = models.CharField(null=True, blank=True, max_length=900)
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "

    class MPTTMeta:
        order_insertion_by = ["name"]


class LocalSceneFolders(models.Model):
    name = models.CharField(max_length=500, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Playlist(models.Model):
    name = models.CharField(max_length=500, unique=True)
    scenes = models.ManyToManyField(
        Scene, related_name="playlists", blank=True # null=True, 
    )
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "


@receiver(signals.post_save, sender=ActorTag)
def create_scene_tag(sender, **kwargs):
    saved_actor_tag_instance = kwargs.get("instance")

    if not SceneTag.objects.filter(name=saved_actor_tag_instance.name):
        SceneTag.objects.create(name=saved_actor_tag_instance.name)

    saved_actor_tag_instance.scene_tags.add(
        SceneTag.objects.get(name=saved_actor_tag_instance.name)
    )

    signals.post_save.disconnect(create_scene_tag, sender=ActorTag)
    saved_actor_tag_instance.save()
    signals.post_save.connect(create_scene_tag, sender=ActorTag)
