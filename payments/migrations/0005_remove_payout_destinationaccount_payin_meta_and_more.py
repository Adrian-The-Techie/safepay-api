# Generated by Django 4.0.1 on 2024-06-12 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_payout_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payout',
            name='destinationAccount',
        ),
        migrations.AddField(
            model_name='payin',
            name='meta',
            field=models.TextField(default='meta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payin',
            name='notes',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payout',
            name='destination_account',
            field=models.CharField(default=254700221171, max_length=255),
            preserve_default=False,
        ),
    ]
