# Generated by Django 3.1.4 on 2020-12-29 19:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('grabber_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='id_in_source',
            new_name='source_picture_id',
        ),
        migrations.RenameField(
            model_name='picture',
            old_name='source_id',
            new_name='source_profile_id',
        ),
    ]
