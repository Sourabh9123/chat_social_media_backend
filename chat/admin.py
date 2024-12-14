from django.contrib import admin
from chat.models import Message

class MessageAdmin(admin.ModelAdmin):
    # print(Message._meta.fields)
    list_display = [field.name for field in Message._meta.fields if not field.name =="content"] # this will show all fields 
    list_display_links =["sender", "receiver" ,"id"]

admin.site.register(Message, MessageAdmin)