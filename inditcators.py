import talib
import pandas as pd

def calculate_rsi(data, period):
    """Calculate RSI."""
    return talib.RSI(data, timeperiod=period)

def calculate_ema(data, period):
    """Calculate EMA."""
    return talib.EMA(data, timeperiod=period)

def calculate_macd(data):
    """Calculate MACD and signal line."""
    macd, macd_signal, macd_hist = talib.MACD(data, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, macd_signal, macd_hist
