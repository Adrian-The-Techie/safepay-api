# Generated by Django 4.0.1 on 2024-06-12 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_alter_payout_date_initiated'),
    ]

    operations = [
        migrations.AddField(
            model_name='payout',
            name='payin_ref_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
