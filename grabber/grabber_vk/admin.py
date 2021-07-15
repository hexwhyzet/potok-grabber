from django.contrib import admin

from grabber_app.models import Profile
from grabber_app.service import add_profile_from_dict
from .interface import grab_profile
from .models import VkProfile
from .service import download_profile_name_and_screen_name


@admin.action(description='Download name and screen name')
def download_credentials(modeladmin, request, queryset):
    for vk_profile in queryset:
        download_profile_name_and_screen_name(vk_profile)


@admin.action(description='Load to main db')
def load_to_main_db(modeladmin, request, queryset):
    for vk_profile in queryset:
        add_profile_from_dict(grab_profile(vk_profile), Profile.Source.VK)


@admin.register(VkProfile)
class VkProfileAdmin(admin.ModelAdmin):
    actions = [download_credentials, load_to_main_db]
