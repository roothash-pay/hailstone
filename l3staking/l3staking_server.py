# encoding=utf-8

import pytz
from l3staking.models import (
    Node
)
from services.savour_rpc import l3staking_pb2_grpc, l3staking_pb2
from django.conf import settings

tz = pytz.timezone(settings.TIME_ZONE)


class L3StakingServer(l3staking_pb2_grpc.L3StakingServiceServicer):
    def updateStakingNodeIncome(self, request, context) -> l3staking_pb2.StakingNodeRep:
        address = str(request.address)
        chain_id = str(request.chain_id)
        strategy = str(request.strategy)
        eth_income = str(request.eth_income)
        eth_income_rate = str(request.eth_income_rate)
        dp_income = str(request.dp_income)
        dp_income_rate = str(request.dp_income_rate)
        eth_evil = str(request.eth_evil)
        eth_evil_rate = str(request.eth_evil_rate)
        dp_evil = str(request.dp_evil)
        dp_evil_rate = str(request.dp_evil_rate)
        tvl = str(request.tvl)
        Node.objects.filter(
            address=address,
            chain__chain_id=chain_id,
            strategy__address=strategy
        ).update(
            eth_income=eth_income,
            eth_income_rate=eth_income_rate,
            dp_income=dp_income,
            dp_income_rate=dp_income_rate,
            eth_evil=eth_evil,
            eth_evil_rate=eth_evil_rate,
            dp_evil=dp_evil,
            dp_evil_rate=dp_evil_rate,
            tvl=tvl
        )
        return l3staking_pb2.StakingNodeRep(
            code="200",
            msg="submit stake node income success",
        )
