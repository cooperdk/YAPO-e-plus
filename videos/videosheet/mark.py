from PIL import Image
import sys, os, pathlib

"""

YAPO Watermarker

Adds a watermark to images (hardcoded to upper-right)

"""


def watermark_with_transparency(input_image_path, watermark_image_path):
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


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("python watermark.py <the_image_name>")
        exit(1)
    the_image = sys.argv[1]
    if the_image is None or len(the_image) == 0:
        print("python watermark.py <the_image_name>")
        exit(1)
    else:
        # print("Watermarking " + the_image + " with " + os.path.dirname(__file__) + "/../static/yapo-wm.png")
        watermark_with_transparency(
            the_image, os.path.dirname(__file__) + "/../static/yapo-wm.png"
        )
