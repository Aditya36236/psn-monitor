import os
import requests
import time

# =====================================
# CONFIGURATION
# =====================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://blinkit.com/prn/blinkit-gift-card/prid/768015"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


# =====================================
# TELEGRAM
# =====================================

def send_telegram(message):
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=15
        )

        print("Telegram Status:", response.status_code)
        print(response.text)

    except Exception as e:
        print("Telegram Error:", e)


# =====================================
# STOCK CHECK
# =====================================

def check_stock():
    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Status={response.status_code}"
        )

        if response.status_code != 200:
            print("Page not accessible")
            return

        page = response.text.upper()

        stock_terms = [
            "ADD TO CART",
            "BUY NOW"
        ]

        out_of_stock_terms = [
            "OUT OF STOCK",
            "SOLD OUT",
            "CURRENTLY UNAVAILABLE",
            "NOT AVAILABLE"
        ]

        found_stock = any(term in page for term in stock_terms)
        found_out = any(term in page for term in out_of_stock_terms)

        print("Found stock keyword:", found_stock)
        print("Found out-of-stock keyword:", found_out)

        if found_stock and not found_out:
            send_telegram(
                f"🚨 STOCK DETECTED!\n\n{URL}"
            )

            print("Stock Alert Sent")

        else:
            print("No stock detected")

    except Exception as e:
        print("Error:", e)


# =====================================
# RUN ONCE
# =====================================

check_stock()
