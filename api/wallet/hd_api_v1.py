# encoding=utf-8

import json
from decimal import Decimal
import grpc
from django.db import transaction
from api.wallet.types import AddressTransaction
from common.helpers import ok_json, error_json, d0
from services.account_client import AccountClient
from services.utxo_client import UtxoClient
from services.savour_rpc import common_pb2
from wallet.models import Chain, Asset, Wallet, WalletAsset, Address, AddressAsset, AddresNote, TokenConfig, AddressAmountStat
from api.wallet.constants import (
    NETWORK_MAINNET, NETWORK_TESTNET,
    DEFAULT_RPC_ERROR_CODE, DEFAULT_CLIENT_ERROR_CODE, DEFAULT_SERVER_ERROR_CODE,
    ADDRESS_CONTRACT_DEFAULT, GET_BALANCE_DEFAULT_INDEX
)
from api.wallet.utils import get_asset_prices
import logging

logger = logging.getLogger(__name__)

def get_rpc_client_by_chain(chain_name: str):
    """
    根据链名称获取对应的 gRPC 客户端实例。
    返回 (AccountClient or UtxoClient, None) 或 (None, error_message).
    """
    try:
        db_chain = Chain.objects.filter(name=chain_name).first()
        if not db_chain:
            logger.warning(f"Chain '{chain_name}' not found in database for RPC client retrieval.")
            return None, f"Chain '{chain_name}' not found in database."

        if db_chain.model_type == 'ACCOUNT':
            return AccountClient(), None
        elif db_chain.model_type == 'UTXO':
            return UtxoClient(), None
        else:
            logger.error(f"Unsupported model_type '{db_chain.model_type}' for chain '{chain_name}' in _get_rpc_client_by_chain")
            return None, f"Unsupported model_type '{db_chain.model_type}' for chain '{chain_name}'"
    except Exception as e:
        logger.exception(f"Error getting RPC client for chain {chain_name}: {e}")
        return None, f"Failed to initialize RPC client for chain '{chain_name}'."


def get_support_chain(request):
    params = json.loads(request.body.decode())
    chain_name = params.get('chain', "Ethereum")
    network = params.get('network', NETWORK_MAINNET)
    client, error_msg = get_rpc_client_by_chain(chain_name)
    if client is None:
        return error_json(error_msg, DEFAULT_CLIENT_ERROR_CODE)
    try:
        if isinstance(client, AccountClient):
            result = client.get_support_chains(
                chain=chain_name,
                network=network,
            )
        elif isinstance(client, UtxoClient):
            result = client.get_support_chains(
                chain=chain_name,
                network=network,
            )
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in get_support_chain.")
            return error_json("Internal error: Invalid client type.", DEFAULT_SERVER_ERROR_CODE)
    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_support_chain for {chain_name}/{network}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error calling RPC get_support_chain for {chain_name}/{network}: {e}")
        return error_json("Failed to fetch support chain from RPC.", DEFAULT_SERVER_ERROR_CODE)

    data = {
        "chain": chain_name,
        "network": network,
        "support_chains": result.msg,
    }
    return ok_json(data)


# @check_api_token
def get_balance(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    network = params.get('network', NETWORK_MAINNET)
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    index = params.get('index', GET_BALANCE_DEFAULT_INDEX)
    # TODO 上游服务不支持"", 需要传入"0x00"
    contract_address = params.get('contract_address', ADDRESS_CONTRACT_DEFAULT)
    if contract_address == "":
        contract_address = "0x00"
    logger.info(f"contract_address: {contract_address}")
    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, DEFAULT_CLIENT_ERROR_CODE)

    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json(f"Do not support symbol '{symbol}'", DEFAULT_CLIENT_ERROR_CODE)
    if network not in [NETWORK_MAINNET, NETWORK_TESTNET]:
        return error_json("Do not support network", DEFAULT_CLIENT_ERROR_CODE)
    if not address:
        return error_json("address is empty", DEFAULT_CLIENT_ERROR_CODE)
    try:
        if isinstance(client, AccountClient):
            result = client.get_account(
                chain=chain,
                coin=symbol,
                network=network,
                address=address,
                contract_address=contract_address
            )
        elif isinstance(client, UtxoClient):
            result = client.get_account(
                chain=chain,
                network=network,
                address=address,
                brc20_address=contract_address
            )
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in get_balance.")
            return error_json("Internal error: Invalid client type.", DEFAULT_SERVER_ERROR_CODE)
    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_balance for {chain}/{symbol}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error calling RPC get_account for {chain}/{symbol} in get_balance: {e}")
        return error_json("Failed to fetch balance from RPC.", DEFAULT_SERVER_ERROR_CODE)

    usd_price, cny_price = get_asset_prices(symbol)

    wallet = Wallet.objects.filter(device_id=device_id, wallet_uuid=wallet_uuid).first()
    if wallet is None:
        return error_json("Wallet not found for device/uuid.", 4004)

    data_stat = []
    balance = d0
    raw_balance_from_rpc = "0"

    if result.code == common_pb2.SUCCESS:
        if result.balance and result.balance != "<nil>":
            raw_balance_from_rpc = result.balance
            try:
                balance = Decimal(raw_balance_from_rpc) / Decimal(10 ** int(db_asset.unit))
            except (ValueError, TypeError, Exception) as e:
                logger.warning(f"Could not convert balance '{result.balance}' to Decimal for asset {symbol} with unit {db_asset.unit}. Error: {e}", exc_info=True)
        
        if wallet:
            address_obj = Address.objects.filter(wallet=wallet, index=index, address=address).first()
            if address_obj:
                asset_usd_value = usd_price * balance
                asset_cny_value = cny_price * balance
                
                AddressAsset.objects.update_or_create(
                    wallet=wallet,
                    asset=db_asset,
                    address=address_obj,
                    defaults={
                        'balance': Decimal(raw_balance_from_rpc),
                        'asset_usd': asset_usd_value,
                        'asset_cny': asset_cny_value
                    }
                )
                address_datastats = AddressAmountStat.objects.filter(address=address_obj).order_by("-id")
                for item in address_datastats:
                    data_stat.append(item.to_dict())
            else:
                logger.info(f"Address {address} with index {index} not found for wallet {wallet_uuid} in get_balance. DB update skipped.")
        
        data = {
            "balance": format(balance, ".4f"),
            "asset_usd": format(usd_price * balance, ".4f"),
            "asset_cny": format(cny_price * balance, ".4f"),
            "data_stat": data_stat,
        }
        return ok_json(data)
    else:
        logger.warning(f"RPC call failed for get_balance ({chain}/{symbol}/{address}): {result.code} - {result.msg}")
        if wallet:
            address_obj = Address.objects.filter(wallet=wallet, index=index, address=address).first()
            if address_obj:
                address_asset = AddressAsset.objects.filter(wallet=wallet, asset=db_asset, address=address_obj).first()
                if address_asset and address_asset.balance is not None:
                    try:
                        balance = Decimal(str(address_asset.balance)) / Decimal(10 ** int(db_asset.unit))
                    except Exception as e:
                        logger.warning(f"Could not convert DB balance '{address_asset.balance}' to Decimal for {symbol}. Error: {e}", exc_info=True)
                address_datastats = AddressAmountStat.objects.filter(address=address_obj).order_by("-id")
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
    chain_name = params.get('chain', "Ethereum")

    db_chain = Chain.objects.filter(name=chain_name).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain_name}'", 4000)

    wallet = Wallet.objects.filter(device_id=device_id, wallet_uuid=wallet_uuid, chain=db_chain).first()
    if wallet is None:
        return error_json(f"No wallet found for device '{device_id}', uuid '{wallet_uuid}' on chain '{chain_name}'",
                          4004)

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

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json(f"Do not support symbol '{symbol}'", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json(f"Do not support network '{network}'", 4000)
    if not address:
        return error_json("address is empty", 4000)

    if isinstance(client, AccountClient):
        try:
            result = client.get_account(
                chain=chain,
                coin=symbol,
                network=network,
                address=address
            )
            if result.code == common_pb2.SUCCESS:
                data = {
                    "nonce": result.sequence,
                }
                return ok_json(data)
            else:
                logger.warning(f"RPC call failed for get_nonce ({chain}/{address}): {result.code} - {result.msg}")
                return error_json(f"RPC server failed: {result.msg}", 5000)
        except grpc.RpcError as e:
            logger.error(f"RPC Error in get_nonce for {chain}/{address}: {e.details()}", exc_info=True)
            return error_json(f"RPC Error: {e.details()}", 5003)
        except Exception as e:
            logger.exception(f"Error calling RPC get_account for nonce: {e}")
            return error_json("Failed to fetch nonce from RPC.", 5000)
    elif isinstance(client, UtxoClient):
        logger.info(f"Nonce is not applicable for UTXO chain '{chain}' in get_nonce.")
        return error_json(f"Nonce is not applicable for UTXO chain '{chain}'", 4000)
    else:
        logger.error(f"Internal error: Invalid client type '{type(client)}' in get_nonce.")
        return error_json("Internal error: Invalid client type.", 5000)


# @check_api_token
def get_account_info(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    contract_address = params.get('contract_address', ADDRESS_CONTRACT_DEFAULT)
    if contract_address == "":
        contract_address = "0x00"

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)
    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if not address:
        return error_json("address is empty", 4000)

    try:
        if isinstance(client, AccountClient):
            result = client.get_account(
                chain=chain,
                coin=symbol,
                network=network,
                address=address,
                contract_address=contract_address
            )
            if result.code == common_pb2.SUCCESS:
                data = {
                    "account_number": result.account_number,
                    "sequence": result.sequence,
                    "balance": result.balance,
                }
                return ok_json(data)
            else:
                logger.warning(f"RPC call failed for get_account_info (Account) ({chain}/{address}): {result.code} - {result.msg}")
                return error_json(f"RPC server failed: {result.msg}", 5000)
        elif isinstance(client, UtxoClient):
            result = client.get_account(
                chain=chain,
                network=network,
                address=address
            )
            if result.code == common_pb2.SUCCESS:
                data = {
                    "balance": result.balance,
                    "account_number": None,
                    "sequence": None,
                }
                return ok_json(data)
            else:
                logger.warning(f"RPC call failed for get_account_info (UTXO) ({chain}/{address}): {result.code} - {result.msg}")
                return error_json(f"RPC server failed: {result.msg}", 5000)
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in get_account_info.")
            return error_json("Internal error: Invalid client type.", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_account_info for {chain}/{address}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", 5003)
    except Exception as e:
        logger.exception(f"Error calling RPC get_account for info: {e}")
        return error_json("Failed to fetch account info from RPC.", 5000)


# @check_api_token
def get_fee(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    fee_way = params.get('fee_way', "low")

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)

    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if fee_way not in ["low", "medium", "high"]:
        return error_json(f"Invalid fee_way '{fee_way}'. Must be low, medium, or high.", 4000)

    try:
        if isinstance(client, (AccountClient, UtxoClient)):
            result = client.get_fee(
                chain=chain,
                coin=symbol,
                network=network,
            )
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in get_fee.")
            return error_json("Internal error: Invalid client type.", 5000)

        if result.code == common_pb2.SUCCESS:
            gas_price = None
            if fee_way == "high":
                gas_price = getattr(result, 'fast_fee', None) or getattr(result, 'best_fee', None)
            elif fee_way == "medium":
                gas_price = getattr(result, 'normal_fee', None) or getattr(result, 'best_fee', None)
            else:
                gas_price = getattr(result, 'slow_fee', None) or getattr(result, 'best_fee', None)

            if gas_price is None:
                logger.warning(f"Could not determine gas price for fee_way '{fee_way}' from RPC response: {result}")
                return error_json(f"Failed to get '{fee_way}' gas price from RPC.", 5000)

            data = {"gas": gas_price}
            return ok_json(data)
        else:
            logger.warning(f"RPC call failed for get_fee ({chain}/{symbol}): {result.code} - {result.msg}")
            return error_json(f"RPC server failed: {result.msg}", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_fee for {chain}/{symbol}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", 5003)
    except Exception as e:
        logger.exception(f"Error calling RPC get_fee: {e}")
        return error_json("Failed to fetch fee from RPC.", 5000)


# @check_api_token
def get_sign_tx_info(request):
    params = json.loads(request.body.decode())
    network = params.get('network', NETWORK_MAINNET)
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address')

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, DEFAULT_CLIENT_ERROR_CODE)

    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json(f"Do not support symbol '{symbol}'", DEFAULT_CLIENT_ERROR_CODE)
    if not address:
        return error_json("address is empty", DEFAULT_CLIENT_ERROR_CODE)
    if network not in [NETWORK_MAINNET, NETWORK_TESTNET]:
        return error_json("Do not support network", DEFAULT_CLIENT_ERROR_CODE)

    nonce = None
    gas_list = []
    
    try:
        if isinstance(client, AccountClient):
            fee_result = client.get_fee(chain=chain, coin=symbol, network=network, address=address)
        elif isinstance(client, UtxoClient):
            fee_result = client.get_fee(chain=chain, coin=symbol, network=network)
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' for fee in get_sign_tx_info.")
            return error_json("Internal error: Invalid client type for fee.", DEFAULT_SERVER_ERROR_CODE)

        if fee_result.code == common_pb2.SUCCESS:
            slow = getattr(fee_result, 'slow_fee', None) or getattr(fee_result, 'best_fee', None)
            normal = getattr(fee_result, 'normal_fee', None) or getattr(fee_result, 'best_fee', None)
            fast = getattr(fee_result, 'fast_fee', None) or getattr(fee_result, 'best_fee', None)
            gas_list = [
                {"index": 0, "gas_price": slow or "0"},
                {"index": 1, "gas_price": normal or "0"},
                {"index": 2, "gas_price": fast or "0"}
            ]

            if isinstance(client, AccountClient):
                nonce_result = client.get_account(chain=chain, coin=symbol, network=network, address=address)
                if nonce_result.code == common_pb2.SUCCESS:
                    nonce = nonce_result.sequence
                else:
                    logger.warning(f"RPC call for get_account (nonce) failed in get_sign_tx_info ({chain}/{address}): {nonce_result.code} - {nonce_result.msg}")
                    return error_json(f"Failed to fetch nonce: {nonce_result.msg}", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_sign_tx_info for {chain}/{symbol}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error fetching tx info: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error in get_sign_tx_info for {chain}/{symbol}: {e}")
        return error_json("Failed to fetch transaction info.", DEFAULT_SERVER_ERROR_CODE)

    usd_price, _ = get_asset_prices(symbol)

    data = {
        "usd_price": format(usd_price, ".4f"),
        "nonce": nonce,
        "gas_limit": "91000",
        "gas_list": gas_list,
    }
    return ok_json(data)


# @check_api_token
def send_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', NETWORK_MAINNET)
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    rawtx = params.get('rawtx', None)

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)

    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if not rawtx:
        return error_json("rawtx is empty", 4000)

    try:
        if isinstance(client, (AccountClient, UtxoClient)):
            result = client.send_tx(
                chain=chain,
                coin=symbol,
                network=network,
                raw_tx=rawtx,
            )
            if result.code == common_pb2.SUCCESS:
                data = {
                    "hash": result.tx_hash
                }
                return ok_json(data)
            else:
                logger.warning(f"RPC call failed for send_transaction ({chain}, symbol {symbol}): {result.code} - {result.msg}")
                error_detail = f"RPC server failed: {result.msg}" if result.msg else "RPC server failed"
                return error_json(error_detail, 5000)
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in send_transaction.")
            return error_json("Internal error: Invalid client type.", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in send_transaction for {chain}/{symbol}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error calling RPC send_tx ({chain}/{symbol}): {e}")
        return error_json("Failed to send transaction via RPC.", 5000)


# @check_api_token
def get_address_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', NETWORK_MAINNET)
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    address = params.get('address', "")
    contract_addr = params.get('contract_addr', "0x00")
    try:
        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 10))
        if page < 1: page = 1
        if page_size < 1: page_size = 10
    except (ValueError, TypeError):
        return error_json("Invalid page or page_size parameter.", 4000)

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)

    db_asset = Asset.objects.filter(name=symbol).first()
    if db_asset is None:
        return error_json("Do not support symbol", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if not address:
        return error_json("address is empty", 4000)

    try:
        if isinstance(client, AccountClient):
            result = client.get_tx_by_address(
                chain=chain,
                coin=symbol,
                network=network,
                address=address,
                contract_address=contract_addr,
                page=page,
                pagesize=page_size,
            )
        elif isinstance(client, UtxoClient):
            brc20_address_param = contract_addr
            result = client.get_tx_by_address(
                chain=chain,
                coin=symbol,
                network=network,
                address=address,
                brc20_address=brc20_address_param,
                page=page,
                pagesize=page_size,
            )
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in get_address_transaction.")
            return error_json("Internal error: Invalid client type.", 5000)

        if result.code == common_pb2.SUCCESS:
            tx_data_return = []
            for item in result.tx:
                addr_tx = AddressTransaction(item)
                tx_data_return.append(addr_tx.as_json(symbol, address, contract_addr, chain))
            return ok_json(tx_data_return)
        else:
            logger.warning(f"RPC call failed for get_address_transaction ({chain}/{address}): {result.code} - {result.msg}")
            return error_json(f"RPC server failed: {result.msg}", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_address_transaction for {chain}/{address}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error processing address transactions for {chain}/{address}: {e}")
        return error_json(f"Failed to process transactions: {str(e)}", 5000)


# @check_api_token
def get_hash_transaction(request):
    params = json.loads(request.body.decode())
    network = params.get('network', NETWORK_MAINNET)
    chain = params.get('chain', "Ethereum")
    symbol = params.get('symbol', "ETH")
    hash_val = params.get('hash', "")

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)

    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain}'", 4000)
    db_asset = Asset.objects.filter(name=symbol, chain=db_chain).first()
    if db_asset is None:
        return error_json(f"Do not support symbol '{symbol}' for chain '{chain}'", 4000)
    if network not in ["mainnet", "testnet"]:
        return error_json("Do not support network", 4000)
    if not hash_val:
        return error_json("hash is empty", 4000)

    try:
        if isinstance(client, (AccountClient, UtxoClient)):
            result = client.get_tx_by_hash(
                chain=chain,
                coin=symbol,
                network=network,
                hash=hash_val
            )
            if result.code == common_pb2.SUCCESS:
                if result.tx:
                    tx_data = {
                        "hash": result.tx.hash,
                        "index": getattr(result.tx, 'index', None),
                        "froms": [f.address for f in getattr(result.tx, 'froms', [])] or [getattr(result.tx, 'from', None)],
                        "tos": [t.address for t in getattr(result.tx, 'tos', [])] or [getattr(result.tx, 'to', None)],
                        "values": [v.value for v in getattr(result.tx, 'values', [])] or [getattr(result.tx, 'value', None)],
                        "fee": result.tx.fee,
                        "status": result.tx.status,
                        "type": getattr(result.tx, 'type', None),
                        "height": result.tx.height,
                        "contract_address": getattr(result.tx, 'contract_address', getattr(result.tx, 'brc20_address', None)),
                        "datetime": result.tx.datetime,
                        "data": getattr(result.tx, 'data', None),
                    }
                    return ok_json(tx_data)
                else:
                    return error_json("Transaction not found by hash.", 4004)
            else:
                logger.warning(f"RPC call failed for get_hash_transaction ({chain}/{hash_val}): {result.code} - {result.msg}")
                error_detail = f"RPC server failed: {result.msg}" if result.msg else "RPC server failed"
                return error_json(error_detail, 5000)
        else:
            logger.error(f"Internal error: Invalid client type '{type(client)}' in get_hash_transaction.")
            return error_json("Internal error: Invalid client type.", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_hash_transaction for {chain}/{hash_val}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error calling RPC get_tx_by_hash: {e}")
        return error_json("Failed to fetch transaction by hash from RPC.", 5000)


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
    index = params.get('index', GET_BALANCE_DEFAULT_INDEX)
    address = params.get('address', "")
    contract_addr = params.get('contract_addr', "")
    if contract_addr == "":
        contract_addr = "0x00"

    if not chain: return error_json("chain is empty", 4000)
    if not symbol: return error_json("symbol is empty", 4000)
    if network not in ["mainnet", "testnet"]: return error_json("Do not support network", 4000)
    if not device_id: return error_json("device_id is empty", 4000)
    if not wallet_uuid: return error_json("wallet_uuid is empty", 4000)
    if not wallet_name: return error_json("wallet_name is empty", 4000)
    if not address: return error_json("address is empty", 4000)

    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain}'", 4000)

    db_asset = Asset.objects.filter(name=symbol, chain=db_chain).first()
    if db_asset is None:
        db_asset_generic = Asset.objects.filter(name=symbol, chain__isnull=True).first()
        if db_asset_generic is None:
            return error_json(f"Do not support symbol '{symbol}' for chain '{chain}' or generically.", 4000)
        else:
            db_asset = db_asset_generic

    wallet, created = Wallet.objects.update_or_create(
        chain=db_chain,
        device_id=device_id,
        wallet_uuid=wallet_uuid,
        defaults={
            'wallet_name': wallet_name
        }
    )

    if created:
        wallet.asset_usd = d0
        wallet.asset_cny = d0
        wallet.save(update_fields=['asset_usd', 'asset_cny'])

    wallet_asset, asset_created = WalletAsset.objects.update_or_create(
        wallet=wallet,
        asset=db_asset,
        contract_addr=contract_addr,
        defaults={}
    )

    addr_obj, addr_created = Address.objects.update_or_create(
        wallet=wallet,
        address=address,
        index=index,
        defaults={}
    )

    if addr_created:
        AddressAsset.objects.create(
            wallet=wallet,
            asset=db_asset,
            address=addr_obj,
            balance=d0,
            asset_usd=d0,
            asset_cny=d0
        )

    return ok_json("submit wallet success")


# @check_api_token
@transaction.atomic()
def batch_submit_wallet(request):
    params = json.loads(request.body.decode())
    batch_wallet = params.get('batch_wallet', None)
    if batch_wallet is None:
        return error_json("batch_wallet is empty", 4000)

    submitted_count = 0
    errors = []

    for idx, wallet_data in enumerate(batch_wallet):
        chain_name = wallet_data.get("chain")
        symbol_name = wallet_data.get("symbol")
        device_id = wallet_data.get("device_id")
        wallet_uuid = wallet_data.get("wallet_uuid")
        wallet_name = wallet_data.get("wallet_name")
        index = wallet_data.get("index")
        address = wallet_data.get("address")
        contract_addr = wallet_data.get("contract_addr", "")
        if contract_addr == "":
            contract_addr = "0x00"

        if not all([chain_name, symbol_name, device_id, wallet_uuid, wallet_name, index is not None, address]):
            errors.append(f"Item {idx}: Missing required fields.")
            continue

        db_chain = Chain.objects.filter(name=chain_name).first()
        if db_chain is None:
            errors.append(f"Item {idx}: Chain '{chain_name}' not supported.")
            continue

        db_asset = Asset.objects.filter(name=symbol_name, chain=db_chain).first() or \
                   Asset.objects.filter(name=symbol_name, chain__isnull=True).first()
        if db_asset is None:
            errors.append(f"Item {idx}: Symbol '{symbol_name}' not supported for chain '{chain_name}'.")
            continue

        try:
            wallet, created = Wallet.objects.update_or_create(
                chain=db_chain,
                device_id=device_id,
                wallet_uuid=wallet_uuid,
                defaults={
                    'wallet_name': wallet_name
                }
            )

            if created:
                wallet.asset_usd = d0
                wallet.asset_cny = d0
                wallet.save(update_fields=['asset_usd', 'asset_cny'])

            wallet_asset, asset_created = WalletAsset.objects.update_or_create(
                wallet=wallet,
                asset=db_asset,
                contract_addr=contract_addr,
                defaults={}
            )

            addr_obj, addr_created = Address.objects.update_or_create(
                wallet=wallet,
                address=address,
                index=index,
                defaults={}
            )

            if addr_created:
                AddressAsset.objects.create(
                    wallet=wallet,
                    asset=db_asset,
                    address=addr_obj,
                    balance=d0,
                    asset_usd=d0,
                    asset_cny=d0
                )
            submitted_count += 1
        except Exception as e:
            errors.append(f"Item {idx}: Error processing - {e}")

    if errors:
        return ok_json({
            "message": f"Batch submitted with {len(errors)} errors.",
            "submitted_count": submitted_count,
            "errors": errors
        })
    else:
        return ok_json("batch submit wallet success")


#  @check_api_token
@transaction.atomic()  # Make atomic
def delete_wallet(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', None)
    wallet_uuid = params.get('wallet_uuid', None)
    chain = params.get('chain', None)

    if not all([device_id, wallet_uuid, chain]):
        return error_json("invalid Params (device_id, wallet_uuid, chain required)", 4000)

    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain}'", 4000)

    wallet_qs = Wallet.objects.filter(
        chain=db_chain,
        device_id=device_id,
        wallet_uuid=wallet_uuid,
    )
    wallet = wallet_qs.first()

    if wallet:
        AddressAmountStat.objects.filter(address__wallet=wallet).delete()
        AddressAsset.objects.filter(wallet=wallet).delete()
        Address.objects.filter(wallet=wallet).delete()
        WalletAsset.objects.filter(wallet=wallet).delete()
        wallet_qs.delete()
        return ok_json("delete wallet success")
    else:
        return error_json("Wallet not found for deletion.", 4004)


# @check_api_token
@transaction.atomic()  # Make atomic
def delete_wallet_token(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', None)
    wallet_uuid = params.get('wallet_uuid', None)
    symbol = params.get('symbol', None)
    contract_addr = params.get('contract_addr', None)
    chain = params.get('chain', None)

    if not all([device_id, wallet_uuid, symbol, chain]):
        return error_json("Invalid Params (device_id, wallet_uuid, symbol, chain required)", 4000)

    db_chain = Chain.objects.filter(name=chain).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain}'", 4000)

    db_asset = Asset.objects.filter(name=symbol, chain=db_chain).first() or \
               Asset.objects.filter(name=symbol, chain__isnull=True).first()
    if db_asset is None:
        return error_json(f"Do not support symbol '{symbol}' for chain '{chain}'.", 4000)

    wallet = Wallet.objects.filter(
        chain=db_chain,
        device_id=device_id,
        wallet_uuid=wallet_uuid,
    ).first()

    if not wallet:
        return error_json("Wallet not found.", 4004)

    # 当contract_addr为空字符串时转换为"0x00"
    if contract_addr == "":
        contract_addr = "0x00"

    deleted_count, _ = WalletAsset.objects.filter(
        wallet=wallet,
        asset=db_asset,
        contract_addr=contract_addr,
    ).delete()

    address_list = Address.objects.filter(wallet=wallet)
    AddressAsset.objects.filter(
        wallet=wallet,
        asset=db_asset,
        address__in=address_list
    ).delete()

    if deleted_count > 0:
        return ok_json("delete wallet token success")
    else:
        return error_json("Token configuration not found for this wallet.", 4004)


#  @check_api_token
def get_unspend_list(request):
    params = json.loads(request.body.decode())
    network = params.get('network', "mainnet")
    chain = params.get('chain', "bitcoin")
    address = params.get('address', "")

    client, error_msg = get_rpc_client_by_chain(chain)
    if client is None:
        return error_json(error_msg, 4000)

    if not isinstance(client, UtxoClient):
        logger.warning(f"get_unspent_list called for non-UTXO chain '{chain}'.")
        return error_json(f"Unspent outputs are only applicable for UTXO chains, not '{chain}'.", 4000)
    if network not in [NETWORK_MAINNET, NETWORK_TESTNET]:
        return error_json("Do not support network", 4000)
    if not address:
        return error_json("address is empty", 4000)

    try:
        result = client.get_unspent_outputs(
            chain=chain,
            network=network,
            address=address
        )
        if result.code == common_pb2.SUCCESS:
            unspent_outputs = []
            for utxo in result.unspent_outputs:
                unspent_outputs.append({
                    "tx_id": utxo.tx_id,
                    "tx_hash_big_endian": utxo.tx_hash_big_endian,
                    "tx_output_n": getattr(utxo, 'tx_output_n', None),
                    "script": utxo.script,
                    "value": getattr(utxo, 'value', None) or getattr(utxo, 'unspent_amount', None),
                    "value_hex": getattr(utxo, 'value_hex', None),
                    "confirmations": getattr(utxo, 'confirmations', None),
                    "height": getattr(utxo, 'height', None),
                    "block_time": getattr(utxo, 'block_time', None),
                    "address": getattr(utxo, 'address', None),
                    "index": getattr(utxo, 'index', getattr(utxo, 'tx_output_n', None)),
                })
            return ok_json(unspent_outputs)
        else:
            logger.warning(f"RPC call failed for get_unspent_outputs ({chain}/{address}): {result.code} - {result.msg}")
            return error_json(f"RPC server failed: {result.msg}", 5000)

    except grpc.RpcError as e:
        logger.error(f"RPC Error in get_unspent_list for {chain}/{address}: {e.details()}", exc_info=True)
        return error_json(f"RPC Error: {e.details()}", DEFAULT_RPC_ERROR_CODE)
    except Exception as e:
        logger.exception(f"Error calling RPC get_unspent_outputs ({chain}/{address}): {e}")
        return error_json("Failed to fetch unspent outputs from RPC.", 5000)

# @check_api_token
def get_note_book(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    try:
        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 10))
        if page < 1: page = 1
        if page_size < 1: page_size = 10
    except (ValueError, TypeError):
        return error_json("Invalid page or page_size.", 4000)

    if not device_id:
        return error_json("device_id is required.", 4000)

    start = (page - 1) * page_size
    end = start + page_size
    address_notes_qs = AddresNote.objects.filter(device_id=device_id).order_by("-id")
    total = address_notes_qs.count()
    address_notes_qs = address_notes_qs[start:end]

    ret_address_data = []
    for address_note in address_notes_qs:
        ret_address_data.append(address_note.list_to_dict())

    data = {
        "total": total,
        "data": ret_address_data
    }
    return ok_json(data)


# @check_api_token
def add_note_book(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id')
    chain_name = params.get('chain')
    asset_name = params.get('asset')
    memo = params.get('memo')
    address = params.get('address')

    if not all([device_id, chain_name, asset_name, memo, address]):
        return error_json("Missing required fields (device_id, chain, asset, memo, address).", 4000)

    db_chain = Chain.objects.filter(name=chain_name).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain_name}'", 4000)

    db_asset = Asset.objects.filter(name=asset_name, chain=db_chain).first() or \
               Asset.objects.filter(name=asset_name, chain__isnull=True).first()
    if db_asset is None:
        return error_json(f"Do not support symbol '{asset_name}' for chain '{chain_name}'.", 4000)

    address_db_exists = AddresNote.objects.filter(
        device_id=device_id,
        address=address,
        chain=db_chain,
        asset=db_asset
    ).exists()

    if address_db_exists:
        return error_json("This address note already exists for this device/chain/asset.", 4009)
    else:
        try:
            AddresNote.objects.create(
                chain=db_chain,
                asset=db_asset,
                device_id=device_id,
                memo=memo,
                address=address
            )
            return ok_json("add note book success")
        except Exception as e:
            logger.error(f"Error creating address note: {e}")
            return error_json(f"Failed to add note book: {e}", 5000)


# @check_api_token
def upd_note_book(request):
    params = json.loads(request.body.decode())
    try:
        address_id = int(params.get('address_id'))
    except (ValueError, TypeError, TypeError):
        return error_json("Invalid address_id.", 4000)

    memo = params.get('memo')
    address = params.get('address')

    if not all([memo, address]):
        return error_json("Missing required fields (memo, address).", 4000)

    updated_count = AddresNote.objects.filter(id=address_id).update(
        memo=memo,
        address=address
    )

    if updated_count > 0:
        return ok_json("update note book success")
    else:
        return error_json("Address note not found.", 4004)


# @check_api_token
def del_note_book(request):
    params = json.loads(request.body.decode())
    try:
        address_id = int(params.get('address_id'))
    except (ValueError, TypeError, TypeError):
        return error_json("Invalid address_id.", 4000)

    deleted_count, _ = AddresNote.objects.filter(id=address_id).delete()

    if deleted_count > 0:
        return ok_json("delete note book success")
    else:
        return error_json("Address note not found.", 4004)


# @check_api_token
def hot_token_list(request):
    params = json.loads(request.body.decode())
    chain_name = params.get('chain', "Ethereum")

    db_chain = Chain.objects.filter(name=chain_name).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain_name}'", 4000)

    token_config_list = TokenConfig.objects.filter(
        chain=db_chain,
        is_hot="yes"
    ).order_by("id")

    token_config_data = []
    for token_config in token_config_list:
        token_config_data.append(token_config.list_to_dict())

    return ok_json(token_config_data)


# @check_api_token
def search_add_token(request):
    params = json.loads(request.body.decode())
    chain_name = params.get('chain', "Ethereum")
    token_name = params.get('token_name')

    if not token_name:
        return error_json("token_name parameter is required for search.", 4000)

    db_chain = Chain.objects.filter(name=chain_name).first()
    if db_chain is None:
        return error_json(f"Do not support chain '{chain_name}'", 4000)

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

    if not device_id:
        return error_json("device_id is required.", 4000)

    wallet_list = Wallet.objects.filter(
        device_id=device_id,
    ).order_by("id")

    total_asset_usd_stat = d0
    total_asset_cny_stat = d0
    token_list_return = []

    for wallet in wallet_list:
        total_asset_usd_stat += wallet.asset_usd or d0
        total_asset_cny_stat += wallet.asset_cny or d0

        wallet_asset_list = WalletAsset.objects.filter(
            wallet=wallet,
        ).order_by("id")

        wallet_balance_list = []
        for wallet_asset in wallet_asset_list:
            wallet_balance_list.append(wallet_asset.to_dict())

        wallet_balance_data = {
            "chain": wallet.chain.name,
            "wallet_name": wallet.wallet_name,
            "wallet_uuid": wallet.wallet_uuid,
            "wallet_balance": wallet_balance_list,
            "wallet_total_usd": format(wallet.asset_usd or 0, ".4f"),
            "wallet_total_cny": format(wallet.asset_cny or 0, ".4f"),
        }
        token_list_return.append(wallet_balance_data)

    data = {
        "total_asset_usd": format(total_asset_usd_stat, ".4f"),
        "total_asset_cny": format(total_asset_cny_stat, ".4f"),
        "wallet_data": token_list_return,
    }
    return ok_json(data)


# @check_api_token
def update_wallet_name(request):
    params = json.loads(request.body.decode())
    device_id = params.get('device_id', "")
    wallet_uuid = params.get('wallet_uuid', "")
    wallet_name = params.get('wallet_name', "")
    chain_name = params.get('chain', "")

    if not chain_name:
        return error_json("chain parameter is required.", 4000)
    if not wallet_name:
        return error_json("wallet name is null", 4000)
    if not device_id:
        return error_json("device_id is required", 4000)
    if not wallet_uuid:
        return error_json("wallet_uuid is required", 4000)

    db_chain = Chain.objects.filter(name=chain_name).first()
    if not db_chain:
        return error_json(f"Chain '{chain_name}' not supported.", 4000)
    updated_count = Wallet.objects.filter(
        device_id=device_id,
        wallet_uuid=wallet_uuid,
        chain=db_chain,
    ).update(wallet_name=wallet_name)

    if updated_count > 0:
        return ok_json("update wallet name success")
    else:
        return error_json(f"Wallet not found for device '{device_id}', uuid '{wallet_uuid}' on chain '{chain_name}'.", 4004)
