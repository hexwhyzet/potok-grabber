from grabber_reddit.api import reddit_api_request


def strip_reddit_prefix(string):
    """
    The function removes t1_, t2_ and etc prefixes
    """
    return string.split("_")[-1]


def filter_list_of_posts(list_of_posts):
    def not_video(post):
        return not post["is_video"]

    def one_image(post):
        return len(post["preview"]["images"]) == 1

    def is_not_gif(post):
        return not post["url"].endswith(".gif") and not post["url"].endswith(".gifv")

    filters = [
        not_video,
        one_image,
        is_not_gif,
    ]

    for filter_func in filters:
        list_of_posts = list(filter(filter_func, list_of_posts))

    return list(list_of_posts)


def extract_pictures_from_post(list_of_posts):
    def extract_picture(post):
        picture = {
            "source_profile_id": strip_reddit_prefix(post["subreddit_id"]),
            "source_picture_id": post["preview"]["images"][0]["id"],
            "date": int(post["created_utc"]),
            "url": post["url"],
            "size": None,
        }
        return picture

    pictures = list(map(extract_picture, list_of_posts))
    return pictures


def extract_profile(page_info):
    stripped_page_info = {
        "source_profile_id": strip_reddit_prefix(page_info["id"]),
        "name": page_info["title"],
        "screen_name": page_info["display_name_prefixed"],
        "avatar_url": page_info["icon_img"],
        "avatar_size": None,
    }
    return stripped_page_info


def handle_posts(posts):
    filtered_posts = filter_list_of_posts(posts)
    extracted_pictures = extract_pictures_from_post(filtered_posts)
    return extracted_pictures


def grab_pictures_via_api(subreddit_name, count):
    assert count <= 100
    posts = reddit_api_request(f"{subreddit_name}/new", params={"limit": count})['data']['children']
    pictures = handle_posts(map(lambda x: x['data'], posts))
    return pictures


def grab_profile_via_api(subreddit_name):
    profile = reddit_api_request(f"{subreddit_name}/about")['data']
    return extract_profile(profile)


if __name__ == '__main__':
    print(grab_profile_via_api("r/dankmemes"))
