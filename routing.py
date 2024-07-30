from django.urls import path, re_path
from django.conf.urls import url

from payments import consumers

websocket_urlpatterns = [
    url(r"^ws/(?P<room_name>[^/]+)", consumers.ChatConsumer)
]