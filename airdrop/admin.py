# encoding=utf-8

from django.contrib import admin
from airdrop.models import (
    AirdropUser,
    PointsRecord,
    ProjectInterAction,
    Questions,
    Period,
    PeriodReward
)


@admin.register(AirdropUser)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'points')


@admin.register(PointsRecord)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'type', 'points')


@admin.register(ProjectInterAction)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'describe', 'language', 'points_type', 'project_type', 'once_points', 'daily_max_points', 'max_points')


@admin.register(Questions)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'language')


@admin.register(Period)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sub_title', 'link_url', 'period')


@admin.register(PeriodReward)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'amount', 'is_send')