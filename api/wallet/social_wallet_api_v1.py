#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from common.api_auth import check_api_token
from common.helpers import d0, dec
from services.wallet_client import WalletClient
from services.savour_rpc import common_pb2


# @check_api_token
def get_recovery_key(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    contract_address = params.get('contract_address', "")
    return ok_json("")


# @check_api_token
def set_recovery_key(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    contract_address = params.get('contract_address', "")
    return ok_json("")


