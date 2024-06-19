from django.urls import path
from . import views

urlpatterns=[
    path("transact", views.send, name="transact"),
    path("result", views.result, name="result"),
    path("fee", views.getFees, name="fee"),
    path("filter", views.getTransactions, name="filter"),
    path("update", views.update, name="update"),
]