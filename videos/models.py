from __future__ import unicode_literals

from django.urls import reverse
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from django.db.models import signals

import datetime


# Create your models here.


class ActorAlias(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_exempt_from_one_word_search = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} "


class SceneTag(models.Model):
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
    scene_tags = models.ManyToManyField(SceneTag, blank=True, related_name="actor_tags")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "


class Actor(models.Model):
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
    actor_tags = models.ManyToManyField(ActorTag, blank=True, related_name="actors")
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
    actor_aliases = models.ManyToManyField(ActorAlias, blank=True, related_name="actors")
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("videos:actor-details", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name or ""

    def get_name_hyphens(self):
        return self.name.replace(" ", "-")

    def get_name_delimiter(self, delimiter):
        return self.name.replace(" ", delimiter)


class Website(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    play_count = models.IntegerField(default=0)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    thumbnail = models.CharField(max_length=640, null=True, blank=True)
    scene_tags = models.ManyToManyField(SceneTag, blank=True, related_name="websites")
    website_alias = models.TextField(default="", blank=True)
    exclusions = models.TextField(default="", null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    url = models.TextField(max_length=256, default="", null=True, blank=True)
    tpdb_id = models.IntegerField(default=0)
    filename_format = models.TextField(max_length=256, default="", null=True, blank=True)

    def __str__(self):
        return f"{self.name} "


class Scene(models.Model):
    name = models.CharField(max_length=500)
    clean_title = models.CharField(max_length=320, null=True, blank=True)
    tpdb_id = models.CharField(null=True, default="", max_length=48, blank=True)
    tpdb_scanned = models.BooleanField(default=False)
    tpdb_scanned_match = models.BooleanField(default=False)
    tpdb_scanned_unsure = models.BooleanField(default=False)
    url = models.CharField(max_length=320, null=True, blank=True)
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
    scene_tags = models.ManyToManyField(SceneTag, blank=True, related_name="scenes")
    actors = models.ManyToManyField(Actor, blank=True, related_name="scenes")
    websites = models.ManyToManyField(Website, blank=True, related_name="scenes")
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

    def get_absolute_url(self):
        return reverse("videos:scene-details", kwargs={"pk": self.pk})


class Folder(MPTTModel):
    name = models.CharField(max_length=300, unique=True)
    last_folder_name_only = models.CharField(max_length=100, null=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", db_index=True, on_delete=models.PROTECT
    )
    scenes = models.ManyToManyField(Scene, related_name="folders_in_tree")
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
    scenes = models.ManyToManyField(Scene, related_name="playlists", blank=True)
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
