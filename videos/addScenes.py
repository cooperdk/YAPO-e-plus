import json
import os.path
from videos import ffmpeg_process
import django
from videos import filename_parser
import videos.videosheet as videosheet
from PIL import Image
import videos.scrapers.scanners as scanners

django.setup()

from videos.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

# These should be lower-case.
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

import logging
log = logging.getLogger(__name__)

def get_files(walk_dir, make_video_sample):

    for root, subdirs, files in os.walk(walk_dir):
        if root.startswith("$") or root.startswith(".") or subdirs.startswith("$") or subdirs.startswith("."):
            log.info("Skipping an off-limits path ($ or . as first character in dirname)")
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            filename_extension = os.path.splitext(file_path)[1]
            if filename_extension.lower() in ACCEPTED_VIDEO_EXTENSIONS:
                log.info(f"Filename is {file_path}, extension is {filename_extension}")
                create_scene(file_path, make_video_sample)

def create_sample_video(scene : Scene):
    video_path = scene.get_media_path("sample")
    video_filename_path = os.path.join(video_path, "sample.mp4")

    # Has the sample already been created?
    if os.path.isfile(video_filename_path):
        log.info(f"Sample for {scene.name} already exists!")
        return

    log.info(f"Trying to create a sample video for scene: {scene.name}")
    success = ffmpeg_process.ffmpeg_create_sammple_video(scene)
    if success:
        log.info(f"Sample video for scene: {scene.name} created successfully.")
    else:
        log.info(f"Something went wrong while trying to create video sample for scene: {scene.name}")

def do_ffprobe(scene_in_db):
    log.info("Trying to use ffprobe on scene... ", end="")
    if not ffmpeg_process.ffprobe_get_data_without_save(scene_in_db):
        log.info("ffprobe failed.")
        return False

    scene_in_db.save()
    log.info("OK, taking a screenshot... ", end="")
    ffmpeg_process.ffmpeg_take_scene_screenshot_without_save(scene_in_db)
    log.info("Screenshot taken.")

    return True

def create_sheet_for_scene(scene_in_db : Scene):
    sheet_width = Config().sheet_width
    sheet_grid = Config().sheet_grid
    if sheet_width > 2048:
        sheet_width = 2048
    if sheet_width < 800:
        sheet_width = 800

    sheet_path = scene_in_db.get_media_path("sheet.jpg")
    if os.path.exists(sheet_path):
        log.info("Contact sheet for this scene already exists, not re-generating.")
        return

    file_path = os.path.abspath(scene_in_db.path_to_file)
    log.info(f"Generating Contact Sheet ({sheet_width} px wide, grid: {sheet_grid}... ")

    args = [
        "videosheet",
        file_path,
        "--show-timestamp",
        "--width", str(sheet_width),
        "--grid", sheet_grid,
        "--quality", "75",
        "--timestamp-format", "{H}:{M}:{S}",
        "--template", os.path.abspath(os.path.join(Config().site_path, 'static', 'yapo.template')),
        "--timestamp-border-mode",
        "--timestamp-font-size", "15",
        "--start-delay-percent", "1",
        "--start-delay-percent", "0",
        "--format", "jpg",
        "-o", os.path.abspath(sheet_path),
    ]
    try:
        videosheet.main(args)

        log.info("Contact Sheet saved to %s" % (os.path.abspath(sheet_path)))
    except Exception as e:
        log.error(f"Error creating contact sheet: {e}")

    watermark(os.path.abspath(sheet_path), os.path.join(Config().site_path, 'static', 'yapo-wm.png'))


def create_scene(scene_path, make_sample_video):
    current_scene = Scene()
    current_scene.path_to_file = scene_path
    path_to_dir, filename = os.path.split(scene_path)
    current_scene.name = os.path.splitext(filename)[0]
    # TODO: Insert website abbreviation function call here
    current_scene.path_to_dir = path_to_dir

    # If the scene already exists, use the existing scene.
    # Take a note if we're re-using one, since we'll skip a load of scraping if so.
    if Scene.objects.filter(path_to_file=current_scene.path_to_file):
        log.info("Scene already exists, skipping scene.")
        current_scene = Scene.objects.get(path_to_file=current_scene.path_to_file)
        isPreExistingScene = True
    else:
        isPreExistingScene = False

    if not do_ffprobe(current_scene):
        log.error(f"Failed to probe scene {current_scene.name}, skipping scene...")
        return

    create_sheet_for_scene(current_scene)
    if make_sample_video:
        create_sample_video(current_scene)

    if isPreExistingScene:
        current_scene.save()
        return

    add_scene_to_folder_view(current_scene)

    actors = list(
        Actor.objects.extra(select={"length": "Length(name)"}).order_by("-length")
    )
    actors_alias = list(
        ActorAlias.objects.extra(select={"length": "Length(name)"}).order_by("-length")
    )
    scene_tags = SceneTag.objects.extra(
        select={"length": "Length(name)"}
    ).order_by("-length")
    websites = Website.objects.extra(
        select={"length": "Length(name)"}
    ).order_by("-length")

    # This is the TpDB scanner invoker. Now, YAPO will only slowparse the scene if necessary
    succ = scanners.tpdb(current_scene.id, True) if Config().tpdb_enabled else False
    if succ:
        scene_tags = list(
            SceneTag.objects.extra(select={ "length": "Length(name)" }).order_by("-length")
        )
        log.info("Parsing locally registered scene tags...")
        scene_path = current_scene.path_to_file.lower()
        filename_parser.parse_scene_tags_in_scene(current_scene, scene_path, scene_tags)

        if not Config().tpdb_websites:
            log.info("Parsing locally registered websites...")
            scene_path = filename_parser.parse_website_in_scenes(current_scene, scene_path, websites)

        if not Config().tpdb_actors:
            log.info("Parsing locally registered actors and aliases...")
            scene_path = filename_parser.parse_actors_in_scene(current_scene, scene_path, actors, actors_alias)
    else:
        log.info("Scene was not found on TpDB, parsing it internally...")

    filename_parser.parse_scene_all_metadata(
        current_scene, actors, actors_alias, scene_tags, websites
    )


def add_scene_to_folder_view(scene_to_add):
    path = os.path.normpath(scene_to_add.path_to_dir)

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

    path_with_ids = []
    recursive_add_folders(None, folders, scene_to_add, path_with_ids)


def recursive_add_folders(parent, folders, scene_to_add, path_with_ids):
    if len(folders) != 0:
        if parent is None:
            path_with_ids = []
            if not Folder.objects.filter(name=folders[0]):
                temp = Folder.objects.create(name=folders[0])
                log.info(f"Created virtual folder: {temp.name}")
                parent = Folder.objects.get(name=folders[0])
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()
                path_with_ids.append(
                    {"name": parent.last_folder_name_only, "id": parent.id}
                )
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
                del folders[0]
            else:
                parent = Folder.objects.get(name=folders[0])
                path_with_ids.append(
                    {"name": parent.last_folder_name_only, "id": parent.id}
                )
                if parent.path_with_ids is None:
                    parent.path_with_ids = json.dumps(path_with_ids)
                    parent.save()
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
                log.info(f"Created virtual folder: {parent.name}")
                if parent.last_folder_name_only is None:
                    parent.last_folder_name_only = folders[0]
                parent.save()

            if parent.last_folder_name_only is None:
                parent.last_folder_name_only = folders[0]
                parent.save()
            path_with_ids.append(
                {"name": parent.last_folder_name_only, "id": parent.id}
            )
            if parent.path_with_ids is None:
                parent.path_with_ids = json.dumps(path_with_ids)
                parent.save()
            del folders[0]
            recursive_add_folders(parent, folders, scene_to_add, path_with_ids)
    else:
        if not parent.scenes.filter(name=scene_to_add.name):
            parent.scenes.add(scene_to_add)
            log.info(f"Added Scene: {scene_to_add.name} to virtual folder {parent.name}")
            parent.save()

def write_actors_to_file():
    actors = Actor.objects.all()
    actors_string = ",".join([actor.name for actor in actors])

    with open("actors.txt", "w") as file:
        file.write(actors_string)

def populate_last_folder_name_in_virtual_folders():
    all_folders = Folder.objects.all()
    for folder in all_folders:
        if not folder.last_folder_name_only:
            log.info(f"Folder name is {folder.name}")
            name = os.path.normpath(folder.name)
            only_last = os.path.basename(name)
            if only_last == "":
                only_last = name
            log.info(f"Folder last name is {only_last}")
            folder.last_folder_name_only = only_last
            folder.save()

def watermark(input_image_path, watermark_image_path):
    if not os.path.exists(input_image_path):
        log.warning("Not watermarking, as the image file doesn't exist.")
        return

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
