import MetaTrader5 as mt5
import pandas as pd

# MT5 ga ulanish
if not mt5.initialize():
    print("MT5 ga ulanishda xatolik")
    quit()

# XAU/USD bo‘yicha 1 soatlik ma’lumot olish
symbol = "XAUUSD"
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 1000)

# DataFrame ga o‘tkazish
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')  # Vaqtni to‘g‘rilash

# Faylga saqlash
df.to_csv("XAUUSD_1H_data.csv", index=False)
print("✅ Ma’lumot saqlandi: XAUUSD_1H_data.csv")

mt5.shutdown()
