from rest_framework.serializers import ModelSerializer
from account.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class UserSerializerGeneralInfo(ModelSerializer):
    profile_picture = serializers.URLField(source="profile.profile_picture", read_only=True)
    class Meta:
        model = User
        fields  = ['id',  "email", "first_name", "last_name", "username" ,"profile_picture"]



class UserSerializer(ModelSerializer):
    profile_picture = serializers.URLField(read_only=True, source="profile.profile_picture")
    class Meta:
        model = User
        # fields  = "__all__"
        fields  = ['id',  "email", "first_name", "last_name","username" ,"profile_picture", "password"]
        read_only_fields = ['username', "is_staff"  , "is_superuser"]
        # exclude = ['password']
        
        
        




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    
   


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()