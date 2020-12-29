from django.db import models


class Picture(models.Model):
    source_profile_id = models.IntegerField()
    source_picture_id = models.IntegerField()
    url = models.CharField(max_length=1000, default=None, null=True, blank=True)
    date = models.IntegerField()
    exported = models.BooleanField(default=False)
    size = models.IntegerField()
    source = models.CharField(max_length=100)


class Profile(models.Model):
    source_profile_id = models.IntegerField()
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=1000)
    avatar_size = models.IntegerField()
    source = models.CharField(max_length=100)
