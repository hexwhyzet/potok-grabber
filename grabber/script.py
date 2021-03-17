import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grabber.settings')
django.setup()

from grabber_app.models import Picture

Picture.objects.all().update(exported=False)
