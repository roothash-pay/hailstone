# encoding=utf-8
import pytz

from django.conf import settings
from django.db import models
from common.models import BaseModel, Asset


class StakingChain(BaseModel):
    name = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='链名称'
    )
    chain_id = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='链ID'
    )
    rpc_url = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="节点 rpc",
    )

    class Meta:
        verbose_name = 'StakingChain'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'title': self.name,
            'chain_id': self.chain_id,
            'rpc_url': str(self.rpc_url),
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }


class StakingStrategy(BaseModel):
    chain = models.ForeignKey(
        StakingChain,
        blank=True,
        related_name='staking_chain_strategies',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='质押的链'
    )
    name = models.CharField(
        default="Social",
        max_length=100,
        unique=False,
        verbose_name='质押模块名称'
    )
    address = models.CharField(
        default="",
        max_length=100,
        unique=False,
        verbose_name='策略地址'
    )

    class Meta:
        verbose_name = 'StakingStrategy'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Node(BaseModel):
    chain = models.ForeignKey(
        StakingChain,
        blank=True,
        related_name='staking_chain',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='质押的链'
    )
    strategy = models.ForeignKey(
        StakingStrategy,
        blank=True,
        related_name='staking_chain',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='质押策略'
    )
    name = models.CharField(
        default="unknown",
        max_length=500,
        unique=False,
        verbose_name='节点名称'
    )
    eth_income = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='Eth 收益金额'
    )
    eth_income_rate = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='Eth 收益率'
    )
    dp_income = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='DP 收益金额'
    )
    dp_income_rate = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='DP 收益率'
    )
    eth_evil = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='Eth 惩罚金额'
    )
    eth_evil_rate = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='Eth 惩罚率'
    )
    dp_evil = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='DP 惩罚金额'
    )
    dp_evil_rate = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='DP 惩罚率'
    )
    tvl = models.CharField(
        default="0",
        max_length=500,
        unique=False,
        verbose_name='总质押量'
    )

    class Meta:
        verbose_name = 'Node'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        return {
            'id': self.id,
            'chain': self.chain.name,
            'strategy': self.strategy.name,
            'name': self.name,
            'eth_income': self.eth_income,
            'eth_income_rate': self.eth_income_rate,
            'dp_income': self.dp_income,
            'dp_income_rate': self.dp_income_rate,
            'eth_evil': self.eth_evil,
            'eth_evil_rate': self.eth_evil_rate,
            'dp_evil': self.eth_evil,
            'dp_evil_rate': self.eth_evil_rate,
            'tvl': self.tvl,
            'created_at': self.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        }
