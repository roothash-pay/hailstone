# api/tests/test_wallet_api.py
# Tests for Wallet related APIs (/api/get_balance, /api/add_note_book, etc.)
from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from wallet.models import Wallet, WalletAsset, Address, AddressAsset
from common.models import Chain, Asset
import json
from unittest.mock import patch
import services.account_client
from services.savour_rpc import common_pb2


class WalletAPITests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 创建测试所需的基础数据
        cls.chain = Chain.objects.create(name="Arbitrum")
        cls.eth_asset = Asset.objects.create(name="ETH", mark="ETH", unit="18", chain=cls.chain)
        cls.usdt_asset = Asset.objects.create(name="USDT", mark="USDT", unit="6", chain=cls.chain)
        
        # 创建测试钱包
        cls.wallet = Wallet.objects.create(
            chain=cls.chain,
            device_id="test_device_id",
            wallet_uuid="test_wallet_uuid",
            wallet_name="Test Wallet",
            asset_usd=100.0,
            asset_cny=700.0
        )
        
        # 创建钱包资产
        cls.wallet_asset_eth = WalletAsset.objects.create(
            wallet=cls.wallet, 
            asset=cls.eth_asset,
            contract_addr="",
            balance=1.0,
            asset_usd=100.0,
            asset_cny=700.0
        )
        
        cls.wallet_asset_usdt = WalletAsset.objects.create(
            wallet=cls.wallet, 
            asset=cls.usdt_asset,
            contract_addr="0xdAC17F958D2ee523a2206206994597C13D831ec7",
            balance=0.0,
            asset_usd=0.0,
            asset_cny=0.0
        )
        
        # 创建地址
        cls.address = Address.objects.create(
            wallet=cls.wallet,
            index="0",
            address="0x98E9D288743839e96A8005a6B51C770Bbf7788C0"
        )
        
        # 创建地址资产
        cls.address_asset_eth = AddressAsset.objects.create(
            wallet=cls.wallet,
            asset=cls.eth_asset,
            address=cls.address,
            balance=1.0,
            asset_usd=100.0,
            asset_cny=700.0
        )
        
        cls.address_asset_usdt = AddressAsset.objects.create(
            wallet=cls.wallet,
            asset=cls.usdt_asset,
            address=cls.address,
            balance=0.0,
            asset_usd=0.0,
            asset_cny=0.0
        )

    def setUp(self):
        # 每个测试方法执行前调用
        self.client = Client()

    def test_get_balance(self):
        """测试按地址查询余额"""
        # 创建模拟响应对象
        mock_response = type('obj', (object,), {
            'code': common_pb2.SUCCESS,
            'balance': '1000000000000000000',  # 1 ETH (以wei为单位)
            'asset_usd': '3000.00',
            'asset_cny': '21000.00',
            'data_stat': []
        })
        
        # 使用patch模拟account_client.get_balance方法
        with patch.object(services.account_client.AccountClient, 'get_balance', return_value=mock_response):
            request_data = {
                "device_id": "test_device_id",
                "wallet_uuid": "test_wallet_uuid",
                "index": "0",
                "chain": "Arbitrum",
                "symbol": "ETH",
                "network": "mainnet",
                "address": "0x98E9D288743839e96A8005a6B51C770Bbf7788C0",
                "contract_address": ""
            }
            
            response = self.client.post(
                reverse('get_balance'),
                data=json.dumps(request_data),
                content_type='application/json'
            )
            
            # 检查响应状态码
            self.assertEqual(response.status_code, 200)
            
            # 检查响应内容
            response_data = json.loads(response.content)
            self.assertTrue(response_data['ok'])
            self.assertEqual(response_data['code'], 200)
            
            # 验证返回数据结构
            result = response_data['result']
            self.assertIn('balance', result)
            self.assertIn('asset_usd', result)
            self.assertIn('asset_cny', result)
            self.assertIn('data_stat', result)
        
    def test_get_wallet_balance(self):
        """测试按钱包查询余额"""
        request_data = {
            "device_id": "test_device_id",
            "wallet_uuid": "test_wallet_uuid",
            "chain": "Arbitrum"
        }
        
        response = self.client.post(
            reverse('get_wallet_balance'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应状态码
        self.assertEqual(response.status_code, 200)
        
        # 检查响应
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        
        # 验证返回数据结构
        result = response_data['result']
        self.assertEqual(result['chain'], "Arbitrum")
        self.assertEqual(result['device_id'], "test_device_id")
        self.assertEqual(result['wallet_uuid'], "test_wallet_uuid")
        self.assertEqual(result['wallet_name'], "Test Wallet")
        self.assertIn('token_list', result)
        
    def test_submit_wallet_info(self):
        """测试提交钱包信息"""
        # 使用一个新的钱包信息
        request_data = {
            "chain": "Arbitrum",
            "symbol": "ETH",
            "network": "mainnet",
            "device_id": "new_device_id",
            "wallet_uuid": "new_wallet_uuid",
            "wallet_name": "New Wallet",
            "index": "0",
            "address": "0x1111111111111111111111111111111111111111",
            "contract_addr": ""
        }
        
        response = self.client.post(
            reverse('submit_wallet_info'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['result'], "submit wallet success")
        
        # 验证数据已创建
        self.assertTrue(Wallet.objects.filter(
            device_id="new_device_id",
            wallet_uuid="new_wallet_uuid"
        ).exists())
        
    def test_batch_submit_wallet(self):
        """测试批量提交钱包信息"""
        request_data = {
            "batch_wallet": [
                {
                    "chain": "Arbitrum",
                    "symbol": "ETH",
                    "network": "mainnet",
                    "device_id": "batch_device_id",
                    "wallet_uuid": "batch_wallet_uuid",
                    "wallet_name": "Batch Wallet",
                    "index": "0",
                    "address": "0x2222222222222222222222222222222222222222",
                    "contract_addr": ""
                }
            ]
        }
        
        response = self.client.post(
            reverse('batch_submit_wallet'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['result'], "batch submit wallet success")
        
        # 验证数据已创建
        self.assertTrue(Wallet.objects.filter(
            device_id="batch_device_id",
            wallet_uuid="batch_wallet_uuid"
        ).exists())
        
    def test_get_wallet_asset(self):
        """测试获取钱包资产"""
        request_data = {
            "device_id": "test_device_id"
        }
        
        response = self.client.post(
            reverse('get_wallet_asset'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        
        # 验证返回数据结构
        result = response_data['result']
        self.assertIn('total_asset_usd', result)
        self.assertIn('total_asset_cny', result)
        self.assertIn('token_list', result)
        
    def test_update_wallet_name(self):
        """测试更新钱包名称"""
        request_data = {
            "device_id": "test_device_id",
            "wallet_uuid": "test_wallet_uuid",
            "wallet_name": "Updated Wallet Name"
        }
        
        response = self.client.post(
            reverse('update_wallet_name'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['result'], "update wallet name success")
        
        # 验证名称已更新
        updated_wallet = Wallet.objects.get(
            device_id="test_device_id",
            wallet_uuid="test_wallet_uuid"
        )
        self.assertEqual(updated_wallet.wallet_name, "Updated Wallet Name")
        
    def test_delete_wallet(self):
        """测试删除钱包"""
        # 先创建一个要删除的钱包
        delete_wallet = Wallet.objects.create(
            chain=self.chain,
            device_id="delete_device_id",
            wallet_uuid="delete_wallet_uuid",
            wallet_name="Delete Wallet",
            asset_usd=0.0,
            asset_cny=0.0
        )
        
        request_data = {
            "device_id": "delete_device_id",
            "wallet_uuid": "delete_wallet_uuid",
            "chain": "Arbitrum"
        }
        
        response = self.client.post(
            reverse('delete_wallet'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['result'], "delete wallet success")
        
        # 验证钱包已删除
        self.assertFalse(Wallet.objects.filter(
            device_id="delete_device_id",
            wallet_uuid="delete_wallet_uuid"
        ).exists())
        
    def test_delete_wallet_token(self):
        """测试删除钱包代币"""
        # 创建要删除的代币
        delete_wallet = Wallet.objects.create(
            chain=self.chain,
            device_id="token_device_id",
            wallet_uuid="token_wallet_uuid",
            wallet_name="Token Wallet",
            asset_usd=0.0,
            asset_cny=0.0
        )
        
        delete_wallet_asset = WalletAsset.objects.create(
            wallet=delete_wallet, 
            asset=self.usdt_asset,
            contract_addr="0x000",
            balance=0.0,
            asset_usd=0.0,
            asset_cny=0.0
        )
        
        request_data = {
            "device_id": "token_device_id",
            "wallet_uuid": "token_wallet_uuid",
            "chain": "Arbitrum",
            "symbol": "USDT",
            "contract_addr": "0x000"
        }
        
        response = self.client.post(
            reverse('delete_wallet_token'),
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # 检查响应
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['result'], "delete wallet token success")
        
        # 验证代币已删除
        self.assertFalse(WalletAsset.objects.filter(
            wallet=delete_wallet,
            asset=self.usdt_asset,
            contract_addr="0x000"
        ).exists())
