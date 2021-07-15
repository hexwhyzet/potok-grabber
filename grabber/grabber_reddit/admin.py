from django.contrib import admin

from grabber_app.models import Profile
from grabber_app.service import add_profile_from_dict
from .interface import grab_profile
from .models import RedditProfile
from .service import download_profile_name_and_source_id


@admin.action(description='Download name and source_id')
def download_credentials(modeladmin, request, queryset):
    for reddit_profile in queryset:
        download_profile_name_and_source_id(reddit_profile)


@admin.action(description='Load to main db')
def load_to_main_db(modeladmin, request, queryset):
    for reddit_profile in queryset:
        add_profile_from_dict(grab_profile(reddit_profile.screen_name), Profile.Source.Reddit)


@admin.register(RedditProfile)
class RedditProfileAdmin(admin.ModelAdmin):
    actions = [download_credentials, load_to_main_db]
