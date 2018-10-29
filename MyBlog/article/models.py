from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse

from django.utils import timezone
from slugify import slugify

# 文章栏目
class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name="article_column", on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


# 文章标签
class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name="tag", on_delete=models.CASCADE)
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag

# 文章
class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name="article_column", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name="article_tag", blank=True)
    article_collect = models.ManyToManyField(User, related_name="collection_article", blank=True)


    class Meta:
        ordering = ("title",)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("list_article_detail", args=[self.id, self.slug])

# 评论
class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="comments", on_delete=models.CASCADE)
    commentator = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)

# 收藏
class Collection(models.Model):
    collector = models.ForeignKey(User, related_name="collector", on_delete=models.CASCADE)
    article_collect = models.ManyToManyField(ArticlePost, related_name="collection_article", blank=True)

    def __str__(self):
        return self.article_collect




