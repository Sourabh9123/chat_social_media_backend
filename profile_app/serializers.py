from rest_framework import serializers
from profile_app.models import Profile, Follow
from account.serializers import UserSerializerGeneralInfo
from post_app.models import Post




class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    followers = UserSerializerGeneralInfo(many=True, read_only=True)
    following = UserSerializerGeneralInfo(many=True, read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True, method_name="get_full_name")
    total_post = serializers.SerializerMethodField(read_only=True, method_name="get_total_post")
    username = serializers.CharField(source="user.username")
    
    class Meta:
        model = Profile
        fields = [ 'user',
                  'username',
                   'bio',
                   'full_name',
                   'total_post',
                    'profile_picture',
                    'location', 
                    'created_at',
                    'followers',
                    'following', 
                    'updated_at', 
                    'followers_count',
                    'following_count']
        read_only_fields = ['created_at', 'updated_at', 'followers_count', 'following_count']


    def  get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name} " 
    

    def get_total_post(self, obj):
        return Post.objects.filter(author=obj.user).count()
    


class ProfileGeneralSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(source="user.username",  read_only=True)
    class Meta:
        model = Profile
        fields = ["user", "profile_picture",'username']




class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']