from django.apps import AppConfig


class GrabberAppConfig(AppConfig):
    name = 'grabber_app'

    def ready(self):
        from grabber_app.scheduler import scheduler
        scheduler()
