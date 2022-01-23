import sys

from django.apps import AppConfig


class GrabberRedditConfig(AppConfig):
    name = 'grabber_reddit'

    def ready(self):
        if 'runserver' in sys.argv:
            from grabber_reddit.scheduler import IMPORT_INTERVAL_SECONDS
            from grabber_reddit.service import all_reddit_profiles
            from grabber_app.base_model import set_random_last_update_time
            set_random_last_update_time(all_reddit_profiles(), IMPORT_INTERVAL_SECONDS)

            from grabber_reddit.service import download_name_and_source_id_to_reddit_profiles
            download_name_and_source_id_to_reddit_profiles()

            from grabber.settings import enable_reddit_scheduler
            if enable_reddit_scheduler:
                from grabber_reddit.scheduler import start_scheduler
                start_scheduler()
