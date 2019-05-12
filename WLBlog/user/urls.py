from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.one, name='one'),
    path('login', views.user_login, name="login"),
    path('register', views.user_register, name="register"),
    path('logout', views.user_logout, name="logout"),
    path('user-info/<int:bloger_id>', views.user_info, name="user_info"),   # 用户信息
    path('edit-user-information', views.edit_user_info, name="edit_user_information"),  # 修改用户信息
    path('attention', views.attention, name="attention"),   # 订阅
    path('leave-message', views.leave_message, name="leave_message"),   # 留言
    path('leave-message-list', views.leave_list, name="leave_message_list"),     # 留言列表
    path('read-leaf', views.read_leaf, name="read_leaf"),   # 阅读留言
]

