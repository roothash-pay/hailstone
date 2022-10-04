#encoding=utf-8

import json
from typing import Any, Dict, List, Optional, Union
from services.savour_rpc import wallet_pb2
from market.models import Asset
from decimal import Decimal


class AddressTransaction:
    tx_address: wallet_pb2.TxAddressResponse

    def __init__(self, tx_address):
        self.tx_address = tx_address

    def get_asset_unit(self, symbol):
        asset = Asset.objects.filter(
            name=symbol
        ).order_by("-id").first()
        return asset.unit

    def as_json(self, symbol, address, contract_address) -> Dict[str, Any]:
        address_to_list = []
        address_from_list = []
        value_list = []
        for to_item in self.tx_address.tos:
            address_to_list.append(to_item.address)
        for from_item in self.tx_address.froms:
            address_from_list.append(from_item.address)
        for value_item in self.tx_address.values:
            value_list.append(value_item.value)
        if address == address_from_list[0]:
            tx_in_out = "from"
        else:
            tx_in_out = "to"
        return {
            "block_number": self.tx_address.height,
            "asset_name": symbol,
            "hash": self.tx_address.hash,
            "from": address_from_list[0],
            "to": address_to_list[0],
            "value":format((Decimal(value_list[0]) / Decimal(10 ** int(self.get_asset_unit(symbol)))), ".4f"),
            "contract_address": contract_address,
            "fee": format((Decimal(self.tx_address.fee) / Decimal(10 ** int(self.get_asset_unit(symbol)))), ".4f"),
            "txreceipt_status": self.tx_address.status,
            "tx_in_out": tx_in_out,
            "date_time": self.tx_address.datetime,
        }
