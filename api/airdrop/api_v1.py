#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from airdrop.models import (
   AirdropUser,
   PointsRecord
)

# @check_api_token
def get_points_by_address(request):
    params = json.loads(request.body.decode())
    address = params.get("address", None)
    if address is None:
        return error_json("address is empty", 4000)
    airdrop_user = AirdropUser.objects.filter(address=address).first()
    if airdrop_user is not None:
        return ok_json(airdrop_user.as_dict())
    else:
        return error_json("No this user address points", 4000)

# @check_api_token
def get_points_record_by_address(request):
    params = json.loads(request.body.decode())
    address = params.get("address", None)
    if address is None:
        return error_json("address is empty", 4000)
    page = params.get('page', 1)
    page_size = params.get('page_size', 20)
    start = (page - 1) * page_size
    end = start + page_size
    points = PointsRecord.objects.filter(address=address).order_by("-id")[start:end]
    total = PointsRecord.objects.filter(address=address).order_by("-id").count()
    point_list = []
    for point in points:
        point_list.append(point.as_dict())
    data = {
        "total": total,
        "points": point_list,
    }
    return ok_json(data)


