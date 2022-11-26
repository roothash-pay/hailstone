#encoding=utf-8

import pytz
from django.db import models
from common.models import DecField, BaseModel, BoolYesOrNoSelect, Chain, Asset
from django.conf import settings
from common.helpers import d0


tz = pytz.timezone(settings.TIME_ZONE)


class Wallet(BaseModel):
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        related_name="wallet_chain",
        null=True, blank=True,
        verbose_name='chain'
    )
    device_id = models.CharField(max_length=70, verbose_name='device id')
    wallet_uuid = models.CharField(max_length=70, verbose_name='wallet uuid')
    wallet_name = models.CharField(max_length=70, verbose_name='wallet name')
    asset_usd = DecField(default=d0, verbose_name="total usd")
    asset_cny = DecField(default=d0, verbose_name="total cny")

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.wallet_name

    def create_wallet_asset(
            self, asset: Asset, contract_addr: str, **kw
    )->"WalletAsset":
        kw["wallet"] = self
        kw["asset"] = asset
        kw["contract_addr"] = contract_addr
        kw["asset_usd"] = d0
        kw["asset_cny"] = d0
        kw["balance"] = d0
        wallet_asset = WalletAsset.objects.create(**kw)
        return wallet_asset

    def create_address(
            self, index: str, address: str, **kw
    ) -> "Address":
        kw["wallet"] = self
        kw["index"] = index
        kw["address"] = address
        address = Address.objects.create(**kw)
        return address

    def to_dict(self):
        return {
            "id": self.id,
            "chain": self.chain.name,
            "device_id": self.device_id,
            "wallet_uuid": self.wallet_uuid,
            "wallet_name": self.wallet_name,
            "asset_usd": format(self.asset_usd, ".2f"),
            "asset_cny": format(self.asset_cny, ".2f")
        }


class WalletAsset(BaseModel):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE,
        related_name="wallet_asset_wallet",
        null=True, blank=True,
        verbose_name='wallet'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="wallet_asset_asset",
        verbose_name='asset'
    )
    contract_addr = models.CharField(max_length=70, verbose_name='contract address')
    asset_usd = DecField(default=d0, verbose_name="wallet usd")
    asset_cny = DecField(default=d0, verbose_name="wallet cny")
    balance = DecField(default=d0, verbose_name="wallet balance")

    class Meta:
        verbose_name = 'WalletAsset'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.contract_addr

    def to_dict(self):
        address_list_dict = []
        address_list = Address.objects.filter(wallet=self.wallet).order_by("id")
        for address in address_list:
            address_list_dict.append(address.to_dict(self.asset))
        return {
            "id": self.id,
            "chain": self.wallet.chain.name,
            "symbol": self.asset.name,
            "logo": str(self.asset.active_logo),
            "contract_addr": self.contract_addr,
            "balance": format(self.balance, ".4f"),
            "asset_usd": format(self.asset_usd, ".2f"),
            "asset_cny": format(self.asset_cny, ".2f"),
            "address_list": address_list_dict,
        }


class Address(BaseModel):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="wallet_address",
        verbose_name='wallet'
    )
    index = models.CharField(max_length=10, verbose_name='address index', db_index=True)
    address = models.CharField(max_length=70, verbose_name='address')

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

    def create_address_asset(
            self, asset: Asset, **kw
    ):
        kw["wallet"] = self.wallet
        kw["asset"] = asset
        kw["address"] = self
        kw["asset_usd"] = d0
        kw["asset_cny"] = d0
        kw["balance"] = d0
        address_asset = AddressAsset.objects.create(**kw)
        return address_asset

    def to_dict(self, asset: Asset):
        address_asset = AddressAsset.objects.filter(
            wallet=self.wallet,
            asset=asset,
            address=self).first()
        if address_asset is not None:
            balance = address_asset.balance
            asset_usd = address_asset.asset_usd
            asset_cny = address_asset.asset_cny
        else:
            balance = d0
            asset_usd = d0
            asset_cny = d0
        return {
            "id": self.id,
            "index": self.index,
            "address": self.address,
            "balance": format(balance, ".4f"),
            "asset_usd": format(asset_usd, ".2f"),
            "asset_cny": format(asset_cny, ".2f"),
        }


class AddressAsset(BaseModel):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE,
        related_name="address_asset_wallet",
        null=True, blank=True,
        verbose_name='wallet'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        related_name="address_asset_asset",
        null=True, blank=True,
        verbose_name='asset'
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE,
        related_name="address_asset_address",
        null=True, blank=True,
        verbose_name='address'
    )
    asset_usd = DecField(default=d0, verbose_name="address usd")
    asset_cny = DecField(default=d0, verbose_name="address cny")
    balance = DecField(default=d0, verbose_name="address balance")

    class Meta:
        verbose_name = 'AddressAsset'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address.address

    def to_dict(self):
        return {
            "balance": format(self.balance, ".4f"),
            "asset_usd": format(self.asset_usd, ".2f"),
            "asset_cny": format(self.asset_cny, ".2f"),
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
        verbose_name='chain name'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='asset name'
    )
    token_name = models.CharField(max_length=70, verbose_name='token name')
    token_symbol = models.CharField(max_length=70, verbose_name='Token symbol')
    contract_addr = models.CharField(max_length=70, verbose_name='contract address')
    decimal = models.CharField(max_length=10, verbose_name='token decimal', db_index=True)
    is_hot = models.CharField(
        max_length=32,
        choices=BoolYesOrNoSelect,
        default='no',
        verbose_name="is_hot asset"
    )

    class Meta:
        verbose_name = 'TokenConfig'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token_name

    def list_to_dict(self):
        return {
            "id": self.id,
            "asset_id": self.asset.id,
            "token_name": self.asset.name,
            "logo": str(self.asset.logo),
            "active_logo": str(self.asset.active_logo),
            "token_symbol": self.token_symbol,
            "contract_addr": self.contract_addr,
            "unit": self.decimal,
        }


class TxRecord(BaseModel):
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='chain name'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='asset name'
    )
    from_addr = models.CharField(max_length=70, verbose_name='sender')
    to_addr = models.CharField(max_length=70, verbose_name='reviver')
    amount = DecField(default=d0, verbose_name="amount")
    memo = models.CharField(max_length=70, verbose_name='memo')
    hash = models.CharField(max_length=70, verbose_name='hash')
    block_height = models.CharField(max_length=70, verbose_name='block_height')
    tx_time = models.CharField(max_length=70, verbose_name='tx_time')

    class Meta:
        verbose_name = 'TxRecord'
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
        verbose_name='chain name'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='asset name'
    )
    device_id = models.CharField(max_length=70, verbose_name='device id')
    memo = models.CharField(max_length=70, verbose_name='memo')
    address = models.CharField(max_length=70, verbose_name='address')

    class Meta:
        verbose_name = 'AddresNote'
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


class WalletHead(BaseModel):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='wallet'
    )
    wallet_head = models.CharField("wallethead", max_length=512)

    class Meta:
        verbose_name = 'WalletHead'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.wallet_head

    def to_dict(self):
        return {
            "id": self.id,
            "wallet_head": self.wallet_head
        }