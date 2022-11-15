#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from wallet.models import WalletHead
from common.helpers import gen_rsa_crypto_key

EMPTY = [None, "None", 0, ""]

# @check_api_token
def get_head(request):
    params = json.loads(request.body.decode())
    wallet_id = params.get("wallet_id", None)
    if wallet_id in EMPTY:
        return error_json("Invalid Params")
    resp = []
    list_head = WalletHead.objects.filter(wallet_id=wallet_id)
    for head in list_head:
        resp.append(head.to_dict())
    return ok_json(resp)


def save_head(request):
    params = json.loads(request.body.decode())
    wallet_head = params.get("wallet_head", None)
    wallet_id = params.get("wallet_id", None)
    if wallet_head in EMPTY or wallet_id in EMPTY:
        return error_json("Invalid Params")

    target = WalletHead.objects.filter(wallet_id=wallet_id, wallet_head=wallet_head)
    if len(target) != 0:
        return ok_json(target[0].to_dict())
    else:
        private_key, public_key = gen_rsa_crypto_key()
        # TODO upload encrypt_head ipfs
        # encrypt_head = encrypt_data(wallet_head, public_key)
        head_ipfs_addr = "ipfs://ip.addr"

        s = WalletHead.objects.create(
            wallet_id=wallet_id,
            wallet_head=wallet_head,
            head_public_key=public_key,
            head_private_key=private_key,
            head_ipfs_addr=head_ipfs_addr,
        )
    return ok_json(s.to_dict())

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


