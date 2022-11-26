#encoding=utf-8

from django.contrib import admin
from wallet.models import (
    Chain,
    Asset,
    Wallet,
    WalletAsset,
    Address,
    AddressAsset,
    TxRecord,
    TokenConfig,
    AddresNote,
    AddressAmountStat,
    WalletHead,
)

@admin.register(AddressAmountStat)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'amount')

@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'wallet_uuid', 'wallet_name', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'wallet_name')

@admin.register(WalletAsset)
class WalletAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract_addr', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'contract_addr')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'index', 'address', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'address')


@admin.register(AddressAsset)
class AddressAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'balance')

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

@admin.register(WalletHead)
class WalletHeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet_head')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'wallet_head')