#encoding=utf-8

import logging

from django.core.management.base import BaseCommand
from common.helpers import d0, dec, sleep
from services.market_client import MarketClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass

