from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from sportsblog import settings



static_storage = FileSystemStorage(location=settings.STATICFILES_DIRS[0])

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png', storage=static_storage)

class TeamProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True) 
    def user_can_modify(self, user):
        return user == self.author or user.is_superuser 

class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    def user_can_modify(self, user):
        return user == self.author or user.is_superuser


