from rest_framework.serializers import ModelSerializer
from account.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class UserSerializerGeneralInfo(ModelSerializer):
    class Meta:
        model = User
        fields  = ['id',  "email", "first_name", "last_name",]



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields  = "__all__"
        # fields  = ['id',  "email", "first_name", "last_name",   "is_staff" ,  "is_superuser"]
        exclude = ['password']
        
        




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    
   


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()