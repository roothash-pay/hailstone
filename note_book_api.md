## Address note book api module

### 1. add address to note book
- request way: post
- api name: api/add_note_book
- request example
```
{
    "device_id": "test111111111",
    "chain": "Arbitrum",
    "asset": "ETH",
    "memo": "test",
    "address": "0x00000000000000000000000000000004"
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": "add note book success"
}
```


### 2. get adddress list from address book
- request way: post
- api name: api/get_note_book
- request example
```
{
    "device_id": "test111111111",
    "page": 1,
    "page_size": 10
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": {
        "total": 3,
        "data": [
            {
                "id": 3,
                "chain": "Arbitrum",
                "asset": "ETH",
                "device_id": "test111111111",
                "memo": "test",
                "address": "0x00000000000000000000000000000002"
            },
            {
                "id": 2,
                "chain": "Arbitrum",
                "asset": "ETH",
                "device_id": "test111111111",
                "memo": "test",
                "address": "0x00000000000000000000000000000001"
            },
            {
                "id": 1,
                "chain": "Arbitrum",
                "asset": "ETH",
                "device_id": "test111111111",
                "memo": "test",
                "address": "0x00000000000000000000000000000004"
            }
        ]
    }
}
```


### 3. update address book
- request way: post
- api name: api/upd_note_book
- request example
```
{
    "address_id": 3,
    "memo": "0000",
    "address": "0x999999999999999900000000000001"
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": "update note book success"
}
```


### 4. delete address book
- request way: post
- api name: api/add_note_book
- request example
```
{
    "address_id": 3
}
```

response example

```
{
    "ok": true,
    "code": 200,
    "result": "delete note book success"
}
```

