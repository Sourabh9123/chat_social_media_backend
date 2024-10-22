from django.urls import path
from profile_app.views import ProfileCreateListView ,UserProfileDetails, FollowAPIView


urlpatterns = [
    path("",ProfileCreateListView.as_view(), name="user-profile" ),
    path("details/<uuid:user_id>/",UserProfileDetails.as_view(), name="user-profile-details" ),
    path('follow/<uuid:user_id>/', FollowAPIView.as_view(), name='follow-api'),

    
]
