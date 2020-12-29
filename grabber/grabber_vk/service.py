from .handler import profile_id_by_source_name
from .models import VkProfile


def all_profile_ids():
    profiles = VkProfile.objects.all()
    source_ids = []
    for profile in profiles:
        if profile.converted:
            source_ids.append(profile.source_id)
        else:
            source_id = profile_id_by_source_name(profile.source_name)

            profile.source_id = source_id
            profile.converted = True
            profile.save()

            source_ids.append(source_id)
    return source_ids


def add_profiles_source_id(source_id):
    if not VkProfile.objects.filter(source_id=source_id).exists():
        VkProfile.objects.create(
            source_id=abs(int(source_id)),
            converted=True,
        )


def add_profiles_source_name(source_name):
    add_profiles_source_id(profile_id_by_source_name(source_name))
