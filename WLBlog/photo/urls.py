from django.urls import path

from photo import views

app_name = "photo"
urlpatterns = [
    path('photo-list', views.photo, name="photo_list"),
    path('add-new-photo', views.add_new_photo, name="add_new_photo"),   # 添加相册
    path('edit-photo-name', views.edit_photo, name="edit_photo"),   # 修改相册
    path('delete-photo', views.delete_photo, name="delete_photo"),  # 删除相册
    path('image-list', views.img_list, name="img_list"),     # 相册图片列表
    path('image-tile', views.img_tile, name="img_tile"),     # 平铺图片
    path('get-img-tile', views.get_img_tile, name="get_img_tile"),  # 平铺图片
    path('image-fall', views.img_fall, name="img_fall"),     # 瀑布流
    path('get-img-fall', views.get_img_fall, name="get_img_fall"),  # 瀑布流
    path('add-photo-img', views.add_photo_img, name="add_photo_img"),   # 上传图片
    path('delete_photo_img', views.delete_photo_img, name="delete_photo_img"),  # 删除图片
]
