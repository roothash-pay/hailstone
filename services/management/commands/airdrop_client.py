#encoding=utf-8

import grpc
from django.core.management.base import BaseCommand
from services.airdrop_client import AirdropClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        airC = AirdropClient()
        response = airC.submit_dapplink_points(1, "")
        print("response==", response)

