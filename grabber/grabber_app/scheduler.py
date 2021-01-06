import time

import schedule

from grabber_app.config import Secrets, Config
from grabber_app.notification import send_message
from grabber_app.sender import send_pictures, send_profiles
from grabber_app.service import mark_all_as_exported
from grabber_vk.interface import grab_pictures, grab_profiles

secret = Secrets()
config = Config()


def job():
    grab_profiles()
    grab_pictures()
    send_profiles()
    send_pictures()
    mark_all_as_exported()
    send_message("Работа выполнена")


def force_send():
    send_profiles()
    send_pictures(exported=True)
    send_pictures(exported=False)


def scheduler():
    print("Scheduler started working!")
    schedule.every(3).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(600)


if __name__ == '__main__':
    scheduler()
