from datetime import timedelta
from random import randint

from django.db import models
from django.db.models import QuerySet, Q
from django.utils import timezone

from grabber_app.config import Secrets, Config

secret = Secrets()
config = Config()


class BaseModel(models.Model):
    last_update_date = models.DateTimeField(null=True, blank=True)


def refresh_last_update_date(profile):
    profile.last_update_date = timezone.now()
    profile.save()


def unset_last_update_date(profiles: QuerySet[BaseModel]):
    return profiles.filter(Q(last_update_date=None))


def set_random_last_update_time(profiles: QuerySet[BaseModel], import_interval_seconds: int):
    for profile in profiles:
        profile.last_update_date = timezone.now() - timedelta(seconds=randint(0, import_interval_seconds))
        profile.save()


def filter_profiles_that_need_to_be_updated(profiles: QuerySet[BaseModel], import_interval_seconds):
    threshold_date = timezone.now() - timedelta(seconds=import_interval_seconds)
    return profiles.filter(~Q(last_update_date=None)).filter(last_update_date__lt=threshold_date)
