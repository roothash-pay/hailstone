#encoding=utf-8

from django.contrib import admin
from airdrop.models import (
    AirdropUser,
    PointsRecord
)

@admin.register(AirdropUser)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'points')

@admin.register(PointsRecord)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'type', 'points')
