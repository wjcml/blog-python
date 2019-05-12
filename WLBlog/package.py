from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 分页功能
def pagination(replace, page, num):
    if page == None:
        page = 1
    if num == None:
        num = 10
    paginator = Paginator(replace, num)
    try:
        current_page = paginator.page(page)
        paginations = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        paginations = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        paginations = current_page.object_list

    return paginations, current_page


# 将标签id和标签名封装到列表字典中
def tags_to_dict(tags):
    tags_dict = dict()
    tags_dict_list = []
    try:
        for tag in tags:
            # tags_dict['tag_id'] = tag.id
            # tags_dict['tag_name'] = tag.tag
            tags_dict_list.append({"tag_id": tag.id, "tag_name": tag.tag})

        return tags_dict_list
    except Exception as e:
        print(e)

