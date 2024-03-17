# encoding=utf-8

import json
from common.helpers import ok_json
from website.models import (
    Event,
    Forum,
    BlogCat,
    Blog
)


# @check_api_token
def get_event_list(request):
    params = json.loads(request.body.decode())
    page = params.get('page', 1)
    page_size = params.get('page_size', 20)
    start = (page - 1) * page_size
    end = start + page_size
    events = Event.objects.all().order_by("-id")[start:end]
    total = Event.objects.all().order_by("-id").count()
    event_list = []
    for event in events:
        event_list.append(event.as_dict())
    data = {
        "total": total,
        "event_list": event_list,
    }
    return ok_json(data)


# @check_api_token
def get_forum_list(request):
    params = json.loads(request.body.decode())
    page = params.get('page', 1)
    page_size = params.get('page_size', 20)
    start = (page - 1) * page_size
    end = start + page_size
    forums = Forum.objects.all().order_by("-id")[start:end]
    total = Forum.objects.all().order_by("-id").count()
    forum_list = []
    for forum in forums:
        forum_list.append(forum.as_dict())
    data = {
        "total": total,
        "forum_list": forum_list,
    }
    return ok_json(data)


# @check_api_token
def get_blog_cat_list(request):
    blog_cats = BlogCat.objects.all()
    blog_cat_list = []
    for blog_cat in blog_cats:
        blog_cat_list.append(blog_cat.as_dict())
    return ok_json(blog_cat_list)


# @check_api_token
def get_blog_list(request):
    params = json.loads(request.body.decode())
    cat_id = params.get('cat_id', 0)
    page = params.get('page', 1)
    page_size = params.get('page_size', 20)
    start = (page - 1) * page_size
    end = start + page_size
    bcat = BlogCat.objects.filter(id=cat_id).first()
    if bcat is None:
        blogs = Blog.objects.all().order_by("-id")[start:end]
        total = Blog.objects.all().order_by("-id").count()
    else:
        blogs = Blog.objects.filter(cat=bcat).order_by("-id")[start:end]
        total = Blog.objects.filter(cat=bcat).order_by("-id").count()
    blog_list = []
    for blog in blogs:
        blog_list.append(blog.as_dict())
    data = {
        "total": total,
        "blog_list": blog_list,
    }
    return ok_json(data)
