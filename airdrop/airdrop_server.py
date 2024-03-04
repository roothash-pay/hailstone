#encoding=utf-8

import pytz
from airdrop.models import AirdropUser, PointsRecord
from services.savour_rpc import airdrop_pb2_grpc, common_pb2, airdrop_pb2
from django.conf import settings

tz = pytz.timezone(settings.TIME_ZONE)

class AirdropServer(airdrop_pb2_grpc.AirdropServiceServicer):
    def submitDppLinkPoints(self, request, context) -> airdrop_pb2.DppLinkPointsResponse:
        airdrop_user: AirdropUser
        type = str(request.type)
        address = str(request.address)
        points = int(request.points)
        airdrop_tmp_user = AirdropUser.objects.filter(address=address).first()
        if airdrop_tmp_user is not None:
            airdrop_tmp_user.points += points
            airdrop_tmp_user.save()
            airdrop_user = airdrop_tmp_user
        else:
            airdrop_user = AirdropUser.objects.create(
                address=address,
                points=points
            )
        PointsRecord.objects.create(
            user=airdrop_user,
            address=address,
            type=type,
            points=points
        )
        return airdrop_pb2.DppLinkPointsResponse(
            code=common_pb2.SUCCESS,
            msg="submit dapplink points success",
        )

