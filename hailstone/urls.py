# encoding=utf-8

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api", include("api.urls")),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 增加此行
]
