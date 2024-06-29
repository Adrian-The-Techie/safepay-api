from django.urls import path, re_path

from payments import consumers

websocket_urlpatterns = [
    re_path(r"^ws/(?P<room_name>[^/]+)", consumers.ChatConsumer.as_asgi())
]