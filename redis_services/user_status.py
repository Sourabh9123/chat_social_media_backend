from redis_services.redis_client import redis_client
import json



def get_online_users():
    users = redis_client.get("online_user")
    # if users is None:
    #     return {}
    return json.loads(users) if users else {}



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




















### online user logic

# redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)


# def get_online_users():
#     users = redis_client.get("online_user")
#     # if users is None:
#     #     return {}
#     return json.loads(users) if users else {}


# def set_online_user(user_json):
   
#     online_users = get_online_users()  
#     if not online_users:
#         print("No user is currently online")

  
#     online_users[str(user_json['id'])] = user_json
   
#     redis_client.set('online_user', json.dumps(online_users))

    
# def remove_online_user(user_id):
#     online_users = get_online_users() 
#     if online_users is None:
#         return  print(f"None User is Online")
    
#     if str(user_id) in online_users:
#         del online_users[str(user_id)] 
#         redis_client.set('online_user', json.dumps(online_users))  
#         print(f"User {user_id} removed from online users.")
#     else:
#         print(f"User {user_id} not found in online users.")


### online user logic ends
