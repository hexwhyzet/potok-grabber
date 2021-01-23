from django.http import JsonResponse

from grabber_app.models import Profile
from .handler import grab_pictures_via_api_from, grab_profile_via_api_from
from .service import add_profiles_source_id, add_profiles_source_name, all_profile_ids

MAX_NUMBER = 100


def upload_new_vk_profile_to_main_db():
    for vk_profile_id in all_profile_ids():
        if not Profile.objects.filter(source_profile_id=vk_profile_id).exists():
            grab_profile(vk_profile_id)


def grab_all_profiles():
    for profile_id in all_profile_ids():
        grab_profile_via_api_from(profile_id)


def grab_profile(profile_id):
    grab_profile_via_api_from(profile_id)


def grab_pictures(profile_id):
    grab_pictures_via_api_from(profile_id, MAX_NUMBER)


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
