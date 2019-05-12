from django import forms
from django.forms import ValidationError


# 相册
class PhotoForm(forms.Form):
    new_photo = forms.CharField(required=True, max_length=200, error_messages={'required': "相册名不能为空",
                                                                               'max_length': "相册名太长"})


class EditPhotoForm(forms.Form):
    photo_name = forms.CharField(required=True, max_length=200, error_messages={'required': "相册名不能为空",
                                                                                'max_length': "相册名太长"})


class PhotoImgForm(forms.Form):
    title = forms.CharField(required=True, max_length=200, error_messages={'required': "名称不能为空",
                                                                           'max_length': "名称太长"})
    description = forms.CharField(required=False, max_length=500, error_messages={'max_length': "描述太长"})
    photo_img = forms.FileField(required=True, error_messages={'required': "图片不能为空"})

    def clean_photo_img(self):
        photo_img = self.cleaned_data['photo_img']
        if photo_img:
            valid_extensions = ['jpg', 'jpeg', 'png']
            extension = photo_img.name.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError("只能上传'jpg','jpeg','png'格式的图片")
            return photo_img
