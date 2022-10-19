from json import loads

import requests

if __name__ == '__main__':
    from config import Secrets, Config
else:
    from grabber_reddit.config import Secrets, Config

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
    try:
        return json["response"]
    except:
        print(json)


def get_posts(owner_id, count):
    params = {"owner_id": -owner_id, "count": count}
    return vk_api_request("wall.get", params)["items"]


def get_group_by_id(group_id):
    params = {"group_id": group_id, "fields": ["photo_max_orig"]}
    return vk_api_request("groups.getById", params)[0]


if __name__ == '__main__':
    text = get_group_by_id(187042498)
    print(text)
