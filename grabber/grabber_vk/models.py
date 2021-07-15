from django.db import models


class VkProfile(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    screen_name = models.CharField(null=True, blank=True, max_length=100)
    source_id = models.IntegerField(blank=False, null=False)

    def __str__(self):
        if self.name is not None:
            return f"{self.name} ({self.screen_name})"
        if self.screen_name is not None:
            return self.screen_name
        else:
            return self.source_id
