from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from django.dispatch import receiver
from .models import Notification
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

"""

Channel layer configured in settings
Channel group name for a user is the combination of username and user id
For eg : ram_1
User identified from scope that uses AuthMiddlewareStack configured in asgi.py
Uses AsyncWebSocketConsumer 
Group recieves message from model and in turn sent to client websocket

"""    
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = self.user.username + '_' + str(self.user.id)

        if (self.user.is_superuser):
            await self.accept()

            # Join admin_group group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

   
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass      

    async def admin_notify(self,event):
        await self.send(event['data'])    


  
  



