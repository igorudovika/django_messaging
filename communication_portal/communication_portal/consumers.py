import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WSConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)('render_updates_group', self.channel_name)
        self.accept()

    def send_message_to_frontend(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def disconnect(self, close_code):
        self.channel_layer.group_discard('render_updates_group', self.channel_name)
