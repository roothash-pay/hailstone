# encoding=utf-8

from django.contrib import admin
from l3staking.models import (
    StakingChain,
    StakingStrategy,
    Node
)

@admin.register(StakingChain)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'chain_id', 'rpc_url')


@admin.register(StakingStrategy)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Node)
class AddressAmountStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'eth_income', 'eth_income_rate', 'dp_income', 'dp_income_rate', 'eth_evil', 'eth_evil_rate', 'dp_evil', 'dp_evil_rate', 'tvl')

