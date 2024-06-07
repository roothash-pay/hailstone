# 1. 获取服务类别接口
 
- 接口参数：无
- 接口请求示范
```
curl --location 'http://127.0.0.1:8089/api/get_services_type'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "name": "编辑用户资料",
            "icon": "https://hailstone.testnet.dapplink.xyz/media/icon/2024/06/07/600x200.jpeg",
            "detail": "编辑用户资料编辑用户资料编辑用户资料",
            "created_at": "2024-06-07 14:49:28"
        }
    ]
}
```
- name: 服务名称
- icon: 服务的图标
- detail：服务描述

# 2. 获取服务类别接口

- 接口参数：无
- 接口请求示范
```
curl --location 'http://127.0.0.1:8089/api/get_core_members'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "name": "seek",
            "photo": "https://hailstone.testnet.dapplink.xyz/media/member/2024/06/07/20240605-144519.jpeg",
            "detail": "Mantle DA 架构师",
            "created_at": "2024-06-07 14:53:25"
        }
    ]
}
```

- name: 姓名
- photo：头像
- detail：详解介绍

# 3. 获取项目信息

- 接口参数：
  - service_type_id 传 0 返回全部项目信息，传对应项目 id 返回项目信息
  - status：传 all 返回所用项目信息， 传人 Ongoing 返回正在进行中的项目
- 接口请求示范
```
curl --location 'http://127.0.0.1:8089/api/get_audit_projects' \
--header 'Content-Type: application/json' \
--data '{
    "service_type_id": 1,
    "status": "all"
}'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "name": "DappLink Bridge",
            "photo": "https://hailstone.testnet.dapplink.xyz/media/audit/2024/06/07/20240531-180630.jpeg",
            "status": "Ongoing",
            "project_link": "http://127.0.0.1:8089/admin/solid/auditproject/add/",
            "detail": "DappLink BridgeDappLink BridgeDappLink BridgeDappLink BridgeDappLink Bridge",
            "report_link": "http://127.0.0.1:8089/admin/solid/auditproject/add/",
            "created_at": "2024-06-07 14:57:22"
        }
    ]
}
```
- name: 项目名称
- photo：项目头像
- status：项目状态
- project_link：项目 github 链接
- detail：项目详解介绍
- report_link：项目审计报告链接

# 4. 获取排行榜

- 接口参数：无
- 接口请求示范
```
curl --location 'http://127.0.0.1:8089/api/get_leadboard_list' \
--data ''
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 3,
            "competitor": "seek01",
            "payouts": "20",
            "solo": "0",
            "high": "0",
            "med": "0",
            "solo_high": "0",
            "solo_med": "0",
            "first_place": "0",
            "created_at": "2024-06-07 15:01:28"
        },
        {
            "id": 4,
            "competitor": "seek02",
            "payouts": "1000",
            "solo": "0",
            "high": "0",
            "med": "0",
            "solo_high": "0",
            "solo_med": "0",
            "first_place": "0",
            "created_at": "2024-06-07 15:01:37"
        },
        {
            "id": 2,
            "competitor": "seek",
            "payouts": "10",
            "solo": "0",
            "high": "0",
            "med": "0",
            "solo_high": "0",
            "solo_med": "0",
            "first_place": "0",
            "created_at": "2024-06-07 15:01:20"
        }
    ]
}
```