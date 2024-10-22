from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from profile_app.models import  Profile, Follow
from account.models import User
from django.contrib.auth import get_user_model
from profile_app.serializers import  ProfileSerializer , FollowSerializer
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
    



class UserProfileDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
     
        get_profile = get_object_or_404(Profile, user_id=user_id)
        serializer = ProfileSerializer(get_profile)
        followers = get_profile.followers # mine followers  people who follow me 
        user_follow = request.user.following.all()
        # print(user_follow)
        # for user in user_follow:
        #     print(user.id)
        
        print(followers, "followers")
        following = get_profile.following # people whom i follow
        print(following, "followings")

        # print(serializer.data)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    




class FollowAPIView(GenericAPIView):

    """
    GET /follow/3/?type=followers    -- This URL fetches the list of followers of the user with user_id=3.

    GET /follow/3/?type=following     -- This URL fetches the list of users that the user with user_id=3 is following.

    POST /follow/3/
    Body: { "user_id": 4 }   This will make the authenticated user follow the user with user_id=4.

    DELETE /follow/3/
    Body: { "user_id": 4 }  This will make the authenticated user unfollow the user with user_id=4.

    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve followers or following users."""
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if request.query_params.get('type') == 'followers':
            followers = Follow.objects.filter(following=user)
            serializer = self.get_serializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.query_params.get('type') == 'following':
            following = Follow.objects.filter(follower=user)
            serializer = self.get_serializer(following, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid request. Provide type=followers or type=following in query params."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """Create a follow relationship (follow another user)."""
        user_to_follow_id = request.data.get('user_id')
        user_to_follow = get_object_or_404(User, id=user_to_follow_id)

        if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(follower=request.user, following=user_to_follow)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Delete a follow relationship (unfollow a user)."""
        user_to_unfollow_id = request.data.get('user_id')
        user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)

        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        if follow.exists():
            follow.delete()
            return Response({"detail": "Successfully unfollowed the user."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
