import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import telegram

# Telegram bot token va chat ID
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Sizning bot tokeningiz
CHAT_ID = 'YOUR_CHAT_ID'  # Sizning chat ID

# Telegram botni yaratish
bot = telegram.Bot(token=TOKEN)

# Ma'lumotlarni yuklash
data = pd.read_csv('XAUUSD_signals.csv')

# Signal uchun xususiyatlarni tanlash (MA_50, MA_200, close narx)
X = data[['MA_50', 'MA_200', 'close']]
y = data['Signal']

# Ma'lumotlarni o‘qitish va test qilish uchun ajratish
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modelini yaratish
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Modelni test qilish
y_pred = model.predict(X_test)

# Natijalar
accuracy = accuracy_score(y_test, y_pred)
print(f"Modelning aniqligi: {accuracy*100:.2f}%")

# Signalni bashorat qilish va qo‘shish
data['AI_Signal'] = model.predict(X)

# Yangi signalni CSV faylga saqlash
data.to_csv('XAUUSD_signals_with_AI.csv', index=False)

# Signalni yuborish
last_signal = data['AI_Signal'].iloc[-1]  # Oxirgi signal

# Signalni Telegramga yuborish
if last_signal == 1:
    bot.send_message(chat_id=CHAT_ID, text="Sotib olish signal: XAUUSD!")
elif last_signal == -1:
    bot.send_message(chat_id=CHAT_ID, text="Sotish signal: XAUUSD!")
else:
    bot.send_message(chat_id=CHAT_ID, text="No signal: XAUUSD!")

print("Signal yuborildi.")
