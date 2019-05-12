from django import forms
from django.forms import ValidationError


# 添加标签
class AddTagForm(forms.Form):
    new_tag = forms.CharField(required=True, max_length=30, error_messages={'required': "标签名不能为空",
                                                                            'max_length': "标签名太长",
                                                                            'invalid': "标签非法"})


# 修改标签
class EditTagForm(forms.Form):
    tag_id = forms.CharField(required=False, max_length=30)
    tag_name = forms.CharField(required=True, max_length=30, error_messages={'required': "标签名不能为空",
                                                                             'max_length': "标签名太长",
                                                                             'invalid': "标签非法"})


# 添加文章
class AddArticleForm(forms.Form):
    article_title = forms.CharField(required=True, max_length=30, error_messages={'required': "标题不能为空",
                                                                                  'max_length': "标题太长",
                                                                                  'invalid': "标题非法"})
    article_body = forms.CharField(required=True, min_length=0, error_messages={'required': "内容不能为空",
                                                                                'min_length': "内容非法",
                                                                                'invalid': "内容非法，请重新填写"})
    checked_tags = forms.CharField(required=True, error_messages={'required': "内容不能为空", 'invalid': "标签非法"})
    is_secret = forms.CharField()

    def clean_checked_tags(self):
        checked_tags = self.cleaned_data['checked_tags']
        if checked_tags:
            return checked_tags.split(",")
        else:
            raise ValidationError("出错啦")

    def clean_article_body(self):
        article_body = self.cleaned_data['article_body']
        if article_body:
            if article_body != '':
                return article_body
            else:
                raise ValidationError("请填写文章内容")
        else:
            raise ValidationError("请填写内容")


# 修改文章
class EditArticleForm(forms.Form):
    article_title = forms.CharField(required=True, max_length=30, error_messages={'required': "标题不能为空",
                                                                                  'max_length': "标题太长",
                                                                                  'invalid': "标题非法"})
    article_body = forms.CharField(required=True, min_length=0, error_messages={'required': "内容不能为空",
                                                                                'min_length': "内容非法",
                                                                                'invalid': "内容非法，请重新填写"})
    checked_tags = forms.CharField(required=True, error_messages={'required': "内容不能为空", 'invalid': "标签非法"})
    is_secret = forms.CharField()

    def clean_checked_tags(self):
        checked_tags = self.cleaned_data['checked_tags']
        if checked_tags:
            return checked_tags.split(",")
        else:
            raise ValidationError("出错啦")

    def clean_article_body(self):
        article_body = self.cleaned_data['article_body']
        if article_body:
            if article_body != '':
                return article_body
            else:
                raise ValidationError("请填写文章内容")
        else:
            raise ValidationError("请填写内容")


# 添加评论
class AddCommentForm(forms.Form):
    comment_body = forms.CharField(required=True, max_length=2000, error_messages={'required': "评论内容不能为空",
                                                                                   'max_length': "评论内容太长"})


# 添加回复
class AddReplyForm(forms.Form):
    reply_body = forms.CharField(required=True, max_length=2000, error_messages={'required': "回复内容不能为空",
                                                                                 'max_length': "回复内容太长"})


# 保存草稿
class SaveDraftForm(forms.Form):
    article_title = forms.CharField(required=True, max_length=30, error_messages={'required': "标题不能为空",
                                                                                  'max_length': "标题太长",
                                                                                  'invalid': "标题非法"})
    article_body = forms.CharField(required=True, min_length=0, error_messages={'required': "内容不能为空",
                                                                                'min_length': "内容非法",
                                                                                'invalid': "内容非法，请重新填写"})

    def clean_article_body(self):
        article_body = self.cleaned_data['article_body']
        if article_body:
            if article_body != '':
                return article_body
            else:
                raise ValidationError("请填写文章内容")
        else:
            raise ValidationError("请填写内容")
