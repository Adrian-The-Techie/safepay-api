from django.urls import path, re_path

from payments import consumers

websocket_urlpatterns = [
    path("ws/<str:phone>", consumers.ChatConsumer.as_asgi())
]