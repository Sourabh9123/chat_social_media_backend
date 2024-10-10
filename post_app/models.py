from django.db import models
from account.models import User
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Post(models.Model):
    id         = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) 
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    title      = models.TextField()
    image      = models.ImageField(upload_to="posts/images", null=True, blank=True)
    draft      = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def total_likes(self):
        return self.likes.count()
    @property
    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return f"posted by - > {self.author}" 
    

    

    

class Like(models.Model):
    id   = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Comment(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    post        = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text        = models.TextField()
    parent      = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} -> {self.text[:20]}"
    
    @property
    def is_reply(self):
        return self.parent is not None
    




class Block(models.Model):
    id   = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False) 
    blocker = models.ForeignKey(User, related_name='blocker', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')  

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
    




class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # To ensure the user can't save the same post multiple times

    def __str__(self):
        return f"{self.user.email} saved {self.post.title}"
    






