from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    pass

class Posts(models.Model):
    postuser = models.ForeignKey("User", on_delete=models.CASCADE, related_name="postuser")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="likes")

    def serialize(self):
        return{
            "id": self.id,
            "author": self.postuser.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.id for user in self.likes.all()]

        }
class Follow(models.Model):
    fuser = models.OneToOneField("User", on_delete=models.CASCADE, null=True, related_name="fuser")
    following = models.ManyToManyField("User", blank=True, related_name="following")
    followed = models.ManyToManyField("User", blank=True, related_name="follower")