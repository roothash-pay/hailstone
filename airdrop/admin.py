# encoding=utf-8

from django.contrib import admin
from airdrop.models import (
    AirdropUser,
    PointsRecord,
    ProjectInterAction,
    Questions
)


@admin.register(AirdropUser)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'points')


@admin.register(PointsRecord)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'type', 'points')


@admin.register(ProjectInterAction)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'describe', 'language', 'type', 'max_points')


@admin.register(Questions)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'language')
