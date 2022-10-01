#encoding=utf-8

import logging

from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient
from services.savour_rpc import common_pb2
from market.models import StablePrice, Asset, MarketPrice


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = MarketClient()
        symbol_result = client.get_symbol_prices()
        if symbol_result.code != common_pb2.SUCCESS:
            logging.warning(symbol_result)
            return
        if len(symbol_result.symbol_prices) == 0:
            logging.warning(symbol_result)
            return

        price_list = []
        for item in symbol_result.symbol_prices:
            price_list.append(
                MarketPrice(
                    usd_price=item.usd_price,
                    cny_price=item.cny_price,
                    avg_price=item.avg_price,
                    buy_price=item.buy_price,
                    sell_price=item.sell_price,
                    margin=item.margin,
                    # symbol_id=int(item.id),
                    # base_asset_id=1,
                    # exchange_id=1,
                    # qoute_asset_id=1,
                ))
        MarketPrice.objects.bulk_create(price_list)

