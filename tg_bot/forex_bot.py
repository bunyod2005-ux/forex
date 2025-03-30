import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import ta  # TA-Lib o‘rniga TA kutubxonasidan foydalanamiz

def initialize_mt5():
    if not mt5.initialize():
        print("MT5 ga ulanishda xatolik")
        mt5.shutdown()

def get_data(symbol, timeframe, bars=500):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def calculate_indicators(df):
    df['EMA_50'] = ta.trend.ema_indicator(df['close'], window=50)
    df['EMA_200'] = ta.trend.ema_indicator(df['close'], window=200)
    df['RSI'] = ta.momentum.rsi(df['close'], window=14)
    df['ATR'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    buy_condition = (
        latest['EMA_50'] > latest['EMA_200'] and 
        latest['RSI'] > 55 and 
        prev['RSI'] < 55 and 
        latest['close'] > latest['EMA_50']
    )
    
    sell_condition = (
        latest['EMA_50'] < latest['EMA_200'] and 
        latest['RSI'] < 45 and 
        prev['RSI'] > 45 and 
        latest['close'] < latest['EMA_50']
    )
    
    if buy_condition:
        return 'BUY', latest['ATR']
    elif sell_condition:
        return 'SELL', latest['ATR']
    else:
        return 'NO SIGNAL', None

def main():
    initialize_mt5()
    symbol = "XAUUSD"
    timeframe = mt5.TIMEFRAME_H1
    
    df = get_data(symbol, timeframe)
    df = calculate_indicators(df)
    signal, atr = generate_signal(df)
    
    if signal != 'NO SIGNAL':
        latest_price = df.iloc[-1]['close']
        
        if signal == 'BUY':
            tp = latest_price + (atr * 2)
            sl = latest_price - (atr * 1.5)
        else:
            tp = latest_price - (atr * 2)
            sl = latest_price + (atr * 1.5)
        
        print(f"📈 Signal: {signal}\n🎯 TP: {tp:.2f}\n🛑 SL: {sl:.2f}")
    else:
        print("🚫 Hech qanday signal yo'q")
    
    mt5.shutdown()
    
if __name__ == "__main__":
    main()
