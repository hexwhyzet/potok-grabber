from django.forms import model_to_dict
from django.http import JsonResponse

from grabber_app.sender import send_all_pictures, send_all_profiles
from grabber_app.service import extract_all_pictures, extract_profiles


def view_send_pictures(request):
    send_all_pictures()
    return JsonResponse({"success": True})


def view_send_profiles(request):
    send_all_profiles()
    return JsonResponse({"success": True})


def view_send_both(request):
    send_all_profiles()
    send_all_pictures()
    return JsonResponse({"success": True})


def get_pictures(request):
    pictures_objects = extract_all_pictures()
    pictures = list(map(model_to_dict, pictures_objects))
    return JsonResponse({"success": True, "content": pictures})


def get_profiles(request):
    profiles_objects = extract_profiles()
    profiles = list(map(model_to_dict, profiles_objects))
    return JsonResponse({"success": True, "content": profiles})
