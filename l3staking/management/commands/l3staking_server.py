#encoding=utf-8

import grpc
from django.core.management.base import BaseCommand
from concurrent import futures
from services.savour_rpc import l3staking_pb2_grpc
from l3staking.l3staking_server import L3StakingServer


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        l3staking_pb2_grpc.add_L3StakingServiceServicer_to_server(
            L3StakingServer(),
            server
        )
        server.add_insecure_port('[::]:50252')
        server.start()
        print("l3 staking rpc server start")
        server.wait_for_termination()