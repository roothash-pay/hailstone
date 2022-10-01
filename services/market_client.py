# encoding=utf-8

import grpc
from django.conf import settings
from services.savour_rpc import market_pb2_grpc
from services.savour_rpc import market_pb2


class MarketClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.MARKET_GRPC_CHANNEL_URL, options=options)
        self.stub = market_pb2_grpc.PriceServiceStub(channel)

    def get_symbols(self, exchange_id: str = "0", consumer_token: str = None) -> market_pb2.SymbolResponse:
        return self.stub.getSymbols(
            market_pb2.SymbolRequest(
                consumer_token=consumer_token,
                exchange_id=exchange_id,
            )
        )

    def get_symbol_prices(self, exchange_id: str = "0", symbol_id: str = "0", consumer_token: str = None):
        return self.stub.getSymbolPrices(
            market_pb2.SymbolPriceRequest(
                consumer_token=consumer_token,
                exchange_id=exchange_id,
                symbol_id=symbol_id,
            )
        )

    def get_assets(self, is_base: bool, exchange_id: str, consumer_token: str = None):
        return self.stub.getAssets(
            market_pb2.AssetRequest(
                consumer_token=consumer_token,
                exchange_id=exchange_id,
                is_base=is_base,
            )
        )

    def get_exchanges(self, consumer_token: str = None):
        return self.stub.getExchanges(
            market_pb2.ExchangeRequest(
                consumer_token=consumer_token,
            )
        )

    def get_stable_coins(self, consumer_token: str = None):
        return self.stub.getStableCoins(
            market_pb2.StableCoinRequest(
                consumer_token=consumer_token,
            )
        )

    def get_stable_coin_price(self, coin_id: str = "0", consumer_token: str = None):
        return self.stub.getStableCoinPrice(
            market_pb2.StableCoinPriceRequest(
                consumer_token=consumer_token,
                coin_id=coin_id,
            )
        )
