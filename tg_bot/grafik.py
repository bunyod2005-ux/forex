import pandas as pd
import matplotlib.pyplot as plt

# CSV fayldan ma'lumotlarni yuklash
df = pd.read_csv("xauusd_1h_data_mt5.csv")

# Vaqt formatini to‘g‘rilash
df['time'] = pd.to_datetime(df['time'])

# Grafik chizish
plt.figure(figsize=(10, 5))
plt.plot(df['time'], df['close'], label='Close Price', color='blue')
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('XAU/USD 1H Close Price Chart')
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()
