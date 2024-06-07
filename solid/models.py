# encoding=utf-8
import pytz

from django.conf import settings
from django.db import models
from common.models import BaseModel, Asset


StatusChoice = [(x, x) for x in ['Prepare', 'Ongoing', 'End']]
tz = pytz.timezone(settings.TIME_ZONE)

class ServiceType(BaseModel):
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='服务名称'
    )
    icon = models.ImageField(
        upload_to='icon/%Y/%m/%d/',
        blank=True,
        null=True
    )
    detail = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='服务描述'
    )

    class Meta:
        verbose_name = 'ServiceType'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'name': self.name,
            'icon': settings.IMG_URL + str(self.icon),
            'detail': self.detail,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class AuditProject(BaseModel):
    service_type = models.ForeignKey(
        ServiceType,
        related_name="services_type",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目类别",
    )
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='审计项目的名称'
    )
    photo = models.ImageField(
        upload_to='audit/%Y/%m/%d/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=100,
        choices=StatusChoice,
        default="Ongoing",
        verbose_name='项目状体'
    )
    project_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="项目链接",
    )
    detail = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='项目描述'
    )
    report_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="项目链接",
    )

    class Meta:
        verbose_name = 'AuditProject'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'photo': settings.IMG_URL + str(self.photo),
            'status': self.status,
            'project_link': self.project_link,
            'detail': self.detail,
            'report_link': self.report_link,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class CoreMember(BaseModel):
    name = models.CharField(
        default="Social",
        max_length=100,
        unique=False,
        verbose_name='成员姓名'
    )
    photo = models.ImageField(
        upload_to='member/%Y/%m/%d/',
        blank=True,
        null=True
    )
    detail = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='成员简介'
    )

    class Meta:
        verbose_name = 'CoreMember'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'photo': settings.IMG_URL + str(self.photo),
            'detail': self.detail,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class LoadBoard(BaseModel):
    competitor = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='审计员名称'
    )
    payouts = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='获取的总收益'
    )
    total_findings = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='找到的总问题数'
    )
    solo = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='个人找到的问题'
    )
    high = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='找到的高危漏洞数量'
    )
    med = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='找到的中危漏洞数量'
    )
    solo_high = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='个人找到的高危漏洞数量'
    )
    solo_med = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='个人找到的中危漏洞数量'
    )
    first_place = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='第一位置发现数量'
    )

    class Meta:
        verbose_name = 'LeadBoard'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.competitor

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'competitor': self.competitor,
            'payouts': self.payouts,
            'solo': self.solo,
            'high': self.high,
            'med': self.med,
            'solo_high': self.solo_high,
            'solo_med': self.solo_med,
            'first_place': self.first_place,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }
