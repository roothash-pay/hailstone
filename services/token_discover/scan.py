from services.token_discover.base_scan import EtherScan


class EthScan(EtherScan):
    def __init__(self):
        super().__init__()
        self.scan_url = 'https://etherscan.io/address/'
        self.chain = 'ETH'
        self.header = {
            'authority': 'etherscan.io',
        }


class PolygonScan(EtherScan):
    def __init__(self):
        super().__init__()
        self.scan_url = 'https://polygonscan.com'
        self.chain = 'Polygon'
        self.header = {
            'authority': 'polygonscan.com',
        }


class Optimism(EtherScan):
    def __init__(self):
        super().__init__()
        self.scan_url = 'https://optimistic.etherscan.io'
        self.chain = 'Optimism'
        self.header = {
            'authority': 'optimistic.etherscan.io',
        }


class Arbi(EtherScan):
    def __init__(self):
        super().__init__()
        self.scan_url = 'https://arbiscan.io'
        self.chain = 'Arbi'
        self.header = {
            'authority': 'arbiscan.io',
        }
