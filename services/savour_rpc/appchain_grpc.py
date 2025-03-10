# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: savour_rpc/appchain.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

from services.savour_rpc import appchain_pb2


class AppChainServiceBase(abc.ABC):

    @abc.abstractmethod
    async def L1StakerRewardsAmount(self, stream: 'grpclib.server.Stream[appchain_pb2.L1StakerRewardsAmountRequest, savour_rpc.appchain_pb2.L1StakerRewardsAmountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def L2StakerRewardsAmount(self, stream: 'grpclib.server.Stream[appchain_pb2.L2StakerRewardsAmountRequest, savour_rpc.appchain_pb2.L2StakerRewardsAmountResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/services.savour_rpc.appchain.AppChainService/L1StakerRewardsAmount': grpclib.const.Handler(
                self.L1StakerRewardsAmount,
                grpclib.const.Cardinality.UNARY_UNARY,
                appchain_pb2.L1StakerRewardsAmountRequest,
                appchain_pb2.L1StakerRewardsAmountResponse,
            ),
            '/services.savour_rpc.appchain.AppChainService/L2StakerRewardsAmount': grpclib.const.Handler(
                self.L2StakerRewardsAmount,
                grpclib.const.Cardinality.UNARY_UNARY,
                appchain_pb2.L2StakerRewardsAmountRequest,
                appchain_pb2.L2StakerRewardsAmountResponse,
            ),
        }


class AppChainServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.L1StakerRewardsAmount = grpclib.client.UnaryUnaryMethod(
            channel,
            '/services.savour_rpc.appchain.AppChainService/L1StakerRewardsAmount',
            appchain_pb2.L1StakerRewardsAmountRequest,
            appchain_pb2.L1StakerRewardsAmountResponse,
        )
        self.L2StakerRewardsAmount = grpclib.client.UnaryUnaryMethod(
            channel,
            '/services.savour_rpc.appchain.AppChainService/L2StakerRewardsAmount',
            appchain_pb2.L2StakerRewardsAmountRequest,
            appchain_pb2.L2StakerRewardsAmountResponse,
        )
