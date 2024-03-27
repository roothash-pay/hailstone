# L3质押接口

## 1. 获取支持的链

接口请求
```
curl --location --request POST 'http://127.0.0.1:8000/api/get_staking_chains' \
--data ''
```
返回值

```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "title": "Op",
            "chain_id": "1011",
            "rpc_url": "https://docsend.com/view/um727ucvskffethr",
            "created_at": "2024-03-27 19:59:38"
        },
        {
            "id": 2,
            "title": "zkfair",
            "chain_id": "1011",
            "rpc_url": "https://docsend.com/view/um727ucvskffethr",
            "created_at": "2024-03-27 19:59:47"
        }
    ]
}
```


## 2. 根据链获取策略节点列表

接口请求
```
curl --location 'http://127.0.0.1:8000/api/get_staking_node_list' \
--header 'Content-Type: application/json' \
--data '{
    "chain_id": 2
}'
```
返回值

```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "stategy_name": "Social",
            "node_list": [
                {
                    "id": 2,
                    "chain": "zkfair",
                    "strategy": "Social",
                    "name": "DappLink Node2",
                    "eth_income": "0",
                    "eth_income_rate": "0",
                    "dp_income": "0",
                    "dp_income_rate": "0",
                    "eth_evil": "0",
                    "eth_evil_rate": "0",
                    "dp_evil": "0",
                    "dp_evil_rate": "0",
                    "tvl": "0",
                    "created_at": "2024-03-27 20:01:02"
                }
            ]
        },
        {
            "stategy_name": "Gaming",
            "node_list": [
                {
                    "id": 4,
                    "chain": "zkfair",
                    "strategy": "Gaming",
                    "name": "DappLink Node",
                    "eth_income": "0",
                    "eth_income_rate": "0",
                    "dp_income": "0",
                    "dp_income_rate": "0",
                    "eth_evil": "0",
                    "eth_evil_rate": "0",
                    "dp_evil": "0",
                    "dp_evil_rate": "0",
                    "tvl": "0",
                    "created_at": "2024-03-27 20:01:35"
                }
            ]
        }
    ]
}
```