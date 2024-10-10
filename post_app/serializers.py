from rest_framework import serializers

from post_app.models import ( Post, Comment,
                              Like , Block,
                              SavedPost,
                             )
from account.serializers import UserSerializerGeneralInfo
from django.db.models import Count, Exists, OuterRef





class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializerGeneralInfo(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user','post', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = UserSerializerGeneralInfo(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "text",
            "post",
            "replies",
            "created_at",
        ]


    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostCreateSerializer(serializers.ModelSerializer):
    author = UserSerializerGeneralInfo(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post', 'saved_at', ]
        read_only_fields = ['saved_at']



class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializerGeneralInfo(read_only=True)  # Author details
    likes = LikeSerializer(many=True, read_only=True)  # Nested likes
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    saved_post = serializers.SerializerMethodField(method_name="get_saved_post")
    

    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'image', 'created_at', 'updated_at',
            'total_likes', 'total_comments', 'likes', 'comments','saved_post','draft',
        ]
       

    def get_total_likes(self, obj):
        return obj.total_likes
    
    def get_total_comments(self, obj):
        return obj.total_comments
   
    
    def get_saved_post(self, obj):
        # Get the user from the request context
        user = self.context['request'].user
  
        if user.is_authenticated:
            print(user, " -----user")
            return SavedPost.objects.filter(user=user, post=obj).exists()
        return False

    # @staticmethod
    # def get_queryset(user):
    #     # Efficiently fetch all the required data using select_related, annotate, and Exists
    #     saved_posts = SavedPost.objects.filter(user=user, post=OuterRef('pk'))
        
    #     return Post.objects.prefetch_related('likes', 'comments', 'author__saved_posts') \
    #         .select_related('author') \
    #         .annotate(
    #             total_likes=Count('likes'),
    #             total_comments=Count('comments'),
    #             saved_post=Exists(saved_posts)
    #         ).order_by('-created_at')

    # total_likes = serializers.IntegerField()
    # total_comments = serializers.IntegerField()
    # saved_post = serializers.BooleanField()



class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['blocker', 'blocked', 'blocked_at']
        read_only_fields = ['blocker', 'blocked_at']




class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']