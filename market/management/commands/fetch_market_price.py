#encoding=utf-8

import logging

from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient
from services.savour_rpc import common_pb2


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = MarketClient()
        symbol_result = client.get_symbol_prices()
        if symbol_result.code != common_pb2.SUCCESS:
            logging.warning(symbol_result)
            return
        if len(symbol_result.coin_prices) == 0:
            return
        print(symbol_result)
