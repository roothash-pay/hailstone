# encoding=utf-8

import json
import logging
from google.protobuf.json_format import MessageToJson

from common.helpers import ok_json, error_json
from l3staking.models import (
    StakingChain,
    StakingStrategy,
    Node,
)
from services.appchain_client import (
    AppChainClient
)

logger = logging.getLogger(__name__)
# @check_api_token
def get_staking_chains(request):
    staking_chains = StakingChain.objects.all()
    staking_chain_list = []
    for sc in staking_chains:
        staking_chain_list.append(sc.as_dict())
    return ok_json(staking_chain_list)


# @check_api_token
def get_staking_node_list(request):
    params = json.loads(request.body.decode())
    chain_id = params.get('chain_id', 0)
    staking_chain = StakingChain.objects.filter(id=chain_id).first()
    if staking_chain is None:
        return error_json("No support chain", 4000)
    staking_strategies = StakingStrategy.objects.filter(chain=staking_chain)
    staking_strategies_node_list = []
    for ss in staking_strategies:
        staking_nodes = Node.objects.filter(chain_id=ss.chain, strategy=ss).order_by("-id")
        staking_node_list = []
        for node in staking_nodes:
            staking_node_list.append(node.as_dict())
        staking_strategies_node_list.append({
            "stategy_name": ss.name,
            "node_list": staking_node_list
        })
    return ok_json(staking_strategies_node_list)


# @check_api_token
def get_node_detail(request):
    params = json.loads(request.body.decode())
    node_id = params.get('node_id', 0)
    chain_id = params.get('chain_id', "0")
    staker_address = params.get('staker_address', "0x")
    strategies = params.get('strategies', "0x")
    type = params.get('type', "L1")
    appChainClient = AppChainClient()
    if type in ["L1", "l1"]:
        l1_stakers_rewards = appChainClient.l1_staker_reward_amount(
            chain_id=chain_id,
            staker_address=staker_address,
            strategies=strategies,
        )
        print(l1_stakers_rewards)
    else:
        l2_stakers_rewards = appChainClient.l2_staker_reward_amount(
            chain_id=chain_id,
            staker_address=staker_address,
            strategy=strategies,
        )
        print(l2_stakers_rewards)
    staking_node = Node.objects.filter(id=node_id).first()
    if staking_node is None:
        return error_json("Do not exist node", 4000)
    return ok_json(staking_node.as_dict())


# @check_api_token
def get_l2_stake_record(request):
    params = json.loads(request.body.decode())
    staker_address = params.get('staker_address', "0x")
    strategy = params.get('strategy', "0x")
    page = params.get('page', 1)
    page_size = params.get('page_size', 10)
    appChainClient = AppChainClient()
    l2_stake_record = appChainClient.l2_stake_record(
        staker_address=staker_address,
        strategy=strategy,
        page=page,
        page_size=page_size
    )
    logger.debug(l2_stake_record)
    serialized = MessageToJson(l2_stake_record)
    jb = json.loads(serialized)
    return ok_json(jb.page)


# @check_api_token
def get_l2_unstake_record(request):
    params = json.loads(request.body.decode())
    staker_address = params.get('staker_address', "0x")
    strategy = params.get('strategy', "0x")
    page = params.get('page', 1)
    page_size = params.get('page_size', 10)
    appChainClient = AppChainClient()
    l2_unstake_record = appChainClient.l2_unstake_record(
        staker_address=staker_address,
        strategy=strategy,
        page=page,
        page_size=page_size
    )
    logger.debug(l2_unstake_record)
    serialized = MessageToJson(l2_unstake_record)
    jb = json.loads(serialized)
    return ok_json(jb.page)
