import datetime
import os
import re
import struct

import django

from configuration import Config
import logging
log = logging.getLogger(__name__)
from videos import const

django.setup()

from videos.models import Actor, Scene, ActorAlias, SceneTag, Website

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

def get_hash(path: str):
  """
  This function produces a hash for a video file: size + 64bit chksum of the first and
  last 64k (even if they overlap because the file is smaller than 128k)
  It will take approx. 30 seconds to generate 100 hashes on a regular hard disk.
  This is the OSO/ISDB hasher which is also used by opensubtitles.
  """
  try:
    longlongformat = 'Q'  # unsigned long long little endian
    bytesize = struct.calcsize(longlongformat)
    fmt = "<%d%s" % (65536 // bytesize, longlongformat)

    f = open(path, "rb")

    filesize = os.fstat(f.fileno()).st_size
    filehash = filesize

    if filesize < 65536 * 2:
      log.error(f"File size error: {path}")
      return "SizeError"

    buf = f.read(65536)
    longlongs = struct.unpack(fmt, buf)
    filehash += sum(longlongs)

    f.seek(-65536, os.SEEK_END)  # size is always > 131072
    buf = f.read(65536)
    longlongs = struct.unpack(fmt, buf)
    filehash += sum(longlongs)
    filehash &= 0xFFFFFFFFFFFFFFFF

    f.close()
    returnedhash = "%016x" % filehash
    return returnedhash
  except Exception as e:
    log.error(f"Cannot hash: {path} : {e}")
    raise

def rehash ():
  num = 0
  scenes = Scene.objects.order_by("id")  # name
  for scene in scenes:
    scene.hash = get_hash(scene.path_to_file)
    scene.save()
    num += 1
    log.info(f"{num} hashes checked/regenerated...")

def filter_alias(actor_alias):
  filtered_alias = list()
  for alias in actor_alias:
    if " " in alias.name or alias.is_exempt_from_one_word_search:
      filtered_alias.append(alias)

  return filtered_alias


def if_new_actors():
  actors = list(Actor.objects.filter(modified_date__gt=const.LAST_ALL_SCENE_TAG))
  if len(actors) > 0:
    return [True, actors]
  else:
    return [False, actors]


def if_new_alias():
  alias = list(ActorAlias.objects.filter(date_added__gt=const.LAST_ALL_SCENE_TAG))
  if len(alias) > 0:
    return [True, alias]
  else:
    return [False, alias]


def if_new_tags():
  tags = list(SceneTag.objects.filter(modified_date__gt=const.LAST_ALL_SCENE_TAG))
  if len(tags) > 0:
    return [True, tags]
  else:
    return [False, tags]


def if_new_websites():
  website = list(Website.objects.filter(modified_date__gt=const.LAST_ALL_SCENE_TAG))
  if len(website) > 0:
    return [True, website]
  else:
    return [False, website]


def parse_all_scenes(ignore_last_lookup):
  actors = list(
    Actor.objects.extra(select={"length": "Length(name)"}).order_by("-length")
  )
  actors_alias = list(
    ActorAlias.objects.extra(select={"length": "Length(name)"}).order_by("-length")
  )
  scene_tags = list(
    SceneTag.objects.extra(select={"length": "Length(name)"}).order_by("-length")
  )
  websites = list(
    Website.objects.extra(select={"length": "Length(name)"}).order_by("-length")
  )

  scenes = Scene.objects.all()
  scene_count = scenes.count()
  counter = 1

  if ignore_last_lookup:
    for scene in scenes:
      percent = (counter / scene_count) * 100
      os.system("cls" if os.name == "nt" else "clear")
      log.info(f"{int(percent)}% done - scene {counter} out of {scene_count} - ignoring last lookup")

      filtered_alias = filter_alias(actors_alias)

      parse_scene_all_metadata(scene, actors, filtered_alias, scene_tags, websites)
      counter += 1

  else:
    if const.LAST_ALL_SCENE_TAG:

      a = if_new_actors()
      if a[0]:
        actors = a[1]
        actors.sort(key=lambda x: len(x.name), reverse=True)
      else:
        actors = list()

      b = if_new_alias()
      if b[0]:
        actors_alias = b[1]

        actors_alias = filter_alias(actors_alias)

        actors_alias.sort(key=lambda x: len(x.name), reverse=True)
      else:
        actors_alias = list()

      c = if_new_tags()
      if c[0]:
        scene_tags = c[1]
        scene_tags.sort(key=lambda x: len(x.name), reverse=True)
      else:
        scene_tags = list()

      d = if_new_websites()
      if d[0]:
        websites = d[1]
        websites.sort(key=lambda x: len(x.name), reverse=True)
      else:
        websites = list()

      for scene in scenes:
        percent = (counter / scene_count) * 100
        os.system("cls" if os.name == "nt" else "clear")
        log.info(f"{int(percent)}% done - scene {counter} out of {scene_count} - not ignoring last lookup")

        if (a[0]) or (b[0]) or (c[0]) or (d[0]):
          parse_scene_all_metadata(
            scene, actors, actors_alias, scene_tags, websites
          )
        counter += 1

    else:
      for scene in scenes:

        log.info(f"Scene {counter} out of {scene_count}")

        if scene.last_filename_tag_lookup:
          actors_filtered = list(
            Actor.objects.filter(
              modified_date__gt=scene.last_filename_tag_lookup
            )
          )
          actors_filtered.sort(key=lambda x: len(x.name), reverse=True)

          actors_alias_filtered = list(
            ActorAlias.objects.filter(
              date_added__gt=scene.last_filename_tag_lookup
            )
          )
          actors_alias_filtered.sort(key=lambda x: len(x.name), reverse=True)

          scene_tags_filtered = list(
            SceneTag.objects.filter(
              modified_date__gt=scene.last_filename_tag_lookup
            )
          )
          scene_tags_filtered.sort(key=lambda x: len(x.name), reverse=True)

          websites_filtered = list(
            Website.objects.filter(
              modified_date__gt=scene.last_filename_tag_lookup
            )
          )
          websites_filtered.sort(key=lambda x: len(x.name), reverse=True)

          actors_alias_filtered = filter_alias(actors_alias_filtered)

          parse_scene_all_metadata(
            scene,
            actors_filtered,
            actors_alias_filtered,
            scene_tags_filtered,
            websites_filtered,
          )
        else:

          filtered_alias = filter_alias(actors_alias)

          parse_scene_all_metadata(
            scene, actors, filtered_alias, scene_tags, websites
          )
        counter += 1

  now = datetime.datetime.now()

  Config().last_all_scene_tag = now

  Config().save()

  const.LAST_ALL_SCENE_TAG = now

  log.info("Finished parsing...")


def parse_scene_all_metadata(scene, actors, actors_alias, scene_tags, websites):
  log.info(f"Parsing scene path: {scene.path_to_file}")

  scene_path = scene.path_to_file.lower()

  # remove dates from scene path (Maybe later parse dates for scene release dates, right now release dates formats
  # are not consistan through the files)
  # scene_path = re.sub(r'"(.*)(\w+ \d{1,2}, \d{4})"', r'\1', scene_path)

  log.info("Looking for websites...")
  scene_path = parse_website_in_scenes(scene, scene_path, websites)

  log.info("Looking for actors and aliases...")
  scene_path = parse_actors_in_scene(scene, scene_path, actors, actors_alias)

  log.info("Looking for scene tags...")
  scene_path = parse_scene_tags_in_scene(scene, scene_path, scene_tags)

  if not (scene.hash):
    log.info("Hashing scene... ")
    scene.hash = get_hash(scene.path_to_file)
    log.info(f"ID: {scene.hash}")
  else:
    log.info(f"Scene already hashed ({scene.hash})")
  scene.last_filename_tag_lookup = datetime.datetime.now()

  log.info("Finished parsing scene, touching last lookup")

  scene.save()


def occurrences(what, string_to_search):
  ans = list()
  can_be_next_occurrence = True
  start_index = 0

  while can_be_next_occurrence:
    try:
      index = string_to_search.index(what, start_index)
      ans.append(index)
      start_index = index + 1
    except ValueError:
      can_be_next_occurrence = False

  return ans


def string_search_without_regex(actor, scene_path):
  ans = {"success": 0, "scene_path": scene_path}
  actor_name_lower = actor.name.lower()
  string_to_search_in = scene_path

  # scene_path_lower = scene_path.lower()

  # actor_name_lower = actor_name_lower.replace(' ', '?')

  actor_name_split = actor_name_lower.split(" ")

  actor_name_split_backup = list(actor_name_split)
  all_good = False
  total_fail = False
  total_success = False
  name_to_check = actor_name_split[0]

  first_name_occurrences = occurrences(name_to_check, string_to_search_in)
  name_length = len(name_to_check)
  del actor_name_split[0]
  for x in range(len(first_name_occurrences)):
    if not total_success:
      all_good = True
      begin_index = first_name_occurrences[x] + name_length
      actor_name_split_index = 0
      if not total_fail:
        while actor_name_split_index < len(actor_name_split):
          next_name = actor_name_split[actor_name_split_index]
          next_name_length = len(next_name)
          substring = string_to_search_in[
                      begin_index: begin_index + next_name_length + 1
                      ]
          try:
            index = substring.index(next_name)
            begin_index = begin_index + index + next_name_length
            actor_name_split_index += 1
            if actor_name_split_index >= len(actor_name_split):
              total_success = True
          except ValueError:
            try:
              last_occurrence = first_name_occurrences[x + 1]
              break
            except IndexError:
              actor_name_split_index += 1
              all_good = False
              total_fail = True
    else:
      break

    ans["success"] = all_good

  if all_good:
    for name in actor_name_split_backup:
      scene_path = scene_path.replace(name, "")

  ans["scene_path"] = scene_path
  return ans


def parse_actors_in_scene(scene_to_parse, scene_path, actors, actors_alias):
    # MyModel.objects.extra(select={'length':'Length(name)'}).order_by('length')

  for actor in actors:
    # If actor name is only one word or exempt from being searched even though it is one word.

    if actor.name.count(" ") > 0 or actor.is_exempt_from_one_word_search:
      ans = string_search_without_regex(actor, scene_path)

      if ans["success"]:
        scene_path = ans["scene_path"]
        add_actor_to_scene(actor, scene_to_parse)

        if actor.actor_tags.count() > 0:
          log.info(f"Actor has {actor.actor_tags.count()} tags...")

          for actor_tag in actor.actor_tags.all():
            current_tag = actor_tag.scene_tags.first()
            exclude = False
            if current_tag:

              if not SceneTag.objects.filter(name=actor_tag.name):
                current_tag = SceneTag(name=actor_tag.name)
                current_tag.save()
              else:

                current_tag = SceneTag.objects.filter(
                  name=actor_tag.name
                ).first()
                actor_tag.scene_tags.add(current_tag)

              if not scene_to_parse.scene_tags.filter(id=current_tag.id):

                if "," in current_tag.exclusions:

                  for excl in current_tag.exclusions.split(","):
                    excl = excl.strip().lower()
                    log.info(f"There is an exclusion: {excl}...")

                    if len(excl) > 2:
                      # TODO: FIXME: Here we generate a regex and then ignore it. Is this an error?
                      regex_search_term = get_regex_search_term(
                        excl, "."
                      )

                      if excl in scene_to_parse.name.lower():
                        exclude = True
                        log.info(f"Not inserting actor tag [{current_tag}] due to an exclusion.")

                        break

                else:
                  excl = current_tag.exclusions.strip().lower()
                  if len(excl) > 2:
                    log.info("One exclusion, longer than 2 chars...")
                    # TODO: FIXME: Here we generate a regex and then ignore it. Is this an error?
                    regex_search_term = get_regex_search_term(
                      excl, "."
                    )
                    if excl in scene_to_parse.name.lower():
                      exclude = True
                      log.info(f"[Excl] [{current_tag}]")

                      break

                # FIXME: I think the nesting is wrong here, does this function work?
                if exclude == False:
                  log.info(f"[{current_tag}]")
                  scene_to_parse.scene_tags.add(current_tag)

  for alias in actors_alias:
    if alias.name.count(" ") > 0 or alias.is_exempt_from_one_word_search:
      ans = string_search_without_regex(alias, scene_path)

      if ans["success"]:
        scene_path = ans["scene_path"]

        actor_in_alias = alias.actors.first()
        log.info(f"{alias.name} is an alias for {actor_in_alias.name}")
        add_actor_to_scene(actor_in_alias, scene_to_parse)

  return scene_path


def add_actor_to_scene(actor_to_add, scene_to_add_to):
  if not scene_to_add_to.actors.filter(pk=actor_to_add.pk):
    log.info(f"Adding Actor: {actor_to_add.name} to the scene {scene_to_add_to.name}")
    scene_to_add_to.actors.add(actor_to_add)
    scene_to_add_to.save()
  else:
    log.info(f"Actor: {actor_to_add.name} is already registered to the scene {scene_to_add_to.name}")


def get_regex_search_term(name, delimiter):
  regex_special_chars = "\+*?[^]$(){}=!<>|:-"
  for char in regex_special_chars:
    if char in name:
      name = name.replace(char, "")
  name_split_list = name.split(delimiter)
  is_first_iteration = True
  regex_search_term = ".{0,1}".join(part_of_name for part_of_name in name_split_list)
  return regex_search_term


def parse_scene_tags_in_scene(scene, scene_path, scene_tags):
  for scene_tag in scene_tags:
    exclude = False
    regex_search_term = get_regex_search_term(scene_tag.name, ".")
    if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
      scene_path = re.sub(regex_search_term, "", scene_path, flags=re.IGNORECASE)
      if not scene.scene_tags.filter(name=scene_tag.name):

        for excl in scene_tag.exclusions.split(","):
          excl = excl.strip().lower()
          if len(excl) > 2:
            # FIXME/TODO: this makes a regex but doesn't use it?
            regex_search_term = get_regex_search_term(excl, ".")
            log.info(f"Testing exclude word: {excl}, scene: {scene.name}")
            if excl in scene.name.lower():
              exclude = True
              log.info(f"Not inserting tag [{scene_tag.name}] due to an exclusion.")
              break

        if exclude == False:
          log.info(f"Adding Tag: {scene_tag.name} to the scene {scene.name}")
          scene.scene_tags.add(scene_tag)

    if scene_tag.scene_tag_alias != "":
      for scene_tag_alias in scene_tag.scene_tag_alias.split(","):
        exclude = False
        scene_tag_alias_stripped = scene_tag_alias.strip()
        regex_search_term = get_regex_search_term(scene_tag_alias_stripped, ".")
        if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
          scene_path = re.sub(regex_search_term, "", scene_path, flags=re.IGNORECASE)
          if not scene.scene_tags.filter(name=scene_tag.name):
            for excl in scene_tag.exclusions.split(","):
              excl = excl.strip().lower()
              if len(excl) > 2:
                # FIXME/TODO: this makes a regex but doesn't use it
                regex_search_term = get_regex_search_term(excl, ".")
                log.info(f"Testing exclude word: {excl}, scene: {scene.name}")
                if excl in scene.name.lower():
                  exclude = True
                  log.info(f"Not inserting tag [{scene_tag.name}] due to an exclusion.")
                  break

            if exclude == False:
              log.info(f"Adding Tag: {scene_tag.name} to the scene {scene.name}")
              scene.scene_tags.add(scene_tag)
  return scene_path


def parse_website_in_scenes(scene, scene_path, websites):
  for website in websites:
    exclude = False
    regex_search_term = get_regex_search_term(website.name, ".")
    if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
      scene_path = re.sub(regex_search_term, "", scene_path, flags=re.IGNORECASE)
      if not scene.websites.filter(name=website.name):
        for excl in website.exclusions.split(","):
          excl = excl.strip().lower()
          if len(excl) > 2:
            # FIXME/TODO: this makes a regex but doesn't use it
            regex_search_term = get_regex_search_term(excl, ".")
            log.info(f"Testing exclude word: {excl}, scene: {scene.name}")
            if excl in scene.name.lower() and not (website.name.lower() in scene.name.lower()):
              exclude = True
              log.info(f"Not registering website [{website}] due to an exclusion.")
              break

        if exclude == False:
          log.info(f"Adding website: {website.name} to the scene {scene.name}")
          scene.websites.add(website)

      if exclude == False and website.scene_tags.count() > 0:
        for scene_tag in website.scene_tags.all():
          if not scene.scene_tags.filter(id=scene_tag.id):
            log.info(f"Adding Scene Tag '{website.name}' to the scene {scene.name}")
            scene.scene_tags.add(scene_tag)
    if website.website_alias != "":
      exclude = False
      for website_alias in website.website_alias.split(","):
        website_alias_stripped = website_alias.strip()
        regex_search_term = get_regex_search_term(website_alias_stripped, ".")

        if re.search(regex_search_term, scene_path, re.IGNORECASE) is not None:
          scene_path = re.sub(regex_search_term, "", scene_path, flags=re.IGNORECASE)
          if not scene.websites.filter(name=website.name):
            for excl in website.exclusions.split(","):
              excl = excl.strip().lower()
              if len(excl) > 2:
                # TODO/FIXME: regex not used etc
                regex_search_term = get_regex_search_term(excl, ".")
                log.info(f"Testing exclude word: {excl}, scene: {scene.name}")
                if excl in scene.name.lower() and not (
                    website_alias_stripped.lower() in scene.name.lower()
                ):
                  exclude = True
                  log.info(f"Not registering website [{website}] due to an exclusion.")
                  break

          if exclude == False:
            log.info(f"Adding website: {website.name} to the scene {scene.name}")
            scene.websites.add(website)

          if exclude == False and website.scene_tags.count() > 0:
            for scene_tag in website.scene_tags.all():
              if not scene.scene_tags.filter(id=scene_tag.id):
                log.info(f"Adding Scene Tag '{website.name}' to the scene {scene.name}")
            scene.scene_tags.add(scene_tag)

  return scene_path

def main():
  parse_all_scenes(False)

if __name__ == "__main__":
  main()
