from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_GET, require_POST

from package import pagination
from photo.forms import PhotoForm, EditPhotoForm, PhotoImgForm
from photo.models import Photo, PhotoImg
from user.models import User


# 相册列表
@login_required(login_url="/")
@require_GET
def photo(request):
    user = request.user
    bloger = User.objects.filter(id=user.id, deleted=0).first()
    try:
        page = request.GET.get("page", None)  # 页码
        num = request.GET.get("num", None)  # 每页数量
        content = dict()
        photos = Photo.objects.filter(user_id=user.id, deleted=0).order_by("-created")
        paginations, current_page = pagination(photos, page, num)
        content['user'] = user
        content['bloger'] = bloger
        content['photos'] = paginations
        content['page'] = current_page

        return render(request, "photo/photo_list.html", content)

    except Exception as e:
        print(e)


# 新增相册
@login_required(login_url="/")
@require_POST
@transaction.atomic
def add_new_photo(request):
    user = request.user
    photo_form = PhotoForm(request.POST)
    if not photo_form.is_valid():
        return JsonResponse({'code': False, 'msg': "相册名非法"})

    try:
        photo_name = photo_form.cleaned_data['new_photo']
        Photo.objects.create(user_id=user.id, photo_name=photo_name)

        return JsonResponse({'code': True, 'msg': "新增相册成功"})
    except Exception as e:
        print(e)


# 新增相册
@login_required(login_url="/")
@require_POST
@transaction.atomic
def edit_photo(request):
    user = request.user
    photo_form = EditPhotoForm(request.POST)
    if not photo_form.is_valid():
        return JsonResponse({'code': False, 'msg': "相册名非法"})

    try:
        photo_id = request.POST['photo_id']
        photo_name = photo_form.cleaned_data['photo_name']
        Photo.objects.filter(id=photo_id, deleted=0).update(photo_name=photo_name)

        return JsonResponse({'code': True, 'msg': "修改相册成功"})
    except Exception as e:
        print(e)


@login_required(login_url="/")
@require_POST
@transaction.atomic
def delete_photo(request):
    user = request.user
    try:
        photo_id = request.POST['photo_id']
        Photo.objects.filter(id=photo_id, deleted=0).update(deleted=1)
        PhotoImg.objects.filter(photo_id=photo_id, deleted=0).update(deleted=1)

        return JsonResponse({'code': True, 'msg': "删除相册成功"})
    except Exception as e:
        print(e)


@login_required(login_url="/")
@require_GET
def img_list(request):
    photo_id = request.GET['photo_id']
    category = 'list'
    content = get_photo_img(request, photo_id, category)
    content['photo_id'] = photo_id
    return render(request, "photo/image_list.html", content)


@login_required(login_url="/")
@require_GET
def get_img_tile(request):
    user = request.user
    photo_id = request.GET['photo_id']
    bloger = User.objects.filter(id=user.id, deleted=0).first()

    images = PhotoImg.objects.filter(photo_id=photo_id, deleted=0)
    # 获取日期
    year_month_list = []
    year_list = []
    month_list = []
    date_dict = dict()
    date_list = []
    for image in images:
        pub_date = image.created.strftime("%Y-%m")
        if pub_date not in year_month_list:
            year_month_list.append(pub_date)

    for year_month in year_month_list:
        y_m = year_month.split('-')
        if y_m[0] not in year_list:
            year_list.append(y_m[0])

    for year in year_list:
        for year_month in year_month_list:
            y_m = year_month.split('-')
            if year == y_m[0]:
                month_list.append(y_m[1])
        date_dict['year'] = year
        date_dict['month'] = month_list
        date_list.append(date_dict)

    content = dict()
    content['user'] = user
    content['bloger'] = bloger
    content['photo_id'] = photo_id
    content['date'] = date_list
    return render(request, "photo/image_tile.html", content)


@login_required(login_url="/")
@require_GET
def img_tile(request):
    photo_id = request.GET['photo_id']
    category = 'tile'
    content = get_photo_img(request, photo_id, category)
    return JsonResponse(content)


@login_required(login_url="/")
@require_GET
def img_fall(request):
    photo_id = request.GET['photo_id']
    category = 'fall'
    content = get_photo_img(request, photo_id, category)
    return JsonResponse(content)


@login_required(login_url="/")
@require_GET
def get_img_fall(request):
    user = request.user
    photo_id = request.GET['photo_id']
    bloger = User.objects.filter(id=user.id, deleted=0).first()
    content = dict()
    content['user'] = user
    content['bloger'] = bloger
    content['photo_id'] = photo_id
    return render(request, "photo/image_fall.html", content)


# 得到相册图片
def get_photo_img(req, photo_id, category):
    user = req.user
    bloger = User.objects.filter(id=user.id, deleted=0).first()
    content = dict()
    if category == 'list':
        try:
            page = req.GET.get("page", None)  # 页码
            num = req.GET.get("num", None)  # 每页数量
            photo_imgs = PhotoImg.objects.filter(photo_id=photo_id, deleted=0).order_by("-created")

            paginations, current_page = pagination(photo_imgs, page, num)

            content['user'] = user
            content['bloger'] = bloger
            content['photo_imgs'] = paginations
            content['page'] = current_page
            content['photo_id'] = photo_id

            return content

        except Exception as e:
            print(e)

    if category == 'fall':
        try:
            nid = req.GET['nid']
            # 每次加载15张图片
            dif = int(nid) + 15
            photo_imgs = PhotoImg.objects.values('id', 'title', 'img_url', 'description').filter(photo_id=photo_id, id__gt=nid, id__lt=dif, deleted=0)

            content['data'] = list(photo_imgs)
            content['code'] = True

            return content
        except Exception as e:
            print(e)

    if category == 'tile':
        try:
            checked_date = req.GET.get('checked_date', None)
            nid = req.GET['nid']
            # 每次加载20张图片
            dif = int(nid) + 20
            if checked_date == None or checked_date == '':
                photo_imgs = PhotoImg.objects.values('id', 'title',
                                                     'img_url', 'description').filter(photo_id=photo_id,
                                                                                      id__gt=nid,
                                                                                      id__lt=dif,
                                                                                      deleted=0).order_by("created")
            else:
                photo_imgs = PhotoImg.objects.values('id', 'title',
                                                     'img_url', 'description').filter(photo_id=photo_id,
                                                                                      created__icontains=checked_date,
                                                                                      deleted=0).order_by("created")
            content['data'] = list(photo_imgs)
            if photo_imgs:
                content['code'] = True
            else:
                content['code'] = False

            return content

        except Exception as e:
            print(e)


# 添加图片
@login_required(login_url="/")
@require_POST
@transaction.atomic
def add_photo_img(request):
    user = request.user
    photo_img_form = PhotoImgForm(request.POST, request.FILES)
    if not photo_img_form.is_valid():
        return JsonResponse({'code': False, 'msg': "上传失败，请重新上传"})
    try:
        title = photo_img_form.cleaned_data['title']
        description = photo_img_form.cleaned_data['description']
        photo_img = photo_img_form.cleaned_data['photo_img']
        photo_id = request.POST["photo_id"]

        PhotoImg.objects.create(title=title, description=description, img_url=photo_img, photo_id=photo_id)

        return JsonResponse({'code': True, 'msg': "上传成功"})
    except Exception as e:
        print(e)


# 删除图片
@login_required(login_url="/")
@require_POST
@transaction.atomic
def delete_photo_img(request):
    user = request.user
    photo_img_id = request.POST['photo_img_id']
    try:
        PhotoImg.objects.filter(id=photo_img_id, deleted=0).update(deleted=1)
        return JsonResponse({'code': True, 'msg': "删除成功"})
    except Exception as e:
        print(e)
