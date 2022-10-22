from django.core.management.base import BaseCommand
from market.models import MarketPrice
from api.market.consumers import get_market_sub_client, set_market_exchange_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_market_data()
        dispatch_market_data()


def dispatch_market_data():
    print('dispatch_market_data')
    sub_clients = get_market_sub_client()
    for key in sub_clients:
        client = sub_clients[key]
        client.send_exchange_data()


def fetch_market_data():
    print('fetch_market_data')

    temp_market_dict = {}
    market_price_list = MarketPrice.objects.filter(exchange_id__in=[1]).order_by("id")
    for market_price in market_price_list:
        if market_price.exchange_id not in temp_market_dict:
            temp_market_dict[market_price.exchange_id] = []
        temp_market_dict[market_price.exchange_id].append(market_price.as_dict())

    set_market_exchange_data(temp_market_dict)
