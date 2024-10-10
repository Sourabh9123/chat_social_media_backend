from rest_framework import serializers
from profile_app.models import Profile
from account.serializers import UserSerializerGeneralInfo
from post_app.models import Post




class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    followers = UserSerializerGeneralInfo(many=True, read_only=True)
    following = UserSerializerGeneralInfo(many=True, read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True, method_name="get_full_name")
    total_post = serializers.SerializerMethodField(read_only=True, method_name="get_total_post")
    
    class Meta:
        model = Profile
        fields = [ 'user',
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
    
