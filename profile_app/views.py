from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from profile_app.models import  Profile
from account.models import User
from django.contrib.auth import get_user_model
from profile_app.serializers import  ProfileSerializer
from rest_framework.response import Response
from rest_framework import status






User = get_user_model()


class ProfileCreateListView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user =  request.user
        get_profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(get_profile)
        # print(serializer.data)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    

    
