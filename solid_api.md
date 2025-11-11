# 1.获取编程语言
 
- 接口参数：无
- 接口请求示范
```
curl --location 'http://127.0.0.1:8000/api/get_languages'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "name": "Solidity",
            "created_at": "2025-11-11 15:10:07"
        }
    ]
}
```
- name: 编程语言名称

# 2. 获取项目类别
- 接口参数：无
- 接口请求示范
```
curl --location 'http://127.0.0.1:8000/api/get_project_type'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "name": "Defi/infra",
            "created_at": "2025-11-11 15:09:33"
        }
    ]
}
```

- name: 名称

# 3. 获取网络列表

- 接口参数：无
- 接口请求示范
```
curl --location 'http://127.0.0.1:8000/api/get_network_list'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": [
        {
            "id": 1,
            "project_type": "Defi/infra",
            "coding_language": "Solidity",
            "name": "RootHash Chain",
            "sub_name": "rhs",
            "icon": "https://hailstone.testnet.dapplink.xyz/media/network/2025/11/11/e0d4d231-fef8-4496-ba17-c495b0b588be.jpeg",
            "detail": "RootHash Chain RootHash Chain RootHash ChainRootHash ChainRootHash ChainRootHash ChainRootHash Chain",
            "created_at": "2025-11-11 15:11:04"
        }
    ]
}
```

- name: 名称


# 4. 获取项目信息

- 接口参数：
  - service_type_id 传 0 返回全部项目信息，传对应项目 id 返回项目信息
  - status：传 all 返回所用项目信息， 传人 Ongoing 返回正在进行中的项目
- 接口请求示范
```
curl --location 'http://127.0.0.1:8089/api/get_audit_projects' \
--header 'Content-Type: application/json' \
--data '{
    "language_id": 1,
    "project_type_id": 1,
    "network_id": 1,
    "status": "Ongoing"
}'
```
- 接口返回值
```
{
    "ok": true,
    "code": 200,
    "result": {
        "total": 1,
        "projects": [
            {
                "id": 1,
                "project_type": "Defi/infra",
                "coding_language": "Solidity",
                "network": "RootHash Chain",
                "name": "TheWeb3",
                "start_time": "2025-10-11",
                "end_time": "2025-10-21",
                "cycle": "10 天",
                "photo": "https://hailstone.testnet.dapplink.xyz/media/audit/2025/11/11/e0d4d231-fef8-4496-ba17-c495b0b588be.jpeg",
                "bounty_fund": "unknown",
                "status": "Ongoing",
                "project_link": "https://web3-security-labs.vercel.app/community",
                "detail": "unknown",
                "report_link": "https://web3-security-labs.vercel.app/community",
                "x_link": "https://web3-security-labs.vercel.app/community",
                "telegram": "https://web3-security-labs.vercel.app/community",
                "discord": "https://web3-security-labs.vercel.app/community",
                "github": "https://web3-security-labs.vercel.app/community",
                "community_link": "https://web3-security-labs.vercel.app/community",
                "bounty_description": "101010101101010",
                "created_at": "2025-11-11 15:15:43"
            }
        ]
    }
}
```
- name: 项目名称
- photo：项目头像
- status：项目状态
- project_link：项目 github 链接
- detail：项目详解介绍
- report_link：项目审计报告链接

# 5. 获取排行榜

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

# 6.提交项目信息

```
http://127.0.0.1:8000/api/create_audit_project
```
- request
```
{
    "name": "DappLink Smart Contract Audit",
    "project_type_id": 1,
    "coding_language_id": 1,
    "network_id": 1,
    "user_id": 2,
    "start_time": "2025-11-11",
    "end_time": "2025-11-20",
    "cycle": "9 days",
    "status": "Ongoing",
    "detail": "Smart contract security audit for Layer2 bridge",
    "bounty_fund": "5000 USDT",
    "project_link": "https://dapplink.xyz",
    "report_link": "https://dapplink.xyz/report.pdf",
    "x_link": "https://x.com/dapplink",
    "telegram": "https://t.me/dapplink",
    "discord": "https://discord.gg/dapplink",
    "github": "https://github.com/dapplink",
    "community_link": "https://community.dapplink.xyz",
    "bounty_description": "Top 3 auditors will share the reward pool"
}
```

- response
```
{
    "ok": true,
    "code": 200,
    "result": {
        "id": 2,
        "project_type": "Defi/infra",
        "coding_language": "Solidity",
        "network": "RootHash Chain",
        "name": "DappLink Smart Contract Audit",
        "start_time": "2025-11-11",
        "end_time": "2025-11-20",
        "cycle": "9 days",
        "photo": "https://hailstone.testnet.dapplink.xyz/media/",
        "bounty_fund": "5000 USDT",
        "status": "Ongoing",
        "project_link": "https://dapplink.xyz",
        "detail": "Smart contract security audit for Layer2 bridge",
        "report_link": "https://dapplink.xyz/report.pdf",
        "x_link": "https://x.com/dapplink",
        "telegram": "https://t.me/dapplink",
        "discord": "https://discord.gg/dapplink",
        "github": "https://github.com/dapplink",
        "community_link": "https://community.dapplink.xyz",
        "bounty_description": "Top 3 auditors will share the reward pool",
        "created_at": "2025-11-11 15:42:33"
    }
```

# 7.咨询项目

- http://127.0.0.1:8000/api/submit_ask_audit

- request
```
{
  "name": "Alice",
  "contact": "alice@example.com",
  "company": "CertiK",
  "completed_time": "2025-12-01",
  "repo_link": "https://github.com/example/project",
  "detail": "审计 ERC20 合约",
  "ecosystem": "Ethereum",
  "find_us_way": "通过朋友推荐",
  "images": "audit1.png"
}
```

- reponse 

```
{
    "ok": true,
    "code": 200,
    "result": {
        "id": 1,
        "name": "Alice",
        "repo_link": "https://github.com/example/project"
    }
}
```
