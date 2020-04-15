import json
import os
from videos import ffmpeg_process
import django
from videos import filename_parser
import videos.const as const

django.setup()

from videos.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

ACCEPTED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".flv", ".rm", ".wmv", ".mov", ".m4v", ".mpg", ".mpeg", ".mkv"}
TEST_PATH = "Z:\\XBMC\\PR\\19062016"


def get_files(walk_dir, make_video_sample):
    # norm_path = os.path.normpath(path)
    # files_in_dir = os.listdir(norm_path)

    print('walk_dir = ' + walk_dir)

    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    # walk_dir = os.path.abspath(walk_dir)
    print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

    for root, subdirs, files in os.walk(walk_dir):
        # print('--\nroot = ' + root)
        # list_file_path = os.path.join(root, 'my-directory-list.txt')
        # print('list_file_path = ' + list_file_path)

        # with open(list_file_path, 'wb') as list_file:
        #     for subdir in subdirs:
        #         print('\t- subdirectory ' + subdir)

        for filename in files:
            file_path = os.path.join(root, filename)
            filename_extension = os.path.splitext(file_path)[1]
            for filename_extension_to_test in ACCEPTED_VIDEO_EXTENSIONS:
                if filename_extension_to_test == filename_extension:
                    output_string = "Filename is %s and the extension is %s" % (file_path, filename_extension,)
                    print(output_string.encode('utf-8'))
                    create_scene(file_path, make_video_sample)
                    break


def create_sample_video(scene):
    print("Trying to create a sample video for scene: {}".format(scene.name))
    success = ffmpeg_process.ffmpeg_create_sammple_video(scene)
    if success:
        print("Sample video for scene: {} created successfully.".format(scene.name))
    else:
        print(
            "Something went wrong while trying to create video sample for scene: {}".format(scene.name))


def create_scene(scene_path, make_sample_video):
    current_scene = Scene()
    current_scene.path_to_file = scene_path
    path_to_dir, filename = os.path.split(scene_path)
    current_scene.name = os.path.splitext(filename)[0]
    current_scene.path_to_dir = path_to_dir

    print("Scene Name: %s\nPath to Dir: %s\nPath to File: %s" % (
        current_scene.name, current_scene.path_to_dir, current_scene.path_to_file))

    if Scene.objects.filter(path_to_file=current_scene.path_to_file):
        print("Scene Already Exists!")
        scene_in_db = Scene.objects.get(path_to_file=current_scene.path_to_file)
        if scene_in_db.thumbnail is None:
            print("Trying to use ffprobe on scene: {}".format(scene_in_db.name))
            if ffmpeg_process.ffprobe_get_data_without_save(scene_in_db):
                print(
                    "ffprobe successfully gathered information on scene: {}...\nTaking a screenshot with ffmpeg...".format(
                        scene_in_db.name))

                ffmpeg_process.ffmpeg_take_scene_screenshot_without_save(scene_in_db)

                print("Screenshot of scene {} taken...".format(
                    scene_in_db.name))

        if make_sample_video:
            video_filename_path = os.path.join(const.MEDIA_PATH, 'scenes', str(scene_in_db.id), 'sample',
                                               'sample.mp4')
            if not os.path.isfile(video_filename_path):
                create_sample_video(scene_in_db)
            else:
                print("Sample for {} already exists!".format(scene_in_db.name))

            scene_in_db.save()
    else:
        print("Trying to use ffprobe on scene: {}".format(current_scene.name))
        if ffmpeg_process.ffprobe_get_data_without_save(current_scene):
            current_scene.save()
            print(
                "ffprobe successfully gathered information on scene: {}...\nTaking a screenshot with ffmpeg...".format(
                    current_scene.name))

            ffmpeg_process.ffmpeg_take_scene_screenshot_without_save(current_scene)

            print("Screenshot of scene {} taken...".format(
                current_scene.name))

            if make_sample_video:
                create_sample_video(current_scene)

            add_scene_to_folder_view(current_scene)

            current_scene.save()

            actors = list(Actor.objects.extra(select={'length': 'Length(name)'}).order_by('-length'))
            actors_alias = list(ActorAlias.objects.extra(select={'length': 'Length(name)'}).order_by('-length'))
            scene_tags = SceneTag.objects.extra(select={'length': 'Length(name)'}).order_by('-length')
            websites = Website.objects.extra(select={'length': 'Length(name)'}).order_by('-length')

            filename_parser.parse_scene_all_metadata(current_scene, actors, actors_alias, scene_tags, websites)
        else:
            print("Failed to probe scene {}, skipping scene...".format(current_scene.name))






def add_scene_to_folder_view(scene_to_add):
    # scene_path = os.path.normpath(scene_to_add.path_to_dir)

    path = os.path.normpath(scene_to_add.path_to_dir)

    # drive, path = os.path.splitdrive(scene_path)

    print(path)
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()

    # print (drive)
    is_first = True
    parent = ""
    # for folder in folders:
    #     print (folder)
    path_with_ids = []
    recursive_add_folders(None, folders, scene_to_add, path_with_ids)


def recursive_add_folders(parent, folders, scene_to_add, path_with_ids):
    if len(folders) != 0:
        if parent is None:
            path_with_ids = []
            if not Folder.objects.filter(name=folders[0]):
                temp = Folder.objects.create(name=folders[0])
                print("Created virtual folder: " + temp.name)
                parent = Folder.objects.get(name=folders[0])
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()
                path_with_ids.append({'name': parent.last_folder_name_only,
                                      'id': parent.id})
                # print ("Parent Name is {}, Path with Id's are {}".format(parent.name, path_with_ids.encode('utf-8')))
                #print(json.dumps(path_with_ids))
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
                # print ("Last folder name is : {}".format(folders[0]))
                del folders[0]

            else:
                parent = Folder.objects.get(name=folders[0])
                path_with_ids.append({'name': parent.last_folder_name_only,
                                      'id': parent.id})
                # print ("Parent Name is {}, Path with Id's are {}".format(parent.name, path_with_ids.encode('utf-8')))
                #print(json.dumps(path_with_ids))
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
                # print ("Last folder name is : {}".format(folders[0]))
                del folders[0]

            recursive_add_folders(parent, folders, scene_to_add, path_with_ids)
        else:
            folder_to_add = os.path.join(parent.name, folders[0])
            parent_children = parent.get_children()

            if_in_children = False
            for child in parent_children:
                if child.name == folder_to_add:
                    if_in_children = True
                    parent = child
                    break

            if not if_in_children:
                parent = Folder.objects.create(name=folder_to_add, parent=parent)
                print("Created virtual folder: " + parent.name)
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()

            if parent.last_folder_name_only is None:
                parent.last_folder_name_only = folders[0]
                parent.save()
            path_with_ids.append({'name': parent.last_folder_name_only,
                                  'id': parent.id})
            # print ("Parent Name is {}, Path with Id's are {}".format(parent.name.encode('utf-8'),
            #                                                          path_with_ids))
            #print(json.dumps(path_with_ids))
            if parent.path_with_ids is None:
                parent.path_with_ids = json.dumps(path_with_ids)
                parent.save()
            # print ("Last folder name is : {}".format(folders[0]))
            del folders[0]
            recursive_add_folders(parent, folders, scene_to_add, path_with_ids)
    else:
        if not parent.scenes.filter(name=scene_to_add.name):
            parent.scenes.add(scene_to_add)
            print("Added Scene: " + scene_to_add.name + " to virtual folder " + parent.name)
            parent.save()


# Not implemented correctly
# right now there is no way to clean empty dirs from db.
def clean_empty_folders():
    all_folders = Folder.objects.filter(level=0)

    for folder in all_folders:
        recursive_function(folder)
        print(folder)


def recursive_function(parent, folder):
    print("In folder " + folder.name)
    if folder.get_next_sibling() is not None:
        sibling = folder.get_next_sibling()
        recursive_function(folder, sibling)

    if len(folder.get_children()) != 0:
        children = folder.get_children()
        for child in children:
            recursive_function(folder, child)
    else:
        print("         " + folder.name + " is leaf")
        if folder.scenes.all().count() == 0:
            name = folder.name
            parent.children.filter(pk=folder.id).delete()
            # folder.delete()
            print(name + " didn't have any scenes and was deleted!")


            # siblings = folder.get_siblings()
            # for sibling in siblings:
            #     recursive_function(sibling)


def write_actors_to_file():
    actors = Actor.objects.all()
    actors_string = ""
    for actor in actors:
        actors_string += "," + actor.name

    file = open("actors.txt", "w")

    file.write(actors_string)

    file.close()


def populate_last_folder_name_in_virtual_folders():
    all_folders = Folder.objects.all()
    for folder in all_folders:
        if not folder.last_folder_name_only:
            print("Folder name is" + folder.name)
            name = os.path.normpath(folder.name)
            only_last = os.path.basename(name)
            if only_last == "":
                only_last = name
            print("Folder last name is {}".format(only_last))
            folder.last_folder_name_only = only_last
            folder.save()


def main():
    scenes = Scene.objects.all()
    for scene in scenes:
        add_scene_to_folder_view(scene)

        # populate_last_folder_name_in_virtual_folders()
        #write_actors_to_file()
        #clean_empty_folders()
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

        # get_files(TEST_PATH)
        #find_duplicates()
        # scenes_virtual_folder = Scene.objects.all()
        # for s in scenes_virtual_folder:
        #     add_scene_to_folder_view(s)
        #     # for x in range(1377, 1387):
        #     #     scene = Scene.objects.get(pk=x)
        #     #     add_scene_to_folder_view(scene)
        #     #
        #     #     # scene = Scene.objects.first()


if __name__ == "__main__":
    main()
