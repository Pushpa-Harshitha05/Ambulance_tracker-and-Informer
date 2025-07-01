import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.hospital_id = self.scope['url_route']['kwargs']['hospital_id']
        self.room_group_name = f"hospital_{self.hospital_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_notification',
                'message': f"Ambulance incoming for {data['emergency']} at location ({data['latitude']}, {data['longitude']})"
            }
        )
    
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
