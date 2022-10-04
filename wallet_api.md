## Wallet api module

### 1. query balance by address 
- request way: post
- api name: api/get_balance
- request example
```
{
    "chain": "eth",
    "symbol": "eth",
    "network": "mainnet",
    "address": "0x98E9D288743839e96A8005a6B51C770Bbf7788C0",
    "contract_address": ""
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": {
        "balance": "3.943168895484885777",
        "usdt_price": "5216.911027948891005115425000",
        "cny_price": "36414.03897508326143810720135"
    }
}
```


### 2. query balance by wallet 
- request way: post
- api name: api/get_balance
- request example
```
{
    "device_id": "100220112ea",
    "wallet_uuid": "20122310101",
    "chain": "Ethereum"
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": {
        "total_asset": 1000000,
        "coin_asset": [
            {
                "id": 1,
                "chain": "Ethereum",
                "symbol": "ETH",
                "icon": "",
                "network": "mainnet",
                "device_id": "100220112ea",
                "wallet_uuid": "20122310101",
                "wallet_name": "savour",
                "address": "0xECF09D36f07EC396f97DD448D9E4bcb19fE4Ec3A",
                "contract_addr": "",
                "usdt_price": "2.646050000000000000000000000E-15",
                "cny_price": "1.846942900000000112721600000E-14",
                "balance": "2.000000000000E-18"
            },
            {
                "id": 2,
                "chain": "Ethereum",
                "symbol": "USDT",
                "icon": "",
                "network": "mainnet",
                "device_id": "100220112ea",
                "wallet_uuid": "20122310101",
                "wallet_name": "savour",
                "address": "0xECF09D36f07EC396f97DD448D9E4bcb19fE4Ec3A",
                "contract_addr": "0xECF09D36f07EC396f97DD448D9E4bcb19fE4Ec3A",
                "usdt_price": "0.0001000000000000000000000000000",
                "cny_price": "0.0007100000000000000000000000000",
                "balance": "0.000100000000000000000000000000"
            }
        ]
    }
}
```



