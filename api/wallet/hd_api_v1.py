#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from common.api_auth import check_api_token
from wallet.models import (
    Chain,
    Asset,
    Wallet,
    WalletAsset,
    Address,
    AddressAsset,
    AddresNote,
    TokenConfig,
    AddressAmountStat
)
from common.helpers import d0, dec
from services.wallet_client import WalletClient
from services.savour_rpc import common_pb2
from market.models import StablePrice, MarketPrice
from decimal import Decimal
from api.wallet.types import AddressTransaction
from django.db import transaction

EMPTY = [None, "None", 0, ""]


# @check_api_token
def get_balance(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    index = params.get('index', "0")
    contract_addr = params.get('contract_addr', "")
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
        contract_address=contract_addr
    )
    if symbol not in ["USDT", "USDC", "DAI"]:
        market_price = MarketPrice.objects.filter(
            qoute_asset__id=db_asset.id,
            exchange__name="binance"
        ).order_by("-id").first()
        if market_price is not None:
            usd_price = market_price.usd_price
            cny_price = market_price.cny_price
        else:
            usd_price, cny_price = 1, 7
    else:
        stable_price = StablePrice.objects.filter(
            asset__id=db_asset.id,
        ).order_by("-id").first()
        if stable_price is not None:
            usd_price = stable_price.usd_price
            cny_price = stable_price.cny_price
        else:
            usd_price, cny_price = 1, 7
    wallet = Wallet.objects.filter(device_id=device_id, wallet_uuid=wallet_uuid).first()
    if wallet is None:
        return error_json("no this wallet", 4000)
    data_stat = []
    if result.code == common_pb2.SUCCESS:
        data_stat = []
        balance = Decimal(result.balance) / Decimal(10 ** int(db_asset.unit))
        address = Address.objects.filter(wallet=wallet, index=index, address=address).first()
        if address is not None:
            address_asset = AddressAsset.objects.filter(wallet=wallet, asset=db_asset, address=address).first()
            if address_asset is not None:
                address_asset.asset_usd = usd_price * balance
                address_asset.asset_cny = cny_price * balance
                address_asset.balance = Decimal(result.balance)
                address_asset.save()
            address_datastats = AddressAmountStat.objects.filter(address=address).order_by("-id")
            for item in address_datastats:
                data_stat.append(item.to_dict())
        data = {
            "balance": format(balance, ".4f"),
            "asset_usd": format(usd_price * balance, ".4f"),
            "asset_cny": format(cny_price * balance, ".4f"),
            "data_stat": data_stat,
        }
        return ok_json(data)
    else:
        address = Address.objects.filter(wallet=wallet, index=index, address=address).first()
        balance = d0
        if address is not None:
            address_asset = AddressAsset.objects.filter(wallet=wallet, assset=db_asset, address=address).first()
            balance = Decimal(address_asset.balance) / Decimal(10 ** int(db_asset.unit))
            address_datastats = AddressAmountStat.objects.filter(address=address).order_by("-id")
            for item in address_datastats:
                data_stat.append(item.to_dict())
        data = {
            "balance": format(balance, ".4f"),
            "asset_usd": format(usd_price * balance, ".4f"),
            "asset_cny": format(cny_price * balance, ".4f"),
            "data_stat": data_stat
        }
        return ok_json(data)


# @check_api_token
def get_wallet_balance(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    chain = params.get('chain', "Ethereum")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    wallet = Wallet.objects.filter(device_id=device_id, wallet_uuid=wallet_uuid, chain=db_chain).first()
    if wallet is None:
        return error_json("no this wallet", 4000)
    token_list = []
    wallet_asset_list = WalletAsset.objects.filter(wallet=wallet).order_by("id")
    for wallet_asset in wallet_asset_list:
        token_list.append(wallet_asset.to_dict())
    data = {
        "chain": wallet.chain.name,
        "network": "mainnet",
        "device_id": device_id,
        "wallet_uuid": wallet_uuid,
        "wallet_name": wallet.wallet_name,
        "asset_usd": format(wallet.asset_usd, ".4f"),
        "asset_cny": format(wallet.asset_cny, ".4f"),
        "token_list": token_list,
    }
    return ok_json(data)


# @check_api_token
def get_nonce(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
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
    chain = params.get('chain', "Solana")
    symbol = params.get('symbol', "Sol")
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
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
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
def get_sign_tx_info(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address')
    db_asset = Asset.objects.filter(name=symbol).first()
    wallet_client = WalletClient()
    gas_result = wallet_client.get_gasPrice(
        chain=chain,
        coin=symbol,
        network=network,
    )
    gaslst = [
        {
            "index": 0,
            "gas_price": format(Decimal(gas_result.gas), ".4f"),
        },
        {
            "index": 1,
            "gas_price": format(Decimal(gas_result.gas) * Decimal(5), ".4f"),
        },
        {
            "index": 2,
            "gas_price": format(Decimal(gas_result.gas) * Decimal(10), ".4f"),
        }
    ]
    result = wallet_client.get_nonce(
        chain=chain,
        coin=symbol,
        network=network,
        address=address
    )
    if symbol not in ["USDT", "USDC", "DAI"]:
        market_price = MarketPrice.objects.filter(
            qoute_asset__id=db_asset.id,
            exchange__name="binance"
        ).order_by("-id").first()
        if market_price is not None:
            usd_price = market_price.usd_price
        else:
            usd_price = 0
    else:
        stable_price = StablePrice.objects.filter(
            asset__id=db_asset.id,
        ).order_by("-id").first()
        if stable_price is not None:
            usd_price = stable_price.usd_price
        else:
            usd_price = 1
    data = {
        "usdt_pirce": usd_price,
        "nonce": result.nonce,
        "gas_limit": 91000,
        "gas_list": gaslst,
    }
    return ok_json(data)


# @check_api_token
def send_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
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
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    contract_addr = params.get('contract_addr', "")
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
    try:
        wallet_client = WalletClient()
        result = wallet_client.get_tx_by_address(
            chain=chain,
            coin=symbol,
            address=address,
            contract_address=contract_addr,
            page=int(page),
            pagesize=int(page_size),
        )
        if result.code == common_pb2.SUCCESS:
            print(result)
            tx_data_return = []
            for item in result.tx:
                addr_tx = AddressTransaction(item)
                tx_data_return.append(addr_tx.as_json(symbol, address, contract_addr))
            return ok_json(tx_data_return)
        else:
            return error_json("rpc server fail")
    except:
        return ok_json([])


# @check_api_token
def get_hash_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
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
@transaction.atomic()
def submit_wallet_info(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    network = params.get('network', "mainnet")
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    wallet_name = params.get('wallet_name', "")
    index = params.get('index', "0")
    address = params.get('address', "")
    contract_addr = params.get('contract_addr', "")
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
    db_asset = Asset.objects.filter(name=symbol, chain=db_chain).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    wallet_exist = Wallet.objects.filter(
        chain=db_chain,
        device_id=device_id,
        wallet_uuid=wallet_uuid,
        wallet_name=wallet_name
    ).first()
    if wallet_exist is None:
        wallet = Wallet.objects.create(
            chain=db_chain,
            device_id=device_id,
            wallet_uuid=wallet_uuid,
            wallet_name=wallet_name,
            asset_usd=d0,
            asset_cny=d0
        )
    else:
        wallet = wallet_exist
    wallet_asset_exist = WalletAsset.objects.filter(
        wallet=wallet,
        asset=db_asset,
        contract_addr=contract_addr
    ).first()
    if wallet_asset_exist is None:
        wallet.create_wallet_asset(
            asset=db_asset,
            contract_addr=contract_addr
        )
    address_exist = Address.objects.filter(
        wallet=wallet,
        index=index,
        address=address,
    ).first()
    if address_exist is None:
        create_addr = wallet.create_address(
            index=index,
            address=address,
        )
        create_addr.create_address_asset(
            asset=db_asset
        )
    return ok_json("submit wallet success")


# @check_api_token
def batch_submit_wallet(request):
    params = json.loads(request.body.decode())
    batch_wallet = params.get('batch_wallet', None)
    if batch_wallet is None:
        return error_json("batch_wallet is empty", 4000)
    for wallet in batch_wallet:
        db_chain = Chain.objects.filter(name=wallet.get("chain")).first()
        db_asset = Asset.objects.filter(name=wallet.get("symbol"), chain=db_chain).first()
        if db_chain is not None and  db_asset is not None:
            wallet = Wallet.objects.create(
                chain=db_chain,
                device_id=wallet.get("device_id"),
                wallet_uuid=wallet.get("wallet_uuid"),
                wallet_name=wallet.get("wallet_name"),
                asset_usd=d0,
                asset_cny=d0,
                balance=d0
            )
            wallet.create_wallet_asset(
                asset=db_asset,
                contract_addr=wallet.get("contract_addr")
            )
            wallet.create_address(
                index=wallet.get("index"),
                address=wallet.get("address"),
            )
    return ok_json("batch submit wallet success")


#  @check_api_token
def delete_wallet(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', None)
    wallet_uuid = params.get('wallet_uuid', None)
    chain = params.get('chain', None)
    if device_id in EMPTY or wallet_uuid in EMPTY or chain in EMPTY:
        return error_json("invalid Params", 4000)
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    wallet_d = Wallet.objects.filter(
        chain=db_chain,
        device_id=device_id,
        wallet_uuid=wallet_uuid,
    )
    wallet = wallet_d.first()
    WalletAsset.objects.filter(
        wallet=wallet
    ).delete()
    AddressAsset.objects.filter(
        wallet=wallet
    ).delete()
    Address.objects.filter(
        wallet=wallet
    ).delete()
    wallet_d.delete()
    return ok_json("delete wallet success")


# @check_api_token
def delete_wallet_token(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', None)
    wallet_uuid = params.get('wallet_uuid', None)
    symbol = params.get('symbol', None)
    contract_addr = params.get('contract_addr', None)
    chain = params.get('chain', None)
    if device_id in EMPTY or wallet_uuid in EMPTY or symbol in EMPTY or contract_addr in EMPTY or chain in EMPTY:
        return error_json("Invalid Params", 4000)
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    db_asset = Asset.objects.filter(name=symbol, chain=db_chain).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    wallet = Wallet.objects.filter(
        chain=db_chain,
        device_id=device_id,
        wallet_uuid=wallet_uuid,
    ).first()
    WalletAsset.objects.filter(
        wallet=wallet,
        asset=db_asset,
        contract_addr=contract_addr,
    ).delete()
    address_list = Address.objects.filter(
        wallet=wallet,
    )
    for address in address_list:
        AddressAsset.objects.filter(
            wallet=wallet,
            asset=db_asset,
            address=address
        ).delete()
    return ok_json("delete wallet token success")


#  @check_api_token
def get_unspend_list(request):
    params = json.loads(request.body.decode())
    return ok_json("ok")


# @check_api_token
def get_note_book(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    page = params.get('page')
    page_size = params.get('page_size')
    start = (page - 1) * page_size
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


# @check_api_token
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
    address_db = AddresNote.objects.filter(
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


# @check_api_token
def upd_note_book(request):
    params = json.loads(request.body.decode())
    address_id = int(params.get('address_id'))
    memo = params.get('memo')
    address = params.get('address')
    AddresNote.objects.filter(id=address_id).update(
        memo=memo,
        address=address
    )
    return ok_json("update note book success")


# @check_api_token
def del_note_book(request):
    params = json.loads(request.body.decode())
    address_id = int(params.get('address_id'))
    AddresNote.objects.filter(id=address_id).delete()
    return ok_json("delete note book success")


# @check_api_token
def hot_token_list(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', "Ethereum")
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    token_config_list = TokenConfig.objects.filter(
        chain=db_chain,
        is_hot="yes"
    ).order_by("id")
    token_config_data = []
    for token_config in token_config_list:
        token_config_data.append(token_config.list_to_dict())
    return ok_json(token_config_data)


# @check_api_token
def sourch_add_token(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', "Ethereum")
    token_name = params.get('token_name')
    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json("Do not support chain", 4000)
    token_config_list = TokenConfig.objects.filter(
        chain=db_chain,
        token_name__icontains=token_name,
    ).order_by("id")
    token_config_data = []
    for token_config in token_config_list:
        token_config_data.append(token_config.list_to_dict())
    return ok_json(token_config_data)


# @check_api_token
def get_wallet_asset(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    wallet_list = Wallet.objects.filter(
        device_id=device_id,
    ).order_by("id")
    total_asset_usd_stat = d0
    total_asset_cny_stat = d0
    token_list_return = []
    for wallet in wallet_list:
        total_asset_usd_stat += wallet.asset_usd
        total_asset_cny_stat += wallet.asset_cny
        wallet_asset_list = WalletAsset.objects.filter(
            wallet=wallet,
        ).order_by("id")
        wallet_balance_list= []
        for wallet_asset in wallet_asset_list:
            wallet_balance_list.append(wallet_asset.to_dict())
        wallet_balance_data = {
            "wallet_name": wallet.wallet_name,
            "wallet_balance": wallet_balance_list
        }
        token_list_return.append(wallet_balance_data)
    data = {
        "total_asset_usd": format(total_asset_usd_stat, ".4f"),
        "total_asset_cny": format(total_asset_cny_stat, ".4f"),
        "token_list": token_list_return,
    }
    return ok_json(data)


# @check_api_token
def update_wallet_name(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    wallet_name = params.get('wallet_name', "")
    if wallet_name in ["", None]:
        return error_json("wallet name is null", 4000)
    wallet = Wallet.objects.filter(
        device_id=device_id,
        wallet_uuid=wallet_uuid,
    ).first()
    if wallet is None:
        return error_json("No this wallet", 4000)
    else:
        wallet.wallet_name = wallet_name
        wallet.save()
    return ok_json("update wallet name success")
