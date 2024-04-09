# encoding=utf-8

import grpc
from django.conf import settings
from services.savour_rpc import appchain_pb2_grpc, appchain_pb2


class AppChainClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel("acorus-rpc.testnet.dapplink.xyz:443", options=options)
        self.stub = appchain_pb2_grpc.AppChainServiceStub(channel)

    def l1_staker_reward_amount(self, chain_id: str, staker_address: str, strategies: str, consumer_token: str = None) -> appchain_pb2.L1StakerRewardsAmountResponse:
        return self.stub.L1StakerRewardsAmount(
            appchain_pb2.L1StakerRewardsAmountRequest(
                chain_id=chain_id,
                staker_address=staker_address,
                strategies=strategies
            )
        )

    def l2_staker_reward_amount(self, chain_id: str, staker_address: str, strategy: str, consumer_token: str = None) -> appchain_pb2.L2StakerRewardsAmountResponse:
        return self.stub.L2StakerRewardsAmount(
            appchain_pb2.L2StakerRewardsAmountRequest(
                chain_id=chain_id,
                staker_address=staker_address,
                strategy=strategy
            )
        )
    def l2_stake_record(self, staker_address: str, strategy: str,page: int,page_size: int, consumer_token: str = None) -> appchain_pb2.L2StakerRewardsAmountResponse:
        return self.stub.L2StakeRecord(
            appchain_pb2.L2StakeRecordRequest(
                staker_address=staker_address,
                strategy=strategy,
                page=page,
                page_size=page_size
            )
        )
    def l2_unstake_record(self, staker_address: str, strategy: str,page: int,page_size: int, consumer_token: str = None) -> appchain_pb2.L2StakerRewardsAmountResponse:
        return self.stub.L2UnStakeRecord(
            appchain_pb2.L2UnStakeRecordRequest(
                staker_address=staker_address,
                strategy=strategy,
                page=page,
                page_size=page_size
            )
        )