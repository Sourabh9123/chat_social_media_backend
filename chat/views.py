from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import Message
from django.contrib.auth import get_user_model
from account.models  import User
from chat.serializers import MessageSerializer

from django.db.models import Q



User = get_user_model()

class UserChatHistoryView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        qs = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-created_at')
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

