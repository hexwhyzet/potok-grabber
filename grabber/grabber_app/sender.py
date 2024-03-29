from json import dumps

import requests

from grabber_app.config import Secrets, Config
from grabber_app.functions import chunks
from grabber_app.models import Profile
from grabber_app.service import extract_all_pictures, extract_profiles, profile_to_dict, picture_to_dict, \
    mark_as_exported

config = Config()
secrets = Secrets()


def create_archive(python_obj):
    json_archive = dumps(python_obj)
    return json_archive


def split_in_chunks(python_obj):
    json_archives = [dumps(x) for x in chunks(python_obj, size=config["chunk_size"])]
    return json_archives


def send_archive_to_server(archive, method):
    url = config["main_server_url"] + "/api/" + str(method)
    params = {"archive": archive}
    result = requests.post(url, data=params)
    return result


def send_all_pictures(exported=False):
    pictures_objects = extract_all_pictures(exported=exported)
    send_pictures(pictures_objects)


def send_all_profiles():
    profile_objects = extract_profiles()
    profiles = list(map(profile_to_dict, profile_objects))
    for chunk_archive in split_in_chunks(profiles):
        try:
            send_archive_to_server(chunk_archive, "send_profiles")
        except Exception as e:
            print(e)


def send_pictures(pictures):
    pictures_dicts = list(map(picture_to_dict, pictures))
    for chunk_archive in split_in_chunks(pictures_dicts):
        try:
            send_archive_to_server(chunk_archive, "send_pictures")
        except Exception as e:
            print(e)
            return
    mark_as_exported(pictures)


def send_profile(profile: Profile):
    profile_dict = profile_to_dict(profile)
    try:
        send_archive_to_server(create_archive([profile_dict]), "send_profiles")
    except Exception as e:
        print(e)


def force_send():
    send_all_profiles()
    send_all_pictures(exported=True)
    send_all_pictures(exported=False)

# def send_profiles():
#     profile_objects = extra
