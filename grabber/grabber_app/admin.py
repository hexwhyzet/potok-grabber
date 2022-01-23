from django.contrib import admin
from django.utils.html import format_html

import grabber_app.service as service
from grabber_app import sender
from grabber_app.models import Picture, Profile


@admin.action(description='Send profiles to main server')
def send_profiles(modeladmin, request, queryset):
    for profile in queryset:
        sender.send_profile(profile)


@admin.action(description='Send pictures to main server')
def send_pictures(modeladmin, request, queryset):
    if isinstance(modeladmin, ProfileAdmin):
        for profile in queryset:
            sender.send_pictures(profile.pictures.filter(exported=False))
    if isinstance(modeladmin, PictureAdmin):
        sender.send_pictures(queryset)


@admin.action(description='Mark pictures as unexported')
def mark_as_unexported(modeladmin, request, queryset):
    for profile in queryset:
        service.mark_as_unexported(profile.pictures.all())


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "screen_name", "source_tag", "source_profile_id", "unexported", "exported")
    actions = [send_profiles, send_pictures, mark_as_unexported]

    @staticmethod
    def source_tag(profile: Profile):
        return profile.source

    @staticmethod
    def unexported(profile: Profile):
        unexported = profile.pictures.filter(exported=False).count()
        return str(unexported)

    @staticmethod
    def exported(profile: Profile):
        exported = profile.pictures.filter(exported=True).count()
        return str(exported)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("id", "profile_name", "profile_screen_name", "image_tag")
    actions = [send_pictures]

    @staticmethod
    def profile_name(picture: Picture):
        return picture.profile.name

    @staticmethod
    def profile_screen_name(picture: Picture):
        return picture.profile.screen_name

    @staticmethod
    def image_tag(picture: Picture):
        return format_html(
            f"<img src='{picture.url}' width='200' height='200'/>")
