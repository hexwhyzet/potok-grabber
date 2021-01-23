from datetime import datetime, timedelta
from random import randint

from django.utils import timezone

from grabber_app.config import Secrets, Config
from grabber_app.models import Picture, Profile

secret = Secrets()
config = Config()


def add_pictures_from_dict(pictures_dict, source):
    for picture_dict in pictures_dict:
        add_picture_from_dict(picture_dict, source)


def add_picture_from_dict(picture_dict, source):
    if Picture.objects.filter(source_profile_id=picture_dict["source_profile_id"],
                              source_picture_id=picture_dict["source_picture_id"]).exists():
        return
        # Picture.objects.filter(source_profile_id=picture_dict["source_profile_id"],
        #                        source_picture_id=picture_dict["source_picture_id"]).update(
        #     source_profile_id=picture_dict["source_profile_id"],
        #     source_picture_id=picture_dict["source_picture_id"],
        #     date=picture_dict["date"],
        #     url=picture_dict["url"],
        #     size=picture_dict["size"],
        #     source=source,
        # )
    else:
        Picture.objects.create(
            source_profile_id=picture_dict["source_profile_id"],
            source_picture_id=picture_dict["source_picture_id"],
            date=picture_dict["date"],
            url=picture_dict["url"],
            size=picture_dict["size"],
            source=source,
        )


def add_profile_from_dict(profile_dict, source):
    if Profile.objects.filter(source_profile_id=profile_dict["source_profile_id"]).exists():
        Profile.objects.filter(source_profile_id=profile_dict["source_profile_id"]).update(
            name=profile_dict["name"],
            screen_name=profile_dict["screen_name"],
            avatar_url=profile_dict["avatar_url"],
            avatar_size=profile_dict["avatar_size"],
            source=source,
        ),
    else:
        Profile.objects.create(
            source_profile_id=profile_dict["source_profile_id"],
            name=profile_dict["name"],
            screen_name=profile_dict["screen_name"],
            avatar_url=profile_dict["avatar_url"],
            avatar_size=profile_dict["avatar_size"],
            source=source,
        )


def extract_all_pictures(exported=False):
    pictures = Picture.objects.filter(exported=exported)
    return pictures


def extract_pictures(profile: Profile):
    pictures = Picture.objects.filter(exported=False, source_profile_id=profile.source_profile_id)
    return pictures


def extract_profiles():
    profiles = Profile.objects.filter()
    return profiles


def mark_as_exported(pictures):
    for picture in pictures:
        picture.exported = True
        picture.save()


def change_last_update_date_to_now(profile):
    profile.last_update_date = timezone.now()
    profile.save()


def mark_all_as_exported():
    Picture.objects.filter(exported=False).update(exported=True)


def set_random_last_update_time():
    import_interval = config["import_interval_seconds"]
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.last_update_date = timezone.now() - timedelta(seconds=randint(0, import_interval))
        profile.save()


def get_profiles_that_need_to_be_updated():
    import_interval = config["import_interval_seconds"]
    threshold_date = timezone.now() - timedelta(seconds=import_interval)
    profiles = Profile.objects.filter(last_update_date__lt=threshold_date)
    return profiles



