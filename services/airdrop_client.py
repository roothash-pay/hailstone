# encoding=utf-8

import grpc
from django.conf import settings
from services.savour_rpc import airdrop_pb2_grpc, airdrop_pb2


class AirdropClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel("127.0.0.1:50251", options=options)
        self.stub = airdrop_pb2_grpc.AirdropServiceStub(channel)

    def submit_dapplink_points(self, type: int, consumer_token: str = None) -> airdrop_pb2.DppLinkPointsRep:
        ret_value = self.stub.submitDppLinkPoints(
            airdrop_pb2.DppLinkPointsReq(
                consumer_token=consumer_token,
                type="0",
                address="0xf6f75BF38ED11F984Ac195e8b8a61Df73bA48892"
            )
        )
        print("ret===", ret_value.code, ret_value.msg)
        return ret_value
