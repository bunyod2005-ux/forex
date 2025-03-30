import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

# Ma'lumotlarni yuklash
df = pd.read_csv("XAUUSD_1H_data.csv")

# Target (signal) yaratish: narx ko‘tarilsa 1, tushsa 0
df['Signal'] = (df['close'].shift(-1) > df['close']).astype(int)

# Kerakli ustunlarni ajratish
X = df[['open', 'high', 'low', 'close', 'tick_volume']]
y = df['Signal']

# Train-test bo‘lish
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modeli
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Modelni saqlash
model.save_model("xgboost_model.json")
print("✅ Model saqlandi: xgboost_model.json")
