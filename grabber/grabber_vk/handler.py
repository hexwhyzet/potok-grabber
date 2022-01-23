from grabber_vk.api import get_posts, get_group_by_id

if __name__ == '__main__':
    from grabber_reddit.config import Secrets, Config
else:
    from grabber_reddit.config import Secrets, Config

config = Config()
secrets = Secrets()


def filter_list_of_posts(list_of_posts):
    def is_post_not_add(post):
        return not post["marked_as_ads"]

    def does_post_contain_only_one_photo(post):
        if "attachments" not in post:
            return False
        photos = list(filter(lambda x: x["type"] == "photo", post["attachments"]))
        return len(photos) == 1

    def does_post_have_short_text(post):
        return len(post["text"]) < 150

    def does_not_text_include_link(post):
        triggers = [
            "www",
            "http",
            "https",
            "vk.com",
            "vk.me",
            "tg",
            "www",
            ".com",
            ".ru",
        ]
        for trigger in triggers:
            if trigger in post["text"]:
                return False
        return True

    def does_post_not_have_copyright(post):
        return "copyright" not in post

    # def does_post_not_have_api_source(post):
    #     return post["post_source"]["type"] != "api"

    filters = [
        is_post_not_add,
        does_post_contain_only_one_photo,
        does_post_have_short_text,
        does_not_text_include_link,
        does_post_not_have_copyright,
    ]

    for filter_func in filters:
        list_of_posts = list(filter(filter_func, list_of_posts))

    return list(list_of_posts)


def extract_photo_url(photos_dict):
    available_photo_sizes = photos_dict['sizes']
    sorted_available_photo_widths = list(sorted(available_photo_sizes, key=lambda x: int(x['width']), reverse=True))
    photo_url = sorted_available_photo_widths[0]['url']
    return photo_url


def extract_pictures_from_post(list_of_posts):
    def extract_picture(post):
        photo_url = extract_photo_url(post["attachments"][0]["photo"])
        picture = {
            "source_profile_id": abs(int(post["owner_id"])),
            "source_picture_id": post["id"],
            "date": post["date"],
            "url": photo_url,
        }
        return picture

    pictures = list(map(extract_picture, list_of_posts))
    return pictures


def extract_profile(page_info):
    photo_url = extract_photo_url(page_info)
    stripped_page_info = {
        "source_profile_id": abs(int(page_info["id"])),
        "name": page_info["name"],
        "screen_name": page_info["screen_name"],
        "avatar_url": photo_url,
    }
    return stripped_page_info


def handle_posts(posts):
    filtered_posts = filter_list_of_posts(posts)
    extracted_pictures = extract_pictures_from_post(filtered_posts)
    return extracted_pictures


def profile_id_by_source_name(group_id):
    return get_group_by_id(group_id)['id']


def grab_vk_pictures(source_id, count):
    posts = get_posts(source_id, count)
    pictures = handle_posts(posts)
    return pictures


def grab_vk_profile(source_id):
    profile = extract_profile(get_group_by_id(source_id))
    return profile


if __name__ == '__main__':
    # pictures = grab_pictures_via_api_from(profile_id_by_source_name("yungbidlo"), 100)
    # print(pictures)
    pass
