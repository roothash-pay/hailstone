# api/wallet/utils.py
import logging
from decimal import Decimal, InvalidOperation
from typing import Tuple, Optional, Any

from api.wallet.constants import STABLECOINS, DEFAULT_USD_PRICE, DEFAULT_CNY_PRICE, EXCHANGE_BINANCE
from market.models import MarketPrice, StablePrice, Asset

logger = logging.getLogger(__name__)


def _safe_decimal_conversion(
        raw_value: Any,             # 从数据库获取的原始价格值
        default_value: Decimal,     # 转换失败或原始值为 None 时的回退 Decimal 值
        symbol_for_log: str,        # 用于日志的代币符号
        price_type_for_log: str,    # 用于日志的价格类型 (e.g., "USD", "CNY")
        source_for_log: str         # 用于日志的价格来源 (e.g., "market_price_db", "stable_price_db")
) -> Decimal:
    """Helper to safely convert a raw value to Decimal, with logging and fallback."""
    if raw_value is None:
        return default_value
    try:
        return Decimal(str(raw_value))
    except (InvalidOperation, ValueError, TypeError) as e:
        logger.warning(
            f"Could not convert {price_type_for_log} from {source_for_log} ('{raw_value}') "
            f"to Decimal for symbol '{symbol_for_log}'. Error: {e}. Using default: {default_value}"
        )
        return default_value


def get_asset_prices(symbol: str, asset_obj: Optional[Asset] = None) -> Tuple[Decimal, Decimal]:
    """
    Helper function to get USD and CNY prices for a given symbol.
    Returns (usd_price, cny_price).
    Uses default prices if specific prices are not found or symbol is a stablecoin without specific price.
    Optionally accepts an Asset object to directly use its properties if needed,
    though current logic primarily relies on the symbol string.
    """
    # Initialize with module-level defaults which are already Decimals
    usd_price, cny_price = DEFAULT_USD_PRICE, DEFAULT_CNY_PRICE 

    if symbol not in STABLECOINS:
        symbol_name_pair = f"{symbol}/USDT"  # Example: "ETH/USDT"
        market_price_db = MarketPrice.objects.filter(
            symbol__name=symbol_name_pair,
            exchange__name=EXCHANGE_BINANCE
        ).order_by("-id").first()
        if market_price_db:
            usd_price = _safe_decimal_conversion(
                market_price_db.usd_price, 
                DEFAULT_USD_PRICE, 
                symbol, 
                "USD", 
                "market_price_db"
            )
            cny_price = _safe_decimal_conversion(
                market_price_db.cny_price, 
                DEFAULT_CNY_PRICE, 
                symbol, 
                "CNY", 
                "market_price_db"
            )
    else:  # It's a stablecoin
        stable_price_db = StablePrice.objects.filter(
            asset__name=symbol,  # Assuming StablePrice is linked to Asset by name
        ).order_by("-id").first()
        if stable_price_db:
            usd_price = _safe_decimal_conversion(
                stable_price_db.usd_price, 
                DEFAULT_USD_PRICE, 
                symbol, 
                "USD", 
                "stable_price_db"
            )
            cny_price = _safe_decimal_conversion(
                stable_price_db.cny_price, 
                DEFAULT_CNY_PRICE, 
                symbol, 
                "CNY", 
                "stable_price_db"
            )

    return usd_price, cny_price
