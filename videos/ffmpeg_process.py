import glob
import os
import sys
import platform

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

import shutil
import subprocess
import time

import stat
import django
import json
import re
import urllib.request as urllib
from configuration import Config
django.setup()

from videos.models import Scene


if platform.system() == "Linux" or platform.system() == "Darwin":
    # Linux or OS X
    FFPROBE_BIN = "ffprobe"
    FFMPEG_BIN = "ffmpeg"
elif platform.system() == "Windows":
    # Windows
    FFPROBE_BIN = os.path.join("videos", "ffmpeg", "ffprobe")
    FFMPEG_BIN = os.path.join("videos", "ffmpeg", "ffmpeg")

if not os.path.exists(Config().temp_path):
    os.makedirs(Config().temp_path)

if not os.path.exists(Config().site_media_path):
    os.makedirs(Config().site_media_path)

FFMPEG_TEMP_OUTPUT_IMAGES = os.path.join(Config().temp_path, "img%03d.jpg")
OUTPUT_VIDEO_FRAMERATE = 15
OUTPUT_VIDEO_NAME = os.path.join(Config().temp_path, "out.mp4")
FFPROBE_JSON_ARGUMENTS = "-v quiet -print_format json -show_format -show_streams"
FFMPEG_SCREENSHOT_ARGUMENTS = (
    '-vf "thumbnail,scale=1280:720,pad=ih*16/9:ih:(ow-iw)/2:(oh-ih)/2" -frames:v 1'
)
DEFAULT_SCREENSHOT_TIME = "00:01:30"
SCREENSHOT_OUTPUT_PATH = os.path.join(Config().temp_path, "thumb.jpg")
SAMPLE_RESOLUTION = "640:360"




def execute_subprocess(command_call, type_of_bin,):
    """Function to execute a process like FFMPEG.

    Args:
        command_call (str): A string containing the executable to call
        type_of_bin (str): Unused

    Returns:
        ans: response data
    """

    command_call = command_call

    p = subprocess.Popen(
        command_call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )

    # p.wait()

    # result = subprocess.Popen(command_call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    a = p.communicate()
    # print(p.returncode)
    # print (a[0])

    # print(a[0])

    ans = {}
    if p.returncode == 0:
        ans["success"] = True
        if type_of_bin == "ffprobe":
            ans["response"] = json.loads(a[0].decode())

    else:
        ans["success"] = False

    if b"Output file is empty, nothing was encoded" in a[0]:
        ans["success"] = False

    return ans


def ffmpeg_take_screenshot(screenshot_time, filename):
    """Generate a screenshot of a scene.

    Args:
        screenshot_time: The time in the video that a screenshot should be
            taken.
        filename: The path to the file to generate a screenshot for.
    """
    command_call = '{} -y -ss {} -i "{}" {} {}'.format(
        FFMPEG_BIN,
        screenshot_time,
        filename,
        FFMPEG_SCREENSHOT_ARGUMENTS,
        SCREENSHOT_OUTPUT_PATH,
    )

#    print("Taking screenshot of video...")  # (command_call)

    return execute_subprocess(command_call, "ffmpeg")


def ffprobe(filename):
    """
    Args:
        filename:
    """
    command_call = '{} {} "{}"'.format(FFPROBE_BIN, FFPROBE_JSON_ARGUMENTS, filename)
    # print("Calling ffprobe...")# command call: {}".format(command_call))

    return execute_subprocess(command_call, "ffprobe")


def get_length(filename):
    # result = subprocess.Popen([FFPROBE_BIN, filename],
    #                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    """
    Args:
        filename:
    """
    command_call = '{} "{}"'.format(FFPROBE_BIN, filename)
#    print("Getting video length...")  # (command_call)

    result = subprocess.Popen(
        command_call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )
    a = result.communicate()
#    print("Video is " + result.returncode + " in length")

    # print(a[0])

    if result.returncode == 0:
        ans = a[0]
    else:
        ans = -1

    return ans


# ffmpeg -i input.flv -vf fps=1 out%d.png
def make_screenshots(fps_of_screenshots, filename):
    """
    Args:
        fps_of_screenshots:
        filename:
    """
    input_argument = '-i "{}"'.format(filename)
    video_filters = "-q:v 4 -vf fps={},scale=640:-2".format(fps_of_screenshots)

    print("Taking screenshots...")
    # print("{} {} {} {}".format(FFMPEG_BIN, input_argument, video_filters, FFMPEG_TEMP_OUTPUT_IMAGES))


# ffmpeg -framerate 1/5 -i img%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4


def make_video_from_screenshots(framerate):
    """
    Args:
        framerate:
    """
    framerate_argument = "-framerate {}".format(framerate)
    input_argument = "-i {}".format(FFMPEG_TEMP_OUTPUT_IMAGES)
    other_arguments = "-q:v 4 -c:v libx264 -pix_fmt yuv420p -preset ultrafast"
    output_video = OUTPUT_VIDEO_NAME
    command_call = "{} {} {} {} {}".format(
        FFMPEG_BIN, framerate_argument, input_argument, other_arguments, output_video
    )
    print(
        "Making video from frames..."
    )  # using ffmpeg command: \n{}".format(command_call))
    execute_subprocess(command_call, "ffmpeg")
    # p = subprocess.Popen(command_call, shell=True)
    # p.wait()


def seconds_to_string(seconds):
    """
    Args:
        seconds:
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "{0:0>2}:{1:0>2}:{2:0>2}".format(int(h), int(m), int(s))


def time_markers(
    total_seconds,
    first_segment_seconds_from_begining,
    last_segment_seconds_from_end,
    number_of_parts,
):
    """
    Args:
        total_seconds:
        first_segment_seconds_from_begining:
        last_segment_seconds_from_end:
        number_of_parts:
    """
    mark_time_dict = {0: seconds_to_string(first_segment_seconds_from_begining)}
    part_marker = (total_seconds - 2) / number_of_parts

    is_short_scene = part_marker < first_segment_seconds_from_begining

    marker = 0
    counter = 0
    for x in range(0, number_of_parts):
        if counter == 0 or counter == (number_of_parts - 1):
            counter += 1
        else:

            if is_short_scene:
                while marker < first_segment_seconds_from_begining:
                    marker += part_marker
                else:
                    marker += part_marker
                    is_short_scene = False

            else:
                marker += part_marker

            mark_time_dict[counter] = seconds_to_string(marker)
            counter += 1

    last_mark = (total_seconds - 2) - last_segment_seconds_from_end
    mark_time_dict[number_of_parts] = seconds_to_string(last_mark)

    return mark_time_dict


def make_sample_video(
    filename,
    video_total_seconds,
    sample_video_length_in_seconds,
    number_of_segments,
    input_fps,
    first_segment_start_in_seconds,
    last_segment_seconds_from_end,
):
    # if int(scene_resolution_width) < int(default_width_pixels):
    # default_width_pixels = scene_resolution_width
    """
    Args:
        filename:
        video_total_seconds:
        sample_video_length_in_seconds:
        number_of_segments:
        input_fps:
        first_segment_start_in_seconds:
        last_segment_seconds_from_end:
    """
    seconds_per_segment = sample_video_length_in_seconds / number_of_segments

    frames_per_segment = float(input_fps) * seconds_per_segment

    frames_per_segment = int(frames_per_segment)
    segments_start_timestamp = time_markers(
        video_total_seconds,
        first_segment_start_in_seconds,
        last_segment_seconds_from_end,
        number_of_segments,
    )
    success = False
    start_number = 000

    for key, seek_time in segments_start_timestamp.items():
        # print(seek_time)
        output = extract_frames_in_given_time(
            filename, seek_time, frames_per_segment, start_number,
        )
        if output == -1:
            return success
        start_number += frames_per_segment

    success = True

    return success


def extract_frames_in_given_time(filename, seek_time, frames_per_segment, start_number):
    """
    Args:
        filename:
        seek_time:
        frames_per_segment:
        start_number:
    """
    seek_argument = "-ss {}".format(seek_time)
    input_argument = '-i "{}"'.format(filename)
    number_of_frames_argument = "-vframes {}".format(frames_per_segment)
    # scale_argument = "-q:v 1 -vf scale={}:trunc(ow/a/2)*2".format(image_width_pixels)

    # scales images to a fixed 16:9 size and adds black bars
    scale_argument = '-q:v 4 -vf "scale={},pad=ih*16/9:ih:(ow-iw)/2:(oh-ih)/2"'.format(
        SAMPLE_RESOLUTION
    )
    start_number_argument = "-start_number {}".format(start_number)

    command_call = "{} {} {} {} {} {} {}".format(
        FFMPEG_BIN,
        seek_argument,
        input_argument,
        number_of_frames_argument,
        scale_argument,
        start_number_argument,
        FFMPEG_TEMP_OUTPUT_IMAGES,
    )
    print(
        "Extracting frames from scene..."
    )  # using ffmpeg command: \n{}".format(command_call))

    p = subprocess.Popen(
        command_call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )
    a = p.communicate()
    # print(p.returncode)

    # print(a[0])

    output = a[0]

    if p.returncode == 0:
        ans = a[0]
    else:
        ans = -1
        print("Something went wrong while extracting video frames, exiting function...")
        print("This is the output of the error: {}".format(a[0]))

    if b"Output file is empty, nothing was encoded" in output:
        ans = -1

    return ans


def move_sample_movie_to_correct_dir(
    scene, success, dest_filename, dest_path, org_path, type_of_media
):
    """
    Args:
        scene:
        success:
        dest_filename:
        dest_path:
        org_path:
        type_of_media:
    """
    if success:

        save_path = os.path.normpath(dest_path)
        filename = dest_filename

        original_path = os.path.normpath(org_path)
        destination_path = os.path.join(save_path, filename)

        if os.path.isdir(save_path):
            shutil.move(original_path, destination_path)
        else:
            os.makedirs(save_path)
            shutil.move(original_path, destination_path)

        if type_of_media == "video":
            delete_temp_files()

        return destination_path
    else:
        delete_sucess = False
        for x in range(1, 5):
            try:
                delete_temp_files()
                delete_sucess = True
                break
            except OSError as e:

                print(e.message)
                time.sleep(5)

        if not delete_sucess:
            delete_temp_files()


def delete_temp_files():
    """Function to remove any temporary files

    :parameter None

    Nothing :return: None
    """
    files = glob.glob(os.path.join(Config().temp_path, "*"))
    for f in files:
        os.remove(f)


def parse_ffprobe_data(ffprobe_json_output):
    """
    Args:
        ffprobe_json_output:
    """
    ans = dict()

    ans["bitrate"] = int(ffprobe_json_output["format"]["bit_rate"])

    ans["duration"] = int(round(float(ffprobe_json_output["format"]["duration"])))

    ans["size"] = int(ffprobe_json_output["format"]["size"])

    for st in ffprobe_json_output["streams"]:
        if st["codec_type"] == "video":
            ans["width"] = int((st["width"]))
            ans["height"] = int(st["height"])
            ans["codec"] = str(st["codec_name"])

            temp = st["avg_frame_rate"]

            m = re.match("(\d+)/(\d+)", temp)
            framerate_numerator = int(m.group(1))
            framerate_denominator = int(m.group(2))

            try:
                ans["framerate"] = round(framerate_numerator / framerate_denominator)
            except ZeroDivisionError:
                print(
                    "Average framerate in JSON is "
                    + temp
                    + " could not divide by zero!"
                )
                ans["framerate"] = 0

    return ans


def ffmpeg_take_scene_screenshot_without_save(scene):
    # When we get here we assume that the scene was alrady probed with ffprobe, therefore it has all the video metadata.

    # {10 /x + y  = 1} , {7200 / x + y = 300} where 10 and 7200 are the duration of the original video
    # and 1 and 300 are the time in seconds where we should take the screen shot.
    # EX if the video is 45 second long the screenshot will be taken on the 2nd second
    # if the video duration is half an hour the screenshot will be taken at 74 seconds
    # x=24.0468 y=0.584145

    """
    Args:
        scene:
    """
    x = 3.0468  ## was 24!
    y = 0.584145

    screenshot_time = seconds_to_string(int(scene.duration / x + y))

    a = ffmpeg_take_screenshot(screenshot_time, scene.path_to_file)

    if a["success"]:
        print("Screenshot Taken")
        dest_path = os.path.join(Config().site_media_path, "scenes", str(scene.id), "thumb")
        z = move_sample_movie_to_correct_dir(
            scene, True, "thumb.jpg", dest_path, SCREENSHOT_OUTPUT_PATH, "image"
        )
        time.sleep(1)
        thumb_path = os.path.relpath(z, start="data")
        as_uri = urllib.pathname2url(thumb_path)
        scene.thumbnail = as_uri


def ffprobe_get_data_without_save(scene):
    """
    Args:
        scene:
    """
    ans = False
    ffprobe_json_output = ffprobe(scene.path_to_file)

    if ffprobe_json_output["success"]:
        try:
            parsed_ffprobe_data = parse_ffprobe_data(ffprobe_json_output["response"])

            if "framerate" in parsed_ffprobe_data:
                scene.framerate = parsed_ffprobe_data["framerate"]
            else:
                scene.framerate = 0

            if "bitrate" in parsed_ffprobe_data:
                scene.bit_rate = parsed_ffprobe_data["bitrate"]
            else:
                scene.bit_rate = 0

            if "size" in parsed_ffprobe_data:
                scene.size = parsed_ffprobe_data["size"]
            else:
                scene.size = 0

            if "codec" in parsed_ffprobe_data:
                scene.codec_name = parsed_ffprobe_data["codec"]
            else:
                scene.codec_name = "N/A"

            if "height" in parsed_ffprobe_data:
                scene.height = parsed_ffprobe_data["height"]
            else:
                scene.height = 0

            if "width" in parsed_ffprobe_data:
                scene.width = parsed_ffprobe_data["width"]
            else:
                scene.width = 0

            if "duration" in parsed_ffprobe_data:
                scene.duration = parsed_ffprobe_data["duration"]
            else:
                scene.duration = 0
        except KeyError:
            print("Well Fuck! ffprobe didn't find the needed info in the file...")
            ans = False
            return ans

        ans = True
    return ans


def ffmpeg_create_sammple_video(scene):
    """
    Args:
        scene:
    """
    filename = scene.path_to_file
    video_total_seconds = scene.duration

    if video_total_seconds is not None:

        # 600 seconds = 10 min, 7200 sec = 2 hours.
        # sample length between 30 sec and 2 minutes
        # number of segments between 12 sec and 30 minutes

        # {10 /x + y  = 5} , {7200 / x + y = 120} where 10 and 7200 are the max and min second duration of the video
        # and  5 and 120 are the duration of the output sample video
        # x = 62.52 y = 4.84

        x = 62.52
        y = 4.84
        sample_video_length_in_seconds = (video_total_seconds / x) + y

        if sample_video_length_in_seconds < 3:
            sample_video_length_in_seconds = 3
        elif sample_video_length_in_seconds > 120:
            sample_video_length_in_seconds = 120

        # {10 /x + y  = 3} , {7200 / x + y = 30} where 10 and 7200 are the max and min second duration of the video
        # and 3 and 30 are the max and min segments of the video
        # x = 266.296 y = 2.96

        x = 266.296
        y = 2.96
        number_of_segments = int((video_total_seconds / x) + y)

        if number_of_segments < 1:
            number_of_segments = 1
        elif number_of_segments > 30:
            number_of_segments = 30

        # {10 /x + y  = 1} , {7200 / x + y = 300} where 10 and 7200 are the max and min second duration of the video
        # and 1 and 300 are the max and min time we should skip from the begining of the video before we capture the first
        # segment (and from the end before we capture the last one)
        # x=24.0468, y=0.584145

        x = 24.0468
        y = 0.584145
        time_from_edges = int((video_total_seconds / x) + y)
        if time_from_edges < 0:
            time_from_edges = 0

        input_fps = scene.framerate
        first_segment_start_in_seconds = time_from_edges
        last_segment_seconds_from_end = time_from_edges
        # default_width_pixels = 640
        # scene_resolution_width = scene.width

        success = make_sample_video(
            filename,
            video_total_seconds,
            sample_video_length_in_seconds,
            number_of_segments,
            input_fps,
            first_segment_start_in_seconds,
            last_segment_seconds_from_end,
        )

        if success:
            time.sleep(5)
            make_video_from_screenshots(scene.framerate)
            time.sleep(5)

            dest_path = os.path.join(Config().site_media_path, "scenes", str(scene.id), "sample")
            move_sample_movie_to_correct_dir(
                scene,
                success,
                "sample.mp4",
                dest_path,
                os.path.join(Config().temp_path, "out.mp4"),
                "video",
            )

        return success

    else:
        success = False
        return success


def main():
    """Calls functions to probe scenes for metadata and generate a screenshot"""
    
    scenes = Scene.objects.all()
    counter = 0
    for scene in scenes:
        if scene.id > 9410:
            path = scene.path_to_file.encode("utf-8")
            ffprobe_json_output = ffprobe(path)
            if ffprobe_json_output["success"]:
                try:
                    parsed_ffprobe_data = parse_ffprobe_data(
                        ffprobe_json_output["response"]
                    )
                except KeyError:
                    print(
                        "Well Fuck! ffprobe didn't find the needed info in the file..."
                    )
                    continue

                print(scene.name)
                for key, y in parsed_ffprobe_data.items():
                    print(key + ": " + str(y))

                scene.framerate = parsed_ffprobe_data["framerate"]
                scene.bit_rate = parsed_ffprobe_data["bitrate"]
                scene.size = parsed_ffprobe_data["size"]
                scene.codec_name = parsed_ffprobe_data["codec"]
                scene.height = parsed_ffprobe_data["height"]
                scene.width = parsed_ffprobe_data["width"]
                scene.duration = parsed_ffprobe_data["duration"]

                ffmpeg_take_scene_screenshot_without_save(scene)

                scene.save()
        else:
            print("Scene {} was already processed".format(scene.name.encode("utf-8")))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YAPO.settings")

    main()