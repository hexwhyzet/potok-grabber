from django.db import models


class Profile(models.Model):
    class Source(models.Choices):
        VK = 'vk'
        Reddit = 'reddit'
        Custom = 'custom'

    source_profile_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=1000)
    avatar_size = models.IntegerField(null=True, blank=True)
    last_update_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, choices=Source.choices)

    def __str__(self):
        return self.name


class Picture(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pictures', blank=True, null=True)
    source_picture_id = models.CharField(max_length=100)
    url = models.CharField(max_length=1000, default=None, null=True, blank=True)
    date = models.IntegerField()
    exported = models.BooleanField(default=False)
    size = models.IntegerField(null=True, blank=True)
