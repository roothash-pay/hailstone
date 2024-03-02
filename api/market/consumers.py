from channels.generic.websocket import WebsocketConsumer
import json

from apscheduler.scheduler import Scheduler
import pymysql as db
from hailstone.settings import DATABASES

db_config = DATABASES['default']

db_connection = None


def get_connection():
    global db_connection

    if db_connection is not None:
        return db_connection
    db_connection = db.connect(host=db_config['HOST'], user=db_config['USER'], password=db_config['PASSWORD'],
                               db=db_config['NAME'], connect_timeout=10000)
    return db_connection


market_scheduler = Scheduler()

market_exchange_id_dict = {}
market_exchange_sub_client = {}


def dispatch_market_data():
    global market_exchange_sub_client

    for key in market_exchange_sub_client:
        client = market_exchange_sub_client[key]
        client.send_exchange_data()


def get_value(dict_data: dict, key: str):
    if key in dict_data:
        return dict_data[key]
    return None


def format_value(value, base=4):
    try:
        return format(value, "." + str(base) + "f")
    except:
        return None


def format_market_data(item):
    market_data = {
        'id': get_value(item, 'id'),
        'symbol': get_value(item, 'pair'),
        'symbol_id': get_value(item, 'symbol_id'),
        'created_at': get_value(item, 'created_at'),
        'updated_at': get_value(item, 'updated_at'),
        'icon': get_value(item, 'icon'),
        'base_asset': format_value(get_value(item, 'base_asset')),
        'qoute_asset': format_value(get_value(item, 'qoute_asset')),
        'sell_price': format_value(get_value(item, 'sell_price')),
        'buy_price': format_value(get_value(item, 'buy_price')),
        'avg_price': format_value(get_value(item, 'avg_price')),
        'usd_price': format_value(get_value(item, 'usd_price')),
        'cny_price': format_value(get_value(item, 'cny_price')),
        'margin': format_value(get_value(item, 'margin')),
    }
    return market_data


def fetch_market_data():
    global market_exchange_id_dict

    temp_market_dict = {}
    conn = get_connection()
    cursor = conn.cursor(db.cursors.DictCursor)

    sql_str = 'SELECT t1.*,t2.name as pair FROM market_marketprice t1 left join market_symbol t2 on t1.symbol_id = t2.id WHERE exchange_id = %s '
    cursor.execute(sql_str, [1])
    rows = cursor.fetchall()

    if len(rows) == 0:
        return

    for item in rows:
        exchange_id = 0
        if 'exchange_id' in item:
            exchange_id = item['exchange_id']
        if exchange_id not in temp_market_dict:
            temp_market_dict[exchange_id] = []
        temp_market_dict[exchange_id].append(format_market_data(item))
    cursor.close()
    conn.commit()
    market_exchange_id_dict.clear()
    market_exchange_id_dict = temp_market_dict


@market_scheduler.interval_schedule(seconds=3)
def market_fetch_job():
    fetch_market_data()
    dispatch_market_data()


# market_scheduler.start()


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
        }, default=str), )

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
