# encoding=utf-8

import logging
from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient
from market.models import StablePrice
from services.savour_rpc import common_pb2


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = MarketClient()
        consumer_token = None
        stable_result = client.get_stable_coin_price(
            consumer_token=consumer_token,
            coin_id=None,
        )
        if stable_result.code != common_pb2.SUCCESS:
            logging.warning(stable_result)
            return

        if len(stable_result.coin_prices == 0):
            return

        price_list = []
        for coin_price in stable_result.coin_prices:
            price_list.append(StablePrice(usd_price=coin_price.usd_price,
                                          cny_price=coin_price.cny_price,
                                          asset_id=coin_price.id))
        StablePrice.objects.bulk_create(price_list)
