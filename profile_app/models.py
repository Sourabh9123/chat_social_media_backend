from django.db import models
from django.contrib.auth import get_user_model
from account.models import User

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,blank=True, null=True)  # Link to the User model
    bio = models.TextField(max_length=150, blank=True)  # Short bio, similar to Instagram
    profile_picture = models.ImageField(upload_to='profile_pictures/', default="profile_pictures/fabrice-villard-Jrl_UQcZqOc-unsplash.jpg", blank=True, null=True)  # Profile picture
    location = models.CharField(max_length=100, blank=True)  # Location (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # When the profile was created
    updated_at = models.DateTimeField(auto_now=True)  # When the profile was last updated

    def __str__(self):
        return f"{self.user.email}'s profile"



    @property
    def followers(self):
        """Get all followers of the user."""
   
        followers = User.objects.filter(following__following=self.user).distinct()
        return followers
        # return User.objects.filter(followers__following=self.user).exclude(id=self.user.id)

    @property
    def following(self):
        """Get all users that the user is following."""
   
        followings = User.objects.filter(followers__follower=self.user).distinct()
        return followings
        # return User.objects.filter(following__follower=self.user).exclude(id=self.user.id)
        # return User.objects.filter(following__follower=self.user)
    

    @property
    def followers_count(self):
        """Get all followers of the user."""
        return User.objects.filter(followers__following=self.user).count()

    @property
    def following_count(self):
        """Get all users that the user is following."""
        return User.objects.filter(following__follower=self.user).count()

   




class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)# User who follows
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE) # User being followed
    created_at = models.DateTimeField(auto_now_add=True)  # When the follow relationship was created
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('follower', 'following')  # Ensure unique relationships

    def __str__(self):
        return f"{self.follower.email} follows {self.following.email}"


    """A follower is a user who subscribes to another user’s updates.
    For example, if User A follows User B, then User A is a follower of User B.

    #
    Following refers to the users that a particular user subscribes to.
    Continuing with the example, if User A follows User B, then User B is 
    someone that User A is following.
    
    """

