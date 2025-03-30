import pandas as pd
import MetaTrader5 as mt5
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# MetaTrader 5 bilan bog'lanish
if not mt5.initialize():
    print("MT5 bilan bog'lanib bo'lmadi. Iltimos, terminalni tekshiring.")
    exit()

# XAU/USD (Oltin) bo'yicha 1 soatlik (1H) ma'lumotlarni olish
symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_H1
n_bars = 8760  # 1 yil = 8760 soat

# Ma'lumotlarni yuklab olish
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_bars)
if rates is None or len(rates) == 0:
    print("Ma'lumotlarni olishda xatolik yuz berdi. Iltimos, ulanish va symbolni tekshiring.")
    mt5.shutdown()
    exit()

# Ma'lumotlarni DataFrame formatiga o'tkazish
data = pd.DataFrame(rates)
data['time'] = pd.to_datetime(data['time'], unit='s')

# Harakatlanuvchi o'rtacha (MA) indikatorlarini hisoblash
data['MA_50'] = data['close'].rolling(window=50, min_periods=1).mean()
data['MA_200'] = data['close'].rolling(window=200, min_periods=1).mean()

# Signal generatsiya qilish
data['Signal'] = 0
data.loc[data['MA_50'] > data['MA_200'], 'Signal'] = 1  # Sotib olish signal
data.loc[data['MA_50'] < data['MA_200'], 'Signal'] = -1  # Sotish signal

# Signal ustunini to‘g‘rilash
data['Signal'] = data['Signal'].replace({-1: 0, 1: 1, 0: 2})  # Signal qiymatlarini 0, 1, 2 ga o‘zgartirish

# XGBoost uchun xususiyatlarni tanlash (MA_50, MA_200, close narx)
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

# MT5ni to‘xtatish
mt5.shutdown()
