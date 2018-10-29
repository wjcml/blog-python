from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from account.forms import LoginForm, RegistrationForm, UserForm, UserInfoForm


from account.models import UserInfo, Follow

# 用户登录
from article.models import Collection


def user_login(request):
    if request.method =="POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponseRedirect(reverse("user_login"))

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


# 用户注册
def user_register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse("user_login"))
        else:
            return HttpResponse("注册失败")
    else:
        user_form = RegistrationForm()
        return render(request, "account/register.html", {"form": user_form})

# 用户个人信息显示
@login_required(login_url='/account/login/')
def myinfo(request):
    user =User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/user_info.html", {"user": user, "userinfo": userinfo})

# 修改个人信息
@login_required(login_url="/account/login/")
def edit_myinfo(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userinfo.phone = userinfo_cd['phone']
            userinfo.birth = userinfo_cd['birth']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userinfo.save()
        return HttpResponseRedirect('/account/myinfo/')
    else:
        user_form = UserForm(instance=request.user)
        userinfo_form = UserInfoForm(initial={"phone": userinfo.phone, "birth": userinfo.birth, "school": userinfo.school, "company": userinfo.company, "profession": userinfo.profession, "address": userinfo.address, "aboutme": userinfo.aboutme})

        return render(request, "account/edit_myinfo.html", {"user_form": user_form, "userinfo_form": userinfo_form, "userinfo":userinfo})

# 头像上传
def myphoto(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, "account/myphoto.html",)