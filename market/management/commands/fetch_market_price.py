# encoding=utf-8

import logging

from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient
from services.savour_rpc import common_pb2
from market.models import StablePrice, Asset, MarketPrice, Symbol, Exchange


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
        print(symbol_result)
        symbol_list = []
        exchange_list = []
        asset_name_list = []

        for item in symbol_result.symbol_prices:
            asset_name_list.append(item.base)
            asset_name_list.append(item.quote)
            exchange_list.append(item.exchange)
            symbol_list.append(item.symbol)

        price_list = []

        asset_dict = {}
        symbol_dict = {}
        exchange_dict = {}
        symbols = Symbol.objects.filter(name__in=symbol_list)
        for symbol in symbols:
            symbol_dict[symbol.name] = symbol

        exchanges = Exchange.objects.filter(name__in=exchange_list)
        for exchange in exchanges:
            exchange_dict[exchange.name] = exchange

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
                    symbol=symbol_dict[item.symbol],
                    exchange=exchange_dict[item.exchange],
                    qoute_asset=quote_asset,
                    base_asset=base_asset,
                ))
        MarketPrice.objects.bulk_create(price_list)
