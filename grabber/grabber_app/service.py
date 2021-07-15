from datetime import timedelta
from random import randint

from django.utils import timezone

from grabber_app.config import Secrets, Config
from grabber_app.models import Picture, Profile
from grabber_reddit import interface as reddit_grabber_interface
from grabber_vk import interface as vk_grabber_interface

secret = Secrets()
config = Config()


def add_pictures_from_dict(pictures_dict, source):
    for picture_dict in pictures_dict:
        add_picture_from_dict(picture_dict, source)


def add_picture_from_dict(picture_dict, source):
    profile = Profile.objects.get(source_profile_id=picture_dict["source_profile_id"])
    if Picture.objects.filter(profile=profile,
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
            profile=profile,
            source_picture_id=picture_dict["source_picture_id"],
            date=picture_dict["date"],
            url=picture_dict["url"],
            size=picture_dict["size"],
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
        "avatar_size": profile.avatar_size,
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
        "size": picture.size,
        "source": picture.profile.source,
    }
    return picture


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


def mark_as_unexported(pictures):
    for picture in pictures:
        picture.exported = False
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


def download_profile_from_source_server(profile: Profile):
    if profile.source == Profile.Source.VK.value:
        profile_dictionary = vk_grabber_interface.grab_profile(profile.source_profile_id)
        add_profile_from_dict(profile_dictionary, Profile.Source.VK.value)

    if profile.source == Profile.Source.Reddit.value:
        profile_dictionary = vk_grabber_interface.grab_profile(profile.screen_name)
        add_profile_from_dict(profile_dictionary, Profile.Source.Reddit.value)


def download_pictures_from_source_server(profile: Profile):
    if profile.source == Profile.Source.VK.value:
        pictures_dictionaries = vk_grabber_interface.grab_pictures(profile.source_profile_id)
        add_pictures_from_dict(pictures_dictionaries, Profile.Source.VK.value)

    if profile.source == Profile.Source.Reddit.value:
        pictures_dictionaries = reddit_grabber_interface.grab_pictures(profile.screen_name)
        add_pictures_from_dict(pictures_dictionaries, Profile.Source.Reddit.value)


def export_to_main_db_new_profiles():
    profiles_dicts = vk_grabber_interface.unexported_to_main_db_profiles_dicts()
    for profile_dict in profiles_dicts:
        add_profile_from_dict(profile_dict, Profile.Source.VK)

    profiles_dicts = reddit_grabber_interface.unexported_to_main_db_profiles_dicts()
    for profile_dict in profiles_dicts:
        add_profile_from_dict(profile_dict, Profile.Source.Reddit)
