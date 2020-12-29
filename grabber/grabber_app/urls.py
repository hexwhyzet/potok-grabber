from django.contrib import admin
from django.urls import path

from . import view

urlpatterns = [
    path('send_pictures', view.view_send_pictures),
    path('send_profiles', view.view_send_profiles),
    path('send_both', view.view_send_both),
    path('pictures', view.get_pictures),
    path('profiles', view.get_profiles),
]
