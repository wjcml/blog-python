from django.urls import path

from article.searchView import MySearchView
from . import views

app_name = "article"
urlpatterns = [
    path('add-blog-article', views.get_add_article, name="add_blog_article"),   # 写博客
    path('edit-article/<int:article_id>', views.edit_article, name="edit_article"),     # 修改文章
    path('article-list', views.article_list, name="article_list"),    # 博客列表
    path('other-article-list/<int:bloger_id>', views.other_article_list, name="other_article_list"),    # 别人的文章
    path('article-detail/<int:article_id>', views.article_detail, name="article_detail"),  # 文章详情
    path('click-like/<int:article_id>', views.click_like, name="click_like"),   # 点赞
    path('collect-article/<int:article_id>', views.collection_article, name="collect_article"),     # 收藏
    path('delete-collection', views.delete_collection, name="delete_collection"),   # 删除收藏
    path('my-collection-list', views.my_collection_list, name="my_collection_list"),    # 我的收藏
    path('add-new-comment', views.add_new_comment, name="add_new_comment"),     # 发表评论
    path('add-new-reply', views.add_new_reply, name="add_new_reply"),     # 回复
    path('tags-list', views.get_tags, name="tags_list"),    # 标签列表
    path('add-new-tag', views.add_new_tag, name="add_new_tag"),    # 新增标签
    path('edit-tag', views.edit_tag, name="edit_tag"),    # 修改标签
    path('delete-tag', views.delete_tag, name="delete_tag"),  # 删除标签
    path('save-draft', views.save_draft, name="save_draft"),    # 保存草稿
    path('draft-list', views.draft_list, name="draft_list"),    # 草稿箱
    path('delete-draft', views.delete_draft, name="delete_draft"),  # 删除草稿
    path('edit-draft/<int:draft_id>', views.edit_draft, name="edit_draft"),     # 编辑草稿
    path('get-tag-article/<int:tag_id>', views.get_tag_article, name="get_tag_article"),    # 某标签文章
    path('archive-article', views.archive_article, name="archive_article"),     # 归档
    path('archive-article/<slug:type>', views.archive_article, name="archive_article"),     # 归档
    path('get-msg-num', views.get_message_num, name="get_msg_num"),     # 获取消息个数
    path('msg-list', views.msg_list, name="msg_list"),  # 消息列表
    path('read-msg', views.read_msg, name="read_msg"),  # 阅读消息

    path(r'search/', MySearchView.as_view(), name='haystack_search'),   # 全局搜索
]
