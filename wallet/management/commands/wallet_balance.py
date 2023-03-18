#encoding=utf-8

from django.core.management.base import BaseCommand
from wallet.models import WalletAsset, AddressAsset
from common.helpers import d0


class Command(BaseCommand):
    def handle(self, *args, **options):
        wallet_asset_list = WalletAsset.objects.all()
        for wallet_asset in wallet_asset_list:
            address_asset_list = AddressAsset.objects.filter(wallet=wallet_asset.wallet, asset=wallet_asset.asset)
            wallet_asset_usd = d0
            wallet_asset_cny = d0
            for address_asset in address_asset_list:
                wallet_asset_usd += address_asset.asset_usd
                wallet_asset_cny += address_asset.asset_cny
            wallet_asset.asset_usd = wallet_asset_usd
            wallet_asset.asset_cny = wallet_asset_cny
            wallet_asset.save()
