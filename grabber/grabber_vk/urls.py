from django.contrib import admin
from django.urls import path

from . import interface

urlpatterns = [
    path('download', interface.grab_pictures),
    path('load_ids', interface.load_source_ids),
    path('load_name', interface.load_source_name),
]
