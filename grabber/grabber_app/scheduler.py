import time

import schedule

from grabber_app.config import Secrets, Config
from grabber_app.sender import send_pictures, send_profiles
from grabber_vk.interface import grab_pictures, grab_profiles

from grabber_app.notification import send_message

secret = Secrets()
config = Config()


def job():
    grab_profiles()
    grab_pictures()
    send_profiles()
    send_pictures()
    send_message("Работа выполнена")


def scheduler():
    print("Scheduler started working!")
    schedule.every(3).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(600)


if __name__ == '__main__':
    scheduler()
