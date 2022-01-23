from django.http import JsonResponse

from .service import add_profiles_source_id, add_profiles_source_name

MAX_NUMBER = 100


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
