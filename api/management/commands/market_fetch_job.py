#encoding=utf-8

import datetime
from django.core.management.base import BaseCommand
from api.market.consumers import market_fetch_job


class Command(BaseCommand):
    def handle(self, *args, **options):
        market_fetch_job()


