# encoding=utf-8
import datetime
import uuid

import pytz
from airdrop.models import (
    AirdropUser,
    PointsRecord,
    ProjectInterAction
)
from services.savour_rpc import airdrop_pb2_grpc, common_pb2, airdrop_pb2
from django.conf import settings

tz = pytz.timezone(settings.TIME_ZONE)


def get_bridge_type(bridge_type: str):
    if bridge_type == "0":
        return "BridgeTransfer"
    elif bridge_type == "1":
        return "BridgeStaking"
    elif bridge_type == "2":
        return "BridgeWithdraw"
    elif bridge_type == "3":
        return "bridgeGrants"
    else:
        return "Invite"


class AirdropServer(airdrop_pb2_grpc.AirdropServiceServicer):
    def submitDppLinkPoints(self, request, context) -> airdrop_pb2.DppLinkPointsRep:
        airdrop_user: AirdropUser
        bridge_type = get_bridge_type(str(request.type))
        address = str(request.address)
        projectInteraction = ProjectInterAction.objects.filter(points_type=bridge_type).first()
        if projectInteraction is not None:
            airdrop_tmp_user = AirdropUser.objects.filter(address__icontains=address).first()
            if airdrop_tmp_user is not None:
                today = datetime.datetime.now().date()
                todayUserPointList = PointsRecord.objects.filter(
                    type=bridge_type,
                    address__icontains=address,
                    created_at__gte=str(today) + ' 00:00:00'
                ).all()
                todayUserMaxPoints = 0
                for todayUserPoint in todayUserPointList:
                    todayUserMaxPoints = todayUserMaxPoints + todayUserPoint.points
                if airdrop_tmp_user.points < projectInteraction.max_points and todayUserMaxPoints < projectInteraction.daily_max_points:
                    airdrop_tmp_user.points += projectInteraction.once_points
                    airdrop_tmp_user.save()
                    airdrop_user = airdrop_tmp_user
                else:
                    return airdrop_pb2.DppLinkPointsRep(
                        code=common_pb2.SUCCESS,
                        msg="already arrive to daily or max points",
                    )
            else:
                airdrop_user = AirdropUser.objects.create(
                    invite_code=uuid.uuid4(),
                    address=address,
                    points=projectInteraction.once_points
                )
            PointsRecord.objects.create(
                user=airdrop_user,
                address=address,
                type=bridge_type,
                points=projectInteraction.once_points
            )
            return airdrop_pb2.DppLinkPointsRep(
                code=common_pb2.SUCCESS,
                msg="submit dapplink points success",
            )
