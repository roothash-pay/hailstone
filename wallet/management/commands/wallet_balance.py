#encoding=utf-8

from django.core.management.base import BaseCommand
from wallet.models import Wallet, AddressAsset
from common.helpers import d0


class Command(BaseCommand):
    def handle(self, *args, **options):
        wallet_list = Wallet.objects.all()
        for wallet in wallet_list:
            wallet_asset_usd = d0
            wallet_asset_cny = d0
            address_asset_list = AddressAsset.objects.filter(wallet=wallet)
            for address_asset in address_asset_list:
                wallet_asset_usd += address_asset.asset_usd
                wallet_asset_cny += address_asset.asset_cny
            wallet.asset_usd = wallet_asset_usd
            wallet.asset_cny = wallet_asset_cny
            wallet.save()
