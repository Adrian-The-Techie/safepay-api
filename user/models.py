from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.

ID_TYPE=[
    (1, 'NATIONAL_ID'),
    (2, 'PASSPORT'),
    (3, 'DRIVER\'S LICENSE'),
    (4, 'HUDUMA NUMBER'),
    (5, 'MILITARY_ID')
]
ACCOUNT_STATUS=[
    (1, 'PENDING_VERIFICATION'),
    (1, 'ACTIVE'),
    (3, 'SUSPENDED'),
    (4, 'DEACTIVATED'),
]

class User(AbstractUser):
    id_type=models.IntegerField(choices=ID_TYPE, default=1)
    id_front = CloudinaryField("image")
    id_back = CloudinaryField("image")
    selfie = CloudinaryField("image")
    status= models.IntegerField(choices=ACCOUNT_STATUS, default=1)
    phone_number=models.CharField(max_length=255, null=True, blank=True)
    secondary_phone=models.CharField(max_length=255, null=True, blank=True)
    idNumber=models.CharField(max_length=255, null=True, blank=True)
    money_on_airtime=models.IntegerField(default=0)
    money_on_paybill=models.IntegerField(default=0)
    money_on_buy_goods=models.IntegerField(default=0)
    money_sent=models.IntegerField(default=0)
    total_money_spent=models.IntegerField(default=0)
    url= models.URLField(null=True)
    visibility=models.BooleanField(default=True)
