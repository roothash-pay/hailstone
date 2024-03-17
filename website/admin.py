# encoding=utf-8

from django.contrib import admin
from website.models import (
    Event,
    Forum,
    BlogCat,
    Blog
)


@admin.register(Event)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link_url', 'describe')


@admin.register(Forum)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link_url', 'describe')


@admin.register(BlogCat)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Blog)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link_url', 'tags', 'describe')
