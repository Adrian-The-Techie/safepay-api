from django.db import models
from user.models import User

# Create your models here.



class Payin(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reference_no=models.CharField(max_length=255)
    amount=models.FloatField(max_length=255)
    source_account=models.CharField(max_length=255)
    date_initiated=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(null=True, blank=True)
    responsePayload=models.TextField()
    callbackPayload=models.TextField()
    url=models.UUIDField()
    status=models.CharField(max_length=255, default="PENDING")
    type=models.CharField(max_length=255, default="TRANSFER")
    notes=models.CharField(max_length=255, null=True)
    meta= models.TextField()

class Payout(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reference_no=models.CharField(max_length=255)
    payin_ref_no=models.CharField(max_length=255, null=True, blank=True)
    amount=models.FloatField(max_length=255)
    destination_account=models.CharField(max_length=255)
    channel=models.CharField(max_length=255)
    date_initiated=models.DateTimeField(auto_now_add=True)
    responsePayload=models.TextField()
    callbackPayload=models.TextField()
    url=models.UUIDField()
    status=models.CharField(max_length=255, default="PENDING")
    type=models.CharField(max_length=255, default="TRANSFER")

    