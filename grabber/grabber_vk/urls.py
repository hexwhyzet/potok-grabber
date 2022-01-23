from django.urls import path

from . import interface
from .handler import grab_vk_pictures

urlpatterns = [
    path('download', grab_vk_pictures),
    path('load_ids', interface.load_source_ids),
    path('load_name', interface.load_source_name),
]
