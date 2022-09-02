#encoding=utf-8

import pytz
import json
import logging
import markdown
from django.shortcuts import render
from common.helpers import (
    ok_json,
    error_json
)
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.shortcuts import redirect
from django.conf import settings
from common.api_auth import check_api_token


@check_api_token
def get_balance(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    address = params.get('address', "")
    address = params.get('contract_address', "")
    return ok_json("ok")


@check_api_token
def get_account_info(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    address = params.get('address', "")
    return ok_json("ok")


@check_api_token
def get_fee(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def send_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def get_unspend_list(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def get_address_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def get_hash_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def submit_wallet_info(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def batch_submit_wallet(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def delete_wallet(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def get_note_book(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def add_note_book(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def upd_note_book(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")


@check_api_token
def del_note_book(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    return ok_json("ok")
