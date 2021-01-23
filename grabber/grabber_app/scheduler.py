from apscheduler.schedulers.background import BackgroundScheduler

from grabber_app.config import Secrets, Config
from grabber_app.notification import send_message
from grabber_app.sender import send_profile, send_pictures
from grabber_app.service import get_profiles_that_need_to_be_updated, extract_pictures, \
    mark_as_exported
from grabber_vk.interface import grab_profile, grab_pictures

secret = Secrets()
config = Config()


def job():
    profiles = get_profiles_that_need_to_be_updated()

    for profile in profiles:
        grab_profile(profile.source_profile_id)
        grab_pictures(profile.source_profile_id)
        send_profile(profile)
        unexported_pictures = extract_pictures(profile)
        send_pictures(unexported_pictures)
        mark_as_exported(unexported_pictures)
        send_message(f"{profile.name}: {len(unexported_pictures)} картинок выгружено")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started working in background!")


if __name__ == '__main__':
    pass
