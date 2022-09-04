#encoding=utf-8

import pytz
from django.db import models
from common.models import DecField, BaseModel, BoolYesOrNoSelect
from django.conf import settings
from common.helpers import d0, dec, d1

tz = pytz.timezone(settings.TIME_ZONE)


class Chain(BaseModel):
    name = models.CharField(max_length=70, verbose_name='链名称', db_index=True)
    mark = models.CharField(max_length=70, verbose_name='链名标识')
    icon = models.ImageField(upload_to='wallet/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        verbose_name = '链表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


    def list_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mark": self.user.mark,
            "icon": str(self.icon),
        }


class Asset(BaseModel):
    name = models.CharField(max_length=70, verbose_name='链名称', db_index=True)
    mark = models.CharField(max_length=70, verbose_name='链名标识')
    icon = models.ImageField(upload_to='wallet/%Y/%m/%d/', blank=True, null=True)
    unit = models.CharField(max_length=10, verbose_name='资产精度', db_index=True)
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='链名称'
    )

    class Meta:
        verbose_name = '资产表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def list_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mark": self.user.mark,
            "icon": str(self.icon),
            "unit": self.user.unit,
            "chain": self.chain
        }


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

    def list_to_dict(self):
        return {
            "id": self.id
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
            "id": self.id
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
            "id": self.id
        }