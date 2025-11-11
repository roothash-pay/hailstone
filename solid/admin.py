# encoding=utf-8

from django.contrib import admin
from solid.models import (
    User,
    CodingLanguage,
    ProjectType,
    Network,
    AuditProject,
    ProjectPeopleComments,
    LoadBoard,
    AskAudit
)


@admin.register(User)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')


@admin.register(CodingLanguage)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ProjectType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Network)
class AuditProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'coding_language', 'name')


@admin.register(AuditProject)
class AuditProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'report_link')


@admin.register(ProjectPeopleComments)
class CoreMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'detail')


@admin.register(LoadBoard)
class LoadBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'competitor', 'payouts')


@admin.register(AskAudit)
class LoadBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
