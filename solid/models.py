# encoding=utf-8
import pytz

from django.conf import settings
from django.db import models
from common.models import BaseModel, Asset

StatusChoice = [(x, x) for x in ['Prepare', 'Ongoing', 'End']]
tz = pytz.timezone(settings.TIME_ZONE)


class User(BaseModel):
    address = models.CharField(
        default="",
        max_length=200,
        unique=False,
        verbose_name='钱包地址'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'address': self.address,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class CodingLanguage(BaseModel):
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='编程语言名称'
    )

    class Meta:
        verbose_name = 'CodingLanguage'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class ProjectType(BaseModel):
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='类别名称'
    )

    class Meta:
        verbose_name = 'ProjectType'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class Network(BaseModel):
    project_type = models.ForeignKey(
        ProjectType,
        related_name="project_type_network",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目类别",
    )
    coding_language = models.ForeignKey(
        CodingLanguage,
        related_name="coding_language_network",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目编程",
    )
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='网络名称'
    )
    sub_name = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='子名称'
    )
    icon_url = models.CharField(
        default="",
        max_length=200,
        unique=False,
        verbose_name='icon地址'
    )
    detail = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='网络详细'
    )

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'project_type': self.project_type.name,
            'coding_language': self.coding_language.name,
            'name': self.name,
            'sub_name': self.sub_name,
            'icon': self.icon_url,
            'detail': self.detail,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class AuditProject(BaseModel):
    project_type = models.ForeignKey(
        ProjectType,
        related_name="project_type_relation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目类别",
    )
    coding_language = models.ForeignKey(
        CodingLanguage,
        related_name="coding_language_relation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目编程",
    )
    network = models.ForeignKey(
        Network,
        related_name="coding_language_relation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目编程",
    )
    user = models.ForeignKey(
        User,
        related_name="user_relation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目所属用户",
    )
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='审计项目的名称'
    )
    photo_url = models.CharField(
        default="",
        max_length=200,
        unique=False,
        verbose_name='图片地址'
    )
    start_time = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='审计开始时间'
    )
    end_time = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='审计结束时间'
    )
    cycle = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='审计周期'
    )
    status = models.CharField(
        max_length=100,
        choices=StatusChoice,
        default="Ongoing",
        verbose_name='项目状态'
    )
    detail = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='项目描述'
    )
    bounty_fund = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='项目赏金'
    )
    project_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="项目链接",
    )
    report_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="审计报告链接",
    )
    x_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="X链接",
    )
    telegram = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="Telegram",
    )
    discord = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="Discord 链接",
    )
    github = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="Github 链接",
    )
    community_link = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="Github 链接",
    )
    bounty_description = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='奖励描述'
    )

    class Meta:
        verbose_name = 'AuditProject'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'project_type': self.project_type.name,
            'coding_language': self.coding_language.name,
            'network': self.network.name,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'cycle': self.cycle,
            'photo': self.photo_url,
            'bounty_fund': self.bounty_fund,
            'status': self.status,
            'project_link': self.project_link,
            'detail': self.detail,
            'report_link': self.report_link,
            'x_link': self.x_link,
            'telegram': self.telegram,
            'discord': self.discord,
            'github': self.github,
            'community_link': self.community_link,
            'bounty_description': self.bounty_description,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class ProjectPeopleComments(BaseModel):
    project = models.ForeignKey(
        AuditProject,
        related_name="project_audit_relation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="项目",
    )
    name = models.CharField(
        default="Social",
        max_length=100,
        unique=False,
        verbose_name='成员姓名'
    )
    photo_url = models.CharField(
        default="Social",
        max_length=200,
        unique=False,
        verbose_name='图片路径'
    )
    position = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='成员职位'
    )
    detail = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='成员评论'
    )

    class Meta:
        verbose_name = 'ProjectPeopleComments'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'project_name': self.project.name,
            'project_icon': self.project.photo_url,
            'name': self.name,
            'position': self.position,
            'photo': self.photo_url,
            'detail': self.detail,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class AskAudit(BaseModel):
    name = models.CharField(
        default="0",
        max_length=100,
        unique=False,
        verbose_name='咨询人姓名'
    )
    contact = models.CharField(
        default="0",
        max_length=100,
        unique=False,
        verbose_name='联系方式'
    )
    company = models.CharField(
        default="0",
        max_length=100,
        unique=False,
        verbose_name='审计公司'
    )
    completed_time = models.CharField(
        default="0",
        max_length=100,
        unique=False,
        verbose_name='预计审计完成时间'
    )
    repo_link = models.CharField(
        default="0",
        max_length=100,
        unique=False,
        verbose_name='github repo 链接'
    )
    detail = models.CharField(
        default="unknown",
        max_length=100,
        unique=False,
        verbose_name='详细描述'
    )
    ecosystem = models.CharField(
        default="unknown",
        max_length=100,
        unique=False,
        verbose_name='生态体系'
    )
    find_us_way = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='生态体系'
    )
    image_url = models.CharField(
        default="unknown",
        max_length=200,
        unique=False,
        verbose_name='图片文件'
    )

    class Meta:
        verbose_name = 'AskAudit'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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
            'total_findings': self.total_findings,
            'solo': self.solo,
            'high': self.high,
            'med': self.med,
            'solo_high': self.solo_high,
            'solo_med': self.solo_med,
            'first_place': self.first_place,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }
