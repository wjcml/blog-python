from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.base import View

# Create your views here.


from article.forms import AddTagForm, EditTagForm, AddArticleForm, AddCommentForm, AddReplyForm, EditArticleForm, \
    SaveDraftForm
from article.models import Tags, ArticleTag, Article, Comments, Reply, ClickLike, Collection, ArticleDraft, Message
from package import pagination, tags_to_dict
from user.models import User, UserInfo, Attention

import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# 写博客
@login_required(login_url="/")
@transaction.atomic
def get_add_article(request):
    if request.method == "GET":
        user = request.user
        try:
            bloger = User.objects.filter(id=user.id, deleted=0).first()
            # 将标签id和标签名封装到列表字典中
            tags = Tags.objects.filter(user_id=user.id, deleted=0)
            if tags:
                tags_dict_list = tags_to_dict(tags)
            else:
                tags_dict_list = []

            content = dict()
            content['user'] = user
            content['bloger'] = bloger
            content['tags'] = tags_dict_list

            git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
            content['git'] = git

            return render(request, "article/write_article.html", content)
        except Exception as e:
            print(e)

    if request.method == "POST":
        article_form = AddArticleForm(request.POST)
        try:
            if article_form.is_valid():
                article_title = article_form.cleaned_data["article_title"]
                article_body = article_form.cleaned_data["article_body"]
                checked_tags = article_form.cleaned_data["checked_tags"]
                is_secret = article_form.cleaned_data["is_secret"]
                if is_secret == 'false':
                    is_secret = 0
                else:
                    is_secret = 1

                # 保存文章
                article = Article.objects.create(author_id=request.user.id, title=article_title, body=article_body,
                                                 is_secret=is_secret)

                # 保存文章的标签
                add_articletag_list = []
                for tag in checked_tags:
                    obj = ArticleTag(article_id=article.id, tag_id=tag)
                    add_articletag_list.append(obj)
                ArticleTag.objects.bulk_create(add_articletag_list)

                # 发送消息
                if is_secret == 0:
                    msg_body = "您关注的博主"+request.user.name+"发表了一篇新文章，快去看看吧"
                    msg_user = Attention.objects.filter(attentor_id=request.user.id, deleted=0)
                    if msg_user:
                        save_message(category=2, article_id=article.id, msg_body=msg_body, msg_user=msg_user)

            else:
                return JsonResponse({'code': False, 'msg': "保存失败"})

            return JsonResponse({'code': True, 'msg': "保存成功"})
        except Exception as e:
            print(e)


# 修改文章内容
@login_required(login_url="/")
@transaction.atomic
def edit_article(request, article_id):
    if request.method == "GET":
        user = request.user
        try:
            bloger = User.objects.filter(id=user.id, deleted=0).first()
            # 将标签id和标签名封装到列表字典中
            tags = Tags.objects.filter(user_id=user.id, deleted=0)
            if tags:
                tags_dict_list = tags_to_dict(tags)
            else:
                tags_dict_list = []

            content = dict()
            content['user'] = user
            content['bloger'] = bloger
            content['tags'] = tags_dict_list

            # 获取文章和文章标签
            article = Article.objects.filter(id=article_id, deleted=0).first()
            article_tags = ArticleTag.objects.filter(article_id=article_id, deleted=0)

            content['article'] = article
            content['article_tags'] = article_tags

            git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
            content['git'] = git

            return render(request, "article/edit_article.html", content)
        except Exception as e:
            print(e)

    if request.method == "POST":
        article_form = EditArticleForm(request.POST)
        try:
            if article_form.is_valid():
                article_title = article_form.cleaned_data["article_title"]
                article_body = article_form.cleaned_data["article_body"]
                checked_tags = article_form.cleaned_data["checked_tags"]
                is_secret = article_form.cleaned_data["is_secret"]
                if is_secret == 'false':
                    is_secret = 0
                else:
                    is_secret = 1

                # 更新文章
                Article.objects.filter(id=article_id).update(title=article_title, body=article_body,
                                                             is_secret=is_secret)

                # 得到旧的文章标签
                old_tags_id = []
                old_article_tags = ArticleTag.objects.filter(article_id=article_id, deleted=0)
                for old_article_tag in old_article_tags:
                    old_tags_id.append(str(old_article_tag.tag.id))
                # 改变背后需要保存的标签
                save_tags = [checked_tag for checked_tag in checked_tags if checked_tag not in old_tags_id]
                # 改变后需要删除的标签
                deleted_tags = [old_tag for old_tag in old_tags_id if old_tag not in checked_tags]

                if deleted_tags:
                    for tag_id in deleted_tags:
                        ArticleTag.objects.filter(tag_id=tag_id, article_id=article_id, deleted=0).update(deleted=1)
                if save_tags:
                    for tag_id in save_tags:
                        ArticleTag.objects.create(tag_id=tag_id, article_id=article_id, deleted=0)

                return JsonResponse({'code': True, 'msg': "修改成功"})
            else:
                return JsonResponse({'code': False, 'msg': "保存失败"})
        except Exception as e:
            print(e)


# 自己的文章列表
@login_required(login_url="/")
@require_GET
def article_list(request):
    try:
        page = request.GET.get("page", None)  # 页码
        num = request.GET.get("num", None)  # 每页数量
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        articles = Article.objects.filter(author_id=user.id, deleted=0).order_by("-created")
        # 分页
        paginations, current_page = pagination(articles, page, num)
        content = dict()
        content['user'] = user
        content['bloger'] = bloger
        content['articles'] = paginations
        content['page'] = current_page
        # 提取当前页的每篇文章的标签
        if articles:
            article_and_tag = []
            for article in paginations:
                tag = article.articletag_set.filter(deleted=0)
                article_and_tag.append({'article': article, 'article_tags': tag})
            content['articles'] = article_and_tag
        else:
            content['articles'] = ''

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "article/article_list.html", content)
    except Exception as e:
        print(e)


# 别人的文章列表
@require_GET
def other_article_list(request, bloger_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = ''

    try:
        page = request.GET.get("page", None)
        num = request.GET.get("num", None)
        bloger = User.objects.filter(id=bloger_id, deleted=0).first()
        if bloger == user:
            articles = Article.objects.filter(author_id=bloger_id, deleted=0).order_by("-created")
        else:
            articles = Article.objects.filter(author_id=bloger_id, is_secret=0, deleted=0).order_by("-created")
        # 分页
        paginations, current_page = pagination(articles, page, num)
        content = dict()
        content['user'] = user
        content['bloger'] = bloger
        content['articles'] = paginations
        content['page'] = current_page

        if articles:
            article_and_tag = []
            for article in paginations:
                tag = article.articletag_set.filter(deleted=0)
                article_and_tag.append({'article': article, 'article_tags': tag})
            content['articles'] = article_and_tag
        else:
            content['articles'] = ''

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "article/article_list.html", content)

    except Exception as e:
        print(e)


# 文章详情
def article_detail(request, article_id):
    try:
        content = dict()
        user = request.user
        if user:
            content['user'] = user
            article_like = ClickLike.objects.filter(article_id=article_id, click_liker=user.id, deleted=0)
            if article_like:
                is_like = 'true'
            else:
                is_like = 'false'

            collect_article = Collection.objects.filter(article_id=article_id, user_id=user.id, deleted=0)
            if collect_article:
                is_collect = 'true'
            else:
                is_collect = 'false'
        else:
            content['user'] = ''
            is_like = 'false'
            is_collect = 'false'
        # 获取文章详情
        article = Article.objects.filter(id=article_id, deleted=0).first()
        bloger = User.objects.filter(id=article.author.id).first()
        article_tags = ArticleTag.objects.filter(article_id=article_id, deleted=0)
        content['article'] = article
        content['bloger'] = bloger
        content['article_tags'] = article_tags

        # 获取评论详情
        comment_detail = get_comment_detail(article_id)
        content['comment_detail'] = comment_detail

        content['is_like'] = is_like
        content['is_collect'] = is_collect

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        # 该文章被阅读的次数
        total_views = r.incr("article:{}:views".format(article.id))
        content['total_views'] = total_views

        return render(request, "article/article_detail.html", content)
    except Exception as e:
        print(e)


# 得到评论和回复内容
def get_comment_detail(article_id):
    comment_detail = []
    comments = Comments.objects.filter(article_id=article_id, deleted=0).order_by("-created")
    if not comments:
        comment_detail.append({'comment': comments})
    else:
        for comment in comments:
            replies = Reply.objects.filter(comment_id=comment.id, deleted=0).order_by("created")
            comment_detail.append({'comment': comment, 'replies': replies})
    return comment_detail


# 添加回复
@require_POST
@transaction.atomic
def add_new_reply(request):
    if not request.user.is_authenticated:
        return JsonResponse({'code': False, 'msg': "用户未登录，请先登录"})
    else:
        comment_id = request.POST['comment_id']
        replier_id = request.user.id    # 回复人
        respondent_id = request.POST['respondent_id']   # 被回复人
        reply_form = AddReplyForm(request.POST)
        if not reply_form.is_valid():
            return JsonResponse({'code': False, 'msg': "回复内容不合法"})
        reply_body = reply_form.cleaned_data['reply_body']

        Reply.objects.create(comment_id=comment_id, replier_id=replier_id, respondent_id=respondent_id,
                             reply_body=reply_body)

        # 发送消息
        msg_body = request.user.name+"回复了您一条消息："+reply_body
        comment = Comments.objects.filter(id=comment_id, deleted=0).first()
        save_message(category=3, article_id=comment.article.id, msg_body=msg_body, msg_user=request.user.id)

        return JsonResponse({'code': True, 'msg': "回复成功"})


# 发表评论
@require_POST
@transaction.atomic
def add_new_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'code': False, 'msg': "用户未登录，请先登录"})
    else:
        article_id = request.POST["article_id"]
        commentator_id = request.user.id    # 评论人id
        commentee_id = request.POST["author_id"]    # 被评论人id
        comment_form = AddCommentForm(request.POST)
        if not comment_form.is_valid():
            return JsonResponse({'code': False, 'msg': "评论内容不合法"})
        comment_body = comment_form.cleaned_data['comment_body']

        Comments.objects.create(article_id=article_id, commentator_id=commentator_id, commentee_id=commentee_id,
                                comment_body=comment_body)

        # 发送消息
        msg_body = request.user.name + "发表了评论"
        save_message(category=1, article_id=article_id, msg_body=msg_body, msg_user=commentee_id)

        return JsonResponse({'code': True, 'msg': "发表评论成功"})


# 点赞
@require_POST
@transaction.atomic
def click_like(request, article_id):
    if not request.user.is_authenticated:
        return JsonResponse({'code': False, 'msg': "用户未登录，请先登录"})
    else:
        user = request.user
        article_like = ClickLike.objects.filter(article_id=article_id, click_liker=user.id, deleted=0)
        if article_like:
            return JsonResponse({'code': False, 'msg': "你已经给本文章点过赞了"})
        Article.objects.filter(id=article_id, deleted=0).update(liker=F("liker")+1)
        ClickLike.objects.create(article_id=article_id, click_liker=user)

        return JsonResponse({'code': True, 'msg': "谢谢您为我点赞"})


# 收藏文章
@require_POST
@transaction.atomic
def collection_article(request, article_id):
    if not request.user.is_authenticated:
        return JsonResponse({'code': False, 'msg': "用户未登录"})
    else:
        try:
            user = request.user
            collect_article = Collection.objects.filter(user_id=user.id, article_id=article_id, deleted=0)
            if collect_article:
                return JsonResponse({'code': False, 'msg': "您已经收藏了本文章了"})
            Collection.objects.create(user_id=user.id, article_id=article_id)

            return JsonResponse({'code': True, 'msg': "已收藏本篇文章"})
        except Exception as e:
            print(e)


# 标签列表
@login_required(login_url="/")
@require_GET
def get_tags(request):
    try:
        page = request.GET.get("page", None)    # 页码
        num = request.GET.get("num", None)  # 每页数量
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        tags = Tags.objects.filter(user_id=user.id, deleted=0).order_by("-created")

        # 分页
        paginations, current_page = pagination(tags, page, num)
        content = dict()
        content['user'] = user
        content['bloger'] = bloger
        content['tags'] = paginations
        content['page'] = current_page

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "article/tag_list.html", content)
    except Exception as e:
        print(e)


# 新增标签
@login_required(login_url="/")
@require_POST
@transaction.atomic
def add_new_tag(request):
    tag_form = AddTagForm(request.POST)
    try:
        if tag_form.is_valid():
            tag = tag_form.cleaned_data['new_tag']
            # 检查标签是否已存在
            check_tag = Tags.objects.filter(tag=tag, user_id=request.user.id, deleted=0)
            if check_tag:
                return JsonResponse({'code': False, 'msg': "标签已存在"})
            # 创建标签
            Tags.objects.create(tag=tag, user_id=request.user.id)
            tags = Tags.objects.filter(user_id=request.user.id, deleted=0)
            tags_list = tags_to_dict(tags)
        else:
            return JsonResponse({'code': False, 'msg': "标签名非法"})
        return JsonResponse({'code': True, 'msg': "新标签添加成功", "data": tags_list})
    except Exception as e:
        print(e)
        return JsonResponse({'code': False, 'msg': "出错啦"})


# 修改标签
@login_required(login_url="/")
@require_POST
@transaction.atomic
def edit_tag(request):
    tag_form = EditTagForm(request.POST)
    try:
        if tag_form.is_valid():
            tag_id = tag_form.cleaned_data['tag_id']
            tag = tag_form.cleaned_data['tag_name']
            Tags.objects.filter(id=tag_id, user_id=request.user.id).update(tag=tag)
        else:
            return JsonResponse({'code': False, 'msg': "标签名非法"})
        return JsonResponse({'code': True, 'msg': "修改标签成功"})
    except Exception as e:
        print(e)
        return JsonResponse({'code': False, 'msg': "出错啦"})


# 删除标签
@login_required(login_url="/")
@require_POST
@transaction.atomic
def delete_tag(request):
    try:
        delete_tag_id = request.POST['tag_id']
        delete_tag_name = request.POST['tag_name']
        check_tag = Tags.objects.filter(id=delete_tag_id, user_id=request.user.id, tag=delete_tag_name, deleted=0)
        if check_tag:
            Tags.objects.filter(id=delete_tag_id).update(deleted=1)
            ArticleTag.objects.filter(tag_id=delete_tag_id, deleted=0).update(deleted=1)
        else:
            return JsonResponse({'code': False, 'msg': "标签不存在"})
        return JsonResponse({'code': True, 'msg': "标签"+delete_tag_name+"已删除"})
    except Exception as e:
        print(e)
        return JsonResponse({'code': False, 'msg': "出错啦"})


# 我的收藏列表
@login_required(login_url="/")
@require_GET
def my_collection_list(request):
    try:
        content = dict()
        page = request.GET.get("page", None)  # 页码
        num = request.GET.get("num", None)  # 每页数量
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        collections = Collection.objects.filter(user_id=user.id, deleted=0).order_by("-created")

        paginations, current_page = pagination(collections, page, num)

        content['user'] = user
        content['bloger'] = bloger
        content['collections'] = paginations
        content['page'] = current_page

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "article/collection_article.html", content)
    except Exception as e:
        print(e)


# 删除收藏
@login_required(login_url="/")
@transaction.atomic
def delete_collection(request):
    try:
        article_id = request.POST['article_id']
        Collection.objects.filter(article_id=article_id, deleted=0).update(deleted=1)

        return JsonResponse({'code': True, 'msg': "删除成功"})
    except Exception as e:
        print(e)


# 保存草稿
@login_required(login_url="/")
@require_POST
@transaction.atomic
def save_draft(request):
    article_draft_form = SaveDraftForm(request.POST)
    if not article_draft_form.is_valid():
        return JsonResponse({'code': False, 'msg': "添加失败,请重新添加"})

    try:
        user = request.user
        article_title = article_draft_form.cleaned_data['article_title']
        article_body = article_draft_form.cleaned_data["article_body"]

        ArticleDraft.objects.create(author_id=user.id, title=article_title, body=article_body)

        return JsonResponse({'code': True, 'msg': "保存草稿成功"})
    except Exception as e:
        print(e)


# 草稿箱
@login_required(login_url="/")
def draft_list(request):
    try:
        content = dict()
        page = request.GET.get("page", None)  # 页码
        num = request.GET.get("num", None)  # 每页数量
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        drafts = ArticleDraft.objects.filter(author_id=user.id, deleted=0).order_by("-created")

        paginations, current_page = pagination(drafts, page, num)

        content['user'] = user
        content['bloger'] = bloger
        content['drafts'] = paginations
        content['page'] = current_page

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "draft/draft_list.html", content)

    except Exception as e:
        print(e)


# 删除草稿
@login_required(login_url="/")
@transaction.atomic
def delete_draft(request):
    try:
        draft_id = request.POST['draft_id']
        ArticleDraft.objects.filter(id=draft_id, deleted=0).update(deleted=1)

        return JsonResponse({'code': True, 'msg': "删除草稿成功"})
    except Exception as e:
        print(e)


# 编辑草稿
@login_required(login_url="/")
@transaction.atomic
def edit_draft(request, draft_id):
    if request.method == "GET":
        user = request.user
        try:
            bloger = User.objects.filter(id=user.id, deleted=0).first()
            # 将标签id和标签名封装到列表字典中
            tags = Tags.objects.filter(user_id=user.id, deleted=0)
            if tags:
                tags_dict_list = tags_to_dict(tags)
            else:
                tags_dict_list = []

            content = dict()
            content['user'] = user
            content['bloger'] = bloger
            content['tags'] = tags_dict_list

            draft = ArticleDraft.objects.filter(id=draft_id, author_id=user.id, deleted=0).first()

            content['draft'] = draft

            git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
            content['git'] = git

            return render(request, "draft/edit_draft.html", content)
        except Exception as e:
            print(e)

    if request.method == "POST":
        draft_form = SaveDraftForm(request.POST)
        if not draft_form.is_valid():
            return JsonResponse({'code': False, 'msg': "内容非法，请重新编辑"})
        try:
            article_title = draft_form.cleaned_data["article_title"]
            article_body = draft_form.cleaned_data["article_body"]

            ArticleDraft.objects.filter(id=draft_id, deleted=0).update(title=article_title, body=article_body)

            return JsonResponse({'code': True, 'msg': "保存为草稿成功"})
        except Exception as e:
            print(e)


# 获取某标签文章
def get_tag_article(request, tag_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = ''

    try:
        page = request.GET.get("page", None)
        num = request.GET.get("num", None)
        tag = Tags.objects.filter(id=tag_id, deleted=0).first()

        # article = Article.objects.filter(articletag__tag_id=tag_id, deleted=0, articletag__deleted=0)
        bloger = User.objects.filter(id=tag.user.id, deleted=0).first()
        if bloger == user:
            articles = Article.objects.filter(articletag__tag_id=tag_id, articletag__deleted=0, deleted=0).order_by("-created")
        else:
            articles = Article.objects.filter(articletag__tag_id=tag_id, articletag__deleted=0, is_secret=0, deleted=0).order_by("-created")
        # 分页
        paginations, current_page = pagination(articles, page, num)
        content = dict()
        content['user'] = user
        content['bloger'] = bloger
        content['articles'] = paginations
        content['page'] = current_page

        if articles:
            article_and_tag = []
            for article in paginations:
                tag = article.articletag_set.filter(deleted=0)
                article_and_tag.append({'article': article, 'article_tags': tag})
            content['articles'] = article_and_tag
        else:
            content['articles'] = ''

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "article/article_list.html", content)
    except Exception as e:
        print(e)


# 归档
@login_required(login_url="/")
def archive_article(request, type=None):
    try:
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()

        content = dict()
        content['user'] = user
        content['bloger'] = bloger

        articles = Article.objects.filter(author_id=user.id, deleted=0).order_by("-created")
        date_year_list = Article.objects.archive_date(articles, type)
        archive_list = []
        for date_year in date_year_list:
            index = date_year.replace('-', '_')
            article_list = Article.objects.filter(created__icontains=date_year, author_id=user.id, deleted=0).order_by("-created")
            archive_list.append({'index': index, 'date': date_year, 'article_list': article_list})

        content['archive_list'] = archive_list
        content['count'] = articles.count()
        content['git'] = git

        return render(request, "article/archive.html", content)
    except Exception as e:
        print(e)


# 保存消息(括号里的参数依次为消息类型，留言id，文章id，消息内容，接收消息的用户)
def save_message(category=None, leave_msg_id=None, article_id=None, msg_body=None, msg_user=None):
    try:
        if category == 0:
            Message.objects.create(user_id=msg_user, category=category, message_body=msg_body, leave_msg_id=leave_msg_id)
        elif category == 2:
            for user in msg_user:
                Message.objects.create(user_id=user.follower.id, category=category, message_body=msg_body,
                                       article_id=article_id)
        else:
            Message.objects.create(user_id=msg_user, category=category, message_body=msg_body, article_id=article_id)

        return True
    except Exception as e:
        print(e)
        return False


# 获取消息数量
def get_message_num(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'code': False})

        user = request.user
        msg = Message.objects.filter(user_id=user.id, is_read=0, deleted=0).order_by("-created").count()

        if msg == 0:
            return JsonResponse({'code': False})

        return JsonResponse({'code': True, 'message_num': msg})
    except Exception as e:
        print(e)


# 消息列表
@login_required(login_url="/")
@require_GET
def msg_list(request):
    try:
        page = request.GET.get("page", None)
        num = request.GET.get("num", None)
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        content = dict()
        content['user'] = user
        content['bloger'] = bloger

        messages = Message.objects.filter(user_id=user.id, deleted=0).order_by("-created")

        # 分页
        paginations, current_page = pagination(messages, page, num)

        content['messages'] = paginations
        content['page'] = current_page

        return render(request, "user/message_list.html", content)
    except Exception as e:
        print(e)


# 阅读消息
@login_required(login_url="/")
@require_POST
@transaction.atomic
def read_msg(request):
    try:
        msg_id = request.POST['msg_id']
        Message.objects.filter(id=msg_id, deleted=0).update(is_read=1)

        return JsonResponse({'code': True})
    except Exception as e:
        print(e)
