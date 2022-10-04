from channels.generic.websocket import WebsocketConsumer
import json

import uuid
from market.models import MarketPrice
from apscheduler.scheduler import Scheduler

market_scheduler = Scheduler()

market_exchange_id_dict = {}

market_exchange_sub_client = {}


def dispatch_market_data():
    print('dispatch_market_data')
    global market_exchange_sub_client

    for key in market_exchange_sub_client:
        client = market_exchange_sub_client[key]
        client.send_exchange_data()


def fetch_market_data():
    print('fetch_market_data')
    global market_exchange_id_dict

    temp_market_dict = {}
    market_price_list = MarketPrice.objects.filter(exchange_id__in=[1]).order_by("id")
    for market_price in market_price_list:
        if market_price.exchange_id not in temp_market_dict:
            temp_market_dict[market_price.exchange_id] = []
        temp_market_dict[market_price.exchange_id].append(market_price.as_dict())

    market_exchange_id_dict.clear()
    market_exchange_id_dict = temp_market_dict


@market_scheduler.interval_schedule(seconds=3)
def market_fetch_job():
    fetch_market_data()
    dispatch_market_data()


market_scheduler.start()


class MarketConsumers(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.exchange_id = None

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print('disconnect' + close_code)

    def send_empty_data(self):
        self.send(text_data=json.dumps({
            'code': 1,
            'msg': 'no data',
            'data': None
        }))

    def send_exchange_data(self):
        if self.exchange_id == 0:
            self.send_empty_data()
            return
        if self.exchange_id not in market_exchange_id_dict:
            self.send_empty_data()
            return
        self.send(text_data=json.dumps({
            'code': 0,
            'msg': 'success',
            'data': market_exchange_id_dict[self.exchange_id]
        }))

    def receive(self, text_data=None, bytes_data=None):
        params = json.loads(text_data)
        self.exchange_id = int(params.get('exchange_id', 0))
        # device_id = params.get('device_id', None)
        # if device_id in [None, "", "None", 0]:
        #     self.send_exchange_data(exchange_id)
        self.register()

    def register(self):
        client_id = uuid.uuid4()
        market_exchange_sub_client[client_id] = self
