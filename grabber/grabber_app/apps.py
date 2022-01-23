import sys

from django.apps import AppConfig


class GrabberAppConfig(AppConfig):
    name = 'grabber_app'

    def ready(self):
        if 'runserver' in sys.argv:
            from grabber.settings import enable_main_scheduler
            if enable_main_scheduler:
                from grabber_app.scheduler import start_scheduler
                start_scheduler()
