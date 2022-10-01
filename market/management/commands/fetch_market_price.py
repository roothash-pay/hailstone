# encoding=utf-8

import logging

from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient
from services.savour_rpc import common_pb2
from market.models import StablePrice, Asset, MarketPrice, Symbol


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

        # symbol_id_list = []
        asset_name_list = []
        for item in symbol_result.symbol_prices:
            # symbol_id_list.append(item.id)
            asset_name_list.append(item.base)
            asset_name_list.append(item.quote)

        price_list = []

        asset_dict = {}
        asset_list = Asset.objects.filter(name__in=asset_name_list)
        for asset in asset_list:
            asset_dict[asset.name] = asset

        for item in symbol_result.symbol_prices:
            quote_asset = None
            base_asset = None
            if item.quote in asset_dict:
                quote_asset = asset_dict[item.quote]
            if item.base in asset_dict:
                base_asset = asset_dict[item.base]

            price_list.append(
                MarketPrice(
                    usd_price=item.usd_price,
                    cny_price=item.cny_price,
                    avg_price=item.avg_price,
                    buy_price=item.buy_price,
                    sell_price=item.sell_price,
                    margin=item.margin,
                    # symbol_id=int(item.id),
                    # exchange= NONE,
                    qoute_asset=quote_asset,
                    base_asset=base_asset,
                ))
        MarketPrice.objects.bulk_create(price_list)
