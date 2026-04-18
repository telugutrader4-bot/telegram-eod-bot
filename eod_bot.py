import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@priceactionoptions"

DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")


def get_live_market_data():
    """
    Starter structure for live institutional dashboard.
    We will expand this with full Dhan endpoints.
    """

    headers = {
        "access-token": DHAN_ACCESS_TOKEN,
        "client-id": DHAN_CLIENT_ID,
        "Content-Type": "application/json"
    }

    # Initial structured report (starter production format)
    report = f"""
📊 PRICE ACTION TELUGU
Institutional Smart Money Report

🔥 Top 5 Highest Volume
RELIANCE
SBIN
BEL
TATA MOTORS
IRFC

🟢 Top 5 Highest Delivery %
BEL
IRCTC
HAL
BHEL
COAL INDIA

🔴 Highest Call OI
NIFTY 24500 CE → 1.82 Cr
BANKNIFTY 56000 CE → 95L

🟢 Highest Put OI
NIFTY 24000 PE → 2.10 Cr
BANKNIFTY 55000 PE → 1.12 Cr

🏢 Bulk Deals
RELIANCE
INFY
BEL

🏦 Block Deals
ICICI BANK
TCS
SUNPHARMA

💰 FII / DII
🟢 FII Net Buy → +₹2,350 Cr
🔴 DII Net Sell → -₹1,120 Cr

⚠ For Educational Purposes Only
Price Action Telugu
"""
    return report


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHANNEL_USERNAME,
        "text": message
    }

    response = requests.post(url, data=payload)
    print(response.text)


if __name__ == "__main__":
    message = get_live_market_data()
    send_to_telegram(message)
