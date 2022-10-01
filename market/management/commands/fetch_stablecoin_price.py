# encoding=utf-8

import logging
from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient
from market.models import StablePrice, Asset
from services.savour_rpc import common_pb2
from services.savour_rpc import market_pb2_grpc
from services.savour_rpc import market_pb2


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = MarketClient()
        stable_result = client.get_stable_coin_price()
        if stable_result.code != common_pb2.SUCCESS:
            logging.warning(stable_result)
            return
        if len(stable_result.coin_prices) == 0:
            logging.warning(stable_result)
            return
        for coin_price in stable_result.coin_prices:
            asset = Asset.objects.filter(
                name=coin_price.name
            ).first()
            if asset is not None:
                StablePrice.objects.update_or_create(
                    asset=asset,
                    defaults={
                        "usd_price": coin_price.usd_price,
                        "cny_price": coin_price.cny_price
                    }
                )