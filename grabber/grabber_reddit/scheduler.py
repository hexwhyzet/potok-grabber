from apscheduler.schedulers.background import BackgroundScheduler

from grabber_app.base_model import filter_profiles_that_need_to_be_updated, set_random_last_update_time, \
    unset_last_update_date
from grabber_app.config import Secrets, Config
from grabber_app.models import Profile
from grabber_app.service import add_profile_dict_to_main_db, add_picture_from_dict
from grabber_reddit.handler import grab_reddit_profile, grab_reddit_pictures
from grabber_reddit.models import RedditProfile
from grabber_reddit.service import all_reddit_profiles

secret = Secrets()
config = Config()

IMPORT_INTERVAL_SECONDS = 60 * 60 * 3

MAX_PICTURES_IMPORT = 100

SOURCE = Profile.Source.Reddit.value


def send_reddit_profile_to_main_db(reddit_profile: RedditProfile):
    reddit_profile_dict = grab_reddit_profile(reddit_profile.screen_name)
    add_profile_dict_to_main_db(reddit_profile_dict, SOURCE)


def send_reddit_pictures_of_profile_to_main_db(reddit_profile: RedditProfile):
    reddit_profile_pictures_dicts = grab_reddit_pictures(reddit_profile.screen_name, MAX_PICTURES_IMPORT)
    for reddit_picture_dict in reddit_profile_pictures_dicts:
        add_picture_from_dict(reddit_picture_dict)


def reddit_job():
    set_random_last_update_time(unset_last_update_date(all_reddit_profiles()), IMPORT_INTERVAL_SECONDS)

    reddit_profiles = filter_profiles_that_need_to_be_updated(RedditProfile.objects.all(), IMPORT_INTERVAL_SECONDS)
    for reddit_profile in reddit_profiles:
        send_reddit_profile_to_main_db(reddit_profile)
        send_reddit_pictures_of_profile_to_main_db(reddit_profile)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reddit_job, 'interval', minutes=1)
    scheduler.start()
    print("Reddit scheduler started working in background!")
