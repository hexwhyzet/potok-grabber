from json import loads

import requests

from .config import Secrets, Config

secrets = Secrets()
config = Config()

TOKEN = secrets["vk_token"]
VK_URL = config["vk_url"]
API_VERSION = config["vk_api_version"]


def vk_api_request(method, params=None):
    if params is None:
        params = dict()
    params["access_token"] = TOKEN
    params["v"] = API_VERSION
    response = requests.get(f"{VK_URL}/method/{method}", params).text
    json = loads(response)
    return json["response"]



def get_posts(owner_id, count):
    params = {"owner_id": -owner_id, "count": count}
    return vk_api_request("wall.get", params)["items"]


def get_group_by_id(group_id):
    params = {"group_id": group_id}
    return vk_api_request("groups.getById", params)[0]


if __name__ == '__main__':
    pass

    # text = get_posts(102013506, 100)
    # print(text)
    # with open("example_posts.json", "w", encoding="utf8") as file:
    #     file.write(text)
