from json import dumps

import requests
from django.forms import model_to_dict

from .config import Secrets, Config
from grabber_app.functions import chunks
from grabber_app.service import extract_pictures, extract_profiles

config = Config()
secrets = Secrets()


def create_archive(python_obj):
    json_archive = dumps(python_obj)
    return json_archive


def split_in_chunks(python_obj):
    json_archives = [dumps(x) for x in chunks(python_obj, size=config["chunk_size"])]
    return json_archives


def send_archive_to_server(archive, method):
    url = config["main_server_url"] + "/" + str(method)
    params = {"archive": archive}
    result = requests.post(url, data=params)
    return result


def send_pictures():
    pictures_objects = extract_pictures()
    pictures = list(map(model_to_dict, pictures_objects))
    for chunk_archive in split_in_chunks(pictures):
        try:
            send_archive_to_server(chunk_archive, "send_pictures")
        except Exception as e:
            print(e)


def send_profiles():
    profile_objects = extract_profiles()
    profiles = list(map(model_to_dict, profile_objects))
    for chunk_archive in split_in_chunks(profiles):
        try:
            send_archive_to_server(chunk_archive, "send_profiles")
        except Exception as e:
            print(e)

# def send_profiles():
#     profile_objects = extra
