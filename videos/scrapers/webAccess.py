import datetime
import os
import time
import urllib
from datetime import timedelta
from typing import Dict

import requests

from configuration import Config

import logging
log = logging.getLogger(__name__)

class webAccess:
    requestTimeout: timedelta
    defaultHeaders: Dict[str, str]

    useragent = "YAPO e+ 0.71"

    def __init__(self):
        self.defaultHeaders = {"User-Agent": webAccess.useragent}
        self.requestTimeout = datetime.timedelta(minutes=2)

    def get_with_retry(self, url, headers = [], params = []):
        deadline = datetime.datetime.now() + self.requestTimeout

        headers.extend(self.defaultHeaders)

        while True:
            try:
                response = requests.request('GET', url, headers=headers, params=params)
                response.raise_for_status()
                return response
            except Exception as e:
                if datetime.datetime.now() > deadline:
                    log.exception(f"Exception retrieving {url}: {e} ")

                log.warning(f"Exception retrieving {url}: {e}; will retry.")
                time.sleep(3)

    def download_image(self, image_url : str, output_file_path : str):
        resp = self.get_with_retry(image_url)
        data = resp.read()

        with open(output_file_path, 'wb') as output_file:
            output_file.write(data)

        log.info(f'Image "{image_url}" downloaded to {output_file_path}')

        return True

    def pathname2url(self, path):
        # Chop off the leading site media path
        if path.find(Config().site_media_path) is not 0:
            raise Exception(f"File {path} is not under the media path {Config().site_media_path}")
        path = path[len(Config().site_media_path):]

        # And turn into a URL.
        as_uri = urllib.request.pathname2url(path).strip('/')

        # It'll be under the media directory.
        mediaUrl = Config().site_media_url.strip('/')
        as_uri = "%s/%s" % (mediaUrl, as_uri)

        return as_uri

    # Convert a filename mapping as returned from pathname2url back to a path name.
    def urlpath2pathname(self, url):
        mediaUrl = Config().site_media_url.strip("/\\")
        if url.find(mediaUrl) is not 0:
            raise Exception(f"url {url} is not under the media path {mediaUrl}")
        url = url[len(mediaUrl):]
        url = url.strip('/\\')

        url = os.path.join(Config().site_media_path, url)
        return url

