from django.db import models
from user.models import User

# Create your models here.



class Payin(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reference_no=models.CharField(max_length=255)
    amount=models.FloatField(max_length=255)
    sourceAccount=models.CharField(max_length=255)
    date_initiated=models.DateTimeField(auto_created=True)
    responsePayload=models.TextField()
    callbackPayload=models.TextField()
    url=models.UUIDField()
    status=models.CharField(max_length=255, default="PENDING")
    type=models.CharField(max_length=255, default="TRANSFER")

class Payout(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reference_no=models.CharField(max_length=255)
    amount=models.FloatField(max_length=255)
    destinationAccount=models.CharField(max_length=255)
    date_initiated=models.DateTimeField(auto_created=True)
    responsePayload=models.TextField()
    callbackPayload=models.TextField()
    url=models.UUIDField()
    status=models.CharField(max_length=255, default="PENDING")
    type=models.CharField(max_length=255, default="TRANSFER")

    