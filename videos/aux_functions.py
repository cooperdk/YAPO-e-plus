import os
import videos.const
import urllib.request
from videos.models import Actor


def save_actor_profile_image_from_web(image_link, actor, force):
    save_path = os.path.join(videos.const.MEDIA_PATH,
                             'actor/' + str(actor.id) + '/profile/')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_file_name = os.path.join(save_path, 'profile.jpg')
    if not os.path.isfile(save_file_name) or force:
        urllib.request.urlretrieve(image_link, save_file_name)

    rel_path = os.path.relpath(save_file_name, start='videos')
    as_uri = urllib.request.pathname2url(rel_path)

    actor.thumbnail = as_uri


def actor_folder_from_name_to_id():
    actors = Actor.objects.all()

    for actor in actors:
        rel_path = os.path.relpath(
            os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor.id), 'profile', 'profile.jpg'), start='videos')

        as_uri = urllib.request.pathname2url(rel_path)

        print("Actor {} thumb path is: {} \n and it should be {}".format(actor.name, actor.thumbnail, as_uri))
        print(actor.thumbnail != as_uri)
        if (actor.thumbnail != videos.const.UNKNOWN_PERSON_IMAGE_PATH) and \
                (actor.thumbnail != as_uri):
            try:
                os.rename(os.path.join(videos.const.MEDIA_PATH, 'actor', actor.name),
                          os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor.id)))

                print("Renamed {} to {}".format(os.path.join(videos.const.MEDIA_PATH, 'actor', actor.name),
                                                os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor.id))))
            except FileNotFoundError:

                if os.path.isfile(
                        os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor.id), 'profile', 'profile.jpg')):

                    rel_path_changed = os.path.relpath(
                        os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor.id), 'profile', 'profile.jpg'),
                        start='videos')
                    as_uri_changed = urllib.request.pathname2url(rel_path_changed)
                    actor.thumbnail = as_uri_changed
                    actor.save()
                    print("Changed {} thumb in database to {}".format(actor.name, as_uri_changed))
                else:
                    print("File {} not found!".format(os.path.join(videos.const.MEDIA_PATH, 'actor', actor.name)))

            rel_path_changed = os.path.relpath(
                os.path.join(videos.const.MEDIA_PATH, 'actor', str(actor.id), 'profile', 'profile.jpg'), start='videos')
            as_uri_changed = urllib.request.pathname2url(rel_path_changed)
            actor.thumbnail = as_uri_changed
            actor.save()

            print("Changed {} thumb in database to {}".format(actor.name, as_uri_changed))

    return True


if __name__ == "__main__":
    print("this is main")
