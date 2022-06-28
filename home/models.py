from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class User_register(models.Model):
#     user_name = models.CharField(max_length=50)
#     uder_id = models.CharField(max_length=50)
#     pub_date = models.DateTimeField('date registered')
    
# class User_bookmarked(models.Model)

# AbstractUser 모델 상속
class User(AbstractUser):
    nickname = models.CharField(max_length=10)
    # 관심 질환 및 관심 기관
    disease = models.CharField(max_length=10, null=True, default='')
    organ = models.CharField(max_length=10, null=True, default='')
   

class TimeStamedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract= True
    
    
class Post(TimeStamedModel):
    author = models.ForeignKey(
        User, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='post_author'
    )
    category = models.CharField(max_length=20)
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
    dislikes = models.ManyToManyField(User, related_name='post_dislikes')
    
    
class Comment(TimeStamedModel):
    author = models.ForeignKey(
        User, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='comment_author'
    )
    posts = models.ForeignKey(
        Post, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='comment_post'
    )
    content = models.TextField(blank=True)