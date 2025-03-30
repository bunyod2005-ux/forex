import pandas as pd
import xgboost as xgb

# Modelni yuklash
model = xgb.XGBClassifier()
model.load_model("xgboost_model.json")

# Yangi ma'lumotlarni yuklash
df = pd.read_csv("XAUUSD_1H_data.csv")
X_new = df[['open', 'high', 'low', 'close', 'tick_volume']].iloc[-1:]  # Oxirgi qiymat

# Signal chiqarish
signal = model.predict(X_new)[0]
if signal == 1:
    print("📈 Signal: XAUUSD - BUY 🟢")
else:
    print("📉 Signal: XAUUSD - SELL 🔴")
import requests

TOKEN = "8012999734:AAGVQl-Cnwvlt08cA3LAQPYMuIVH6Mn-n30"
CHAT_ID = "1753672264"

def send_signal(signal_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": signal_text}
    requests.post(url, data=data)

# Signalni AI modeli orqali bashorat qilish
predicted_signal = "📉 Signal: XAUUSD - SELL 🔴"

# Telegram botga yuborish
send_signal(predicted_signal)
