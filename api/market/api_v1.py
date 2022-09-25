#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from common.api_auth import check_api_token
from common.helpers import d0, dec
from services.market_client import MarketClient
from services.savour_rpc import common_pb2


# @check_api_token
def get_symbols(request):
    params = json.loads(request.body.decode())
    consumer_token = params.get('consumer_token', "eth")
    exchange_id = params.get('exchange_id', "1")
    market_client = MarketClient()
    result = market_client.get_symbols(
        consumer_token=consumer_token,
        exchange_id=exchange_id,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return ok_json(result)


# @check_api_token
def get_stable_coin_price(request):
    params = json.loads(request.body.decode())
    consumer_token = params.get('consumer_token', "eth")
    coin_id = params.get('coin_id', "1")
    market_client = MarketClient()
    result = market_client.get_stable_coin_price(
        consumer_token=consumer_token,
        coin_id=coin_id,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return ok_json(result)


# @check_api_token
def get_stable_coins(request):
    params = json.loads(request.body.decode())
    consumer_token = params.get('consumer_token', "eth")
    market_client = MarketClient()
    result = market_client.get_stable_coins(
        consumer_token=consumer_token,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return ok_json(result)


# @check_api_token
def get_exchanges(request):
    params = json.loads(request.body.decode())
    consumer_token = params.get('consumer_token', "eth")
    market_client = MarketClient()
    result = market_client.get_exchanges(
        consumer_token=consumer_token,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return ok_json(result)


# @check_api_token
def get_assets(request):
    params = json.loads(request.body.decode())
    exchange_id = params.get('exchange_id', "eth")
    is_base = params.get('is_base', "eth")
    consumer_token = params.get('consumer_token', "eth")
    market_client = MarketClient()
    result = market_client.get_assets(
        consumer_token=consumer_token,
        exchange_id=exchange_id,
        is_base=is_base,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return ok_json(result)


# @check_api_token
def get_symbol_prices(request):
    params = json.loads(request.body.decode())
    exchange_id = params.get('exchange_id', "eth")
    symbol_id = params.get('symbol_id', "eth")
    consumer_token = params.get('consumer_token', "eth")
    market_client = MarketClient()
    result = market_client.get_symbol_prices(
        consumer_token=consumer_token,
        exchange_id=exchange_id,
        symbol_id=symbol_id,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return ok_json(result)