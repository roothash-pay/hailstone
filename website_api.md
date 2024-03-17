# 网站接口

## 1. 获取博客类别

请求示范
```
curl --location --request POST 'http://127.0.0.1:8000/api/get_blog_cat_list' \
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
            "name": "web3"
        },
        {
            "id": 2,
            "name": "ecosystem"
        }
    ]
}
```

## 2. 获取博客列表

请求示范
```
curl --location 'http://127.0.0.1:8000/api/get_blog_list' \
--header 'Content-Type: application/json' \
--data '{
    "cat_id": 2,
    "page": 1,
    "page_size": 10
}'
```
返回值
```
{
    "ok": true,
    "code": 200,
    "result": {
        "total": 1,
        "blog_list": [
            {
                "id": 1,
                "title": "unknown",
                "cat_name": "unknown",
                "image": "blog/2024/03/17/1280X1280.JPEG",
                "describe": "10DP once,  max 10000DP",
                "link_url": "dapplink protobuf protobufprotobufprotobuf",
                "tags": "hhhh",
                "created_at": "2024-03-17 18:44:53"
            }
        ]
    }
}
```


## 3. 获取事件列表

请求示范
```
curl --location 'http://127.0.0.1:8000/api/get_forum_list' \
--header 'Content-Type: application/json' \
--data '{
    "page": 1,
    "page_size": 10
}'
```
返回值
```
{
    "ok": true,
    "code": 200,
    "result": {
        "total": 1,
        "forum_list": [
            {
                "id": 1,
                "name": "Execute transactions on the testnet cross-chain bridge",
                "link": "dapplink protobuf protobufprotobufprotobuf",
                "describe": "10DP once,  max 10000DP",
                "created_at": "2024-03-17 18:44:04"
            }
        ]
    }
}
}
```


## 4. 获取 forum 列表

请求示范
```
curl --location 'http://127.0.0.1:8000/api/get_forum_list' \
--header 'Content-Type: application/json' \
--data '{
    "page": 1,
    "page_size": 10
}'
```
返回值
```
{
    "ok": true,
    "code": 200,
    "result": {
        "total": 1,
        "forum_list": [
            {
                "id": 1,
                "title": "dapplink protobuf protobufprotobufprotobuf",
                "link": "dapplink protobuf protobufprotobufprotobuf",
                "describe": "dapplink protobuf protobufprotobufprotobuf",
                "created_at": "2024-03-17 18:43:51"
            }
        ]
    }
}
```

