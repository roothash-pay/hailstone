### 1. get exchange by exchange types
- request way: post
- api name: api/get_exchanges
- request example
```
{
   "type": "Cex",    Cex: central exchange; Dex: dex
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "name": "binance",
            "market_type": "Cex",
            "status": "Active"
        },
        {
            "id": 2,
            "name": "okex",
            "market_type": "Cex",
            "status": "Active"
        }
    ]
}
```


### 2. get exchange markets
- request way: post
- api name: api/get_exchange_market
- request example
```
{
   "exchange_id": 1,
   "device_id": 0
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "symbol": "ETH/USDT",
            "base_asset": "USDT",
            "qoute_asset": "ETH",
            "sell_price": "1323.0200",
            "buy_price": "1323.0300",
            "avg_price": "1323.0250",
            "usd_price": "1323.0250",
            "cny_price": "9234.7145",
            "margin": "0.23"
        },
        {
            "id": 3,
            "symbol": "BTC/USDT",
            "base_asset": "USDT",
            "qoute_asset": "BTC",
            "sell_price": "19331.0800",
            "buy_price": "19331.7200",
            "avg_price": "19331.4000",
            "usd_price": "19331.4000",
            "cny_price": "134933.1720",
            "margin": "0.23"
        }
    ]
}
```

### 3. add favorite market
- request way: post
- api name: api/add_favorite_market
- request example
```
{
   "device_id": "00000",
   "market_id": 2
}
```

response example

```
{
    "ok": false,
    "code": 4000,
    "msg": "no this market_price"
}
```
