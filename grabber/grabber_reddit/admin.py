from django.contrib import admin

from .models import RedditProfile
from .scheduler import send_reddit_profile_to_main_db, send_reddit_pictures_of_profile_to_main_db
from .service import download_reddit_profile_name_and_source_id


@admin.action(description='Download profiles from reddit server to main database')
def download_profiles(modeladmin, request, queryset):
    for profile in queryset:
        send_reddit_profile_to_main_db(profile)


@admin.action(description='Download pictures of profiles from reddit server to main database')
def download_pictures(modeladmin, request, queryset):
    for profile in queryset:
        send_reddit_pictures_of_profile_to_main_db(profile)


@admin.action(description='Download name and source_id')
def download_credentials(modeladmin, request, queryset):
    for reddit_profile in queryset:
        download_reddit_profile_name_and_source_id(reddit_profile)


@admin.register(RedditProfile)
class RedditProfileAdmin(admin.ModelAdmin):
    list_display = ["source_id", "name", "screen_name"]

    actions = [download_credentials, download_profiles, download_pictures]
