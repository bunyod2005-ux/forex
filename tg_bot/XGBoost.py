import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Telegram bot tokenini kiriting
API_TOKEN = 'YOUR_API_TOKEN'  # BotFather'dan olingan token
CHAT_ID = 'YOUR_CHAT_ID'  # Sizning chat ID (foydalanuvchi yoki guruh ID)

# XAUUSD signal ma'lumotlarini yuklash (oldingi signalni yaratish)
data = pd.read_csv('XAUUSD_signals.csv')

# XGBoost modelini yaratish va o‘qitish
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

# Signal yuborish funksiyasi
def send_signal(update, context):
    signal = data.tail(1).iloc[0]  # Oxirgi signalni olish
    signal_message = f"Signal: {'Buy' if signal['AI_Signal'] == 1 else 'Sell'}\n"
    signal_message += f"Close: {signal['close']}\nMA_50: {signal['MA_50']}\nMA_200: {signal['MA_200']}"
    
    # Signalni yuborish
    context.bot.send_message(chat_id=CHAT_ID, text=signal_message)

# Botni sozlash
def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Komanda handleri
    dispatcher.add_handler(CommandHandler('signal', send_signal))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# MetaTrader 5 ma'lumotlarini olish va DataFrame yaratish (avvalgi kodni kiritish)

# Signal generatsiya qilish
data['Signal'] = 0
data.loc[data['MA_50'] > data['MA_200'], 'Signal'] = 1  # Sotib olish signal
data.loc[data['MA_50'] < data['MA_200'], 'Signal'] = 2  # Sotish signal, -1 -> 2

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

print("AI signal bashorati va natijalar CSV faylga saqlandi.")

