import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        url = self.scope["url_route"]["kwargs"]["room_name"]
        
        self.room_group_name = url

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({"status":2, "message": "Transaction initiated. STK Push has been initiated. Please enter your M-PESA pin to finish transaction"}))

    def disconnect(self, close_code):
        pass

    def send_message_to_frontend(self, data):
        self.send(json.dumps(data['message']))