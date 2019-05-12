from django import forms
import re
from django.forms import ValidationError

from user.models import User


class LoginForm(forms.Form):
    phone = forms.CharField(required=True, min_length=11, max_length=11, error_messages={'required': "手机号不能为空",
                                                                                         'min_length': "请输入正确的手机号",
                                                                                         'max_length': "请输入正确的手机号",
                                                                                         'invalid': "输入的手机号非法"})
    password = forms.CharField(required=True, min_length=6, max_length=16, error_messages={'required': "密码不能为空",
                                                                                           'min_length': "请输入6~16位的密码",
                                                                                           'max_length': "请输入6~16位的密码",
                                                                                           'invalid': "输入的密码非法"})

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        pattern = '^1[35678]\d{9}$'
        pattern = re.match(pattern, phone)
        if pattern:
            return phone
        else:
            raise ValidationError("请输入正确的手机号")


class RegisterForm(forms.Form):
    name = forms.CharField(required=True, max_length=20, error_messages={'required': "用户名称不能为空",
                                                                         'max_length': "用户名称太长",
                                                                         'invalid': "输入的用户名非法"})
    phone = forms.CharField(required=True, min_length=11, max_length=11, error_messages={'required': "手机号不能为空",
                                                                                         'min_length': "请输入正确的手机号",
                                                                                         'max_length': "请输入正确的手机号",
                                                                                         'invalid': "输入的手机号非法"})
    password = forms.CharField(required=True, min_length=6, max_length=16, error_messages={'required': "密码不能为空",
                                                                                           'min_length': "请输入6~16位的密码",
                                                                                           'max_length': "请输入6~16位的密码",
                                                                                           'invalid': "输入的密码非法"})
    confirm_password = forms.CharField(required=True, min_length=6, max_length=16,
                                       error_messages={'required': "密码不能为空", 'min_length': "请输入6~16位的密码",
                                                       'max_length': "请输入6~16位的密码",
                                                       'invalid': "输入的密码非法"})

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        pattern = '^1[35678]\d{9}$'
        pattern = re.match(pattern, phone)
        if pattern:
            return phone
        else:
            raise ValidationError("请输入正确的手机号")

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError("密码不匹配")


# 编辑个人信息
class EditUserInfoForm(forms.Form):
    name = forms.CharField(required=True, max_length=20, error_messages={'required': "用户名称不能为空",
                                                                         'max_length': "用户名称太长",
                                                                         'invalid': "输入的用户名非法"})
    sex = forms.CharField(required=True, max_length=10, error_messages={'required': "性别不能为空",
                                                                        'max_length': "请输入正确的性别",
                                                                        'invalid': "输入的性别非法"})
    Introduction = forms.CharField(required=False, max_length=200, error_messages={'max_length': "个性标签太长"})
    school = forms.CharField(required=False, max_length=100, error_messages={'max_length': "个性标签太长"})
    address = forms.CharField(required=False, max_length=100, error_messages={'max_length': "籍贯太长"})
    github = forms.CharField(required=False, max_length=500, error_messages={'max_length': "GitHub地址太长",
                                                                             'invalid': "github地址非法"})
    email = forms.EmailField(required=False, max_length=500, error_messages={'max_length': "email太长",
                                                                             'invalid': "email地址非法"})
    interests = forms.CharField(required=False, max_length=500, error_messages={'max_length': "兴趣爱好太长"})
    skill = forms.CharField(required=False, max_length=500, error_messages={'max_length': "技能太长"})
    summary = forms.CharField(required=False, max_length=2000, error_messages={'max_length': "摘要太长"})

    def clean_sex(self):
        sex = self.cleaned_data['sex']
        if sex == '男':
            return 1
        else:
            return 2


# 留言
class LeaveMessageForm(forms.Form):
    leave_body = forms.CharField(required=True, max_length=2000, error_messages={'required': "留言内容不能为空",
                                                                                 'max_length': "留言内容太长"})
