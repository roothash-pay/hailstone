#encoding=utf-8

import datetime
from django.core.management.base import BaseCommand
from market.models import MarketPrice


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.now().date()
        start_date = now - datetime.timedelta(7)
        MarketPrice.objects.filter(created_at__lt=start_date).delete()

