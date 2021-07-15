from grabber_app.models import Profile
from grabber_reddit.handler import grab_pictures_via_api, grab_profile_via_api
from grabber_reddit.models import RedditProfile

MAX_COUNT = 100


def unexported_to_main_db_profiles_dicts():
    unexported_to_main_db_reddit_profiles = RedditProfile.objects.exclude(
        source_id__in=Profile.objects.values_list("source_profile_id", flat=True).all())
    return list(map(lambda _reddit_profile: grab_profile(_reddit_profile.source_id),
                    unexported_to_main_db_reddit_profiles))


def grab_profile(reddit_profile_screen_name):
    return grab_profile_via_api(reddit_profile_screen_name)


def grab_pictures(reddit_profile_screen_name):
    return grab_pictures_via_api(reddit_profile_screen_name, MAX_COUNT)
