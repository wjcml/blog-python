from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.models import Follow
from article.forms import CommentForm
from article.models import ArticlePost, Comment
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# 文章列表（未登录）
def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        article_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all()



# 最新文章
    article_title_latest = article_title.order_by("-created")[0:5]


# 最热文章
    for article_title_hot in article_title:
        r.zincrby("article_ranking", article_title_hot.id, 1)

        article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[0:10]
        article_ranking_ids = [int(id) for id in article_ranking]
        most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
        most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))


# 分页
    paginator = Paginator(article_title, 7)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    if username:
        return render(request, "article/list/author_articles.html", {"articles": articles, "page": current_page, "userinfo": userinfo, "user_user": user, "most_viewed": most_viewed, "article_title_latest": article_title_latest})

    return render(request, "home.html", {"articles": articles, "page": current_page, "most_viewed": most_viewed, "article_title_latest": article_title_latest})


# 文章详情,评论
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))

    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.commentator = request.user
                new_comment.save()
        else:
            return HttpResponseRedirect("/account/login/")
    else:
        comment_form = CommentForm()

    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]

    return render(request, "article/list/article_detail.html", {"article": article, "total_views": total_views, "comment_form": comment_form, "similar_articles": similar_articles})


# 点赞
@login_required(login_url="/account/login/")
@csrf_exempt
@require_POST
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse('2')
        except:
            return HttpResponse("no")

# 收藏
@login_required(login_url="/account/login/")
@csrf_exempt
def article_collect(request):
    if request.method == "POST":
        action = request.POST["action"]
        article_id = request.POST["id"]
        article = ArticlePost.objects.get(id=article_id)
        if action == "collect":
            article.article_collect.add(request.user)
            return HttpResponse("1")
        else:
            article.article_collect.remove(request.user)
            return HttpResponse("2")

    if request.method == "GET":
        collections = request.user.collection_article.all()
        return render(request, "article/column/article_collect.html", {"collections": collections})

# 关注
# @login_required(login_url="/account/login/")
# @csrf_exempt
# def Follows(request):
#     if request.method == "POST":
#         follower = Follow.objects.get(fan=request.user)
#         follower.follow = User.objects.get(id=request.POST["article_user_id"])
#         return HttpResponse("1")