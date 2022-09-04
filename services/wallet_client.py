#encoding=utf-8

import grpc
from django.conf import settings
from services.savour_rpc import wallet_pb2_grpc
from services.savour_rpc import wallet_pb2


class WalletClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.WALLET_GRPC_CHANNEL_URL, options=options)
        self.stub = wallet_pb2_grpc.WalletServiceStub(channel)

    def get_balance(self, chain: str, coin: str, network: str, address: str, contract_address:str, consumer_token: str = None):
        return self.stub.getBalance(
            wallet_pb2.BalanceRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address,
                contract_address=contract_address,
            )
        )

    def get_nonce(self, chain: str, coin: str, network: str, address: str, consumer_token: str = None):
        return self.stub.getNonce(
            wallet_pb2.NonceRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address
            )
        )

    def get_gasPrice(self, chain: str, coin: str, network: str, consumer_token: str = None):
        return self.stub.getGasPrice(
            wallet_pb2.GasPriceRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network
            )
        )

    def send_transaction(self, chain: str, coin: str, network: str, raw_tx:str, consumer_token: str = None):
        return self.stub.SendTx(
            wallet_pb2.SendTxRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                raw_tx=raw_tx
            )
        )

    def get_tx_by_address(self, chain: str, coin: str, network: str, address: str, contract_address: str, page: int, pagesize: int,  consumer_token: str = None):
        return self.stub.getTxByAddress(
            wallet_pb2.TxAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address,
                contract_address=contract_address,
                page=page,
                pagesize=pagesize
            )
        )

    def get_tx_by_hash(self, chain: str, coin: str, network: str, hash: str, consumer_token: str = None):
        return self.stub.getTxByAddress(
            wallet_pb2.TxAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                hash=hash
            )
        )

    def get_account(self, chain: str, coin: str, network: str, address: str, consumer_token: str = None):
        return self.stub.getAccount(
            wallet_pb2.AccountRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address
            )
        )

    def get_utxo(self, chain: str, coin: str, network: str, address: str, consumer_token: str = None):
        return self.stub.getUtxo(
            wallet_pb2.UtxoRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address
            )
        )

    def get_min_rent(self, chain: str, coin: str, network: str, address: str, consumer_token: str = None):
        return self.stub.getMinRent(
            wallet_pb2.MinRentRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address
            )
        )





