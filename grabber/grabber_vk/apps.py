import sys

from django.apps import AppConfig


class GrabberVkConfig(AppConfig):
    name = 'grabber_vk'

    def ready(self):
        if 'runserver' in sys.argv:
            from grabber_vk.scheduler import IMPORT_INTERVAL_SECONDS
            from grabber_vk.service import all_vk_profiles
            from grabber_app.base_model import set_random_last_update_time
            set_random_last_update_time(all_vk_profiles(), IMPORT_INTERVAL_SECONDS)

            from grabber_vk.service import download_name_and_source_name_to_vk_profiles
            download_name_and_source_name_to_vk_profiles()

            from grabber.settings import enable_vk_scheduler
            if enable_vk_scheduler:
                from grabber_vk.scheduler import start_scheduler
                start_scheduler()
