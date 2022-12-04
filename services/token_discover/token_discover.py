from services.token_discover.scan import *

token_discover_list = [
    EthScan,
    PolygonScan,
    Optimism,
    Arbi,
]

token_discover_container = {}

for token_scan in token_discover_list:
    scan = token_scan()
    token_discover_container[scan.chain] = scan
