# encoding=utf-8

from decimal import Decimal
from typing import Any, Dict, Union

from common.models import Asset, Chain
from services.savour_rpc import account_pb2, utxo_pb2


class AddressTransaction:
    tx_message: Union[account_pb2.TxMessage, utxo_pb2.TxMessage]

    def __init__(self, tx_message: Union[account_pb2.TxMessage, utxo_pb2.TxMessage]):
        self.tx_message = tx_message

    def get_asset_unit(self, symbol):
        asset = Asset.objects.filter(
            name=symbol
        ).order_by("-id").first()
        return asset.unit if asset else '0'

    def get_main_chain_coin(self, chain):
        chain_obj = Chain.objects.filter(
            name=chain
        ).order_by("-id").first()
        return chain_obj.mark if chain_obj else ''

    def as_json(self, symbol, address, contract_address, chain) -> Dict[str, Any]:
        address_to_list = []
        address_from_list = []
        value_list = []
        status_name = "Unknown"

        if isinstance(self.tx_message, account_pb2.TxMessage):
            from_addr = getattr(self.tx_message, 'from', None)
            to_addr = getattr(self.tx_message, 'to', None)
            value = getattr(self.tx_message, 'value', None)
            if from_addr: address_from_list.append(from_addr)
            if to_addr: address_to_list.append(to_addr)
            if value: value_list.append(value)
            if hasattr(self.tx_message, 'status'):
                try:
                    status_name = account_pb2.TxStatus.Name(self.tx_message.status)
                except ValueError:
                    status_name = f"UnknownStatus({self.tx_message.status})"

        elif isinstance(self.tx_message, utxo_pb2.TxMessage):
            froms = getattr(self.tx_message, 'froms', [])
            tos = getattr(self.tx_message, 'tos', [])
            values = getattr(self.tx_message, 'values', [])
            address_from_list = [f.address for f in froms]
            address_to_list = [t.address for t in tos]
            value_list = [v.value for v in values]
            if hasattr(self.tx_message, 'status'):
                try:
                    status_name = utxo_pb2.TxStatus.Name(self.tx_message.status)
                except ValueError:
                    status_name = f"UnknownStatus({self.tx_message.status})"

        first_from = address_from_list[0] if address_from_list else None
        if address and first_from and address.lower() == first_from.lower():
            tx_in_out = "from"
        else:
            tx_in_out = "to"

        display_value = "0.0000"
        display_fee = "0.0000"
        main_coin_symbol = self.get_main_chain_coin(chain)
        main_coin_unit = self.get_asset_unit(main_coin_symbol)
        token_unit = self.get_asset_unit(symbol)

        try:
            if self.tx_message.fee and main_coin_unit != '0':
                raw_fee_decimal = Decimal(self.tx_message.fee) / Decimal(10 ** int(main_coin_unit))
                display_fee_attempt = format(raw_fee_decimal, ".8f")
                if display_fee_attempt == "0.00000000" and raw_fee_decimal != Decimal(0):
                    # 如果8位小数显示为0，且原始值不为0，则使用完整精度
                    display_fee = format(raw_fee_decimal, f".{main_coin_unit}f")
                    # 避免尾随过多的0，如果单位本身就很大
                    display_fee = display_fee.rstrip('0').rstrip('.') if '.' in display_fee else display_fee
                    if display_fee == "": display_fee = "0"  # 如果rstrip后为空(例如 0.000 -> 0)
                else:
                    display_fee = display_fee_attempt
                print("display_fee: ", display_fee)
            elif not self.tx_message.fee:  # 如果fee本身就是空或0
                display_fee = "0.00000000"
        except (ValueError, TypeError, Exception) as e:
            print(f"Warning: Could not format fee '{self.tx_message.fee}'. Error: {e}")
            display_fee = "Error"

        value_to_format = value_list[0] if value_list else "0"
        try:
            is_token_transfer = contract_address or (symbol != main_coin_symbol)
            unit_to_use = token_unit if is_token_transfer and token_unit != '0' else main_coin_unit

            if value_to_format and unit_to_use != '0':
                raw_value_decimal = Decimal(value_to_format) / Decimal(10 ** int(unit_to_use))
                display_value_attempt = format(raw_value_decimal, ".4f")
                if display_value_attempt == "0.0000" and raw_value_decimal != Decimal(0):
                    # 如果4位小数显示为0，且原始值不为0，则使用完整精度
                    display_value = format(raw_value_decimal, f".{unit_to_use}f")
                    # 避免尾随过多的0
                    display_value = display_value.rstrip('0').rstrip('.') if '.' in display_value else display_value
                    if display_value == "": display_value = "0"  # 如果rstrip后为空
                else:
                    display_value = display_value_attempt
            elif not value_to_format or value_to_format == "0":  # 如果value本身就是空或0
                display_value = "0.0000"

        except (ValueError, TypeError, Exception) as e:
            print(f"Warning: Could not format value '{value_to_format}'. Error: {e}")
            display_value = "Error"

        return {
            "block_number": self.tx_message.height,
            "asset_name": symbol,
            "hash": self.tx_message.hash,
            "from": address_from_list[0] if address_from_list else None,
            "to": address_to_list[0] if address_to_list else None,
            "value": display_value,
            "contract_address": getattr(self.tx_message, 'contract_address', contract_address),
            "fee": display_fee,
            "txreceipt_status": status_name,
            "tx_in_out": tx_in_out,
            "date_time": self.tx_message.datetime,
            "froms_list": address_from_list if isinstance(self.tx_message, utxo_pb2.TxMessage) else None,
            "tos_list": address_to_list if isinstance(self.tx_message, utxo_pb2.TxMessage) else None,
            "values_list": value_list if isinstance(self.tx_message, utxo_pb2.TxMessage) else None,
        }
