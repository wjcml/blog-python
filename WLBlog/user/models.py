from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.utils.timezone import now

MALE, FEMALE = 1, 2
SEX = (
    (MALE, "男"),
    (FEMALE, "女"),
)

UNREAD, READ = 0, 1
IS_READ = (
    (UNREAD, "未读"),
    (READ, "已读")
)


class AvatarImg(models.Model):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', verbose_name='头像')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_avatar_img'
        managed = False
        verbose_name = '头像'
        verbose_name_plural = verbose_name


class User(AbstractUser):
    name = models.CharField(max_length=20, verbose_name='昵称')
    birth = models.DateField(null=True, blank=True, verbose_name='生日')
    sex = models.IntegerField(choices=SEX, default=1, verbose_name='性别')
    phone = models.CharField(max_length=11, verbose_name='电话')
    Introduction = models.CharField(max_length=200, verbose_name='简介')
    avatar = models.ForeignKey(AvatarImg, on_delete=models.CASCADE, verbose_name='头像')
    password = models.CharField(max_length=16, verbose_name='密码')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_user'
        managed = False
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# 用户信息
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    summary = models.CharField(max_length=2000, blank=True, null=True, verbose_name="摘要")
    school = models.CharField(max_length=100, blank=True, null=True, verbose_name="学校")
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name="籍贯")
    github = models.URLField(max_length=500, blank=True, null=True, verbose_name="github账号")
    interests = models.CharField(max_length=500, blank=True, null=True, verbose_name="兴趣")
    skill = models.CharField(max_length=500, blank=True, null=True, verbose_name="技能")
    email = models.EmailField(max_length=500, blank=True, null=True, verbose_name="Email")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_user_information'
        managed = False
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 订阅/关注
class Attention(models.Model):
    follower = models.ForeignKey(User, related_name="user_follower", on_delete=models.CASCADE, verbose_name="关注人")
    attentor =models.ForeignKey(User, related_name="user_attentor", on_delete=models.CASCADE, verbose_name="被关注人")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_attention'
        managed = False
        verbose_name = '关注'
        verbose_name_plural = verbose_name


# 留言
class UserLeave(models.Model):
    leaver = models.ForeignKey(User, related_name="leaver_user", on_delete=models.CASCADE, verbose_name="留言人")
    leaved_person = models.ForeignKey(User, related_name="leaved_user", on_delete=models.CASCADE, verbose_name="被留言的人")
    leave_body = models.CharField(max_length=2000, verbose_name="留言内容")
    is_read = models.IntegerField(choices=IS_READ, default=0, verbose_name="是否已读")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_user_leave'
        managed = False
        verbose_name = '留言'
        verbose_name_plural = verbose_name
