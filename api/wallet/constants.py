from decimal import Decimal

EXCHANGE_BINANCE = "binance"

NETWORK_MAINNET = "mainnet"
NETWORK_TESTNET = "testnet"
STABLECOINS = ["USDT", "USDC", "DAI"]

# Default error codes specific to wallet API operations
DEFAULT_RPC_ERROR_CODE = 5003
DEFAULT_CLIENT_ERROR_CODE = 4000
DEFAULT_SERVER_ERROR_CODE = 5000

# Default prices, consider if these should be more configurable or app-level settings
DEFAULT_USD_PRICE = Decimal('1.0')
DEFAULT_CNY_PRICE = Decimal('7.0')

# Wallet specific constants
ADDRESS_CONTRACT_DEFAULT = "0x00"
GET_BALANCE_DEFAULT_INDEX = "0" 