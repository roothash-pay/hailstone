#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from common.api_auth import check_api_token
from wallet.models import Chain, Asset, Address, AddresNote
from common.helpers import d0, dec
from services.wallet_client import WalletClient
from services.savour_rpc import common_pb2


# @check_api_token
def get_balance(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    address = params.get('address', "")
    contract_address = params.get('contract_address', "")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if address is None:
        return error_json("address is empty", 4000)
    wallet_client = WalletClient()
    result = wallet_client.get_balance(
        chain=chain,
        coin=symbol,
        network=network,
        address=address,
        contract_address=contract_address
    )
    if result.code == common_pb2.SUCCESS:
        Address.objects.filter(chain=db_chain, address=address, asset=db_asset).update(
            balance=dec(result.balance) / dec(db_asset.unit),
        )
        data = {
            "balance": dec(result.balance) / dec(db_asset.unit),
        }
        return ok_json(data)
    else:
        address_db = Address.objects.filter(chain=db_chain, address=address, asset=db_asset).first()
        data = {
            "balance": address_db.balance,
        }
        return ok_json(data)


# @check_api_token
def get_nonce(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    address = params.get('address', "")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if address is None:
        return error_json("address is empty", 4000)
    wallet_client = WalletClient()
    result = wallet_client.get_nonce(
        chain=chain,
        coin=symbol,
        network=network,
        address=address
    )
    if result.code == common_pb2.SUCCESS:
        data = {
            "nonce": result.nonce,
        }
        return ok_json(data)
    else:
        return error_json("rpc server fail")


# @check_api_token
def get_account_info(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "sol")
    symbol = params.get('symbol', "sol")
    address = params.get('address', "")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if address is None:
        return error_json("address is empty", 4000)
    wallet_client = WalletClient()
    result = wallet_client.get_account(
        chain=chain,
        coin=symbol,
        network=network,
        address=address
    )
    if result.code == common_pb2.SUCCESS:
        data = {
            "account_number": result.account_number,
            "nonce": result.nonce,
        }
        return ok_json(data)
    else:
        return error_json("rpc server fail")


# @check_api_token
def get_fee(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    fee_way = params.get('fee_way', "low")   # low medium high
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    wallet_client = WalletClient()
    result = wallet_client.get_gasPrice(
        chain=chain,
        coin=symbol,
        network=network,
    )
    if result.code == common_pb2.SUCCESS:
        if fee_way == "high":
            gas_pirce = result.gas * 10
        elif fee_way == "medium":
            gas_pirce = result.gas * 5
        else:
            gas_pirce = result.gas
        data = {
            "gas": gas_pirce
        }
        return ok_json(data)
    else:
        return error_json("rpc server fail")


# @check_api_token
def send_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    rawtx = params.get('rawtx', None)
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if rawtx in ["", None]:
        return error_json("rawtx is empty", 4000)
    wallet_client = WalletClient()
    result = wallet_client.send_transaction(
        chain=chain,
        coin=symbol,
        network=network,
        raw_tx=rawtx,
    )
    if result.code == common_pb2.SUCCESS:
        data = {
            "hash": result.hash
        }
        return ok_json(data)
    else:
        return error_json("rpc server fail")


# @check_api_token
def get_address_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    address = params.get('address', "")
    contract_address = params.get('contract_address', "")
    page = params.get('page', "")
    page_size = params.get('page_size', "")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if address is None:
        return error_json("address is empty", 4000)
    wallet_client = WalletClient()
    result = wallet_client.get_tx_by_address(
        chain=chain,
        coin=symbol,
        network=network,
        address=address,
        contract_address=contract_address,
        page=page,
        pagesize=page_size,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("rpc server fail")


# @check_api_token
def get_hash_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    hash = params.get('hash', "")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if hash is None:
        return error_json("hash is empty", 4000)
    wallet_client = WalletClient()
    result = wallet_client.get_tx_by_hash(
        chain=chain,
        coin=symbol,
        network=network,
        hash=hash
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("rpc server fail")


# @check_api_token
def submit_wallet_info(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', "eth")
    symbol = params.get('symbol', "eth")
    network = params.get('network', "mainnet")
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    wallet_name = params.get('wallet_name', "")
    address = params.get('address', "")
    contract_addr = params.get('address', "")
    if chain in ["", None]:
        return error_json("chain is empty", 4000)
    if symbol in ["", None]:
        return error_json("symbol is empty", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if device_id in ["", None]:
        return error_json("device_id is empty", 4000)
    if wallet_uuid in ["", None]:
        return error_json("wallet_uuid is empty", 4000)
    if wallet_name in ["", None]:
        return error_json("wallet_name is empty", 4000)
    if address in ["", None]:
        return error_json("address is empty", 4000)
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    db_address = Address.objects.filter(device_id=device_id, wallet_uuid=wallet_uuid).first()
    if db_address is not None:
        return error_json("this wallet is exist", 4000)
    else:
        Address.objects.create(
            chain=db_chain,
            asset=db_asset,
            network=network,
            device_id=device_id,
            wallet_uuid=wallet_uuid,
            wallet_name=wallet_name,
            address=address,
            contract_addr=contract_addr,
            balance=d0,
        )
    return ok_json("submit wallet success")


# @check_api_token
def batch_submit_wallet(request):
    params = json.loads(request.body.decode())
    batch_wallet = params.get('batch_wallet', None)
    if batch_wallet is None:
        return error_json("batch_wallet is empty", 4000)
    for wallet in batch_wallet:
        db_address = Address.objects.filter(device_id=wallet.get("device_id", "0"), wallet_uuid=wallet.get("wallet_uuid", "0")).first()
        if db_address is None:
            db_chain = Chain.objects.filter(name=wallet.get("chain")).first()
            if db_chain is None:
                return error_json("Do not support chain", 4000)
            db_asset = Asset.objects.filter(name=wallet.get("symbol")).first()
            if db_chain and db_asset is not None:
                Address.objects.create(
                    chain=db_chain,
                    asset=db_asset,
                    network=wallet.get("network"),
                    device_id=wallet.get("device_id"),
                    wallet_uuid=wallet.get("wallet_uuid"),
                    wallet_name=wallet.get("wallet_name"),
                    address=wallet.get("address"),
                    contract_addr=wallet.get("contract_addr"),
                    balance=d0,
                )
    return ok_json("batch submit wallet success")


@check_api_token
def delete_wallet(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    wallet_uuid = params.get('wallet_uuid')
    Address.objects.filter(
        device_id=device_id,
        wallet_uuid=wallet_uuid).delete()
    return ok_json("delete wallet success")


@check_api_token
def get_unspend_list(request):
    params = json.loads(request.body.decode())
    return ok_json("ok")


@check_api_token
def get_note_book(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    page = params.get('page')
    page_size = params.get('page')
    start = page * page_size
    end = start + page_size
    address_list = AddresNote.objects.filter(device_id=device_id).order_by("-id")[start:end]
    total = AddresNote.objects.filter(device_id=device_id).order_by("-id").count()
    ret_address_data = []
    for address in address_list:
        ret_address_data.append(address.list_to_dict())
    data = {
        "total": total,
        "data": ret_address_data
    }
    return ok_json(data)


@check_api_token
def add_note_book(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    chain = params.get('chain')
    asset = params.get('asset')
    memo = params.get('memo')
    address = params.get('address')
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=asset).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    address_db = AddresNote.object.filter(
        chain=db_chain,
        asset=db_asset,
        device_id=device_id,
        memo=memo,
        address=address
    ).first()
    if address_db is not None:
        return error_json("this address exist", 4000)
    else:
        AddresNote.objects.create(
            chain=db_chain,
            asset=db_asset,
            device_id=device_id,
            memo=memo,
            address=address
        )
        return ok_json("add note book success")


@check_api_token
def upd_note_book(request):
    params = json.loads(request.body.decode())
    addr_note_id = int(params.get('addr_note_id'))
    memo = params.get('memo')
    address = params.get('address')
    AddresNote.object.filter(id=addr_note_id).update(
        memo=memo,
        address=address
    )
    return ok_json("update note book success")


@check_api_token
def del_note_book(request):
    params = json.loads(request.body.decode())
    addr_note_id = int(params.get('addr_note_id'))
    AddresNote.objects.filter(id=addr_note_id).delete()
    return ok_json("delete note book success")
