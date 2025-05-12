# api/tests/test_market_api.py
# Tests for Market related APIs (/api/get_exchanges, /api/get_exchange_market, etc.)
from django.core.management import call_command
from django.test import TestCase, Client
import json

from market.models import Exchange, MarketPrice, FavoriteMarket


class TestConfig:
    PRINT_TEST_RESULTS = True  # 控制是否打印测试结果


def print_test_result(test_name, data):
    if TestConfig.PRINT_TEST_RESULTS:
        print(f"\n=== Test Result: {test_name} ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))


# --- 市场 API 测试 ---
class MarketAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Setting up test data for MarketAPITests...")
        try:
            # 执行 init_seed_data 命令来创建测试数据
            call_command('init_seed_data')
            # 获取一个确定的 MarketPrice ID 用于测试收藏功能
            cls.btc_market_on_binance = MarketPrice.objects.get(
                exchange__name='Binance',
                symbol__name='BTC/USDT'
            )
        except Exception as e:
            raise Exception(f"Error during setUpTestData: {e}")

    def setUp(self):
        self.client = Client()
        self.test_device_id = "test_device_fav_123"  # 定义一个测试用的设备 ID
        # 清理可能残留的收藏数据，确保测试隔离
        FavoriteMarket.objects.filter(device_id=self.test_device_id).delete()

    def test_get_exchanges_success_all(self):
        """测试成功获取所有类型的交易所 (POST /api/get_exchanges)"""
        url = '/api/get_exchanges'
        # 不带 type 参数，应该返回所有
        response = self.client.post(url, data={}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_get_exchanges_success_all', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        results = data.get('result', [])
        self.assertTrue(len(results) >= 3)  # 基于 init_seed_data 创建了 Binance, OKX, Uniswap

        # 检查返回的数据是否包含预期的交易所名称
        exchange_names = [item['name'] for item in results]
        self.assertIn('Binance', exchange_names)
        self.assertIn('OKX', exchange_names)
        self.assertIn('Uniswap', exchange_names)

        # 检查返回的数据结构是否符合预期 (抽查一个)
        binance_data = next((item for item in results if item['name'] == 'Binance'), None)
        self.assertIsNotNone(binance_data)
        self.assertEqual(binance_data['market_type'], 'Cex')
        self.assertEqual(binance_data['status'], 'Active')

    def test_get_exchanges_success_cex(self):
        """测试成功获取 Cex 类型的交易所 (POST /api/get_exchanges)"""
        url = '/api/get_exchanges'
        payload = {'type': 'Cex'}
        response = self.client.post(url, data=payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_get_exchanges_success_cex', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        results = data.get('result', [])
        self.assertTrue(len(results) >= 2)  # Binance, OKX

        exchange_names = [item['name'] for item in results]
        self.assertIn('Binance', exchange_names)
        self.assertIn('OKX', exchange_names)
        self.assertNotIn('Uniswap', exchange_names)
        for item in results:
            self.assertEqual(item['market_type'], 'Cex')

    def test_get_exchanges_success_dex(self):
        """测试成功获取 Dex 类型的交易所 (POST /api/get_exchanges)"""
        url = '/api/get_exchanges'
        payload = {'type': 'Dex'}
        response = self.client.post(url, data=payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_get_exchanges_success_dex', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        results = data.get('result', [])
        self.assertTrue(len(results) >= 1)  # Uniswap

        exchange_names = [item['name'] for item in results]
        self.assertNotIn('Binance', exchange_names)
        self.assertNotIn('OKX', exchange_names)
        self.assertIn('Uniswap', exchange_names)
        for item in results:
            self.assertEqual(item['market_type'], 'Dex')

    def test_get_exchange_market_success(self):
        """测试获取交易所的市场列表 (POST /api/get_exchange_market)"""
        url = '/api/get_exchange_market'

        try:
            binance = Exchange.objects.get(name='Binance')
        except Exchange.DoesNotExist:
            self.fail("Seeding failed: Binance exchange not found.")  # 如果种子数据没创建，测试失败

        # exchange_id 和 device_id 二选一传入，优先使用exchange_id
        payload = {'exchange_id': binance.id, 'device_id': 'test_device'}
        response = self.client.post(url, data=payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_get_exchange_market_success', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        results = data.get('result', [])
        # 基于 init_seed_data 创建了 BTC/USDT, ETH/USDT on Binance
        self.assertTrue(len(results) >= 2, f"Expected at least 2 results, got {len(results)}")

        symbols = [item['symbol'] for item in results]
        self.assertIn('BTC/USDT', symbols)
        self.assertIn('ETH/USDT', symbols)

        # 抽查一个结果的详细数据
        btc_market = next((item for item in results if item['symbol'] == 'BTC/USDT'), None)
        self.assertIsNotNone(btc_market)
        self.assertEqual(btc_market['exchange'], 'Binance')  # 确认交易所名称正确
        self.assertEqual(btc_market['base_asset'], 'BTC')
        self.assertEqual(btc_market['qoute_asset'], 'USDT')
        self.assertEqual(btc_market['sell_price'], '65000.5000')  # 注意格式化后的精度
        # 也可以进一步检查其他价格和 margin

    def test_add_favorite_market_success(self):
        """测试成功添加收藏 (POST /api/add_favorite_market)"""
        url = '/api/add_favorite_market'
        payload = {
            'device_id': self.test_device_id,
            'market_id': self.btc_market_on_binance.id
        }
        response = self.client.post(url, data=payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_add_favorite_market_success', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        self.assertEqual(data.get('result'), "add favorite market price success")  # 根据 API 实现调整断言

        # 验证数据库中是否真的添加了记录
        is_favorited = FavoriteMarket.objects.filter(
            device_id=self.test_device_id,
            market_price=self.btc_market_on_binance
        ).exists()
        print_test_result('valid_add_favorite_market', is_favorited)
        self.assertTrue(is_favorited, "FavoriteMarket record was not created in the database.")

    def test_add_favorite_market_duplicate_fails(self):
        """测试重复添加收藏会失败 (POST /api/add_favorite_market)"""
        url = '/api/add_favorite_market'
        payload = {
            'device_id': self.test_device_id,
            'market_id': self.btc_market_on_binance.id
        }

        # 第一次调用 (应该成功)
        response1 = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        self.assertTrue(response1.json().get('ok'))

        # 第二次调用 (应该失败)
        response2 = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response2.status_code, 200)  # API 设计返回 200 但 ok=false
        data = response2.json()
        print_test_result('test_add_favorite_market_duplicate_fails', data)
        self.assertFalse(data.get('ok'))
        self.assertEqual(data.get('code'), 4000)
        self.assertEqual(data.get('msg'), "You have already add this market price")  # 修正：检查 msg 字段

        # 验证数据库中只有一条记录
        count = FavoriteMarket.objects.filter(
            device_id=self.test_device_id,
            market_price=self.btc_market_on_binance
        ).count()
        self.assertEqual(count, 1, "Duplicate FavoriteMarket record was created.")

    def test_remove_favorite_market_success(self):
        """测试成功移除收藏 (POST /api/remove_favorite_market)"""
        # 1. 先添加一个收藏确保它存在
        FavoriteMarket.objects.create(
            device_id=self.test_device_id,
            market_price=self.btc_market_on_binance
        )
        self.assertTrue(FavoriteMarket.objects.filter(device_id=self.test_device_id).exists(),
                        "Setup failed: Favorite was not created.")

        # 2. 调用移除 API
        url = '/api/remove_favorite_market'
        payload = {
            'device_id': self.test_device_id,
            'market_id': self.btc_market_on_binance.id
        }
        response = self.client.post(url, data=payload, content_type='application/json')

        # 3. 验证 API 响应
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_remove_favorite_market_success', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        self.assertEqual(data.get('result'), "remove market price success")

        # 4. 验证数据库记录已被删除
        exists_after_remove = FavoriteMarket.objects.filter(
            device_id=self.test_device_id,
            market_price=self.btc_market_on_binance
        ).exists()
        self.assertFalse(exists_after_remove, "FavoriteMarket record was not deleted from the database.")

    def test_remove_favorite_market_nonexistent_is_ok(self):
        """测试移除不存在的收藏也返回成功 (POST /api/remove_favorite_market)"""
        # 1. 确保收藏不存在 (setUp 中已清理)
        self.assertFalse(FavoriteMarket.objects.filter(device_id=self.test_device_id).exists(),
                         "Test setup failed: Favorite exists unexpectedly.")

        # 2. 调用移除 API
        url = '/api/remove_favorite_market'
        payload = {
            'device_id': self.test_device_id,
            'market_id': self.btc_market_on_binance.id  # 使用一个有效的 market_id
        }
        response = self.client.post(url, data=payload, content_type='application/json')

        # 3. 验证 API 响应 (根据 API 实现，即使没删东西也返回成功)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print_test_result('test_remove_favorite_market_nonexistent_is_ok', data)
        self.assertTrue(data.get('ok'))
        self.assertEqual(data.get('code'), 200)
        self.assertEqual(data.get('result'), "remove market price success")

        # 4. 验证数据库状态未改变 (仍然不存在)
        exists_after_remove = FavoriteMarket.objects.filter(
            device_id=self.test_device_id,
            market_price=self.btc_market_on_binance
        ).exists()
        self.assertFalse(exists_after_remove, "FavoriteMarket record appeared unexpectedly after remove call.")
