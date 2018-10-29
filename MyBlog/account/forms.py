from django import forms

# 登录表单
from django.contrib.auth.models import User

from account.models import UserInfo


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"style": "width:320px;height:40px;font-size:20px;color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);text-indent:10px;", "placeholder": "用户名"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"style": "width:320px;height:40px;font-size:20px;color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);text-indent:10px;", "placeholder": "密码"}))

# 注册表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"style": "width:320px;height:40px;font-size:20px;color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);text-indent:10px;", "placeholder": "密码"}))
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"style": "width:320px;height:40px;font-size:20px;color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);text-indent:10px;", "placeholder": "确认密码"}))

    class Meta:
        model = User
        fields = ("username", "email",)

        widgets = {
            "username": forms.TextInput(attrs={"style": "width:320px;height:40px;font-size:20px;color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);text-indent:10px;", "placeholder": "用户名"}),
            "email": forms.EmailInput(attrs={"style": "width:320px;height:40px;font-size:20px;color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);text-indent:10px;", "placeholder": "邮箱"})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise  forms.ValidationError("密码不匹配")
        return cd['password2']

# 用户信息表单
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("phone", "birth", "school", "company", "profession", "address", "aboutme", "photo")

        widgets = {
            "phone": forms.TextInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
            "birth": forms.DateInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
            "school": forms.TextInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
            "company": forms.TextInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
            "profession": forms.TextInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
            "address": forms.TextInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
            "aboutme": forms.Textarea(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);width:700px;height:90px;resize:none;"}),
            "photo": forms.TextInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )

        widgets = {
            "email": forms.EmailInput(attrs={"style": "color:rgba(69,69,69,0.6);border-radius:5px;border:1px solid rgba(69,69,69,0.4);"}),
        }