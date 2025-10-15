# Auto Crypto Alert

![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-brightgreen)
![Crypto](https://img.shields.io/badge/Crypto-Alert-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

Welcome to **Auto Crypto Alert**, a cryptocurrency price alert tool based on the CoinMarketCap API.

It pushes notifications to your iPhone via the Bark App, with a volume comparable to a phone ringtone, so you’ll never miss a market move even in your sleep :)

[README 中文版](README.md)

## Features

- Monitor multiple cryptocurrencies
- Custom price trigger rules
- Bark push notifications (iOS only)
- Deployable on Google Cloud Functions or run locally

## Project Structure

```
auto-crypto-alert/
│
├─ launch-version/
│ ├─ main.py
│ ├─ rules.json
│ └─ requirements.txt
├─ local-test_version/
│ ├─ main.py
│ └─ rules.json
├─ README.md
└─ README_EN.md
```

## Prerequisites

- [Python development environment (VScode recommended)](https://wiki.python.org/moin/BeginnersGuideChinese)
- [CoinMarketCap API Key](https://coinmarketcap.com/api/)
- [Bark App Key (generated in Bark App)](https://bark.day.app/#/tutorial)
- [Google Cloud Key](https://cloud.google.com/)

## Usage

1. Install dependencies

Local testing version:

```bash
cd local-test-version
pip install requests
```

Production deployment version:

```bash
cd launch-version
python -m pip install -r requirements.txt
```

2. Configure rules

Edit rules.json to set cryptocurrencies, price thresholds, and Bark configuration:

- [CoinMarketCap API Key](https://coinmarketcap.com/api/)： fill in `coinmarketcap_api_key`

- [Bark App Key](https://bark.day.app/#/tutorial)：fill in `bark_api_key`

- Bark parameters:
  - `sound`: alert sound
  - `level`: notification priority (timeSensitive / critical / default)
  - `group`: group name
- Price rules: `field`: price, `operator`: >= or <=, `target`: target price
- Monitored cryptocurrencies: `symbols`
- Conversion currency: `convert`

**Example configuration**

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

3. Run local test:

```bash
cd local-test-version
python main.py
```

4. Deploy to Google Cloud

- Open [Google Cloud Console](https://console.cloud.google.com/)
- Navigate to Functions → Write a Function
- Fill in basic info:
  Function name: crypto_alert
  Region: select your region
  Trigger: HTTP
  Allow unauthenticated access: checked
  Runtime: Python 3.10 or above
- Upload or paste `main.py`, `requirements.txt`, `rules.json` in the inline editor

- Set function entry point: `crypto_alert`

## Disclaimer

- For technical learning and communication only, **not investment advice**. Please evaluate risks yourself: DO YOUR OWN RESEARCH!

- The project is not fully optimized. After deploying on Google Cloud, if a price crosses the alert threshold, your phone may keep receiving notifications. You need to manually cancel or modify rules in the Google Cloud Console.
