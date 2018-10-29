from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('logout/', auth_views.logout, {"template_name": "account/logout.html"}, name="user_logout"),
    path('register/', views.user_register, name="user_register"),
    path('password-change/', auth_views.password_change, {"template_name": "account/password_change_form.html", "post_change_redirect": "/account/password-change-done"}, name="password_change"),
    path('password-change-done/', auth_views.password_change_done, {"template_name": "account/password_change_done.html"}, name="password_change_done"),
    path('myinfo/', views.myinfo, name="my_information"),
    path('edit-myinfo/', views.edit_myinfo, name="edit_myinfo"),
    path('my-image/', views.myphoto, name="my_image")
]