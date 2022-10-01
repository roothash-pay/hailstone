#encoding=utf-8

from django.contrib import admin
from market.models import (
    Exchange,
    Symbol,
    MarketPrice,
    StablePrice,
    FavoriteMarket,
)


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'exchange', 'avg_price')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'symbol')


@admin.register(StablePrice)
class StablePriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'usd_price', 'cny_price')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'asset')


@admin.register(FavoriteMarket)
class FavoriteMarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'created_at')

