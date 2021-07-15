from django.apps import AppConfig


class GrabberVkConfig(AppConfig):
    name = 'grabber_vk'

    def ready(self):
        from grabber_vk.service import download_name_and_source_name_to_profiles
        download_name_and_source_name_to_profiles()
