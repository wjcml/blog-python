from django.urls import path

from . import views, list_views


urlpatterns = [
    path('article-column', views.article_column, name="article_column"),
    path('rename-column/', views.rename_column, name="rename_column"),
    path('delete-column/', views.delete_column, name="delete_column"),
    path('article-post/', views.article_post, name="article_post"),
    path('article-list/', views.article_list, name="article_list"),
    path('redit-article/<int:article_id>', views.redit_article, name="redit_article"),
    path('delete-article/', views.delete_article, name="delete_article"),
    path('article-detail/<int:id>/<slug:slug>', views.article_detail, name="article_detail"),
    path('list-article-detail/<int:id>/<slug:slug>/', list_views.article_detail, name="list_article_detail"),
    path('list-article-title/<slug:username>', list_views.article_titles, name="list_article_title"),
    path('like-article/', list_views.like_article, name="like_article"),
    path('article-tag/', views.article_tag, name="article_tag"),
    path('del-article-tag/', views.del_article_tag, name="del_article_tag"),
    path('article-collect/', list_views.article_collect, name="article_collect"),
    # path('article-follow/', list_views.Follows, name="article_follow"),
]