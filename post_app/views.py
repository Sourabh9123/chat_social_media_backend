from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserSerializer, UserSerializerGeneralInfo
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import  IsAuthenticated

from post_app.models import (
    Post, 
    Comment,
    Like,
    Block,
    SavedPost
)
from post_app.serializers import (
    PostCreateSerializer,
    SavedPostSerializer,
    PostListSerializer ,
    CommentSerializer,
    BlockSerializer,
    LikeSerializer,
    

)







class PostPagination(PageNumberPagination):
    page_size = 5  # Customize the number of posts per page
    page_size_query_param = 'page_size'
    max_page_size = 10




class PostListCreateView(GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # current_user = User.objects.get(email="a@a.com")
        current_user = request.user
        blocked_by_user = Block.objects.filter(blocker=current_user).values_list('blocked', flat=True)
        blocked_user_ids = Block.objects.filter(blocked=current_user).values_list('blocker', flat=True)
        blocked_users = list(blocked_by_user) + list(blocked_user_ids)
   

        # instance = self.get_queryset()
        # instance = self.get_queryset().exclude(author__in=blocked_users).order_by("-created_at")

        # instance_ = Post.objects.prefetch_related('likes', 'comments', 'author__saved_posts').order_by('-created_at')
        # instance_ = Post.objects.select_related('author') \
        #             .prefetch_related('likes', 'comments', 'author__saved_posts') \
        #             .order_by('-created_at')

        instance_ = (Post.objects.select_related('author')  
                    .prefetch_related('likes', 'comments', 'author__saved_posts')  
                    .order_by('-created_at'))

        
        page = self.paginate_queryset(instance_)

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data) # Return paginated response


        serializer = self.get_serializer(instance_ , many=True,context={'request': request})

        return Response({"data": serializer.data},  status=status.HTTP_200_OK )


    def post(self, request,*args, **kwargs):
        
        # will get user by token send from frontend
        user = request.user
        serializer = PostCreateSerializer(data=request.data)
        # print("user requested ------------------- ", user)
        # print(request.data)

        
        if  serializer.is_valid():
            
            data = serializer.validated_data
            
            post = Post.objects.create(
                title  = data['title'],
                image  = data.get('image', ''), 
                author = user
                                )
            print("objects created ---------", post)
            post_serializer = PostCreateSerializer(post)
       


            return Response({"data": post_serializer.data},  status=status.HTTP_201_CREATED )
        return  Response({"data": serializer.errors},  status=status.HTTP_400_BAD_REQUEST )
        return Response({"data": "data"},  status=status.HTTP_200_OK )
    



class PostDetailView(GenericAPIView):

    serializer_class = PostListSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
      
        post = Post.objects.get(id=post_id)
        serializer = PostListSerializer(post)  

        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

      
    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = Post.objects.get(id=post_id)
        return Response({"data":"No Content "}, status=status.HTTP_204_NO_CONTENT)

      
        

    def put(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        data = request.data
        instance = Post.objects.get(id=post_id)
        serializer = PostCreateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"data":"No Content "}, status=status.HTTP_400_BAD_REQUEST)










class CommentListCreateView(GenericAPIView):
    serializer_class = CommentSerializer
    
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id") # here we need to query all comments of single post
        comment = Comment.objects.filter(post_id=post_id)
        serializer = self.serializer_class(comment, many=True)
        
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        data = {} 
        print("-----------------------------------------------------")
        post_id = kwargs.get("post_id")
        user = request.user # will get the user from access token
        post = Post.objects.get(id=post_id)  
        text = request.data
        actual_comment = text['text']

        comment = Comment.objects.create(
                user = user,
                post = post ,
                text = actual_comment
                
        )
    
        

        serializer = CommentSerializer(comment)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    


class CommentDetailView(GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        # print(request.data, " ------------data")
        comment = get_object_or_404(Comment, id=comment_id)

        user = request.user
        if Comment.user == user:
            serializer = CommentSerializer(comment, data=request.data)
            return Response({"success":   "success"})
        
    def put(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        # print(request.data, " ------------data")
        comment = get_object_or_404(Comment, id=comment_id)

        user = request.user
       
        if comment.user == user:
            if  request.data.get("text") == " " or request.data.get("text") == "":
                return Response({"success":   "comment should not be blank"})
            comment.text = request.data.get("text", comment.text)
            comment.save()
            serializer = CommentSerializer(comment)

            return Response({"success":  serializer.data}, status=status.HTTP_200_OK)
        return Response({"data" : "You Do not have permission"}, status=status.HTTP_401_UNAUTHORIZED)
    
        
        
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")

        user = request.user
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == user:
            comment.delete()
            return Response({"success": "success"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"data" : "You Do not have permission"}, status=status.HTTP_401_UNAUTHORIZED)
    






class LikeListCreateView(GenericAPIView):
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        data = {}
        post = get_object_or_404(Post, id=post_id)
        users_who_liked = post.likes.values_list('user' ,flat=True)
        
        users = User.objects.filter(id__in=users_who_liked)
       
        serialized_users = UserSerializerGeneralInfo(users, many=True)
        data['users'] = serialized_users.data
        data['total_likes'] = users.count()
      
        return Response({"data":data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        user = request.user # will come from token
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user = user,
            post = post,
    
        )
        
        if not created:
            like.delete()
    
            return Response({"data":"like Removed"}, status=status.HTTP_200_OK)
        serializer = LikeSerializer(like)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
            




class BlockUserListCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = BlockSerializer


    def get(self, request, *args, **kwargs):
        user = request.user
        # user = get_object_or_404(User, email="a@a.com")
        instance  = Block.objects.filter(blocker=user)
        if not instance:
            return Response( {"blocked users" : "You Haven't Blocked Anyone Yet."}, status=status.HTTP_200_OK)

        serializer  =  BlockSerializer(instance, many=True)
        # print(serializer.data)
        return Response( {"blocked users" : serializer.data}, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, email="a@a.com")
        data  = request.data
     
        if "blocked" in data:
            user_to_blocked = get_object_or_404(User, id=data['blocked'])
            block, created = Block.objects.get_or_create(
                blocker=user,
                blocked=user_to_blocked
            )
            if not created:
                return Response( {"blocked users" : "You have Already Blocke This User"}, status=status.HTTP_200_OK)

            serializer = BlockSerializer(block)

            return Response( {"blocked users" : serializer.data}, status=status.HTTP_200_OK)
        
        return Response( {"blocked users" : "invalid data from request body"}, status=status.HTTP_400_BAD_REQUEST)
            

        

class BlockUserDetailView(GenericAPIView):
    pagination_class = []
    serializer_class = BlockSerializer

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")

        user =  get_object_or_404(User, email="a@a.com")

        user_to_unblock = get_object_or_404(User, id=user_id)
        block = Block.objects.filter(
            blocker=user,
            blocked=user_to_unblock,
        )
        if block.exists():
            block.delete()
            return Response( {"data" : "success user unblocked"}, status=status.HTTP_200_OK)
            
        
        return Response( {"data" : "User was not blocked"}, status=status.HTTP_400_BAD_REQUEST)

            























class PostSavedListCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SavedPost.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user 
        qs = SavedPost.objects.filter(user=user)
        serializer = SavedPostSerializer(qs, many=True)
        return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        user = request.user 
        post_id = request.data.get("post_id")
        instance, created = SavedPost.objects.get_or_create(
            user=user,
            post_id = post_id
        )
        if not created:
            instance.delete()
            return Response({"data" :"remove"}, status=status.HTTP_200_OK)
        serializer = SavedPostSerializer(instance)
        return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
    

class GetPostPicturesListView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer

    def get(self, request, *args, **kwargs):
        return Response({"data":"data"}, status=status.HTTP_200_OK)