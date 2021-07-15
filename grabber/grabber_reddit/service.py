from django.db.models import Q

from grabber_reddit.handler import grab_profile_via_api
from grabber_reddit.models import RedditProfile


def download_name_and_source_id_to_profiles():
    unfilled_profiles = RedditProfile.objects.filter(Q(name=None) | Q(screen_name=None))
    for profile in unfilled_profiles:
        download_profile_name_and_source_id(profile)


def download_profile_name_and_source_id(profile: RedditProfile):
    profile_dict = grab_profile_via_api(profile.screen_name)
    profile.name = profile_dict['name']
    profile.source_id = profile_dict['source_profile_id']
    profile.save()
