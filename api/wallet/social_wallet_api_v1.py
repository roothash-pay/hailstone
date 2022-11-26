#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from wallet.models import (
    Wallet,
    WalletHead
)
from common.helpers import gen_rsa_crypto_key
from services.keylocker_client import KeyLockerClient


EMPTY = [None, "None", 0, ""]


# @check_api_token
def get_head(request):
    params = json.loads(request.body.decode())
    wallet_uuid = params.get("wallet_uuid", None)
    social_code = params.get('social_code', None)
    contract_addr = params.get('contract_addr', None)
    file_cid = params.get('file_cid',  None)
    if wallet_uuid in EMPTY or social_code in EMPTY or contract_addr in EMPTY or file_cid in EMPTY:
        return error_json("Invalid Params", 4000)
    wallet = Wallet.objects.filter(wallet_uuid=wallet_uuid).first()
    if wallet is None:
        return error_json("No this wallet", 4000)
    wallet_head_resp = []
    list_head = WalletHead.objects.filter(wallet=wallet)
    for head in list_head:
        wallet_head_resp.append(head.to_dict())
    return ok_json(wallet_head_resp)


def save_head(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', None)
    wallet_head = params.get("wallet_head", None)
    wallet_uuid = params.get("wallet_uuid", None)
    social_code = params.get('social_code', None)
    password = params.get('password', None)
    if chain in EMPTY or wallet_head in EMPTY or wallet_uuid in EMPTY or social_code in EMPTY or password in EMPTY:
        return error_json("Invalid Params", 4000)
    wallet = Wallet.objects.filter(wallet_uuid=wallet_uuid).first()
    if wallet is None:
        return error_json("No this wallet", 4000)
    target = WalletHead.objects.filter(wallet=wallet, wallet_head=wallet_head).first()
    if target is not None:
        return ok_json(target.to_dict())
    else:
        klclient = KeyLockerClient()
        klclient.set_social_key(
            chain=chain,
            wallet_uuid=wallet_uuid,
            key=wallet_head,
            password=password,
            social_code=social_code,
        )
        s = WalletHead.objects.create(
            wallet=wallet,
            wallet_head=wallet_head,
        )
        return ok_json(s.to_dict())


# @check_api_token
def get_recovery_key(request):
    params = json.loads(request.body.decode())
    file_cid = params.get('network', None)
    chain = params.get('chain', None)
    wallet_uuid = params.get('uuid', None)
    social_code = params.get('social_code', None)
    contract_addr = params.get('contract_addr', None)
    if file_cid in EMPTY or chain in EMPTY or wallet_uuid in EMPTY or social_code in EMPTY or contract_addr in EMPTY:
        return error_json("Invalid Params", 4000)
    klclient = KeyLockerClient()
    gskey = klclient.get_social_key(
        chain=chain,
        wallet_uuid=wallet_uuid,
        social_code=social_code,
        file_cid=file_cid,
        contract=contract_addr
    )
    return ok_json(gskey)


# @check_api_token
def set_recovery_key(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', None)
    wallet_uuid = params.get('wallet_uuid', None)
    key = params.get('key', None)
    password = params.get('password', None)
    social_code = params.get('social_code', None)
    if key in EMPTY or chain in EMPTY or wallet_uuid in EMPTY or social_code in EMPTY or password in EMPTY:
        return error_json("Invalid Params", 4000)
    klclient = KeyLockerClient()
    klclient.set_social_key(
        chain=chain,
        wallet_uuid=wallet_uuid,
        key=key,
        password=password,
        social_code=social_code,
    )
    return ok_json("set recovery key success")


