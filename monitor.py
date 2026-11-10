import requests
import time

# =====================================
# CONFIGURATION
# =====================================

BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"

# URL = "https://blinkit.com/prn/sony-playstation-instant-voucher/prid/698593"
URL="https://blinkit.com/prn/blinkit-gift-card/prid/768015"

CHECK_INTERVAL = 60

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

alert_sent = False


# =====================================
# TELEGRAM
# =====================================

def send_telegram(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=15
        )
        print("Telegram sent")

    except Exception as e:
        print("Telegram error:", e)


# =====================================
# STOCK CHECK
# =====================================

def check_stock():
    global alert_sent

    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        print(
            f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Status={response.status_code}"
        )

        if response.status_code != 200:
            return

        page = response.text.upper()

        # Save HTML for debugging
        with open("blinkit_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        out_of_stock_terms = [
            "OUT OF STOCK",
            "SOLD OUT",
            "CURRENTLY UNAVAILABLE",
            "NOT AVAILABLE"
        ]

        stock_terms = [
            "ADD TO CART",
            "BUY NOW"
        ]

        found_out = any(term in page for term in out_of_stock_terms)
        found_stock = any(term in page for term in stock_terms)

        print("Found stock keyword:", found_stock)
        print("Found out-of-stock keyword:", found_out)

        if found_out:
            in_stock = False
        elif found_stock:
            in_stock = True
        else:
            in_stock = False

        if in_stock and not alert_sent:

            send_telegram(
                f"🚨 PSN Voucher Available!\n\n{URL}"
            )

            alert_sent = True
            print("STOCK FOUND")

        elif not in_stock:

            alert_sent = False
            print("No stock detected")

    except Exception as e:
        print("Error:", e)


# =====================================
# START
# =====================================

send_telegram("✅ Blinkit Monitor Started")

while True:
    check_stock()
    time.sleep(CHECK_INTERVAL)
