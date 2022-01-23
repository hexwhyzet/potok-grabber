from django.db.models import QuerySet

from grabber_app.config import Secrets, Config
from grabber_app.models import Picture, Profile

secret = Secrets()
config = Config()


def add_pictures_from_dict(pictures_dict):
    for picture_dict in pictures_dict:
        add_picture_from_dict(picture_dict)


def add_picture_from_dict(picture_dict: dict):
    profile = Profile.objects.get(source_profile_id=picture_dict["source_profile_id"])
    Picture.objects.update_or_create(profile=profile,
                                     source_picture_id=picture_dict["source_picture_id"],
                                     defaults={
                                         "date": picture_dict["date"],
                                         "url": picture_dict["url"],
                                     })


def add_profile_dict_to_main_db(profile_dict: dict, source: Profile.Source):
    Profile.objects.update_or_create(source_profile_id=profile_dict["source_profile_id"],
                                     source=source,
                                     defaults={
                                         "name": profile_dict["name"],
                                         "screen_name": profile_dict["screen_name"],
                                         "avatar_url": profile_dict["avatar_url"],
                                     })


def profile_url(profile: Profile):
    if profile.source == Profile.Source.VK.value:
        return f"https://vk.com/public{profile.source_profile_id}"
    elif profile.source == Profile.Source.Reddit.value:
        return f"https://reddit.com/{profile.screen_name}"
    else:
        return None


def profile_to_dict(profile: Profile):
    profile = {
        "source_profile_id": profile.source_profile_id,
        "name": profile.name,
        "screen_name": profile.screen_name,
        "avatar_url": profile.avatar_url,
        "source": profile.source,
        "url": profile_url(profile),
    }
    return profile


def picture_to_dict(picture: Picture):
    picture = {
        "source_profile_id": picture.profile.source_profile_id,
        "source_picture_id": picture.source_picture_id,
        "url": picture.url,
        "date": picture.date,
        "source": picture.profile.source,
    }
    return picture


def extract_all_pictures(exported=False):
    pictures = Picture.objects.filter(exported=exported)
    return pictures


def get_unexported_pictures(profile: Profile) -> QuerySet[Picture]:
    return Picture.objects.filter(exported=False, source_profile_id=profile.source_profile_id)


def extract_profiles() -> QuerySet[Profile]:
    profiles = Profile.objects.filter()
    return profiles


def mark_as_exported(pictures):
    for picture in pictures:
        picture.exported = True
        picture.save()


def mark_as_unexported(pictures):
    for picture in pictures:
        picture.exported = False
        picture.save()


def mark_all_as_exported():
    Picture.objects.filter(exported=False).update(exported=True)


def profiles_with_unexported_pictures() -> QuerySet[Profile]:
    return Profile.objects.filter(pictures__exported__in=[False])
