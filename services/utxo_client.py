# encoding=utf-8

import grpc
from django.conf import settings

from services.savour_rpc import utxo_pb2
from services.savour_rpc import utxo_pb2_grpc

class UtxoClient:
    def __init__(self):
        try:
            options = [('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH)]
            channel = grpc.insecure_channel(settings.UTXO_WALLET_GRPC_CHANNEL_URL, options=options)
            # grpc.channel_ready_future(channel).result(timeout=settings.GRPC_TIMEOUT_SECONDS)
            self.stub = utxo_pb2_grpc.WalletUtxoServiceStub(channel)
        except grpc.FutureTimeoutError:
            raise "UTXO Service gRPC server is unavailable."

    def get_support_chains(self, chain: str, network: str, consumer_token: str = None):
        return self.stub.getSupportChains(
            utxo_pb2.SupportChainsRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network
            )
        )

    def convert_address(self, chain: str, network: str, format: str, public_key: str, consumer_token: str = None):
        return self.stub.convertAddress(
            utxo_pb2.ConvertAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                format=format,
                public_key=public_key
            )
        )

    def valid_address(self, chain: str, network: str, format: str, address: str, consumer_token: str = None):
        return self.stub.validAddress(
            utxo_pb2.ValidAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                format=format,
                address=address
            )
        )

    def get_fee(self, chain: str, coin: str, network: str, rawTx: str = "", consumer_token: str = None):
        return self.stub.getFee(
            utxo_pb2.FeeRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                rawTx=rawTx
            )
        )

    def get_account(self, chain: str, network: str, address: str, brc20_address: str = "", consumer_token: str = None):
        # Note: This is UTXO's getAccount, different from Account service
        return self.stub.getAccount(
            utxo_pb2.AccountRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                address=address,
                brc20_address=brc20_address
            )
        )

    def get_unspent_outputs(self, chain: str, network: str, address: str, consumer_token: str = None):
        # Replaces original get_unspend_list concept
        return self.stub.getUnspentOutputs(
            utxo_pb2.UnspentOutputsRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                address=address
            )
        )

    def get_block_by_number(self, chain: str, height: int, consumer_token: str = None):
        return self.stub.getBlockByNumber(
            utxo_pb2.BlockNumberRequest(
                consumer_token=consumer_token,
                chain=chain,
                height=height
            )
        )

    def get_block_by_hash(self, chain: str, hash: str, consumer_token: str = None):
        return self.stub.getBlockByHash(
            utxo_pb2.BlockHashRequest(
                consumer_token=consumer_token,
                chain=chain,
                hash=hash
            )
        )

    def get_block_header_by_hash(self, chain: str, network: str, hash: str):
        # consumer_token seems missing in proto definition for request, add if needed
        return self.stub.getBlockHeaderByHash(
            utxo_pb2.BlockHeaderHashRequest(
                chain=chain,
                network=network,
                hash=hash
            )
        )

    def get_block_header_by_number(self, chain: str, network: str, height: int):
        # consumer_token seems missing in proto definition for request, add if needed
        return self.stub.getBlockHeaderByNumber(
            utxo_pb2.BlockHeaderNumberRequest(
                chain=chain,
                network=network,
                height=height
            )
        )

    def send_tx(self, chain: str, coin: str, network: str, raw_tx: str, consumer_token: str = None):
        return self.stub.SendTx(
            utxo_pb2.SendTxRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                raw_tx=raw_tx
            )
        )

    def get_tx_by_address(self, chain: str, coin: str, network: str, address: str, brc20_address: str, page: int,
                          pagesize: int, cursor: str = "", consumer_token: str = None):
        return self.stub.getTxByAddress(
            utxo_pb2.TxAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address,
                brc20_address=brc20_address,
                page=page,
                pagesize=pagesize,
                cursor=cursor
            )
        )

    def get_tx_by_hash(self, chain: str, coin: str, network: str, hash: str, consumer_token: str = None):
        return self.stub.getTxByHash(
            utxo_pb2.TxHashRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                hash=hash
            )
        )

    def create_un_sign_transaction(self, chain: str, network: str, fee: str, vin: list, vout: list,
                                   consumer_token: str = None):
        return self.stub.createUnSignTransaction(
            utxo_pb2.UnSignTransactionRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                fee=fee,
                vin=vin,
                vout=vout
            )
        )

    def build_signed_transaction(self, chain: str, network: str, tx_data: bytes, signatures: list, public_keys: list,
                                 consumer_token: str = None):
        return self.stub.buildSignedTransaction(
            utxo_pb2.SignedTransactionRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                tx_data=tx_data,
                signatures=signatures,
                public_keys=public_keys
            )
        )

    def decode_transaction(self, chain: str, network: str, raw_data: bytes, vins: list):
        # consumer_token seems missing in proto definition for request, add if needed
        return self.stub.decodeTransaction(
            utxo_pb2.DecodeTransactionRequest(
                chain=chain,
                network=network,
                raw_data=raw_data,
                vins=vins
            )
        )

    def verify_signed_transaction(self, chain: str, network: str, public_key: str, signature: str):
        # consumer_token seems missing in proto definition for request, add if needed
        return self.stub.verifySignedTransaction(
            utxo_pb2.VerifyTransactionRequest(
                chain=chain,
                network=network,
                public_key=public_key,
                signature=signature
            )
        )
