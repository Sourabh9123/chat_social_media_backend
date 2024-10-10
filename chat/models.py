from django.db import models
import uuid
# Create your models here.
from account.models import User
from django.contrib.auth import get_user_model

User = get_user_model()





class Message(models.Model):
    id         = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sender     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages" )  
    receiver   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receive_messages" )  
    content    = models.TextField()
    video      = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    is_seen    = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    # seen_at = models.DateTimeField(null=True, blank=True, )

    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
            models.Index(fields=['created_at']),
        ]





    def __str__(self):
        return f"From -> {self.sender }  -> To ->  {self.receiver }" 


