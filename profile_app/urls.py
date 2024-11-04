from django.urls import path
from profile_app.views import ( ProfileCreateListView 
                                ,UserProfileDetails,
                                  FollowAPIView,
                                  RemoveFollowerView,
                                  UnfollowView,
                                  FollowSuggestionView,
                                  GetOtherProfileView,
                                  OthersFollowers,
                                  OtherFollowings
)

urlpatterns = [
    path("",ProfileCreateListView.as_view(), name="user-profile" ),
    path("other/<uuid:user_id>/",GetOtherProfileView.as_view(), name="other-user-profile" ),
    path("details/<uuid:user_id>/",UserProfileDetails.as_view(), name="user-profile-details" ),
    path('follow/<uuid:user_id>/', FollowAPIView.as_view(), name='follow-api'),
    path('remove/follower/<uuid:user_id>/',RemoveFollowerView.as_view(),name='remove-follower'),
    path('unfollow/<uuid:user_id>/',UnfollowView.as_view(),name='unfollow'),
    path('suggestion/',FollowSuggestionView.as_view(), name="suggestion"),
    path('other/user/followers/<uuid:user_id>/', OthersFollowers.as_view(), name='other-follower'),
    path('other/user/followings/<uuid:user_id>/', OtherFollowings.as_view(), name='other-following'),

    
]
