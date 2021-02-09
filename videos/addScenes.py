import json
import os
import os.path
from videos import ffmpeg_process
import django
from videos import filename_parser
from configuration import Config
import utils.videosheet as videosheet
from PIL import Image
import videos.clients.apiclients as apiclients

django.setup()

from videos.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

ACCEPTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".flv",
    ".rm",
    ".wmv",
    ".mov",
    ".m4v",
    ".mpg",
    ".mpeg",
    ".mkv",
    ".webm"
}

def get_files(walk_dir, make_video_sample):

    for root, subdirs, files in os.walk(walk_dir):

        if not root.startswith("$") or root.startswith("."):

            for filename in files:
                file_path = os.path.join(root, filename)
                filename_extension = os.path.splitext(file_path)[1]
                for filename_extension_to_test in ACCEPTED_VIDEO_EXTENSIONS:
                    if filename_extension_to_test.lower() == filename_extension.lower():
                        print(f"File: {file_path}\n")

                        create_scene(file_path, make_video_sample)
                        print(
                            "\n------------------------------------------------------------------------------\n"
                        )
                        break
        else:
            print("Skipping an off-limits path ($ or . as first character in dirname)")



def create_sample_video(scene):
    # debug
    #print(f"Trying to create a sample video for scene {scene.id}")
    success = ffmpeg_process.ffmpeg_create_sammple_video(scene)
    if success:
        #print(f"Sample video for scene: {scene.name} created successfully.")
        x=x
    else:
        log.info(f"Something went wrong while trying to create video sample for scene: {scene.name}")


def create_scene(scene_path, make_sample_video):
    current_scene = Scene()
    current_scene.path_to_file = scene_path
    path_to_dir, filename = os.path.split(scene_path)
    current_scene.name = os.path.splitext(filename)[0]
    # TODO: Insert website abbreviation function call here
    current_scene.path_to_dir = path_to_dir
    sheet_width = Config().sheet_width
    sheet_grid = Config().sheet_grid
    if sheet_width > 2048:
        sheet_width = 2048
    if sheet_width < 800:
        sheet_width = 800
#    print(
#        "Scene Name: %s\nPath to Dir: %s\nPath to File: %s"
#        % (current_scene.name, current_scene.path_to_dir, current_scene.path_to_file)
#    )

    if Scene.objects.filter(path_to_file=current_scene.path_to_file):
        print("Scene already exists, skipping scene.")
        scene_in_db = Scene.objects.get(path_to_file=current_scene.path_to_file)
        if scene_in_db.thumbnail is None:
            print("Trying to use ffprobe on scene... ",end="")
            if ffmpeg_process.ffprobe_get_data_without_save(scene_in_db):
                print("OK, taking a screenshot... ", end="")

                ffmpeg_process.ffmpeg_take_scene_screenshot_without_save(scene_in_db)

                print("Screenshot taken.")
        sheet_path = os.path.abspath(
            os.path.join(Config().site_media_path, "scenes", str(scene_in_db.id), "sheet.jpg")
        )
        if os.path.exists(sheet_path):
            print("Contact sheet for this scene already exists, not re-generating.")
        else:
            file_path = os.path.abspath(current_scene.path_to_file)
            print(f"Generating Contact Sheet ({sheet_width} px wide, grid: {sheet_grid}... ")
            #               try:

            args = [
                "videosheet",
                file_path,
                "-t",
                "-w",
                str(sheet_width),
                "-g",
                sheet_grid,
                "--quality",
                "75",
                "--timestamp-format",
                "{H}:{M}:{S}",
                "--template",
                os.path.abspath(
                    os.path.join(Config().site_path, 'static', 'yapo.template')
                ),
                "--timestamp-border-mode",
                "--timestamp-font-size",
                "15",
                "--start-delay-percent",
                "1",
                "--start-delay-percent",
                "0",
                "-f",
                "jpg",
                "-o",
                os.path.abspath(sheet_path),
            ]
            try:
                # sys.argv = args
                videosheet.main(args)

                watermark(
                    os.path.abspath(sheet_path), os.path.join(Config().site_path, 'static', 'yapo-wm.png')
                )

                print("Contact Sheet saved to %s" % (os.path.abspath(sheet_path)))
            except:
                print("Error creating contact sheet!")

        if make_sample_video:
            video_filename_path = os.path.join(
                Config().site_media_path, "scenes", str(scene_in_db.id), "sample", "sample.mp4"
            )
            if not os.path.isfile(video_filename_path):
                create_sample_video(scene_in_db)
            else:
                print(f"Sample for {scene_in_db.name} already exists!")

            scene_in_db.save()
        
    else:
        print("Trying to use ffprobe on scene... ", end="")
        if ffmpeg_process.ffprobe_get_data_without_save(current_scene):
            current_scene.save()
            print("Taking a screenshot...", end="")

            ffmpeg_process.ffmpeg_take_scene_screenshot_without_save(current_scene)

            print("Screenshot taken.")


            sheet_path = os.path.abspath(
                os.path.join(Config().site_media_path, "scenes", str(current_scene.id), "sheet.jpg")
            )
            if os.path.exists(sheet_path):
                print("Contact sheet for this scene already exists, not re-generating.")
            else:  
                file_path = os.path.abspath(current_scene.path_to_file)
                print(f"Generating Contact Sheet ({sheet_width} px wide, grid: {sheet_grid})... ")
 #               try:


                args = [
                        "videosheet",
                        file_path,
                        "-t",
                        "-w",
                        str(sheet_width),
                        "-g",
                        sheet_grid,
                        "--quality",
                        "75",
                        "--timestamp-format",
                        "{H}:{M}:{S}",
                        "--template",
                        os.path.abspath(
                            os.path.join(Config().site_path, 'static', 'yapo.template')
                        ),
                        "--timestamp-border-mode",
                        "--timestamp-font-size",
                        "15",
                        "--start-delay-percent",
                        "1",
                        "--start-delay-percent",
                        "0",
                        "-f",
                        "jpg",
                        "-o",
                        os.path.abspath(sheet_path),
                    ]

                try:
                    #sys.argv = args
                    videosheet.main(args)

                    watermark(
                        os.path.abspath(sheet_path), os.path.join(Config().site_path, 'static', 'yapo-wm.png')
                    )


                    print("Contact Sheet saved to %s"%(os.path.abspath(sheet_path)))
                except:
                    print("Error creating contact sheet!")



            if make_sample_video:
                create_sample_video(current_scene)

            add_scene_to_folder_view(current_scene)

            current_scene.save()

            actors = list(
                Actor.objects.extra(select={"length": "Length(name)"}).order_by(
                    "-length"
                )
            )
            actors_alias = list(
                ActorAlias.objects.extra(select={"length": "Length(name)"}).order_by(
                    "-length"
                )
            )
            scene_tags = SceneTag.objects.extra(
                select={"length": "Length(name)"}
            ).order_by("-length")
            websites = Website.objects.extra(
                select={"length": "Length(name)"}
            ).order_by("-length")

            # This is the TpDB scanner invoker. Now, YAPO will only slowparse the scene if necessary
            success_tpdb = False
            filename_parser.scenehash(current_scene)
            if Config().tpdb_enabled:
                success_tpdb = apiclients.tpdb(current_scene.id, True)
                scene_tags = list(
                    SceneTag.objects.extra(select={ "length": "Length(name)" }).order_by("-length")
                )
                print("Parsing locally registered scene tags...")
                scene_path = current_scene.path_to_file.lower()
                filename_parser.parse_scene_tags_in_scene(current_scene, scene_path, scene_tags)

                if not Config().tpdb_websites:
                    print("Parsing locally registered websites...")
                    scene_path = parse_website_in_scenes(scene, scene_path, websites)

                if not Config().tpdb_actors:
                    print("Parsing locally registered actors and aliases...")
                    scene_path = parse_actors_in_scene(scene, scene_path, actors, actors_alias)

                if not success_tpdb:
                    print("The scene was not found on TpDB, parsing it internally...")
                    filename_parser.parse_scene_all_metadata(
                        current_scene, actors, actors_alias, scene_tags, websites
                    )
            else:
                print("The TpDB API client is turned off, parsing the scene internally...")
                filename_parser.parse_scene_all_metadata(
                    current_scene, actors, actors_alias, scene_tags, websites
                )
        else:
            print(f"Failed to probe scene {current_scene.name}, skipping scene...")


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
                print(f"Created virtual folder: {temp.name}")
                parent = Folder.objects.get(name=folders[0])
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()
                path_with_ids.append(
                    {"name": parent.last_folder_name_only, "id": parent.id}
                )
                # print ("Parent Name is {}, Path with Id's are {}".format(parent.name, path_with_ids.encode('utf-8')))
                # print(json.dumps(path_with_ids))
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
                # print ("Last folder name is : {}".format(folders[0]))
                del folders[0]

            else:
                parent = Folder.objects.get(name=folders[0])
                path_with_ids.append(
                    {"name": parent.last_folder_name_only, "id": parent.id}
                )
                # print ("Parent Name is {}, Path with Id's are {}".format(parent.name, path_with_ids.encode('utf-8')))
                # print(json.dumps(path_with_ids))
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
                print(f"Created virtual folder: {parent.name}")
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()

            if parent.last_folder_name_only is None:
                parent.last_folder_name_only = folders[0]
                parent.save()
            path_with_ids.append(
                {"name": parent.last_folder_name_only, "id": parent.id}
            )
            # print ("Parent Name is {}, Path with Id's are {}".format(parent.name.encode('utf-8'),
            #                                                          path_with_ids))
            # print(json.dumps(path_with_ids))
            if parent.path_with_ids is None:
                parent.path_with_ids = json.dumps(path_with_ids)
                parent.save()
            # print ("Last folder name is : {}".format(folders[0]))
            del folders[0]
            recursive_add_folders(parent, folders, scene_to_add, path_with_ids)
    else:
        if not parent.scenes.filter(name=scene_to_add.name):
            parent.scenes.add(scene_to_add)
            print(
                f"Added Scene: {scene_to_add.name} to virtual folder {parent.name}"
            )
            parent.save()


# Not implemented correctly
# right now there is no way to clean empty dirs from db.
def clean_empty_folders():
    all_folders = Folder.objects.filter(level=0)

    for folder in all_folders:
        recursive_function(folder)
        print(folder)


def recursive_function(parent, folder):
    print(f"In folder {folder.name}")
    if folder.get_next_sibling() is not None:
        sibling = folder.get_next_sibling()
        recursive_function(folder, sibling)

    if len(folder.get_children()) != 0:
        children = folder.get_children()
        for child in children:
            recursive_function(folder, child)
    else:
        print(f"         {folder.name} is leaf")
        if folder.scenes.all().count() == 0:
            name = folder.name
            parent.children.filter(pk=folder.id).delete()
            # folder.delete()
            print(f"{name} didn't have any scenes and was deleted!")

            # siblings = folder.get_siblings()
            # for sibling in siblings:
            #     recursive_function(sibling)


def write_actors_to_file():
    actors = Actor.objects.all()
    actors_string = ",".join(actor.name for actor in actors)

    file = open("actors.txt", "w")

    file.write(actors_string)

    file.close()


def populate_last_folder_name_in_virtual_folders():
    all_folders = Folder.objects.all()
    for folder in all_folders:
        if not folder.last_folder_name_only:
            print(f"Folder name is {folder.name}")
            name = os.path.normpath(folder.name)
            only_last = os.path.basename(name)
            if only_last == "":
                only_last = name
            print(f"Folder last name is {only_last}")
            folder.last_folder_name_only = only_last
            folder.save()

def watermark(input_image_path, watermark_image_path):
    if os.path.exists(input_image_path):
        base_image = Image.open(input_image_path).convert(
            "RGBA"
        )  # convert to RGBA is important
        watermark = Image.open(watermark_image_path).convert("RGBA")
        width, height = base_image.size
        mark_width, mark_height = watermark.size
        position = (width - mark_width - 32, 28)  # (height-mark_height-32 for lower-right)
        transparent = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        transparent.paste(watermark, position, mask=watermark)
        # transparent.show()
        transparent = transparent.convert("RGB")
        transparent.save(input_image_path)
    else:
        print("Not watermarking, as the image file doesn't exist.")
def main():
    scenes = Scene.objects.all()
    for scene in scenes:
        add_scene_to_folder_view(scene)

        # populate_last_folder_name_in_virtual_folders()
        # write_actors_to_file()
        # clean_empty_folders()
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

        # get_files(TEST_PATH)
        # find_duplicates()
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
