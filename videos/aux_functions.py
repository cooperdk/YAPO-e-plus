import os
import sys
import pathlib
import yaml
from os import path
import urllib.request
from videos.models import Actor, Scene, ActorTag
#import videos.views
import YAPO.settings as ysettings
import videos.const as constx


def progress (count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '\u2588' * filled_len + '\u2591' * (bar_len - filled_len)

    sys.stdout.write(f"{bar} [{percents}%] ... {suffix}\r                 ")


def progress_end ():
    sys.stdout.flush()


def getMemory ():
    import psutil
    vmem = round(psutil.virtual_memory().total / 1000000000, 0)
    return vmem  # "{:.2}".format(vmem.total/100000000) #shold that be 102400000?


def getCPU ():
    import psutil
    cpufreq = round(psutil.cpu_freq().max / 1000, 1)
    return cpufreq


def getCPUCount ():
    import psutil
    return psutil.cpu_count(logical=False)  # set Logical to true if treads are to be included


def send_piercings_to_actortag (actor):
    piercings = actor.piercings
    if piercings:
        if ("navel" or "belly button" or "bellybutton") in piercings.lower():
            insert_actor_tag(actor, "Pierced navel")
        if "clit" in piercings.lower():
            insert_actor_tag(actor, "Pierced clitoris")
        if ("nipples" or "nipple rings") in piercings.lower():
            insert_actor_tag(actor, "Pierced nipples")
        elif "nipple" in piercings.lower():
            insert_actor_tag(actor, "Pierced single nipple")
        if "septum" in piercings.lower():
            insert_actor_tag(actor, "Pierced septum")
        if "nose" in piercings.lower():
            insert_actor_tag(actor, "Pierced nose")
        if "nostril" in piercings.lower():
            insert_actor_tag(actor, "Pierced nostril")
        if "tongue" in piercings.lower():
            insert_actor_tag(actor, "Pierced tongue")
        if "tragus" in piercings.lower():
            insert_actor_tag(actor, "Pierced tragus")
        if "helix" in piercings.lower():
            insert_actor_tag(actor, "Pierced helix")
        if ("earlobe" or "ear lobe") in piercings.lower():
            insert_actor_tag(actor, "Pierced ear lobe")
        if "lower lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced lower lip")
        if "upper lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced upper lip")
        if "monroe" in piercings.lower():
            insert_actor_tag(actor, "Pierced Monroe")
        if ("dermal" or "surface") in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal")
        if "wrists" in piercings.lower():
            insert_actor_tag(actor, "Pierced wrists")
        elif "wrist" in piercings.lower():
            insert_actor_tag(actor, "Pierced single wrist")
        if "hip" in piercings.lower():
            insert_actor_tag(actor, "Pierced hip")
        elif "hips" in piercings.lower():
            insert_actor_tag(actor, "Pierced hips")
        if "labia" in piercings.lower():
            insert_actor_tag(actor, "Pierced labia")
        if "back dimples" in piercings.lower():
            insert_actor_tag(actor, "Pierced back dimples")
        if ("right brow" or "right eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced right eyebrow")
        elif ("left brow" or "left eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced left eyebrow")
        elif "brow" in piercings.lower():
            insert_actor_tag(actor, "Pierced eyebrow")
        if "ears" in piercings.lower():
            insert_actor_tag(actor, "Pierced ears")
        elif "left ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced left ear")
        elif "right ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced right ear")
        if "chest" in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal on chest")
        if any([piercings.lower() == "none", piercings.lower() == "no piercings", piercings.lower() == "no"]):
            insert_actor_tag(actor, "No piercings")


def insert_actor_tag (actor_to_insert, actor_tag_name):
    actor_tag_name = strip_bad_chars(actor_tag_name)

    if not ActorTag.objects.filter(name=actor_tag_name):
        actor_tag = ActorTag()
        actor_tag.name = actor_tag_name
        actor_tag.save()
        actor_to_insert.actor_tags.add(actor_tag)
    #        print("Added new tag: " + actor_tag_name + " for " + actor_to_insert.name)
    else:
        actor_tag = ActorTag.objects.get(name=actor_tag_name)
        actor_to_insert.actor_tags.add(actor_tag)
        #        print("Added tag: " + actor_tag_name + " for " + actor_to_insert.name)
        actor_tag.save()


def url_is_alive (url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


def strip_bad_chars (name):
    bad_chars = { " " }
    for char in bad_chars:
        if char in name:
            # print("Before: " + name)
            name = name.replace(char, "")
            print(f"Adding Data: {name}")
    return name


def save_actor_profile_image_from_web (image_link, actor, force):
    save_path = os.path.join(
        constx.MEDIA_PATH, "actor", str(actor.id),"profile/"
    )

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_file_name = os.path.join(save_path, "profile.jpg")
    if not os.path.isfile(save_file_name) or force:
        maxretries = 3
        attempt = 0
        while attempt < maxretries:
            try:
                urllib.request.urlretrieve(image_link, save_file_name)
            except http.client.IncompleteRead:
                attempt += 1
                dlerror = 1
            else:
                dlerror = 0
                break

        if dlerror == 0:
            print("Downloaded photo.")
        else:
            print("Download error, you need to try again or insert a photo manually.")

    else:
        print("Skipping, because there's already a usable photo.")
    rel_path = os.path.relpath(save_file_name, start="videos")
    as_uri = urllib.request.pathname2url(rel_path)

    actor.thumbnail = as_uri


def actor_folder_from_name_to_id ():
    actors = Actor.objects.all()

    for actor in actors:
        rel_path = os.path.relpath(
            os.path.join(
                constx.MEDIA_PATH,
                "actor",
                str(actor.id),
                "profile",
                "profile.jpg",
            ),
            start="videos",
        )

        as_uri = urllib.request.pathname2url(rel_path)

        print(
           f"Actor {actor.name} thumb path is: {actor.thumbnail} \n and it should be {as_uri}"
        )
        print(actor.thumbnail != as_uri)
        if (actor.thumbnail != constx.UNKNOWN_PERSON_IMAGE_PATH) and (
                actor.thumbnail != as_uri
        ):
            try:
                os.rename(
                    os.path.join(constx.MEDIA_PATH, "actor", actor.name),
                    os.path.join(constx.MEDIA_PATH, "actor", str(actor.id)),
                )

                print(
                    "Renamed %s to %s"%(
                        os.path.join(constx.MEDIA_PATH, "actor", actor.name),
                        os.path.join(constx.MEDIA_PATH, "actor", str(actor.id)),
                    )
                )
            except FileNotFoundError:

                if os.path.isfile(
                        os.path.join(
                            constx.MEDIA_PATH,
                            "actor",
                            str(actor.id),
                            "profile",
                            "profile.jpg",
                        )
                ):

                    rel_path_changed = os.path.relpath(
                        os.path.join(
                            constx.MEDIA_PATH,
                            "actor",
                            str(actor.id),
                            "profile",
                            "profile.jpg",
                        ),
                        start="videos",
                    )
                    as_uri_changed = urllib.request.pathname2url(rel_path_changed)
                    actor.thumbnail = as_uri_changed
                    actor.save()
                    print(f"Changed {actor.name} thumb in database to {as_uri_changed}")
                else:
                    print("File %s not found!"%(
                            os.path.join(constx.MEDIA_PATH, "actor", actor.name)
                        )
                    )

            rel_path_changed = os.path.relpath(
                os.path.join(
                    constx.MEDIA_PATH,
                    "actor",
                    str(actor.id),
                    "profile",
                    "profile.jpg",
                ),
                start="videos",
            )
            as_uri_changed = urllib.request.pathname2url(rel_path_changed)
            actor.thumbnail = as_uri_changed
            actor.save()

            print(f"Changed {actor.name} thumb in database to {as_uri_changed}")

    return True


if __name__ == "__main__":
    print("this is main")
