import requests
import urllib.parse
import json

# ===================== CONFIG =====================
CONFIG_PATH = "rules.json"  # JSON file with API keys and rules


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ===================== Bark Notifier =====================
class BarkNotifier:
    def __init__(self, bark_api_key, server="https://api.day.app"):
        self.key = bark_api_key
        self.server = server.rstrip("/")

    def send(self, title, body="", **kwargs):
        # Construct URL and send GET request
        params = "&".join(
            [f"{k}={urllib.parse.quote(str(v))}" for k, v in kwargs.items()]
        )
        title_enc = urllib.parse.quote(title)
        body_enc = urllib.parse.quote(body)
        url = f"{self.server}/{self.key}/{title_enc}/{body_enc}?{params}"
        print("Sending request to:", url)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print("✅ Bark push succeeded!")
            else:
                print(f"⚠️ Push failed, HTTP status code: {r.status_code}")
        except Exception as e:
            print(f"❌ Network error: {e}")


# ===================== Fetch Prices =====================
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


def fetch_prices(symbols, convert, api_key):
    # Real API call to CoinMarketCap
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    params = {"symbol": ",".join(symbols), "convert": convert}
    try:
        resp = requests.get(CMC_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", {})
    except Exception as e:
        print("CMC API request error:", e)
        return {}


# ===================== Check Conditions =====================
def check_conditions(prices, rules, convert):
    alerts = []
    for symbol, rule_list in rules.items():
        if symbol not in prices:
            continue
        quote = prices[symbol]["quote"].get(convert, {})
        for rule in rule_list:
            field = rule["field"]
            operator = rule["operator"]
            target = rule["target"]
            value = quote.get(field)
            if value is None:
                continue
            triggered = False
            if operator == ">=" and value >= target:
                triggered = True
            elif operator == "<=" and value <= target:
                triggered = True
            if triggered:
                alert_msg = (
                    f"{symbol} ALERT!\n"
                    f"Field: {field}\n"
                    f"Current Value: {value}\n"
                    f"Condition: {field} {operator} {target}"
                )
                alerts.append(alert_msg)
    return alerts


# ===================== Run Alert =====================
def run_alert():
    CONFIG = load_config()
    bark = BarkNotifier(CONFIG["bark"]["bark_api_key"], CONFIG["bark"]["server"])
    prices = fetch_prices(
        CONFIG["symbols"], CONFIG["convert"], CONFIG["coinmarketcap_api_key"]
    )
    if prices:
        alerts = check_conditions(prices, CONFIG["rules"], CONFIG["convert"])
        for msg in alerts:
            bark.send(
                title="Crypto Alert 🚨",
                body=msg,
                sound=CONFIG["bark"]["sound"],
                level=CONFIG["bark"]["level"],
                group=CONFIG["bark"]["group"],
                call=CONFIG["bark"]["call"],
            )
        return f"{len(alerts)} alert(s) sent"
    else:
        return "No price data received"


# ===================== Local Test =====================
if __name__ == "__main__":
    print(run_alert())
