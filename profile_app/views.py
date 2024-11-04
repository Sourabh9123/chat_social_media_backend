from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from profile_app.models import  Profile, Follow
from account.models import User
from django.contrib.auth import get_user_model
from profile_app.serializers import  ProfileSerializer , FollowSerializer, ProfileGeneralSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from django.db.models import Q , Exists, OuterRef




User = get_user_model()


class ProfileCreateListView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user =  request.user
        get_profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(get_profile)
        # print(serializer.data)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    

class GetOtherProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def  get(self, request, *args, **kwargs):
        current_user = request.user
        
        profile_of_user = kwargs.get('user_id')
        profile = get_object_or_404(Profile, user_id=profile_of_user)
        serializer = ProfileSerializer(profile)
        print(serializer.data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



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
        
        # print(followers, "followers")
        following = get_profile.following # people whom i follow
        # print(following, "followings")

        # print(serializer.data)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    




# this view is retriving onlu current user followers and followings
class FollowAPIView(GenericAPIView):

    """
    GET /follow/uuid:user_id/?type=followers    -- This URL fetches the list of followers of the user with user_id=3.

    GET /follow/uuid:user_id/?type=following     -- This URL fetches the list of users that the user with user_id=3 is following.

    POST /follow/uuid:user_id/
    Body: { "user_id": 4 }   This will make the authenticated user follow the user with user_id=4.

   
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve followers or following users."""
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        current_user = request.user

        
            

        if request.query_params.get('type') == 'followers':
            # Check if each follower is followed by the current user
            followers = Follow.objects.filter(following=user).annotate(
            is_followed_by_current_user=Exists(
                Follow.objects.filter(follower=current_user, following=OuterRef('follower'))
                    )
                )
            serializer = self.get_serializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.query_params.get('type') == 'following':
            # Check if each following user is followed by the current user
            following = Follow.objects.filter(follower=user).annotate(
            is_followed_by_current_user=Exists(
                Follow.objects.filter(follower=current_user, following=OuterRef('following'))
                    )
                )
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

  




class RemoveFollowerView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer


    def delete(self, request, *args, **kwargs):
        """Delete a follow relationship (unfollow a user)."""
        user_to_unfollow_id = kwargs.get('user_id')
        # print(user_to_unfollow_id,"------------------------")

        user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)
        # print(user_to_unfollow, "------------------------------")
        follower =  Follow.objects.filter(follower=user_to_unfollow, following=request.user)
        # print(follower, '-----------------------------------')
        # follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        if follower.exists():
            follower.delete()
            return Response({"detail": "Successfully Remove Follower the user."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You are not Follower this user."}, status=status.HTTP_400_BAD_REQUEST)


class UnfollowView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def delete(self, request, *args, **kwargs):
        """Delete a follow relationship (unfollow a user)."""
        user_to_unfollow_id = kwargs.get('user_id')
        # print(user_to_unfollow_id,"------------------------")

        user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)
        # print(user_to_unfollow, "------------------------------")
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        # print(follow)
        if follow.exists():
            follow.delete()
            return Response({"detail": "Successfully unfollowed the user."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)




class FollowSuggestionPagination(PageNumberPagination):
    page_size = 5  # Number of suggestions per page



# class FollowSuggestionView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProfileGeneralSerializer
#     pagination_class = FollowSuggestionPagination

#     def get(self, request, *args, **kwargs):
#         user = request.user  # Get the current authenticated user
#         following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
#         suggestions = Profile.objects.exclude(Q(user__id__in=following_ids) | Q(id=user.id)).select_related('user')


#         # Apply pagination
#         page = self.paginate_queryset(suggestions)
#         if page is not None:
#             serializer = self.get_paginated_response(self.get_serializer(page, many=True).data)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         # In case there's no pagination applied, return all (which shouldn't happen with the setup)
#         serializer = self.get_serializer(suggestions, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    


class FollowSuggestionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileGeneralSerializer
    pagination_class = FollowSuggestionPagination

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the current authenticated user
        following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        
        # Start with the suggestions that exclude followed and current users
        suggestions = Profile.objects.exclude(Q(user__id__in=following_ids) | Q(id=user.id)).select_related('user').order_by('?')

        # Get the search query from the request
        search_query = request.query_params.get('search', None)

        # Apply search filtering if there's a search query
        if search_query:
            suggestions = Profile.objects.filter(
                Q(user__username__icontains=search_query) 
                # | Q(user__first_name__icontains=search_query) 
                # | Q(user__last_name__icontains=search_query) 
                #| Q(bio__icontains=search_query)  # Add more fields as needed
            )
            # print(suggestions)
            suggestions = suggestions.annotate(
                    is_following=Exists(
                        Follow.objects.filter(follower=user, following=OuterRef('user'))
                    )
                )

            # print(suggestions.is_following, " ---------------------------")
           
            serializer = ProfileGeneralSerializer(suggestions, many=True)
            base_url = "http://127.0.0.1:8000"
            for i in serializer.data:  
                i['profile_picture'] = base_url+i['profile_picture']

            
            
            return  Response({
            "count": 0,
            
            "next": "http://127.0.0.1:8000/api/profile/suggestion/?page=1",
            "previous": None,
            "results": serializer.data
            # 
            }, status=status.HTTP_200_OK)

        # Apply pagination
        page = self.paginate_queryset(suggestions)
        if page is not None:
            serializer = self.get_paginated_response(self.get_serializer(page, many=True).data)
            # print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # In case there's no pagination applied, return all (which shouldn't happen with the setup)
        serializer = self.get_serializer(suggestions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class OthersFollowers(GenericAPIView):
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
    
        current_user = request.user
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        followers = Follow.objects.filter(following=user)
        
        # Add an extra field to check if each follower is followed by the current user
        followers_data = []
        for follower in followers:
            follower_data = FollowSerializer(follower).data
            follower_user = follower.follower
            # print(follower_user.profile.profile_picture, "this is profile -------------------------")
            BASE_URL = "http://localhost:8000/media/"
            # follower_data['profile_picture'] = BASE_URL + str(follower_user.profile.profile_picture)
            follower_data['profile_picture'] = str(follower_user.profile.profile_picture)
            follower_data['user_id'] = str(follower_user.id)
            follower_data['is_followed_by_current_user'] = Follow.objects.filter(follower=current_user, following=follower_user).exists()
            followers_data.append(follower_data)
    
        return Response({"followers": followers_data}, status=status.HTTP_200_OK)
    


class OtherFollowings(GenericAPIView):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        followings = Follow.objects.filter(follower=user)
        

        followings_data = []
        for following in followings:
            following_data = FollowSerializer(following).data
            following_user = following.following
        
            # following_data['profile_picture'] = following_user.
            following_data['user_id'] = str(following_user.id)
            following_data['profile_picture'] = str(following_user.profile.profile_picture)
            following_data['is_followed_by_current_user'] = Follow.objects.filter(follower=current_user, following=following_user).exists()
            followings_data.append(following_data)

        return Response({"followings": followings_data}, status=status.HTTP_200_OK)


        
        


# class FollowerAndFollowingsCountView(GenericAPIView):
    
#     serializer_class = FollowSerializer

#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get('user_id')
#         user = get_object_or_404(User, id= user_id)
#         if request.query_params.get('type') == 'followers':
#             count = Follow.objects.filter(following=user).count()
#             return Response ({"numbers_of_followers":str(count)}, status=status.HTTP_200_OK)
#         elif request.query_params.get('type') == 'following':
#             count = Follow.objects.filter(follower=user).count()
#             return Response ({"numbers_of_followings":str(count)}, status=status.HTTP_200_OK)
#         return Response({"Error":"Something Went Wrong"}, status=status.HTTP_200_OK)






# class FollowAndFollowingOthers(GenericAPIView):
#     serializer_class = FollowSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         current_user = request.user

#         """Retrieve followers or following users."""
#         user_id = kwargs.get('user_id')
#         user = get_object_or_404(User, id=user_id)

#         if request.query_params.get('type') == 'followers':
#             # Check if each follower is followed by the current user
#             followers = Follow.objects.filter(following=user).annotate(
#             is_followed_by_current_user=Exists(
#                 Follow.objects.filter(follower=current_user, following=OuterRef('follower'))
#                     )
#                 )
#             serializer = self.get_serializer(followers, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         elif request.query_params.get('type') == 'following':
#             # Check if each following user is followed by the current user
#             following = Follow.objects.filter(follower=user).annotate(
#             is_followed_by_current_user=Exists(
#                 Follow.objects.filter(follower=current_user, following=OuterRef('following'))
#                     )
#                 )
#             serializer = self.get_serializer(following, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response({"detail": "Invalid request. Provide type=followers or type=following in query params."}, 
#                         status=status.HTTP_400_BAD_REQUEST)




# class ProfileListView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProfileGeneralSerializer
#     queryset = Profile.objects.all()
#     filter_backends = [SearchFilter]
#     search_fields = ['bio', 'location', 'user__first_name', 'user__last_name', 'username']


#     def get(self, request, *args, **kwargs):
#         # Get the filtered queryset
#         queryset = self.filter_queryset(self.get_queryset())

#         # Serialize the data
#         serializer = self.get_serializer(queryset, many=True)

#         # Return the serialized data as a response
#         return Response(serializer.data)
