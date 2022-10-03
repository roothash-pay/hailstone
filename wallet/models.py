#encoding=utf-8

import pytz
from django.db import models
from common.models import DecField, BaseModel, BoolYesOrNoSelect, Chain, Asset
from django.conf import settings
from common.helpers import d0, dec, d1
from market.models import MarketPrice, StablePrice
from decimal import Decimal


tz = pytz.timezone(settings.TIME_ZONE)


class Address(BaseModel):
    NETWORK_CHOICES = [(x, x) for x in ['mainnet', 'testnet']]
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='链名称'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='资产名称'
    )
    network = models.CharField(
        max_length=32,
        choices=NETWORK_CHOICES,
        default='mainnet',
        verbose_name="主网测试网"
    )
    device_id = models.CharField(max_length=70, verbose_name='设备ID')
    wallet_uuid = models.CharField(max_length=70, verbose_name='wallet_uuid')
    wallet_name = models.CharField(max_length=70, verbose_name='钱包名称')
    address = models.CharField(max_length=70, verbose_name='钱包地址')
    contract_addr = models.CharField(max_length=70, verbose_name='合约地址')
    balance = DecField(default=d0, verbose_name="钱包余额")

    class Meta:
        verbose_name = '地址表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

    def get_symbol_price(self):
        balance = Decimal(self.balance) / Decimal(10 ** int(self.asset.unit))
        if self.asset.name not in ["USDT", "USDC", "DAI"]:
            market_price = MarketPrice.objects.filter(
                qoute_asset=self.asset,
                exchange__name="binance"
            ).order_by("-id").first()
            return market_price.usd_price * balance, market_price.cny_price * balance
        else:
            stable_price = StablePrice.objects.filter(
                asset=self.asset,
            ).order_by("-id").first()
            return stable_price.usd_price * balance, stable_price.cny_price * balance

    def list_to_dict(self):
        usd_price, cny_price = self.get_symbol_price()
        return {
            "id": self.id,
            "chain": self.chain.name,
            "symbol": self.asset.name,
            "icon": str(self.asset.icon),
            "network": self.network,
            "device_id": self.device_id,
            "wallet_uuid": self.wallet_uuid,
            "wallet_name": self.wallet_name,
            "address": self.address,
            "contract_addr": self.contract_addr,
            "usdt_price": format(usd_price, ".2f"),
            "cny_price": format(cny_price, ".2f"),
            "balance": format(Decimal(self.balance) / Decimal(10 ** int(self.asset.unit)), ".4f"),
        }


class AddressAmountStat(BaseModel):
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='address'
    )
    amount = DecField(default=d0, verbose_name="amount")
    timedate = models.CharField(max_length=70, verbose_name='timedate')

    class Meta:
        verbose_name = 'AddressAmountStat'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address.address

    def to_dict(self):
        return {
            "amount":format(self.amount, ".2f"),
            "time": self.timedate,
        }


class TokenConfig(BaseModel):
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='链名称'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='资产名称'
    )
    token_name = models.CharField(max_length=70, verbose_name='token 名称')
    icon = models.ImageField(upload_to='wallet/%Y/%m/%d/', blank=True, null=True)
    token_symbol = models.CharField(max_length=70, verbose_name='Token符号')
    contract_addr = models.CharField(max_length=70, verbose_name='合约地址')
    decimal = models.CharField(max_length=10, verbose_name='token 精度', db_index=True)
    is_hot = models.CharField(
        max_length=32,
        choices=BoolYesOrNoSelect,
        default='no',
        verbose_name="是不是热门资产"
    )

    class Meta:
        verbose_name = '资产配置表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token_name

    def list_to_dict(self):
        return {
            "id": self.id,
            "asset_id": self.asset.id,
            "token_name": self.token_name,
            "icon": str(self.icon),
            "token_symbol": self.token_symbol,
            "contract_addr": self.contract_addr,
            "decimal": self.decimal,
        }


class TxRecord(BaseModel):
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='链名称'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='资产名称'
    )
    from_addr = models.CharField(max_length=70, verbose_name='发送方')
    to_addr = models.CharField(max_length=70, verbose_name='接收方')
    amount = DecField(default=d0, verbose_name="转账金额")
    memo = models.CharField(max_length=70, verbose_name='备注')
    hash = models.CharField(max_length=70, verbose_name='交易Hash')
    block_height = models.CharField(max_length=70, verbose_name='所在区块')
    tx_time = models.CharField(max_length=70, verbose_name='交易时间')

    class Meta:
        verbose_name = '交易记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hash

    def list_to_dict(self):
        return {
            "id": self.id
        }


class AddresNote(BaseModel):
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='链名称'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='资产名称'
    )
    device_id = models.CharField(max_length=70, verbose_name='设备ID')
    memo = models.CharField(max_length=70, verbose_name='地址备注')
    address = models.CharField(max_length=70, verbose_name='地址')

    class Meta:
        verbose_name = '地址薄表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

    def list_to_dict(self):
        return {
            "id": self.id,
            "chain": self.chain.name,
            "asset": self.asset.name,
            "device_id": self.device_id,
            "memo": self.memo,
            "address": self.address
        }