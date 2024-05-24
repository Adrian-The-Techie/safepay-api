from django.db import models

DELIVERY_TYPES=[
    ("SMS", "Sms"),
    ("EMAIL", "Email")
]

# Create your models here.
class DeliveryReport(models.Model):
    type = models.CharField(max_length=255, choices=DELIVERY_TYPES)
    recipient=models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    response = models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    url=models.UUIDField()
    visibility=models.BooleanField(default=True)
