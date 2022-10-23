#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from common.api_auth import check_api_token
from common.helpers import d0, dec
from market.models import Exchange, MarketPrice, FavoriteMarket



# @check_api_token
def get_exchanges(request):
    params = json.loads(request.body.decode())
    type = params.get('type', "Cex")
    if type not in ["Cex",  "Dex"]:
        return error_json("Invalid exchange type", 4000)
    exchange_list = Exchange.objects.filter(status='Active')
    return_exchange_list = []
    for exchange in exchange_list:
        return_exchange_list.append(exchange.as_dict())
    return ok_json(return_exchange_list)


# @check_api_token
def get_exchange_market(request):
    params = json.loads(request.body.decode())
    exchange_id = int(params.get('exchange_id', 0))
    device_id = params.get('device_id', None)
    return_market_price_data = []
    if device_id in [None, "0", "", "None", 0,]:
        if exchange_id == 0:
            return error_json("Invalid param exchange_id", 4000)
        exchange = Exchange.objects.filter(id=exchange_id).first()
        if exchange is None:
            return error_json("unsport exchange", 4000)
        market_price_list = MarketPrice.objects.filter(exchange=exchange).order_by("id")
        for market_price in market_price_list:
            return_market_price_data.append(market_price.as_dict())
    else:
        fm_list = FavoriteMarket.objects.filter(device_id=device_id).order_by("id")
        for fm in fm_list:
            return_market_price_data.append(fm.market_price.as_dict())
    return ok_json(return_market_price_data)


# @check_api_token
def get_market_detail(request):
    params = json.loads(request.body.decode())
    market_id = int(params.get('market_id', 0))
    return ok_json(market_id)


# @check_api_token
def add_favorite_market(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', None)
    market_id = params.get('market_id', None)
    if device_id in [None, "None", 0, ""]:
        return error_json("Invalid param device_id")
    if market_id in [None, "None", 0, ""]:
        return error_json("Invalid param market_id")
    market_price = MarketPrice.objects.filter(id=market_id).first()
    if market_price is None:
        return error_json("no this market_price", 4000)
    fm = FavoriteMarket.objects.filter(device_id=device_id, market_price=market_price).first()
    if fm is not None:
        return error_json("You have already add this market price", 4000)
    else:
        FavoriteMarket.objects.create(
            device_id=device_id,
            market_price=market_price
        )
    return ok_json("add favorite market price success")


# @check_api_token
def remove_favorite_market(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', None)
    market_id = params.get('market_id', None)
    if device_id in [None, "None", 0, ""]:
        return error_json("Invalid param device_id")
    if market_id in [None, "None", 0, ""]:
        return error_json("Invalid param market_id")
    market_price = MarketPrice.objects.filter(id=market_id).first()
    if market_price is None:
        return error_json("no this market_price", 4000)
    FavoriteMarket.objects.filter(
        device_id=device_id,
        market_price=market_price
    ).delete()
    return ok_json("remove market price success")
