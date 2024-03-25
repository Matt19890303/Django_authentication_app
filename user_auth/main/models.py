from django.db import models
from django.contrib.auth.models import User

User.add_to_class('is_banned', models.BooleanField(default=False))

# Need to creat a relationship between posts and user so we know which user made which post
class Post(models.Model):
    # If this user is deleted the post will be too
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_author_name(self):
        return self.author.username

    def __str__(self):
        return self.title + "\n" + self.description

