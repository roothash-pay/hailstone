# encoding=utf-8

import grpc
from django.conf import settings

from services.savour_rpc import account_pb2
from services.savour_rpc import account_pb2_grpc


class AccountClient:
    def __init__(self):
        try:
            options = [
                ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
            ]
            channel = grpc.insecure_channel(settings.ACCOUNT_WALLET_GRPC_CHANNEL_URL, options=options)
            # grpc.channel_ready_future(channel).result(timeout=settings.GRPC_TIMEOUT_SECONDS)
            self.stub = account_pb2_grpc.WalletAccountServiceStub(channel)
        except grpc.FutureTimeoutError:
            raise "Account Service gRPC server is unavailable."

    def get_support_chains(self, chain: str, network: str, consumer_token: str = None):
        return self.stub.getSupportChains(
            account_pb2.SupportChainsRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network
            )
        )

    def convert_address(self, chain: str, network: str, type: str, public_key: str, consumer_token: str = None):
        return self.stub.convertAddress(
            account_pb2.ConvertAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                type=type,
                public_key=public_key
            )
        )

    def valid_address(self, chain: str, network: str, address: str, consumer_token: str = None):
        return self.stub.validAddress(
            account_pb2.ValidAddressRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                address=address
            )
        )

    def get_block_by_number(self, chain: str, height: int, view_tx: bool, consumer_token: str = None):
        return self.stub.getBlockByNumber(
            account_pb2.BlockNumberRequest(
                consumer_token=consumer_token,
                chain=chain,
                height=height,
                view_tx=view_tx
            )
        )

    def get_block_by_hash(self, chain: str, hash: str, view_tx: bool, consumer_token: str = None):
        return self.stub.getBlockByHash(
            account_pb2.BlockHashRequest(
                consumer_token=consumer_token,
                chain=chain,
                hash=hash,
                view_tx=view_tx
            )
        )

    def get_block_header_by_hash(self, chain: str, network: str, hash: str, consumer_token: str = None):
        return self.stub.getBlockHeaderByHash(
            account_pb2.BlockHeaderHashRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                hash=hash
            )
        )

    def get_block_header_by_number(self, chain: str, network: str, height: int, consumer_token: str = None):
        return self.stub.getBlockHeaderByNumber(
            account_pb2.BlockHeaderNumberRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                height=height
            )
        )

    def get_block_header_by_range(self, chain: str, network: str, start: str, end: str, consumer_token: str = None):
        return self.stub.getBlockHeaderByRange(
            account_pb2.BlockByRangeRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                start=start,
                end=end
            )
        )

    def get_account(self, chain: str, coin: str, network: str, address: str, contract_address: str = "",
                    proposer_key_index: int = 0, consumer_token: str = None):
        # Combines original get_balance, get_nonce, get_account_info
        return self.stub.getAccount(
            account_pb2.AccountRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                address=address,
                contract_address=contract_address,
                proposer_key_index=proposer_key_index
            )
        )

    def get_fee(self, chain: str, coin: str, network: str, rawTx: str = "", address: str = "",
                consumer_token: str = None):
        # Replaces original get_gasPrice
        return self.stub.getFee(
            account_pb2.FeeRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                rawTx=rawTx,
                address=address
            )
        )

    def send_tx(self, chain: str, coin: str, network: str, raw_tx: str, consumer_token: str = None):
        # Replaces original send_transaction
        return self.stub.SendTx(
            account_pb2.SendTxRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                raw_tx=raw_tx
            )
        )

    def get_tx_by_address(self, chain: str, coin: str, network: str, address: str, contract_address: str, page: int,
                          pagesize: int, consumer_token: str = None):
        # Replaces original get_address_transaction
        return self.stub.getTxByAddress(
            account_pb2.TxAddressRequest(
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
        # Replaces original get_hash_transaction AND corrects the stub call
        return self.stub.getTxByHash(
            account_pb2.TxHashRequest(
                consumer_token=consumer_token,
                chain=chain,
                coin=coin,
                network=network,
                hash=hash
            )
        )

    def build_un_sign_transaction(self, chain: str, network: str, base64_tx: str, consumer_token: str = None):
        return self.stub.buildUnSignTransaction(
            account_pb2.UnSignTransactionRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                base64_tx=base64_tx
            )
        )

    def build_signed_transaction(self, chain: str, network: str, base64_tx: str, signature: str, public_key: str,
                                 consumer_token: str = None):
        return self.stub.buildSignedTransaction(
            account_pb2.SignedTransactionRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                base64_tx=base64_tx,
                signature=signature,
                public_key=public_key
            )
        )

    def decode_transaction(self, chain: str, network: str, raw_tx: str, consumer_token: str = None):
        return self.stub.decodeTransaction(
            account_pb2.DecodeTransactionRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                raw_tx=raw_tx
            )
        )

    def verify_signed_transaction(self, chain: str, network: str, public_key: str, signature: str,
                                  consumer_token: str = None):
        return self.stub.verifySignedTransaction(
            account_pb2.VerifyTransactionRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                public_key=public_key,
                signature=signature
            )
        )

    def get_extra_data(self, chain: str, network: str, address: str, coin: str, consumer_token: str = None):
        return self.stub.getExtraData(
            account_pb2.ExtraDataRequest(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
                address=address,
                coin=coin
            )
        )

    # def get_nft_list_by_address(self, chain: str, network: str, address: str, protocol_type: str, contract_address: str,
    #                             page: int, pagesize: int, consumer_token: str = None):
    #     return self.stub.getNftListByAddress(
    #         account_pb2.NftAddressRequest(
    #             consumer_token=consumer_token,
    #             chain=chain,
    #             network=network,
    #             address=address,
    #             protocol_type=protocol_type,
    #             contract_address=contract_address,
    #             page=page,
    #             pagesize=pagesize
    #         )
    #     )
    #
    # def get_nft_collection(self, chain: str, network: str, token_contract_address: str, filter_type: str, token_id: str,
    #                        page: int, pagesize: int, consumer_token: str = None):
    #     return self.stub.getNftCollection(
    #         account_pb2.NftCollectionRequest(
    #             consumer_token=consumer_token,
    #             chain=chain,
    #             network=network,
    #             token_contract_address=token_contract_address,
    #             filter_type=filter_type,
    #             token_id=token_id,
    #             page=page,
    #             pagesize=pagesize
    #         )
    #     )

    # def get_nft_detail(self, request: account_pb2.NftDetailRequest):  # Placeholder, adjust as needed
    #     # Assuming NftDetailRequest takes consumer_token etc. Adjust parameters based on actual proto definition.
    #     # request.consumer_token = request.consumer_token or None # Example assignment
    #     return self.stub.getNftDetail(request)
    #
    # def get_nft_holder_list(self, request: account_pb2.NftHolderListRequest):  # Placeholder, adjust as needed
    #     # request.consumer_token = request.consumer_token or None
    #     return self.stub.getNftHolderList(request)
    #
    # def get_nft_trade_history(self, request: account_pb2.NftTradeHistoryRequest):  # Placeholder, adjust as needed
    #     # request.consumer_token = request.consumer_token or None
    #     return self.stub.getNftTradeHistory(request)
    #
    # def get_address_nft_trade_history(self,
    #                                   request: account_pb2.AddressNftTradeHistoryRequest):  # Placeholder, adjust as needed
    #     # request.consumer_token = request.consumer_token or None
    #     return self.stub.getAddressNftTradeHistory(request)
