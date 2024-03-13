# 空投接口

## 1. 获取邀请码

接口请求
```
curl --location 'http://127.0.0.1:8000/api/get_invite_code_by_address' \
--header 'Content-Type: application/json' \
--data '{
    "address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F0"
}'
```
返回值

```
{
    "ok": true,
    "code": 200,
    "result": {
        "invite_code": "0000-0000-0000"
    }
}
```


## 2. 提交邀请信息

接口请求
```
curl --location 'http://127.0.0.1:8000/api/submit_invite_info' \
--header 'Content-Type: application/json' \
--data '{
    "invite_code": "0000-0000-0000",
    "address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F1"
}'
```
返回值

```
{
    "ok": true,
    "code": 200,
    "result": {}
}
```


## 3. 获取个人信息和积分

接口请求
```
curl --location 'http://127.0.0.1:8000/api/get_points_by_address' \
--header 'Content-Type: application/json' \
--data '{
    "address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F1"
}'
```
返回值

```
{
    "ok": true,
    "code": 200,
    "result": {
        "id": 5,
        "name": "unknown",
        "photo": "",
        "address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F1",
        "email": null,
        "points": 0,       
        "x_twitter": "",
        "discord": "",
        "telegram": "",
        "info": ""
    }
}
```


## 4. 根据地址获取积分记录

接口请求
```
curl --location 'http://127.0.0.1:8000/api/get_points_record_by_address' \
--header 'Content-Type: application/json' \
--data '{
    "address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F0"
}'
```
返回值

```
{
    "ok": true,
    "code": 200,
    "result": {
        "total": 1,
        "points": [
            {
                "id": 1,
                "name": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F0",
                "type": "BridgeTransfer",
                "points": 1
            }
        ]
    }
}
```

## 5. 获取项目信息

接口请求
```
curl --location --request POST 'http://127.0.0.1:8000/api/get_project_interactions' \
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
            "name": "SavourLabs",
            "describe": "SavourLabsSavourLabsSavourLabsSavourLabs",
            "type": "Project",
            "language": "en",
            "points": 0
        }
    ]
}
```

## 6. 获取问答

接口请求
```
curl --location --request POST 'http://127.0.0.1:8000/api/get_questions' \
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
            "question": "啊啊啊",
            "answer": "a a a",
            "language": "en"
        }
    ]
}
```

