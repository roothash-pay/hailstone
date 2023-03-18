from django.db import models
from common.model_fields import DecField
from common.models import BaseModel, Asset
from common.helpers import d0

CommonStatus = [(x, x) for x in ['Active', 'Down']]
ExchangeCate = [(x, x) for x in ['Cex', 'Dex']]
SymbolCat = [(x, x) for x in ['Spot', 'Future', 'Option']]


class Exchange(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='交易所名称'
    )
    config = models.TextField(
        blank=True,
        verbose_name='配置信息'
    )
    market_type = models.CharField(
        max_length=100,
        choices=ExchangeCate,
        default="Cex",
        verbose_name='交易所类别'
    )
    status = models.CharField(
        max_length=100,
        choices=CommonStatus,
        default='Active',
        verbose_name='状态'
    )

    class Meta:
        verbose_name = 'Exchange'
        verbose_name_plural = verbose_name

    @property
    def is_active(self) -> bool:
        return self.status == 'Active'

    @property
    def is_down(self) -> bool:
        return not self.is_active

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'market_type': self.market_type,
            'status': self.status
        }


class Symbol(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='交易对名称'
    )
    icon = models.ImageField(upload_to='symbol/%Y/%m/%d/', blank=True, null=True)
    base_asset = models.ForeignKey(
        Asset, blank=True,
        related_name='base_symbols',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='base资产'
    )
    quote_asset = models.ForeignKey(
        Asset, blank=True,
        related_name='quote_symbols',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='报价资产'
    )
    status = models.CharField(
        max_length=100,
        choices=CommonStatus,
        default='Active',
        verbose_name='状态'
    )
    category = models.CharField(
        max_length=100,
        choices=SymbolCat,
        default="Spot"
    )

    class Meta:
        verbose_name = 'Symbol'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MarketPrice(BaseModel):
    symbol = models.ForeignKey(
        Symbol, related_name='price_symbol',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    exchange = models.ForeignKey(
        Exchange, related_name='price_exchange',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    base_asset = models.ForeignKey(
        Asset, related_name='base_relate_asset',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    qoute_asset = models.ForeignKey(
        Asset, related_name='qoute_relate_asset',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    sell_price = DecField(default=0)
    buy_price = DecField(default=0)
    usd_price = DecField(default=0)
    cny_price = DecField(default=0)
    avg_price = DecField(default=0)
    margin = DecField(default=0)

    class Meta:
        verbose_name = 'MarketPrice'
        verbose_name_plural = verbose_name

    def as_dict(self):
        if self.margin >= d0:
            margin = '+' + str(format(self.margin, ".2f")) + '%'
        else:
            margin = '-' + str(format(self.margin, ".2f")) + '%'
        return {
            'id': self.id,
            'symbol': self.symbol.name,
            'exchange': self.exchange.name,
            'icon': str(self.symbol.icon),
            'base_asset': self.base_asset.name,
            'qoute_asset': self.qoute_asset.name,
            'sell_price': format(self.sell_price, ".4f"),
            'buy_price': format(self.buy_price, ".4f"),
            'avg_price': format(self.avg_price, ".4f"),
            'usd_price': format(self.usd_price, ".4f"),
            'cny_price': format(self.cny_price, ".4f"),
            'margin': margin,
        }


class StablePrice(BaseModel):
    asset = models.ForeignKey(
        Asset, related_name='otc_asset',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    usd_price = DecField(default=0)
    cny_price = DecField(default=0)

    class Meta:
        verbose_name = 'StablePrice'
        verbose_name_plural = verbose_name

    def as_dict(self):
        return {
            'asset': self.asset.name,
            'usd_price': format(self.usd_price, ".4f"),
            'cny_price': format(self.cny_price, ".4f")
        }


class FavoriteMarket(BaseModel):
    device_id = models.CharField(max_length=70, verbose_name='设备ID')
    market_price = models.ForeignKey(
        MarketPrice, related_name='symbol_market_price',
        null=True, blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'FavoriteMarket'
        verbose_name_plural = verbose_name

    def as_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'market_price': self.market_price.as_dict()
        }

