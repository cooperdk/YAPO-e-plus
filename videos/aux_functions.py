import os
import videos.const as const
import urllib.request


def save_actor_profile_image_from_web(image_link, actor):
    save_path = os.path.join(const.MEDIA_PATH,
                             'actor/' + actor.name + '/profile/')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_file_name = os.path.join(save_path, 'profile.jpg')
    if not os.path.isfile(save_file_name):
        urllib.request.urlretrieve(image_link, save_file_name)

    rel_path = os.path.relpath(save_file_name, start='videos')
    as_uri = urllib.request.pathname2url(rel_path)

    actor.thumbnail = as_uri



if __name__ == "__main__":
    print("this is main")
