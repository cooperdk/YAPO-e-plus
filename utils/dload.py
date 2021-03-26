import os, sys, time
import re
from contextlib import closing
from shutil import copyfileobj
import urllib.request as request
import zipfile
from urllib.parse import urlparse
import requests

def save(url, path="", overwrite=False):
    """
    Download and save a remote file
    :param url: str - file url to download
    :param path: str - (optional) Full path to save the file, ex: c:/test.txt or /home/test.txt.
    Defaults to script location and url filename
    :param overwrite: bool - (optional)  If True the local file will be overwritten, False will skip the download
    :return: str - The full path of the downloaded file or an empty string
    """

    try:
        if getattr(sys, 'frozen', False):
            # frozen
            c_path = os.path.dirname(sys.executable)
        else:
            # unfrozen
            c_path = os.path.dirname(os.path.realpath(__file__))

        #namespace = sys._getframe(1).f_globals  # caller's globals
        #c_path = os.path.dirname(namespace['__file__'])
        fn = os.path.basename(urlparse(url).path)
        fn = fn if fn else f"dload{rand_fn()}"
        path = path if path.strip() else c_path+os.path.sep+fn
        if not overwrite and os.path.isfile(path):
            return path
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
        return path
    except:
        pass
    return ""


def save_unzip(zip_url, extract_path="", delete_after=False):
    """
    Save and Extract a remote zip
    :param zip_url: str - the zip file url to download
    :param extract_path: str - (optional) the path to extract the zip file, defaults to local dir
    :param delete_after: bool - (optional) if the zip file should be deleted after, defaults to False
    :return: str - the extract path or an empty string
    """
    try:
        if getattr(sys, 'frozen', False):
            # frozen
            c_path = os.path.dirname(sys.executable)
        else:
            # unfrozen
            c_path = os.path.dirname(os.path.realpath(__file__))
        #namespace = sys._getframe(1).f_globals  # caller's globals
        #c_path = os.path.dirname(namespace['__file__'])
        fn = os.path.basename(urlparse(zip_url).path)
        fn = fn if fn.strip() else f"dload{rand_fn()}"
        zip_path = save(zip_url, f"{c_path}/{fn}")
        folder = os.path.splitext(fn)[0]
        extract_path = extract_path if extract_path.strip() else c_path+os.path.sep+folder
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        if delete_after and os.path.isfile(zip_path):
            os.remove(zip_path)
        return extract_path
    except:
        pass
    return ""

