import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grabber.settings')
django.setup()

from grabber_app.models import Picture, Profile

Picture.objects.filter(source_profile_id=149594529).delete()
Profile.objects.filter(source_profile_id=149594529).delete()
