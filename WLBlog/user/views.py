import os

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from article.models import Article
from article.views import save_message
from user.forms import RegisterForm, LoginForm, EditUserInfoForm, LeaveMessageForm
from user.models import User, UserInfo, Attention, UserLeave, AvatarImg


def one(request):
    if request.user.is_authenticated:
        return render(request, "base.html", {'user': request.user})
    else:
        return render(request, "base.html")


# 首页
def home(request):
    content = dict()
    if request.user.is_authenticated:
        content['user'] = request.user
    else:
        content['user'] = ''

    articles = Article.objects.filter(is_secret=0, deleted=0).order_by("-updated")
    content['articles'] = articles
    return render(request, "home.html", content)


# 用户登录
def user_login(request):
    if request.method == "POST":
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            phone = user_form.cleaned_data['phone']
            password = user_form.cleaned_data['password']
            user = User.objects.filter(phone=phone, deleted=0).first()
            if user:
                if user.password == password:
                    login(request, user)
                    data = dict()
                    data['name'] = user.name
                    return JsonResponse({'code': True, 'msg': "登录成功", 'data': data})
                else:
                    return JsonResponse({'code': False, 'msg': "用户名或密码错误"})
            else:
                return JsonResponse({'code': False, 'msg': "用户未注册"})
        else:
            return JsonResponse({'code': False, 'msg': "登录失败"})
    return JsonResponse({'code': False, 'msg': "出错了"})


# 用户注册
@transaction.atomic
def user_register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            name = user_form.cleaned_data['name']
            phone = user_form.cleaned_data['phone']
            password = user_form.cleaned_data['confirm_password']
            user = User.objects.filter(phone=phone, deleted=0)
            if user:
                return JsonResponse({'code': False, 'msg': "该手机号已注册"})
            else:
                u = User.objects.create(name=name, phone=phone, password=password)
                UserInfo.objects.create(user_id=u.id)

            return JsonResponse({'code': True, 'msg': "注册成功"})
        else:
            return JsonResponse({'code': False, 'msg': "注册失败"})
    else:
        return JsonResponse({'code': False, 'msg': "出错啦"})


# 退出登录
def user_logout(request):
    logout(request)
    return JsonResponse({'code': True, 'msg': "退出登录啦"})


# 用户信息
def user_info(request, bloger_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = ''

    bloger = User.objects.filter(id=bloger_id, deleted=0).first()
    userinfo = UserInfo.objects.filter(user_id=bloger.id, deleted=0).first()
    content = dict()
    content['user'] = user
    content['bloger'] = bloger
    content['userinfo'] = userinfo

    git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
    content['git'] = git

    return render(request, "user/user_detail.html", content)


# 修改个人信息
@login_required(login_url='/')
@transaction.atomic
def edit_user_info(request):
    if request.method == "GET":
        user = request.user
        bloger = User.objects.filter(id=user.id, deleted=0).first()
        userinfo = UserInfo.objects.filter(user_id=user.id, deleted=0).first()

        content = dict()
        content['user'] = user
        content['bloger'] = bloger
        content['userinfo'] = userinfo

        git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()
        content['git'] = git

        return render(request, "user/edit_user_information.html", content)

    if request.method == "POST":
        user = request.user
        edit_userinfo_form = EditUserInfoForm(request.POST)
        if not edit_userinfo_form.is_valid():
            return JsonResponse({'code': False, 'msg': "你输入的内容有问题，请重新输入"})
        try:
            name = edit_userinfo_form.cleaned_data['name']
            sex = edit_userinfo_form.cleaned_data['sex']
            Introduction = edit_userinfo_form.cleaned_data['Introduction']
            school = edit_userinfo_form.cleaned_data['school']
            address = edit_userinfo_form.cleaned_data['address']
            github = edit_userinfo_form.cleaned_data['github']
            email = edit_userinfo_form.cleaned_data['email']
            interests = edit_userinfo_form.cleaned_data['interests']
            skill = edit_userinfo_form.cleaned_data['skill']
            summary = edit_userinfo_form.cleaned_data['summary']
            avatar = request.FILES.get('avatar')

            if avatar:
                avatar_img = AvatarImg.objects.create(avatar=avatar)
                User.objects.filter(id=user.id, deleted=0).update(name=name, sex=sex, Introduction=Introduction,
                                                                  avatar_id=avatar_img.id)
            else:
                User.objects.filter(id=user.id, deleted=0).update(name=name, sex=sex, Introduction=Introduction)

            UserInfo.objects.filter(user_id=user.id, deleted=0).update(school=school, address=address, github=github,
                                                                       email=email, interests=interests, skill=skill,
                                                                       summary=summary)

            return JsonResponse({'code': True, 'msg': "修改成功"})
        except Exception as e:
            print(e)


# 关注
@require_POST
@transaction.atomic
def attention(request):
    if not request.user.is_authenticated:
        return JsonResponse({'code': False, 'msg': "您还未登录，先登录吧"})
    else:
        try:
            user = request.user
            bloger_id = request.POST['bloger_id']
            bloger = User.objects.filter(id=bloger_id, deleted=0).first()
            if user == bloger:
                return JsonResponse({'code': False, 'msg': "这就是您自己的账号，自己怎么能关注自己呢"})
            else:
                attent = Attention.objects.filter(follower_id=user.id, attentor_id=bloger.id, deleted=0)
                if attent:
                    return JsonResponse({'code': False, 'msg': "您已经关注他了"})

                Attention.objects.create(follower_id=user.id, attentor_id=bloger.id)

            return JsonResponse({'code': True, 'msg': "订阅成功"})
        except Exception as e:
            print(e)


# 留言
@transaction.atomic
def leave_message(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'code': False, 'msg': "您还未登录"})

        try:
            leave_message_form = LeaveMessageForm(request.POST)
            if not leave_message_form.is_valid():
                return JsonResponse({'code': False, 'msg': "留言内容非法"})

            leave_body = leave_message_form.cleaned_data['leave_body']
            user = request.user
            bloger_id = request.POST["bloger_id"]
            message = UserLeave.objects.create(leaver_id=user.id, leaved_person_id=bloger_id, leave_body=leave_body)

            # 发送消息
            msg_body = "您有新的留言消息"
            save_message(category=0, leave_msg_id=message.id, msg_body=msg_body, msg_user=bloger_id)

            return JsonResponse({'code': True, 'msg': "留言成功"})
        except Exception as e:
            print(e)


# 留言列表
@login_required(login_url='/')
def leave_list(request):
    if request.method == "GET":
        try:
            content = dict()
            user = request.user
            bloger = User.objects.filter(id=user.id).first()
            git = UserInfo.objects.values("github").filter(user_id=bloger.id, deleted=0).first()

            content['user'] = user
            content['bloger'] = bloger
            content['git'] = git

            leaves = UserLeave.objects.filter(leaved_person_id=user.id, deleted=0).order_by("-created")
            content['leaves'] = leaves

            return render(request, "user/leave_message.html", content)
        except Exception as e:
            print(e)


# 阅读留言
def read_leaf(request):
    try:
        leaf_id = request.POST["leaf_id"]
        user = request.user
        UserLeave.objects.filter(id=leaf_id, deleted=0).update(is_read=1)
        return JsonResponse({'code': True, "msg": "yes"})
    except Exception as e:
        print(e)

