# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from account.models import User
import jwt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from redis_services.user_status import get_online_users, set_online_user,remove_online_user
from account.serializers import UserSerializer
import time


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # WebSocket connection handshake
        room_id = "chat_room"
        self.room_group_name = f'chat_{room_id}' 
        print(time.time(), " -----------------------------")
        
        # print("--------------------------- scope consumer",self.scope)

        query_string = self.scope['query_string'].decode("utf-8")
        query_params = parse_qs(query_string)
        access_token = query_params.get("token")[0]
        user = await self.get_user(access_token)
        
        user_json = {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username" :user.username
        }
        
        set_online_user(user_json) # set the user online
    
        if user is None:
            await self.close()
            return

        self.scope["user"] = user

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(self.scope['user'])
        
        
        await self.accept()  # Accept the WebSocket connection
        print("accepted")
        online_user = get_online_users()
        # print("online users -------", online_user)
        print(list(online_user.keys()))
     
        await self.send(text_data=json.dumps({
                        "full_name" : str(user.first_name) + " " +str(user.last_name),
                        "email": user.email,
                          "id": str(user.id), }
                      ))

        

    async def disconnect(self, close_code):
        # Called when the WebSocket closes for any reason
        print("inside disconnect")
        user_id = self.scope["user"].id
        remove_online_user(user_id) # remove online user

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
       
        print(text_data)
        print(type(text_data))

        json_data = json.loads(text_data) # converting string data to json or dictionery
    
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': json_data['type'],  # Custom message type here type == chat_message
                'message': json_data['message'],
                "sender_id" : json_data['sender'],
                "receiver_id" : json_data['receiver'],
                
            }
        )


    @database_sync_to_async
    def get_user(self,token):    
       
        try:
            user_details = jwt.decode(token,settings.SECRET_KEY, algorithms=["HS256"])
            user_id = user_details.get("user_id")
    
            user =  User.objects.filter(id=user_id).first()
     
            return user
        except Exception as e:
            print("failed to get user ", str(e))
        



    async def chat_message(self, event):
        # Sends a message back to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps(message))

   