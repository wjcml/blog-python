from django.db import models

# Create your models here.
# 相册
from user.models import User


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    photo_name = models.CharField(max_length=200, verbose_name="相册名")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_photo'
        managed = False
        verbose_name = '相册'
        verbose_name_plural = verbose_name


class PhotoImg(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="相册")
    title = models.CharField(max_length=200, verbose_name="图片标题")
    img_url = models.ImageField(upload_to='photo/%Y/%m/%d', verbose_name="图片地址")
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name="描述")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_photo_img'
        managed = False
        verbose_name = '相册图片'
        verbose_name_plural = verbose_name
