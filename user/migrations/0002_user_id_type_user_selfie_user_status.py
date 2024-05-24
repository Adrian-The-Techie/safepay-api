# Generated by Django 5.0.6 on 2024-05-20 03:01

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_type',
            field=models.IntegerField(choices=[(1, 'NATIONAL_ID'), (2, 'PASSPORT'), (3, "DRIVER'S LICENSE"), (4, 'HUDUMA NUMBER'), (5, 'MILITARY_ID')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='selfie',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[(1, 'PENDING_VERIFICATION'), (1, 'ACTIVE'), (3, 'SUSPENDED'), (4, 'DEACTIVATED')], default=1),
        ),
    ]