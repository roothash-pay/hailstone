#encoding=utf-8

import grpc
from django.core.management.base import BaseCommand
from concurrent import futures
from services.savour_rpc import airdrop_pb2_grpc
from airdrop.airdrop_server import AirdropServer


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        airdrop_pb2_grpc.add_AirdropServiceServicer_to_server(
            AirdropServer(),
            server
        )
        server.add_insecure_port('[::]:50251')
        server.start()
        print("airdrop rpc server start")
        server.wait_for_termination()