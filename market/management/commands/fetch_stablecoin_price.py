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

        asset_name_list = []
        for coin_price in stable_result.coin_prices:
            asset_name_list.append(coin_price.name)

        asset_list = Asset.objects.filter(name__in=asset_name_list).first()

        asset_dict = {}
        for asset_item in asset_list:
            asset_dict[asset_item.name] = asset_item

        price_list = []
        for coin_price in stable_result.coin_prices:
            if coin_price.name not in asset_dict:
                continue
            price_list.append(
                StablePrice(
                    usd_price=coin_price.usd_price,
                    cny_price=coin_price.cny_price,
                    asset=asset_dict[coin_price.name]
                ))

        if len(price_list) > 0:
            StablePrice.objects.bulk_update(price_list)
