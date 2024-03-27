# encoding=utf-8

import json
from common.helpers import ok_json, error_json
from l3staking.models import (
    StakingChain,
    StakingStrategy,
    Node,
)


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
