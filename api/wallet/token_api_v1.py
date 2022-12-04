# encoding=utf-8

import json
from services.token_discover.token_discover import token_discover_container
from common.helpers import (
    ok_json,
    error_json
)

EMPTY = [None, "None", 0, ""]


def get_tokens(request):
    params = json.loads(request.body.decode())
    chain = params.get('chain', "")
    address = params.get('address', "")

    if chain in EMPTY or address in EMPTY:
        return error_json("invalid Params", 4000)
    if chain not in token_discover_container:
        return error_json("not support", 1)

    discover = token_discover_container[chain]
    data = discover.get_tokens(chain, address)
    if data is None:
        return error_json("network error ", 2)

    return ok_json(data)
