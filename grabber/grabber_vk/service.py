from django.db.models import Q

from .handler import profile_id_by_source_name, grab_profile_via_api
from .models import VkProfile


def download_name_and_source_name_to_profiles():
    unfilled_profiles = VkProfile.objects.filter(Q(name=None) | Q(screen_name=None))
    for profile in unfilled_profiles:
        download_profile_name_and_screen_name(profile)


def download_profile_name_and_screen_name(profile: VkProfile):
    profile_dict = grab_profile_via_api(profile.source_id)
    profile.name = profile_dict['name']
    profile.screen_name = profile_dict['screen_name']
    profile.save()


def add_profiles_source_id(source_id):
    if not VkProfile.objects.filter(source_id=source_id).exists():
        VkProfile.objects.create(
            source_id=abs(int(source_id)),
        )


def add_profiles_source_name(source_name):
    add_profiles_source_id(profile_id_by_source_name(source_name))
