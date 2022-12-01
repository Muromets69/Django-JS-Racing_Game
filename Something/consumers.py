import json

from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.db import database_sync_to_async
from .models import Newuser
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]
        self.room_group_name = "chat"
        name = self.scope["url_route"]["kwargs"]["user"]
        
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": f"{name} is connected!"}
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        name = self.scope["url_route"]["kwargs"]["user"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": f"{name} is disconnected!"}
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        user = self.scope["url_route"]["kwargs"]["user"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": f"{user}:{message}"}
        ) 
        
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
        
        
        
        
class GonkaCons(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self,pk):
        return Newuser.objects.get(pk=pk)
    
    @database_sync_to_async
    def get_user_car(self,pk):
        return Newuser.objects.get(pk=pk).car
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room"]
        self.room_group_name = "chat_%s" % self.room_name
        pk = self.scope["url_route"]["kwargs"]["pk"]
        user = await self.get_user(pk)
        car = await self.get_user_car(pk)
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message_gg", "message": 1,"name":car.name,"username":user.username,"lvl":user.ghoul_lvl,"engine":float(car.engine),"gear1":int(car.first),"gear2":int(car.second),"gear3":int(car.third),"gear4":int(car.fouth),"gear5":int(car.fivth),"gear6":int(car.max_speed)}
        )
        await self.accept()
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mess = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message_gg", "message": mess}
        ) 
        
    async def chat_message_gg(self, event):
        message = event["message"]
        eng = event['engine']
        gear1 = event['gear1']
        gear2 = event['gear2']
        gear3 = event['gear3']
        gear4 = event['gear4']
        gear5 = event['gear5']
        gear6 = event['gear6']
        lvl = event['lvl']
        username = event['username']
        carname = event['name']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,"name":carname,"username":username,"lvl":lvl,"engine":eng,"gear1":gear1,"gear2":gear2,"gear3":gear3,"gear4":gear4,"gear5":gear5,"gear6":gear6}))