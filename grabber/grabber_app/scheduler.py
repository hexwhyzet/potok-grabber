from apscheduler.schedulers.background import BackgroundScheduler

from grabber_app.base_model import refresh_last_update_date
from grabber_app.config import Secrets, Config
from grabber_app.notification import send_message
from grabber_app.sender import send_profile, send_pictures
from grabber_app.service import mark_as_exported, profiles_with_unexported_pictures, \
    get_unexported_pictures

secret = Secrets()
config = Config()


def job():
    profiles = profiles_with_unexported_pictures()

    for profile in profiles:
        try:
            send_profile(profile)
            refresh_last_update_date(profile)
        except Exception as e:
            print(f"Profile send filed {e}")

        unexported_pictures = get_unexported_pictures(profile)
        try:
            send_pictures(unexported_pictures)
            mark_as_exported(unexported_pictures)
            send_message(f"{profile.name}: {len(unexported_pictures)} картинок выгружено")
        except Exception as e:
            print(f"Pictures send failed {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=1)
    scheduler.start()
    print("Main scheduler started working in background!")
