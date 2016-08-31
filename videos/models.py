from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import datetime


# Create your models here.


class ActorAlias(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_exempt_from_one_word_search = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return "%s " % (self.name,)


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
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s " % (self.name,)


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
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s " % (self.name,)


class Actor(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    TRANSGENDER = 'T'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (TRANSGENDER, 'Transgender'),
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
    thumbnail = models.CharField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True)
    imdb_id = models.CharField(max_length=25, null=True, blank=True)
    tmdb_id = models.CharField(max_length=25, null=True, blank=True)
    official_pages = models.TextField(default="", blank=True)
    actor_tags = models.ManyToManyField(ActorTag, null=True, blank=True, related_name='actors')
    ethnicity = models.CharField(max_length=30, null=True, blank=True)
    weight = models.CharField(max_length=30, null=True, blank=True)
    country_of_origin = models.CharField(max_length=30, null=True, blank=True)
    tattoos = models.CharField(max_length=600, null=True, blank=True)
    height = models.CharField(max_length=30, null=True, blank=True)
    measurements = models.CharField(max_length=30, null=True, blank=True)
    extra_text = models.TextField(default="", blank=True)
    last_lookup = models.DateTimeField(null=True, blank=True)
    is_exempt_from_one_word_search = models.BooleanField(default=False)
    actor_aliases = models.ManyToManyField(ActorAlias, null=True, blank=True, related_name='actors')
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('videos:actor-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name or u''

    def get_name_hyphens(self):
        return self.name.replace(' ', '-')

    def get_name_delimiter(self, delimiter):
        return self.name.replace(' ', delimiter)


class Website(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    play_count = models.IntegerField(default=0)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)
    scene_tags = models.ManyToManyField(SceneTag, null=True, blank=True, related_name='websites')
    website_alias = models.TextField(default="", blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s " % (self.name,)


class Scene(models.Model):
    name = models.CharField(max_length=500)
    path_to_file = models.CharField(max_length=500, unique=True)
    path_to_dir = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    date_fav = models.DateTimeField(null=True, blank=True)
    date_runner_up = models.DateTimeField(null=True, blank=True)
    last_filename_tag_lookup = models.DateTimeField(null=True, blank=True)
    play_count = models.IntegerField(default=0)
    is_fav = models.BooleanField(default=False)
    is_runner_up = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    description = models.TextField(default="", blank=True)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)
    scene_tags = models.ManyToManyField(SceneTag, blank=True, null=True, related_name='scenes')
    actors = models.ManyToManyField(Actor, null=True, blank=True, related_name='scenes')
    websites = models.ManyToManyField(Website, null=True, blank=True, related_name='scenes')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    bit_rate = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    codec_name = models.CharField(null=True, blank=True, max_length=20)
    framerate = models.FloatField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s " % (self.name,)

    def get_absolute_url(self):
        return reverse('videos:scene-details', kwargs={'pk': self.pk})


class Folder(MPTTModel):
    name = models.CharField(max_length=300, unique=True)
    last_folder_name_only = models.CharField(max_length=100, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    scenes = models.ManyToManyField(Scene, null=True, related_name='folders_in_tree')
    path_with_ids = models.CharField(null=True, blank=True, max_length=900)
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s " % (self.name,)

    class MPTTMeta:
        order_insertion_by = ['name']


class LocalSceneFolders(models.Model):
    name = models.CharField(max_length=500, unique=True)

