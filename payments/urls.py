from django.urls import path
from . import views

urlpatterns=[
    path("disburse", views.disburse, name="disburse")
]