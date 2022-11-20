# encoding=utf-8

import grpc
from django.conf import settings
from services.savour_rpc import keylocker_pb2, keylocker_pb2_grpc


class KeyLockerClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.CHAINEYE_GRPC_CHANNEL_URL, options=options)
        self.stub = keylocker_pb2_grpc.LeyLockerServiceStub(channel)

    def get_support_chain(self, chain: str, network:str = "mainnet", consumer_token: str = None) -> keylocker_pb2.SupportChainRep:
        return self.stub.getSupportChain(
            keylocker_pb2.SupportChainReq(
                consumer_token=consumer_token,
                chain=chain,
                network=network,
            )
        )

    def set_social_key(self, chain: str, uuid:str, key:str, password: str, social_code: str, consumer_token: str = None)-> keylocker_pb2.SetSocialKeyRep:
        return self.stub.setSocialKey(
            keylocker_pb2.SetSocialKeyReq(
                consumer_token=consumer_token,
                chain=chain,
                uuid=uuid,
                key=key,
                password=password,
                social_code=social_code,
            )
        )

    def get_social_key(self, chain: str, uuid:str, social_code: str,  file_cid:str = None, contract: str = None, consumer_token: str = None) -> keylocker_pb2.GetSocialKeyRep:
        return self.stub.getSocialKey(
            keylocker_pb2.GetSocialKeyReq(
                consumer_token=consumer_token,
                chain=chain,
                uuid=uuid,
                file_cid=file_cid,
                contract=contract,
                social_code=social_code,
            )
        )
