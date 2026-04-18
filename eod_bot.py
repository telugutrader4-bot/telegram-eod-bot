import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@priceactionoptions"

def get_eod_data():
    return {
        "high": [
            "HDFC Bank",
            "TCS",
            "BEL"
        ],
        "low": [
            "Paytm",
            "Vodafone Idea"
        ],
        "bulk": [
            "Reliance",
            "Infosys"
        ],
        "block": [
            "ICICI Bank"
        ],
        "delivery": [
            "BEL",
            "IRCTC",
            "BHEL"
        ],
        "fii_dii": [
            "FII Net Buy",
            "DII Net Sell"
        ]
    }

def format_message(data):
    msg = "📊 EOD Market Update\n\n"

    msg += "52W High:\n"
    for item in data["high"]:
        msg += f"{item}\n"

    msg += "\n52W Low:\n"
    for item in data["low"]:
        msg += f"{item}\n"

    msg += "\nBulk Deals:\n"
    for item in data["bulk"]:
        msg += f"{item}\n"

    msg += "\nBlock Deals:\n"
    for item in data["block"]:
        msg += f"{item}\n"

    msg += "\nTop Delivery %:\n"
    for item in data["delivery"]:
        msg += f"{item}\n"

    msg += "\nFII / DII:\n"
    for item in data["fii_dii"]:
        msg += f"{item}\n"

    msg += "\n\nSource: Public Market Data"

    return msg

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)

if __name__ == "__main__":
    data = get_eod_data()
    message = format_message(data)
    send_telegram(message)
