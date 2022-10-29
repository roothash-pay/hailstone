import json
from common.helpers import (
    ok_json,
    error_json,
    gen_rsa_crypto_key,
    encrypt_data,
    decrypt_data,
)

from wallethead.models import Storage

EMPTY = [None, "None", 0, ""]


# @check_api_token
def get_head(request):
    params = json.loads(request.body.decode())
    wallet_id = params.get("wallet_id", None)
    if wallet_id in EMPTY:
        return error_json("Invalid Params")
    resp = []
    list_head = Storage.objects.filter(wallet_id=wallet_id)
    for head in list_head:
        resp.append(head.to_dict())
    return ok_json(resp)


def save_head(request):
    params = json.loads(request.body.decode())
    wallet_head = params.get("wallet_head", None)
    wallet_id = params.get("wallet_id", None)
    if wallet_head in EMPTY or wallet_id in EMPTY:
        return error_json("Invalid Params")

    target = Storage.objects.filter(wallet_id=wallet_id, wallet_head=wallet_head)
    if len(target) != 0:
        return ok_json(target[0].to_dict())
    else:
        private_key, public_key = gen_rsa_crypto_key()
        # TODO upload encrypt_head ipfs
        # encrypt_head = encrypt_data(wallet_head, public_key)
        head_ipfs_addr = "ipfs://ip.addr"

        s = Storage.objects.create(
            wallet_id=wallet_id,
            wallet_head=wallet_head,
            head_public_key=public_key,
            head_private_key=private_key,
            head_ipfs_addr=head_ipfs_addr,
        )
    return ok_json(s.to_dict())
