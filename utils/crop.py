import json, sys, path
from utils import smartcrop
from PIL import Image


def crop(path: str):
'''
crop handles the calls to the smartcrop module
the hardcoded value "basewidth" defines the width of the output image.
Any image provided will be scaled up or down in width to this resolution and then smartcropped.

Args: (str) full path

Output: (bool) True or False
'''

    try:
        image = Image.open(path)
        output_dir = os.path.dirname(os.path.abspath(image))
        output_name = os.path.splitext(image)[0]
        output_ext = os.path.splitext(image)[1]
        output = os.path.abspath(os.path.join(output_dir, output_name + "_banner" + output_ext)
        width, height = img.size[:2]

        basewidth = 1280
        if width < basewidth:
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            image = image.resize((basewidth,hsize), Image.ANTIALIAS)

        sc = smartcrop.SmartCrop()
        result = sc.crop(image, width=x, height=y)
        print(json.dumps(result, indent=2))

        cropped_image = image.crop(box)
        cropped_image.thumbnail((options.width, options.height), Image.ANTIALIAS)
        cropped_image.save(output, 'JPEG', quality=90)
        return true
    except Exception as e:
        log.error(f'PIL: {e}')
        return false