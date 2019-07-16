from wtforms import Form, validators, widgets
from wtforms.fields import simple, html5


# 注册验证
class RegisterForm(Form):
    phone = simple.StringField(
        validators=[
            validators.DataRequired(message="手机号不能为空"),
            validators.Length(max=11, min=7, message="手机号长度不对请输入正确的手机号")
        ],
        widget=widgets.TextInput()
    )
    username = simple.StringField(
        validators=[
            validators.DataRequired(message="用户名不能为空"),
            validators.Length(max=20, message="用户名长度不能超过20")
        ],
        widget=widgets.TextInput()
    )
    password = simple.PasswordField(
        validators=[
            validators.DataRequired(message="密码不能为空"),
            validators.Length(max=16, min=6, message="密码长度应在6~16之间")
        ],
        widget=widgets.PasswordInput()
    )


# 登录验证
class LoginForm(Form):
    phone = simple.StringField(
        validators=[
            validators.DataRequired(message="手机号不能为空"),
            validators.Length(max=11, min=7, message="手机号长度不对,请输入正确的手机号")
        ],
        widget=widgets.TextInput()
    )
    password = simple.PasswordField(
        validators=[
            validators.DataRequired(message="密码不能为空"),
            validators.Length(max=16, min=6, message="密码长度应在6~16之间")
        ],
        widget=widgets.PasswordInput()
    )
