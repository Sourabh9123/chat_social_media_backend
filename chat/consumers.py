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
import redis
from account.serializers import UserSerializer


User = get_user_model()

### online user logic

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)


def get_online_users():
    users = redis_client.get("online_user")
    if users is None:
        return {}
    return json.loads(users)


def set_online_user(user_json):
   
    online_users = get_online_users()  
    if not online_users:
        print("No user is currently online")

  
    online_users[str(user_json['id'])] = user_json
   
    redis_client.set('online_user', json.dumps(online_users))

    
def remove_online_user(user_id):
    online_users = get_online_users() 
    if online_users is None:
        return  print(f"None User is Online")
    
    if str(user_id) in online_users:
        del online_users[str(user_id)] 
        redis_client.set('online_user', json.dumps(online_users))  
        print(f"User {user_id} removed from online users.")
    else:
        print(f"User {user_id} not found in online users.")


### online user logic ends


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # WebSocket connection handshake
        room_id = "video_call"
        self.room_group_name = f'chat_{room_id}' 
     
        query_string = self.scope['query_string'].decode("utf-8")
        query_params = parse_qs(query_string)
        access_token = query_params.get("token")[0]
        user = await self.get_user(access_token)
        
        user_json = {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
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
     
        await self.send(text_data=json.dumps({
                        "full_name" : str(user.first_name) + " " +str(user.last_name),
                        "email": user.email,
                          "id": str(user.id), }
                      ))

        

    async def disconnect(self, close_code):
        # Called when the WebSocket closes for any reason
        print("inside disconnect")
        user_id = self.scope["user"].id
        remove_online_user(user_id)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
       

        json_data = json.loads(text_data)
    
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # Custom message type
                'message': text_data['message'],
                "sender_id" : text_data['sender'],
                "receiver_id" : text_data['receiver'],
                
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


        await self.send(text_data=message)

   