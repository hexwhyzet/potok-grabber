import time

import schedule

from .config import Secrets, Config
from grabber_app.sender import send_pictures, send_profiles
from .interface import grab_all_pictures_and_profiles

secret = Secrets()
config = Config()


def job():
    grab_all_pictures_and_profiles()
    send_profiles()
    send_pictures()


def scheduler():
    print("Scheduler started working!")
    schedule.every(3).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(600)


if __name__ == '__main__':
    scheduler()
