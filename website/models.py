import pytz
from django.conf import settings
from django.db import models
from common.models import BaseModel, Asset


class Forum(BaseModel):
    title = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='标题'
    )
    link_url = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='form 链接'
    )
    describe = models.CharField(
        max_length=500,
        default="",
        blank=True,
        null=True,
        verbose_name="描述",
    )

    class Meta:
        verbose_name = 'Forum'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link_url,
            'describe': str(self.describe),
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class BlogCat(BaseModel):
    name = models.CharField(
        default="unknown",
        max_length=100,
        unique=False,
        verbose_name='分类名称'
    )

    class Meta:
        verbose_name = 'BlogCat'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Blog(BaseModel):
    title = models.CharField(
        default="unknown",
        max_length=200,
        unique=False,
        verbose_name='博客标题'
    )
    image = models.ImageField(
        upload_to='blog/%Y/%m/%d/',
        blank=True,
        null=True
    )
    describe = models.CharField(
        max_length=500,
        default="",
        blank=True,
        null=True,
        verbose_name="描述",
    )
    link_url = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='博客链接'
    )
    tags = models.CharField(
        default="",
        max_length=200,
        unique=False,
        verbose_name='标签'
    )

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'title': self.title,
            'image': str(self.image),
            'describe': self.describe,
            'link_url': self.link_url,
            'tags': self.tags,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class Event(BaseModel):
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='事件名称'
    )
    link_url = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='事件链接'
    )
    describe = models.CharField(
        max_length=500,
        default="",
        blank=True,
        null=True,
        verbose_name="事件描述",
    )

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'name': self.name,
            'link': self.link_url,
            'describe': str(self.describe),
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }
