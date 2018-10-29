from django import forms

from article.models import ArticleColumn, ArticlePost, Comment, ArticleTag


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body")

        widgets = {
            "title": forms.TextInput(attrs={"style": "height:40px;width:500px;border-radius:5px;border:1px solid rgba(69,69,69,0.4);color:rgba(69,69,69,0.6);font-size:20px;"})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

        widgets = {
            "body": forms.Textarea(attrs={"style": "height:90px;width:100%;border-radius:5px;color:rgba(69,69,69,0.6);border:1px solid rgba(69,69,69,0.4);resize:none;", "placeholder": "快来对作者说点什么吧..."})
        }

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ("tag", )
