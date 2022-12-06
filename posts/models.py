from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')   #auther와 likes 둘다 User를 참조하기 때문에 related_name을 지정해서 구분해줘야함
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    body = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.png')
    likes = models.ManyToManyField(User, related_name='like_posts', blank=True)
    published_date = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()