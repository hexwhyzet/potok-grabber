from django.http import JsonResponse

from grabber_app.models import Profile
from .handler import grab_pictures_via_api, grab_profile_via_api
from .models import VkProfile
from .service import add_profiles_source_id, add_profiles_source_name

MAX_NUMBER = 100


def unexported_to_main_db_profiles_dicts():
    unexported_to_main_db_vk_profiles = VkProfile.objects.exclude(
        source_id__in=Profile.objects.values_list("source_profile_id", flat=True).all())
    return list(map(lambda _vk_profile: grab_profile(_vk_profile.source_id), unexported_to_main_db_vk_profiles))


def grab_profile(profile_id):
    return grab_profile_via_api(profile_id)


def grab_pictures(profile_id):
    return grab_pictures_via_api(profile_id, MAX_NUMBER)


def load_source_ids(request):
    content = request.GET["content"]
    source_ids = eval(content)
    for source_id in source_ids:
        add_profiles_source_id(source_id)
    return JsonResponse({"success": True})


def load_source_name(request):
    source_name = request.GET["content"]
    add_profiles_source_name(source_name)
    return JsonResponse({"success": True})
