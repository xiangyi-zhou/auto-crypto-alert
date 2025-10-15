# Auto Crypto Alert

![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-brightgreen)
![Crypto](https://img.shields.io/badge/Crypto-Alert-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

作为散户韭菜和技术极客，尤其是经过 2025 年 10 月 11 日币圈的黑天鹅事件之后，你是否想要免费拥有自己的加密货币预警系统？

欢迎使用 Auto Crypto Alert ，这是一个基于 CoinMarketCap API 的加密货币价格自动提醒工具，通过 Bark App 推送到手机，音量堪比电话铃声，让你不会再在睡梦中错过行情 :)

[README (English Version）](README_EN.md)

## 功能

- 多币种行情监控
- 自定义价格触发规则
- Bark 手机推送（仅支持 IOS）
- 可部署在 Google Cloud Functions 或本地运行

## 项目结构

```
auto-crypto-alert/
│
├─ launch-version/           # 正式部署版本
│   ├─ main.py               # 主程序入口
│   ├─ rules.json            # JSON 文件存放预警规则和 Key
│   └─ requirements.txt      # 部署依赖
├─ local-test_version/       # 本地测试版本
│   ├─ main.py               # 主程序入口
│   └─ rules.json            # JSON 文件存放预警规则和 Key
├─ README.md                 # 中文 README
└─ README_EN.md              # 英文 README
```

## 需要准备什么

- [Python 开发环境（推荐 VScode）](https://wiki.python.org/moin/BeginnersGuideChinese)
- [CoinMarketCap API Key](https://coinmarketcap.com/api/)
- [Bark App Key（在 Bark App 中生成）](https://bark.day.app/#/tutorial)
- [Google Cloud Key](https://cloud.google.com/)

## 使用说明

1. 安装依赖

本地测试版本：

```bash
cd local-test-version
pip install requests
```

正式部署版本：

```bash
cd launch-version
python -m pip install -r requirements.txt
```

2. 配置规则

编辑“rules.json”，设置币种、价格阈值和 Bark 配置:

- [CoinMarketCap API Key](https://coinmarketcap.com/api/)：填 `coinmarketcap_api_key`
- [Bark App Key（在 Bark App 中生成）](https://bark.day.app/#/tutorial)：填 `bark_api_key`
- Bark 参数：
  - `sound`：提醒音
  - `level`：通知优先级（timeSensitive / critical / default）
  - `group`：分组名称
- 价格规则：`field`:price，`operator`: >= 或 <=，`target` : 目标价格
- 监控币种：`symbols`
- 转换币种：`convert`

**配置示例**

```json
  "rules": {
    "BTC": [
      {"field": "price", "operator": ">=", "target": 120000},
      {"field": "price", "operator": "<=", "target": 109407}
    ],
    "ETH": [
      {"field": "price", "operator": ">=", "target": 4000},
      {"field": "price", "operator": "<=", "target": 3500}
    ]
  }
```

3. 本地测试：

```bash
cd local-test-version
python main.py
```

4. 部署到 Google Cloud

## 严正声明

- 仅供技术交流学习，不构成任何投资建议，请自行判断风险 DO YOUR OWN RESEARCH!
- 该项目功能设计目前还不完善，部署到 Google Cloud 之后，如果币价突破预警价格，手机会持续收到提醒，需要在 Google Cloud 控制台手动取消或修改规则
- 该项目会用到多个可能会收费的 API，不要泄露自己的 key，注意使用额度，不要超过免费额度
