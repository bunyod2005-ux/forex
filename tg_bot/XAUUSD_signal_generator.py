import pandas as pd
import datetime

try:
    import MetaTrader5 as mt5
except ModuleNotFoundError:
    print("MetaTrader5 moduli mavjud emas. Iltimos, uni quyidagi buyruq bilan o'rnating: pip install MetaTrader5")
    exit()

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

# Signalni CSV faylga saqlash
data.to_csv('XAUUSD_signals.csv', index=False)

# Natijalarni chiqarish
print("Signal generatsiya qilindi va CSV faylga saqlandi.")
