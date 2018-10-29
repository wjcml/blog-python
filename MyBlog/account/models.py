from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    birth = models.DateField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)

class Follow(models.Model):
    follow = models.ForeignKey(User, related_name="follow_user", on_delete=models.CASCADE)
    fan = models.ForeignKey(User, related_name="fan_user", on_delete=models.CASCADE)

    def __str__(self):
        return "follow:{},fan:{}".format(self.follow, self.fan)