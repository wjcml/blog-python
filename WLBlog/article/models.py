from django.db import models

# Create your models here.
from django.utils.timezone import now

from user.models import User, UserLeave, Attention

UNSECRET, SECRET = 0, 1
IS_SECRET = (
    (UNSECRET, '不是隐私'),
    (SECRET, '隐私'),
)

COMMENT, REPLY = 0, 1
CATEGORY = (
    (COMMENT, '评论'),
    (REPLY, '回复'),
)

LEAVE_MESSAGE, LEAVE_COMMENT, LEAVE_ATTENTION, LEAVE_REPLY = 0, 1, 2, 3
MESSAGE_CATEGORY = (
    (LEAVE_MESSAGE, '留言'),
    (LEAVE_COMMENT, '评论'),
    (LEAVE_ATTENTION, '订阅'),
    (LEAVE_REPLY, '回复'),
)


# 时间管理器，返回一个归档的时间列表
class ArticleManager(models.Manager):
    def archive_date(self, article_list, type=None):
        archive_list = []
        # 需要获取所有的文章model对象。
        for article in article_list:
            # 将每一个文章的发布日期都获取出来，按照'%Y-%M'进行格式化
            if not type == None:
                pub_date = article.created.strftime('%Y-%m')
            else:
                pub_date = article.created.strftime('%Y')
            if pub_date not in archive_list:
                # 如果这个时间字符串不在article_list这个列表中，就把这个年月添加进去
                archive_list.append(pub_date)
        return archive_list


# 标签
class Tags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    tag = models.CharField(max_length=30, verbose_name='标签名')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_tag'
        managed = False
        verbose_name = '标签'
        verbose_name_plural = verbose_name


# 博客文章
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(max_length=30, verbose_name='文章标题')
    body = models.TextField(verbose_name='文章内容')
    is_secret = models.IntegerField(choices=IS_SECRET, default=0, verbose_name='是否为隐私文章')
    liker = models.IntegerField(default=0, verbose_name='喜欢文章人数')
    unliker = models.IntegerField(default=0, verbose_name='不喜欢文章人数')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)
    objects = ArticleManager()

    class Meta:
        db_table = 'tb_article'
        managed = False
        verbose_name = '文章'
        verbose_name_plural = verbose_name


# 收藏
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="收藏文章")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_collection'
        managed = False
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


# 点赞表
class ClickLike(models.Model):
    click_liker = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="点赞人")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="点赞文章")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_click_like'
        managed = False
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


# 文章标签
class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name='标签')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_article_tag'
        managed = False
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name


# 草稿
class ArticleDraft(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(max_length=30, verbose_name='文章标题')
    body = models.TextField(verbose_name='文章内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_article_draft'
        managed = False
        verbose_name = '草稿'
        verbose_name_plural = verbose_name


# 整合集
class CollationSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    first_title = models.CharField(max_length=30, verbose_name='一级标题')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_collation_set'
        managed = False
        verbose_name = '整合集'
        verbose_name_plural = verbose_name


# 整合集二级标题和内容
class CollationSetBody(models.Model):
    collation_set = models.ForeignKey(CollationSet, on_delete=models.CASCADE, verbose_name='整合集')
    second_title = models.CharField(max_length=30, verbose_name='二级标题')
    body = models.TextField(verbose_name='内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_collation_set_body'
        managed = False
        verbose_name = '整合集文章内容'
        verbose_name_plural = verbose_name


# 评论
class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")
    commentator = models.ForeignKey(User, related_name="commentor", on_delete=models.CASCADE, verbose_name="评论人")
    commentee = models.ForeignKey(User, related_name="commenter", on_delete=models.CASCADE, verbose_name="被评论人")
    comment_body = models.CharField(max_length=2000, verbose_name="评论内容")
    category = models.IntegerField(choices=CATEGORY, default=0, verbose_name="判断是评论还是回复，默认是评论")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_comments'
        managed = False
        verbose_name = '评论'
        verbose_name_plural = verbose_name


# 回复
class Reply(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, verbose_name="评论")
    replier = models.ForeignKey(User, related_name="com_replier", on_delete=models.CASCADE, verbose_name="回复人")
    respondent = models.ForeignKey(User, related_name="com_respondent", on_delete=models.CASCADE, verbose_name="被回复人")
    reply_body = models.CharField(max_length=2000, verbose_name="评论内容")
    category = models.IntegerField(choices=CATEGORY, default=1, verbose_name="判断是评论还是回复，默认是回复")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_reply'
        managed = False
        verbose_name = '回复'
        verbose_name_plural = verbose_name


# 消息
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    category = models.IntegerField(choices=MESSAGE_CATEGORY, default=0, verbose_name="判断是留言信息,评论信息,订阅信息还是回复消息，默认是留言")
    message_body = models.CharField(max_length=2000, verbose_name="消息内容")
    leave_msg = models.ForeignKey(UserLeave, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name="如果是留言信息，加入留言id")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="如果是评论信息,订阅信息和回复消息，则加入文章id")
    is_read = models.IntegerField(default=0, verbose_name="是否已读")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_message'
        managed = False
        verbose_name = '消息'
        verbose_name_plural = verbose_name
