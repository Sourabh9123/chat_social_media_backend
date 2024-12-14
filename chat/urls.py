from django.urls import path
from chat.views import UserChatHistoryView

urlpatterns = [
    path("", UserChatHistoryView.as_view(), name="user-chats"),
]

