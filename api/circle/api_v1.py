#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from common.api_auth import check_api_token
from services.chaineye_client import ChaineyeClient
from services.savour_rpc import common_pb2


# @check_api_token
def get_arcticle_list(request):
    params = json.loads(request.body.decode())
    type = params.get('type')
    page = params.get('page', 1)
    page_size = params.get('page_size', 10)
    wallet_client = ChaineyeClient()
    result = wallet_client.get_arcticle_list(
        type=type,
        page=page,
        page_size=page_size,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("get chaineye arcticle list fail", 400)


def get_arcticle_detail(request):
    params = json.loads(request.body.decode())
    type = params.get('type')
    article_id = params.get('article_id')
    wallet_client = ChaineyeClient()
    result = wallet_client.get_arcticle_detail(
        type=type,
        id=article_id
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("get chaineye arcticle detail fail", 400)


def get_comment_list(request):
    params = json.loads(request.body.decode())
    article_id = params.get('article_id')
    page = params.get('page', 1)
    page_size = params.get('page_size', 10)
    wallet_client = ChaineyeClient()
    result = wallet_client.get_comment_list(
        article_id=article_id,
        page=page,
        page_size=page_size,
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("get chaineye comment list fail", 400)



def get_like_address(request):
    params = json.loads(request.body.decode())
    author_id = params.get('author_id')
    wallet_client = ChaineyeClient()
    result = wallet_client.get_like_address(
        author_id=author_id
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("get like address fail", 400)


def like_article(request):
    params = json.loads(request.body.decode())
    tx_hash = params.get('tx_hash')
    like_from = params.get('like_from')
    like_to = params.get('like_to')
    amount = params.get('amount')
    asset_name = params.get('asset_name')
    token_address = params.get('token_address')
    wallet_client = ChaineyeClient()
    result = wallet_client.like_article(
        tx_hash=tx_hash,
        like_from=like_from,
        like_to=like_to,
        amount=amount,
        asset_name=asset_name,
        token_address=token_address
    )
    if result.code == common_pb2.SUCCESS:
        return ok_json(result)
    else:
        return error_json("like article fail", 400)