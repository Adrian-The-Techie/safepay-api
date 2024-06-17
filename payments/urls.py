from django.urls import path
from . import views

urlpatterns=[
    path("transact", views.send, name="transact"),
    path("result", views.result, name="result"),
    path("filter", views.getTransactions, name="filter"),
]