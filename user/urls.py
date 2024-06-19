from django.urls import path
from . import views

urlpatterns=[
    path("", views.UserView.as_view(), name="user_view"),
    path("login/", views.login, name="login"),
    path("home", views.getHomeData, name="home")
]