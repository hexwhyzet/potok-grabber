from django.contrib import admin

from .models import VkProfile
from .scheduler import send_vk_profile_to_main_db, send_vk_pictures_of_profile_to_main_db
from .service import download_profile_name_and_screen_name


@admin.action(description='Download profiles from vk server to main database')
def download_profiles(modeladmin, request, queryset):
    for profile in queryset:
        send_vk_profile_to_main_db(profile)


@admin.action(description='Download pictures of profiles from vk server to main database')
def download_pictures(modeladmin, request, queryset):
    for profile in queryset:
        send_vk_pictures_of_profile_to_main_db(profile)


@admin.action(description='Download name and screen name')
def download_credentials(modeladmin, request, queryset):
    for vk_profile in queryset:
        download_profile_name_and_screen_name(vk_profile.source_id)


@admin.register(VkProfile)
class VkProfileAdmin(admin.ModelAdmin):
    list_display = ["source_id", "name", "screen_name"]

    actions = [download_credentials, download_profiles, download_pictures]
