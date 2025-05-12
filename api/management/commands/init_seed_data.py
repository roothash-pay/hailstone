# api/management/commands/init_seed_data.py
from django.core.management.base import BaseCommand
from django.db import transaction
from market.models import Exchange, Symbol, MarketPrice
from common.models import Asset


class Command(BaseCommand):
    help = 'Populates the database with initial seed data for testing.'

    @transaction.atomic # 确保数据创建在事务中完成
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # --- 创建基础数据 ---
        self.create_base_assets()
        self.create_market_data()

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))

    def create_base_assets(self):
        """创建基础资产数据"""
        self.stdout.write('Creating base assets...')
        # 定义资产及其属性
        assets_data = {
            'USDT': {'mark': 'USDT', 'unit': '6'},
            'BTC': {'mark': 'BTC', 'unit': '8'},
            'ETH': {'mark': 'ETH', 'unit': '18'},
        }
        
        for asset_name, defaults in assets_data.items():
            asset, created = Asset.objects.get_or_create(
                name=asset_name,
                defaults={'mark': defaults['mark'], 'unit': defaults['unit'], 'chain': None} 
            )
            if created:
                self.stdout.write(f'- Created Asset: {asset_name} (Mark: {defaults["mark"]}, Unit: {defaults["unit"]})')
            else:
                self.stdout.write(f'- Asset already exists: {asset_name}')

    def create_market_data(self):
        """创建交易所和市场价格数据"""
        self.stdout.write('Creating market data...')

        # 获取基础资产
        try:
            usdt = Asset.objects.get(name='USDT')
            btc = Asset.objects.get(name='BTC')
            eth = Asset.objects.get(name='ETH')
        except Asset.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Base asset not found, run create_base_assets first. Error: {e}'))
            return

        # 创建交易所
        binance, binance_created = Exchange.objects.get_or_create(
            name='Binance',
            defaults={'market_type': 'Cex', 'status': 'Active'}
        )
        if binance_created: self.stdout.write('- Created Exchange: Binance')

        okx, okx_created = Exchange.objects.get_or_create(
            name='OKX',
            defaults={'market_type': 'Cex', 'status': 'Active'}
        )
        if okx_created: self.stdout.write('- Created Exchange: OKX')

        uniswap, uniswap_created = Exchange.objects.get_or_create(
            name='Uniswap',
            defaults={'market_type': 'Dex', 'status': 'Active'}
        )
        if uniswap_created: self.stdout.write('- Created Exchange: Uniswap')

        # 创建交易对 Symbol
        btc_usdt_symbol, btc_usdt_created = Symbol.objects.get_or_create(
            name='BTC/USDT',
            base_asset=btc,
            quote_asset=usdt,
            defaults={'status': 'Active', 'category': 'Spot'}
        )
        if btc_usdt_created: self.stdout.write('- Created Symbol: BTC/USDT')

        eth_usdt_symbol, eth_usdt_created = Symbol.objects.get_or_create(
            name='ETH/USDT',
            base_asset=eth,
            quote_asset=usdt,
            defaults={'status': 'Active', 'category': 'Spot'}
        )
        if eth_usdt_created: self.stdout.write('- Created Symbol: ETH/USDT')

        # 创建市场价格 MarketPrice
        mp1, mp1_created = MarketPrice.objects.get_or_create(
            exchange=binance,
            symbol=btc_usdt_symbol,
            defaults={
                'base_asset': btc, 'qoute_asset': usdt,
                'sell_price': 65000.50, 'buy_price': 65001.00, 'avg_price': 65000.75,
                'usd_price': 65000.75, 'cny_price': 470000.00, 'margin': 0.15
            }
        )
        if mp1_created: self.stdout.write('- Created MarketPrice: BTC/USDT on Binance')

        mp2, mp2_created = MarketPrice.objects.get_or_create(
            exchange=binance,
            symbol=eth_usdt_symbol,
            defaults={
                'base_asset': eth, 'qoute_asset': usdt,
                'sell_price': 3500.10, 'buy_price': 3500.20, 'avg_price': 3500.15,
                'usd_price': 3500.15, 'cny_price': 25000.00, 'margin': -0.05
            }
        )
        if mp2_created: self.stdout.write('- Created MarketPrice: ETH/USDT on Binance')

        mp3, mp3_created = MarketPrice.objects.get_or_create(
            exchange=okx,
            symbol=btc_usdt_symbol,
            defaults={
                'base_asset': btc, 'qoute_asset': usdt,
                'sell_price': 65010.00, 'buy_price': 65010.80, 'avg_price': 65010.40,
                'usd_price': 65010.40, 'cny_price': 470100.00, 'margin': 0.18
            }
        )
        if mp3_created: self.stdout.write('- Created MarketPrice: BTC/USDT on OKX')