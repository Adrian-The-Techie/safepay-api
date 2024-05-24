# Generated by Django 5.0.6 on 2024-05-22 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('SMS', 'Sms'), ('EMAIL', 'Email')], max_length=255)),
                ('recipient', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('response', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('url', models.UUIDField()),
                ('visibility', models.BooleanField(default=True)),
            ],
        ),
    ]
