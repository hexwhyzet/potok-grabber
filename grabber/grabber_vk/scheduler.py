from apscheduler.schedulers.background import BackgroundScheduler

from grabber_app.base_model import filter_profiles_that_need_to_be_updated, set_random_last_update_time, \
    unset_last_update_date
from grabber_app.config import Secrets, Config
from grabber_app.models import Profile
from grabber_app.service import add_profile_dict_to_main_db, add_picture_from_dict
from grabber_vk.handler import grab_vk_profile, grab_vk_pictures
from grabber_vk.models import VkProfile
from grabber_vk.service import all_vk_profiles

secret = Secrets()
config = Config()

IMPORT_INTERVAL_SECONDS = 60 * 60 * 3

MAX_PICTURES_IMPORT = 100

SOURCE = Profile.Source.VK.value


def send_vk_profile_to_main_db(vk_profile: VkProfile):
    vk_profile_dict = grab_vk_profile(vk_profile.source_id)
    add_profile_dict_to_main_db(vk_profile_dict, SOURCE)


def send_vk_pictures_of_profile_to_main_db(vk_profile: VkProfile):
    vk_profile_pictures_dicts = grab_vk_pictures(vk_profile.source_id, MAX_PICTURES_IMPORT)
    for vk_picture_dict in vk_profile_pictures_dicts:
        add_picture_from_dict(vk_picture_dict)


def vk_job():
    set_random_last_update_time(unset_last_update_date(all_vk_profiles()), IMPORT_INTERVAL_SECONDS)

    vk_profiles = filter_profiles_that_need_to_be_updated(VkProfile.objects.all(), IMPORT_INTERVAL_SECONDS)

    for vk_profile in vk_profiles:
        send_vk_profile_to_main_db(vk_profile)
        send_vk_pictures_of_profile_to_main_db(vk_profile)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(vk_job, 'interval', minutes=1)
    scheduler.start()
    print("VK scheduler started working in background!")
