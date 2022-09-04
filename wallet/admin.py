#encoding=utf-8

from django.contrib import admin
from wallet.models import (
    Chain,
    Asset,
    Address,
    TxRecord,
    TokenConfig,
    AddresNote
)


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'wallet_uuid', 'wallet_name', 'address', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'wallet_name')


@admin.register(TxRecord)
class TxRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_addr', 'to_addr', 'amount', 'hash')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'hash')


@admin.register(TokenConfig)
class TokenConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_name', 'token_symbol', 'contract_addr', 'decimal')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'token_name')


@admin.register(AddresNote)
class AddresNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'memo', 'address')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'address')


