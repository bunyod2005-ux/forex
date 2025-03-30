import requests  

# Telegram ma'lumotlari  
TOKEN = "8012999734:AAGVQl-Cnwvlt08cA3LAQPYMuIVH6Mn-n30"  # O'z tokeningizni yozing  
CHAT_ID = "1753672264"  # O'z chat ID'ingizni yozing  

# Signalni yuborish funksiyasi  
def send_signal(signal_text):  
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"  
    data = {"chat_id": CHAT_ID, "text": signal_text}  
    requests.post(url, json=data)  

# Foydalanish  
send_signal("📈 Signal: XAUUSD - BUY 🟢")  
import requests

# Telegram ma'lumotlari
TOKEN = "8012999734:AAGVQl-Cnwvlt08cA3LAQPYMuIVH6Mn-n30"
CHAT_ID = "1753672264"

# Signal yuborish funksiyasi
def send_signal(signal_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": signal_text}
    requests.post(url, data=data)

# Test qilish uchun
send_signal("📉 Signal: XAUUSD - SELL 🔴")
import requests
import schedule
import time

# 🔹 Telegram ma'lumotlari
TOKEN = "8012999734:AAGVQl-Cnwvlt08cA3LAQPYMuIVH6Mn-n30"  # Bot tokeningizni shu joyga qo'ying
CHAT_ID = "1753672264"  # Chat ID ni shu joyga qo'ying

# 🔹 Signal yuborish funksiyasi
def send_signal(signal_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": signal_text}
    requests.post(url, data=data)

# 🔹 Signal bashorati (bu joyga modelingizdan signal qo'shishingiz mumkin)
def predict_signal():
    # Bu joyda AI modeli yoki boshqa tizimdan signal olinadi
    predicted_signal = "📉 Signal: XAUUSD - SELL 🔴"
    return predicted_signal

# 🔹 Avtomatik signal yuborish funksiyasi
def run_bot():
    signal = predict_signal()
    send_signal(signal)
    print(f"✅ Yuborildi: {signal}")

# 🔹 Har 1 soatda ishlashga sozlash
schedule.every(1).hours.do(run_bot)

# 🔹 Botni doimiy ishlatish
print("🚀 Telegram bot ishga tushdi...")
while True:
    schedule.run_pending()
    time.sleep(1)
