import asyncio
import logging
import MetaTrader5 as mt5
import pandas as pd
import ta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Windows uchun asyncio muammosini hal qilish
if asyncio.get_event_loop_policy().__class__.__name__ != "WindowsSelectorEventLoopPolicy":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = "8012999734:AAGVQl-Cnwvlt08cA3LAQPYMuIVH6Mn-n30"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# MetaTrader 5 ni ishga tushirish
def initialize_mt5():
    if not mt5.initialize():
        logging.error("MetaTrader 5 ga ulanib bo‘lmadi!")
        return False
    return True

# Forex ma'lumotlarini olish
def get_data(symbol="XAUUSD", timeframe=mt5.TIMEFRAME_H1, bars=500):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"{symbol} uchun ma'lumotlarni olishda xatolik! (Bo‘sh ma'lumot)")
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Indikatorlarni hisoblash
def calculate_indicators(df):
    df['EMA_50'] = ta.trend.ema_indicator(df['close'], window=50)
    df['EMA_200'] = ta.trend.ema_indicator(df['close'], window=200)
    df['RSI'] = ta.momentum.rsi(df['close'], window=14)
    df['ATR'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
    return df

# Signal generatsiya qilish
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

# /start komandasi
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Salom! Tahlil qilish uchun /tred ni bosing.")

# /tred komandasi
@dp.message(Command("tred"))
async def tred_command(message: Message):
    if not initialize_mt5():
        await message.answer("❌ MetaTrader 5 ga ulanib bo‘lmadi!")
        return
    
    try:
        df = get_data()
        df = calculate_indicators(df)
        signal, atr = generate_signal(df)

        if signal != "NO SIGNAL":
            latest_price = df.iloc[-1]['close']
            if signal == "BUY":
                tp = latest_price + (atr * 2)
                sl = latest_price - (atr * 1.5)
            else:
                tp = latest_price - (atr * 2)
                sl = latest_price + (atr * 1.5)

            response = (
                f"📊 **Forex bozor tahlili**\n"
                f"📈 **Signal**: {signal}\n"
                f"🎯 **TP**: {tp:.2f}\n"
                f"🛑 **SL**: {sl:.2f}\n"
            )
        else:
            response = "🚫 Hozircha aniq signal yo‘q."

        await message.answer(response)
    except Exception as e:
        logging.error(f"Xatolik: {str(e)}")
        await message.answer(f"⚠️ Xatolik: {str(e)}")
    finally:
        mt5.shutdown()

# Asosiy bot funksiyasi
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

# Botni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
