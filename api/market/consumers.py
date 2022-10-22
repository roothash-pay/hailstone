from channels.generic.websocket import WebsocketConsumer
import json

import copy

market_exchange_id_dict = {}

market_exchange_sub_client = {}


def get_market_sub_client():
    global market_exchange_sub_client
    return copy.copy(market_exchange_sub_client)


def set_market_exchange_data(exchange_dict):
    global market_exchange_id_dict
    market_exchange_id_dict.clear()
    market_exchange_id_dict = exchange_dict


class MarketConsumers(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.exchange_id = None
        self.uuid = None

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        try:
            del market_exchange_sub_client[self.uuid]
        except:
            print('un_register error')

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

        op = params.get('method')
        client_id = params.get('uuid')
        if op == 'register':
            self.exchange_id = int(params.get('exchange_id', 0))
            self.uuid = client_id
            self.register()
        else:
            self.un_register()

    def register(self):
        market_exchange_sub_client[self.uuid] = self

    def un_register(self):
        try:
            del market_exchange_sub_client[self.uuid]
        except:
            print('un_register error')
