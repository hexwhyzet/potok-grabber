# Generated by Django 3.1.4 on 2020-12-29 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabber_app', '0003_picture_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='exported',
            field=models.BooleanField(default=False),
        ),
    ]
