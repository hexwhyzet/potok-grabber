from django.apps import AppConfig


class GrabberAppConfig(AppConfig):
    name = 'grabber_app'

    def ready(self):
        from grabber_vk.interface import upload_new_vk_profile_to_main_db
        upload_new_vk_profile_to_main_db()
        from grabber_app.service import set_random_last_update_time
        set_random_last_update_time()
        from grabber_app.scheduler import start_scheduler
        start_scheduler()
