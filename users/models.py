from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #CASCADE,유저가 삭제되면 프로필도 삭제
    nickname = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    subjects = models.CharField(max_length=128)
    image = models.ImageField(upload_to='profile/', default='default.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)