import json

from django.http import JsonResponse

from .handler import grab_pictures_via_api_from, grab_profile_via_api_from, profile_id_by_source_name
from .service import all_profile_ids, add_profiles_source_id, add_profiles_source_name

MAX_NUMBER = 100


def grab_both():
    for profile_id in all_profile_ids():
        grab_profile_via_api_from(profile_id)
        grab_pictures_via_api_from(profile_id, MAX_NUMBER)


def grab_profiles():
    for profile_id in all_profile_ids():
        grab_profile_via_api_from(profile_id)


def grab_pictures():
    for profile_id in all_profile_ids():
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
