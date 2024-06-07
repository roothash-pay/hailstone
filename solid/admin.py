# encoding=utf-8

from django.contrib import admin
from solid.models import (
    ServiceType,
    AuditProject,
    CoreMember,
    LoadBoard
)

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'detail')


@admin.register(AuditProject)
class AuditProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'report_link')


@admin.register(CoreMember)
class CoreMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(LoadBoard)
class LoadBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'competitor', 'payouts')

