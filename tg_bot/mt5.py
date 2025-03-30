import MetaTrader5 as mt5
import pandas as pd

# MT5 ga ulanish
if not mt5.initialize():
    print("MT5 ga ulanishda xatolik")
    mt5.shutdown()

# XAUUSD bo‘yicha 1 soatlik tarixiy ma’lumot olish
rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 8760)

# Ma’lumotni DataFrame formatiga o‘tkazish
data = pd.DataFrame(rates)
print(data.head())

mt5.shutdown()
