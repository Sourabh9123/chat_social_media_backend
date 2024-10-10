from django.urls import path
from profile_app.views import ProfileCreateListView


urlpatterns = [
    path("",ProfileCreateListView.as_view(), name="user-profile" ),
]
