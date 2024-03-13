# encoding=utf-8

import json
import uuid

from common.helpers import (
    ok_json,
    error_json
)
from airdrop.models import (
    AirdropUser,
    PointsRecord,
    ProjectInterAction,
    Questions
)


# @check_api_token
def get_project_interactions(request):
    pi_lists = ProjectInterAction.objects.all()
    pi_ret_lists = []
    for pl in pi_lists:
        pi_ret_lists.append(pl.as_dict())
    return ok_json(pi_ret_lists)


# @check_api_token
def get_questions(request):
    question_lists = Questions.objects.all()
    question_ret_lists = []
    for ql in question_lists:
        question_ret_lists.append(ql.as_dict())
    return ok_json(question_ret_lists)


# @check_api_token
def get_invite_code_by_address(request):
    params = json.loads(request.body.decode())
    address = params.get("address", None)
    if address is not None:
        airdrop_user = AirdropUser.objects.filter(address=address).first()
        if airdrop_user is not None:
            data = {
                "invite_code": airdrop_user.invite_code,
            }
            return ok_json(data)
        else:
            return error_json("address is not exist", 4000)
    else:
        return error_json("address is none", 4000)


# @check_api_token
def submit_invite_info(request):
    params = json.loads(request.body.decode())
    address = params.get("address", None)
    invite_code = params.get("invite_code", None)
    if address is None or invite_code is None:
        return error_json("address or invite_code params is empty", 4000)
    invite_user = AirdropUser.objects.filter(invite_code=invite_code).first()
    if invite_user is None:
        return error_json("This user is not exist", 4000)
    AirdropUser.objects.create(
        invite_code=uuid.uuid4(),
        invite_me_uuid=invite_user.uuid,
        address=address
    )
    if invite_user.points < 10:
        invite_user.points = invite_user.points + 2
        invite_user.save()
        PointsRecord.objects.create(
            user=invite_user,
            address=invite_user.address,
            type='Invite',
            points=2
        )
    return ok_json({})


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
