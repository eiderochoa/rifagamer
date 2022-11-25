from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class WSConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("prgbar", self.channel_name)
        self.accept()
        self.send(json.dumps({'message':'Ready to show progress'}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("prgbar", self.channel_name)

    def chat_message(self, event):
        print("EVENT TRIGERED")
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'prgbarupdate',
            'message': event['message'],
            'status': event['status'],
            'end':event['end']
        }))
