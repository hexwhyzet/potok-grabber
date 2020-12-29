from django.db import models


class VkProfile(models.Model):
    source_name = models.CharField(null=True, blank=True, max_length=100)
    converted = models.BooleanField(default=False)
    source_id = models.IntegerField(blank=True, null=True, default=None)
