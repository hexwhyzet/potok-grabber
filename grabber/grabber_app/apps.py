from django.apps import AppConfig


class GrabberAppConfig(AppConfig):
    name = 'grabber_app'

    def ready(self):
        pass
        # from grabber_app.service import export_to_main_db_new_profiles
        # export_to_main_db_new_profiles()
        # from grabber_app.service import set_random_last_update_time
        # set_random_last_update_time()
    #     from grabber_app.scheduler import start_scheduler
    #     start_scheduler()
